# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import ldap
from qt import *

from plugins.ifi_user.IfiUserDesign import IfiUserDesign
from base.utils.gui.BrowserWidget import BrowserWidget
from base.backend.ServerList import ServerList
from base.backend.ServerObject import ServerObject
from base.utils.backend.DateHelper import DateHelper
from base.utils.backend.CryptPwGenerator import CryptPwGenerator
from base.utils.gui.BrowserDialog import BrowserDialog
import environment


class IfiUser(IfiUserDesign):

###############################################################################

    def __init__(self,parent = None,name = None,fl = 0):
        IfiUserDesign.__init__(self,parent,name,fl)

###############################################################################

    def create_user(self):
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
        environment.setBusy()
        
        # get data for usernames
        userName = str(self.usernameEdit.text())
        sureName = str(self.sureNameEdit.text())
        givenName = str(self.givenNameEdit.text())
        
        usedNumbers = self.get_used_uidNumbers()
        
        uidNumMin = 2000
        uidNumMax = 65000
        
        # list of free uidNumbers to use for our users
        freeNumbers = self.get_uidNumbers(uidNumMin, uidNumMax, usedNumbers, 1)
        
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
            shadowMax = dateHelper.date_to_unix(year, month, day)
        else:
            days = self.dayBox.value()
            shadowMax = dateHelper.dateduration_to_unix(days)
        
        baseHomeDir = str(self.homeEdit.text())
        groupId = str(self.gidBox.value())
        loginShell = str(self.shellEdit.text())
        
        tmpList = str(self.nodeEdit.text()).split(",")
        server = tmpList[-1]
        del tmpList[-1]
        baseDN = ",".join(tmpList)
        
        tmpObject = ServerList()
        tmpObject.readServerList()
        serverMeta = tmpObject.get_serverobject(server)
        
        try:
            ldapServerObject = ldap.open(serverMeta.host, serverMeta.port)
            ldapServerObject.protocol_version = ldap.VERSION3
            if serverMeta.tls == 1:
                ldapServerObject.start_tls_s()
            ldapServerObject.simple_bind_s(serverMeta.bindDN,
                                serverMeta.bindPassword)
            
            
            pwGenerator = CryptPwGenerator()
            self.passwordEdit.clear()
            
            environment.updateUI()
                
            uidNumber = freeNumbers[0]
            passwordClear, passwordCrypt = pwGenerator.get_random_password()
            homeDir = baseHomeDir + "/" + userName
                
            modList = []
            
            # preserved for new ldap server
            #modList.append(('objectClass', ['qmailUser', 'posixAccount', 'shadowAccount', 'inetOrgPerson']))
            
            modList.append(('objectClass', ['posixAccount', 'shadowAccount', 'inetOrgPerson']))
            
            modList.append(('uid', userName))
            modList.append(('uidNumber', str(uidNumber)))
            modList.append(('cn', sureName + ' ' + givenName))
            modList.append(('sn', sureName))
            modList.append(('givenName', givenName))
            modList.append(('userPassword', "{crypt}" + passwordCrypt))
            modList.append(('loginShell', loginShell))
            modList.append(('shadowExpire', str(shadowMax)))
            modList.append(('gidNumber', groupId))
            modList.append(('homeDirectory', homeDir))
            tmpName = sureName.lower() + "." + givenName.lower()
            
            # preserved for new ldap server
            #modList.append(('mail', [tmpName + "@in.tu-clausthal.de", userName + "@in.tu-clausthal.de"]))
            #modList.append(('mailAlternateAddress', userName + "@mail.in.tu-clausthal.de"))
            
            tmpDN = 'uid=' + userName + "," + baseDN
            searchResult = ldapServerObject.add_s(tmpDN, modList)
            
            # creating automount entry
            modList = []
            modList.append(('objectClass', 'automount'))
            modList.append(('cn', userName))
            modList.append(('automountInformation', '-fstype=nfs,rw,quota,soft,intr home.in.tu-clausthal.de:' + homeDir))
            modList.append(('description', 'Mountpoint des Homeverzeichnisses von ' + userName))
            tmpDN = "cn=" + userName + ",ou=home,ou=automount,dc=in.tu-clausthal,dc=de"
            searchResult = ldapServerObject.add_s(tmpDN, modList)
            
            self.passwordEdit.append(userName + ': ' + passwordClear + "\n") 
                
            ldapServerObject.unbind()
            environment.setBusy(0)
            QMessageBox.information(None,
                self.trUtf8("Success"),
                self.trUtf8("""User was created successfully."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            environment.setBusy(0)
            QMessageBox.critical(None,
                self.trUtf8("Error"),
                self.trUtf8("""Error during creation of user.\nReason: """ + 
                            str(e[0]['desc'])),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)

###############################################################################
            
    def browse_server(self):
        dialog = BrowserDialog(self)
        if dialog.result() == QDialog.Accepted:
            self.nodeEdit.setText(dialog.getItemPath())
        
        

###############################################################################

    def get_used_uidNumbers(self):
        baseString = str(self.nodeEdit.text())
        tmpList = baseString.split(',')
        serverName = tmpList[-1]
        del tmpList[-1]
        ldapObject = ",".join(tmpList)

        serverList = ServerList()
        serverList.readServerList()
        serverMeta = serverList.get_serverobject(serverName)
        
        searchResult = []

        # set gui busy
        environment.setBusy(1)

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

    def get_uidNumbers(self, uidNumMin, uidNumMax, usedNumbers, userCount):
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
    
    
    
    
    
    
    
    
