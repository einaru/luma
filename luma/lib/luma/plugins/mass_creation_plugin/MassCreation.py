# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import ldap
import os.path

from qt import *

import environment
from plugins.mass_creation_plugin.MassCreationDesign import MassCreationDesign
from base.utils.gui.BrowserWidget import BrowserWidget
from base.backend.ServerList import ServerList
from base.backend.ServerObject import ServerObject
from base.utils.backend.DateHelper import DateHelper
from base.utils.backend.CryptPwGenerator import CryptPwGenerator
from base.utils.gui.BrowserDialog import BrowserDialog
from base.utils.gui.PluginInformation import PluginInformation
from base.backend.LumaConnection import LumaConnection
from plugins.mass_creation_plugin import postProcess, preProcess

class MassCreation(MassCreationDesign):

###############################################################################

    def __init__(self,parent = None,name = None,fl = 0):
        MassCreationDesign.__init__(self,parent,name,fl)
        
        self.enableAutomount()

###############################################################################

    def createUsers(self):
        if str(self.nodeEdit.text()) == "":
            QMessageBox.warning(None,
                self.trUtf8("Incomplete Information"),
                self.trUtf8("""Please select a valid node from a ldap server."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)
            return None

        # set gui busy
        environment.setBusy(1)
        
        # get data for usernames
        userMax = self.prefixMaxBox.value()
        userMin = self.prefixMinBox.value()
        userCount = userMax - userMin + 1
        userPrefix = str(self.prefixEdit.text())
            
        usedNumbers = self.getUsedUidNumbers()
        
        uidNumMin = self.uidNumMinBox.value()
        uidNumMax = self.uidNumMaxBox.value()
        
        # list of free uidNumbers to use for our users
        freeNumbers = self.getUidNumbers(uidNumMin, uidNumMax, usedNumbers, userCount)
        
        if freeNumbers == None:
            environment.setBusy(0)
            QMessageBox.warning(None,
                self.trUtf8("Conflict"),
                self.trUtf8("""There are not enough user ids left! 
Try increasing the uidNumber range or delete some users from the subtree."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)
            return None

        
        shadowMax = None
        dateHelper = DateHelper()
        if self.dateButton.isChecked():
            date = self.dateEdit.date()
            year = date.year()
            month = date.month()
            day = date.day()
            shadowMax = dateHelper.dateToUnix(year, month, day)
        else:
            days = self.dayBox.value()
            shadowMax = dateHelper.datedurationToUnix(days)
            
        baseHomeDir = str(self.homeEdit.text())
        groupId = str(self.gidBox.value())
        loginShell = str(self.shellEdit.text())
        
        tmpList = str(self.nodeEdit.text()).split(",")
        server = tmpList[-1]
        del tmpList[-1]
        baseDN = ",".join(tmpList)
        
        tmpObject = ServerList()
        tmpObject.readServerList()
        serverMeta = tmpObject.getServerObject(server)
        
        connectionObject = LumaConnection(serverMeta)
        connectionObject.bind()
        
        pwGenerator = CryptPwGenerator()
        self.passwordEdit.clear()
        createResult = True
        
        for x in range(userMin, userMax+1):
            environment.updateUI()
            
            userName = userPrefix + str(x)
            uidNumber = freeNumbers[0]
            del freeNumbers[0]
            passwordClear, passwordCrypt = pwGenerator.getRandomPassword()
            homeDir = baseHomeDir + "/" + userName
            
            values = {}
            # removed 'account' class
            values['objectClass'] =  ["account", 'posixAccount', 'shadowAccount']
            values['uid'] = [userName]
            values['uidNumber'] = [str(uidNumber)]
            values['cn'] = [userName]
            values['userPassword'] = ["{crypt}" + passwordCrypt]
            values['loginShell'] = [loginShell]
            values['shadowExpire'] = [str(shadowMax)]
            values['gidNumber'] = [groupId]
            values["homeDirectory"] = [homeDir]
            
            print values
            
            preProcess(serverMeta, values)
            
            tmpDN = 'uid=' + userName + "," + baseDN
            modList = ldap.modlist.addModlist(values)
            result = connectionObject.add(tmpDN, modList)
            
            if result == 0:
                createResult = False
                break
                QMessageBox.critical(None,
                    self.trUtf8("Error"),
                    self.trUtf8("""Error during creation of users.
Please see console output for more information."""),
                    self.trUtf8("&OK"),
                    None,
                    None,
                    0, -1)
                    
            # create automount entry
            if self.enableNFSBox.isChecked():
                tmpList = str(self.automountLocationEdit.text()).split(",")
                del tmpList[-1]
                automountDN = ",".join(tmpList)
        
                dn = "cn=" + values["uid"][0] + "," + automountDN
                mountValues = {}
                mountValues["objectClass"] = ["automount"]
                mountValues["cn"] = [values["uid"][0]]
                automountServer = str(self.nfsServerEdit.text())
                automountOptions = str(self.nfsArgumentsEdit.text())
                automountInfo = automountOptions + " " + automountServer + ":" + values["homeDirectory"][0]
                #automountInfo = "-fstype=nfs,rw,quota,soft,intr ciphome.in.tu-clausthal.de:" + values["homeDirectory"][0]
                mountValues["automountInformation"] = [automountInfo]
                mountValues["description"] = ["Mountpoint of the home directory from user " + values["cn"][0]]
                print mountValues
                modlist = ldap.modlist.addModlist(mountValues)
                result = connectionObject.add(dn, modlist)
            
            postProcess(serverMeta, values)
        
            self.passwordEdit.append(userName + ': ' + passwordClear + "\n")
        
        connectionObject.unbind()
        environment.setBusy(0)
        
        if createResult:
            QMessageBox.information(None,
                self.trUtf8("Success"),
                self.trUtf8("""All users were created successfully."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)

###############################################################################
            
    def browseServer(self):
        dialog = BrowserDialog(self)
        if dialog.result() == QDialog.Accepted:
            self.nodeEdit.setText(dialog.getItemPath())
        

###############################################################################

    def getUsedUidNumbers(self):
        baseString = str(self.nodeEdit.text())
        tmpList = baseString.split(',')
        serverName = tmpList[-1]
        del tmpList[-1]
        ldapObject = ",".join(tmpList)

        serverList = ServerList()
        serverList.readServerList()
        serverMeta = serverList.getServerObject(serverName)
        
        searchResult = []
        
        # set gui busy
        environment.setBusy()

        try:
            ldapServerObject = ldap.open(serverMeta.host)
            ldapServerObject.protocol_version = ldap.VERSION3
            if serverMeta.tls == 1:
                ldapServerObject.start_tls_s()
            if len(serverMeta.bindDN) > 0:
                ldapServerObject.simple_bind_s(serverMeta.bindDN,
                                serverMeta.bindPassword)


            resultId = ldapServerObject.search(ldapObject, ldap.SCOPE_SUBTREE,
                "(objectClass=posixAccount)", ["uidNumber"], 0)

            while 1:
                # keep UI responsive
                environment.updateUI()

                result_type, result_data = ldapServerObject.result(resultId, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        for x in result_data:
                            searchResult.append(x)

            if len(serverMeta.bindDN) > 0:
                ldapServerObject.unbind()
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
        
        environment.setBusy(0)
        
        numberList = []
        for x in searchResult:
            number = int(x[1]['uidNumber'][0])
            numberList.append(number)
        return numberList
    
###############################################################################

    def getUidNumbers(self, uidNumMin, uidNumMax, usedNumbers, userCount):
        tmpList = []
        for x in range(uidNumMin, uidNumMax + 1):
            if len(tmpList) == userCount:
                break
            if not (x in usedNumbers):
                tmpList.append(x)
        if len(tmpList) == userCount:
            return tmpList
        else:
            return None
    
###############################################################################

    def browseGroups(self):
        ldapItem = None
        dialog = BrowserDialog(self)
        if dialog.result() == QDialog.Accepted:
            ldapItem = dialog.getLdapItem()
        else:
            return 0
        
        groupId = None
        
        try:
            groupId = ldapItem[1][0][1]['gidNumber'][0]
            self.gidBox.setValue(int(groupId))
        except KeyError:
            QMessageBox.warning(None,
                self.trUtf8("Wrong entry!"),
                self.trUtf8("""The selected ldap entry did not contain the attribute 'gidNumber'."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)
    
###############################################################################

    def enableAutomount(self):
        state = self.enableNFSBox.isChecked()
        
        self.nfsServerEdit.setEnabled(state)
        self.nfsArgumentsEdit.setEnabled(state)
        self.automountLocationEdit.setEnabled(state)
        self.browseAutomountButton.setEnabled(state)
        
###############################################################################

    def browseAutomount(self):
        dialog = BrowserDialog(self)
        if dialog.result() == QDialog.Accepted:
            self.automountLocationEdit.setText(dialog.getItemPath())
    
    
    
    
    
    
