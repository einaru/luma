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
from base.backend.SmartDataObject import SmartDataObject
from base.utils.gui.LumaErrorDialog import LumaErrorDialog

class MassCreation(MassCreationDesign):

###############################################################################

    def __init__(self,parent = None,name = None,fl = 0):
        MassCreationDesign.__init__(self,parent,name,fl)
        
        self.iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        
        self.enableAutomount()

###############################################################################

    def createUsers(self):
        if str(self.nodeEdit.text()) == "":
            self.createButton.setEnabled(True)
            tmpDialog = QMessageBox(self.trUtf8("Incomplete information"),
                self.trUtf8("Please select a valid node from a ldap server."),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton,
                self)
        
            tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
            tmpDialog.exec_loop()
            return

        # set gui busy
        environment.setBusy(True)
        self.createButton.setEnabled(False)
        
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
            environment.setBusy(False)
            self.createButton.setEnabled(True)
            
            tmpDialog = QMessageBox(self.trUtf8("Warning"),
                self.trUtf8("""There are not enough user ids left! 
Try increasing the uidNumber range or delete some users from the subtree."""),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton,
                self)
        
            tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
            tmpDialog.exec_loop()
            return

        
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

        tmpList = str(self.nodeEdit.text()).split("@")
        server = tmpList[-1]
        baseDN = tmpList[0]

        tmpObject = ServerList()
        tmpObject.readServerList()
        serverMeta = tmpObject.getServerObject(server)
        
        connectionObject = LumaConnection(serverMeta)
        bindSuccess, exceptionObject = connectionObject.bind()
        
        if not bindSuccess:
            environment.setBusy(False)
            self.createButton.setEnabled(True)
            
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            return
        
        pwGenerator = CryptPwGenerator()
        self.passwordEdit.clear()
        
        createResult = True
        automountSuccess = True
        
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
            
            preProcess(serverMeta, values)
            
            tmpDN = 'uid=' + userName + "," + baseDN
            dataObject = SmartDataObject((tmpDN, values), serverMeta)
            success, exceptionObject = connectionObject.addDataObject(dataObject)
            
            if not success:
                createResult = False
                break

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
                dataObject = SmartDataObject((dn, mountValues), serverMeta)
                success, exceptionObject = connectionObject.addDataObject(dataObject)
                
                if not success:
                    automountSuccess = False
                    break
            
            postProcess(serverMeta, values)
        
            self.passwordEdit.append(userName + ': ' + passwordClear + "\n")
        
        connectionObject.unbind()
        environment.setBusy(False)
        self.createButton.setEnabled(True)
        
        if not createResult:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not create all users.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
        elif not automountSuccess:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not create all automount information.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
        else:
            tmpDialog = QMessageBox(self.trUtf8("Success"),
                self.trUtf8("""All users were created successfully."""),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton,
                self)
        
            tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "final.png")))
            tmpDialog.exec_loop()

###############################################################################
            
    def browseServer(self):
        dialog = BrowserDialog(self)
        if dialog.result() == QDialog.Accepted:
            self.nodeEdit.setText(dialog.getItemPath())
        

###############################################################################

    def getUsedUidNumbers(self):
        baseString = str(self.nodeEdit.text())
        tmpList = baseString.split('@')
        serverName = tmpList[-1]
        ldapObject = tmpList[0]

        serverList = ServerList()
        serverList.readServerList()
        serverMeta = serverList.getServerObject(serverName)
        
        environment.setBusy(True)
        
        connectionObject = LumaConnection(serverMeta)
        bindSuccess, exceptionObject = connectionObject.bind()
        
        if not bindSuccess:
            environment.setBusy(False)
            
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            return []
        
        success, resultList, exceptionObject = connectionObject.search(ldapObject, ldap.SCOPE_SUBTREE,
                "(objectClass=posixAccount)", ["uidNumber"], 0)
                
        connectionObject.unbind()
        
        environment.setBusy(False)
                
        if success:
            if resultList == None:
                resultList = []

            numberList = []
            for x in resultList:
                number = int(x.getAttributeValue('uidNumber', 0))
                numberList.append(number)
            return numberList
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not retrieve used userid numbers.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            
            return []
    
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
        result = None
        dialog = BrowserDialog(self)
        if dialog.result() == QDialog.Accepted:
            success, resultList, exceptionObject = dialog.getLdapItem()
            if success:
                if len(resultList) > 0:
                    resultItem = resultList[0]
                    groupId = None
        
                    if resultItem.hasAttribute('gidNumber'):
                        groupId = resultItem.getAttributeValue('gidNumber', 0)
                        self.gidBox.setValue(int(groupId))
                    else:
                        tmpDialog = QMessageBox(self.trUtf8("Wrong entry"),
                            self.trUtf8("""The selected ldap entry did not contain the attribute 'gidNumber'."""),
                            QMessageBox.Critical,
                            QMessageBox.Ok,
                            QMessageBox.NoButton,
                            QMessageBox.NoButton,
                            self)
        
                        tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
                        tmpDialog.exec_loop()
                        
                # Search result did not contain any items
                else:
                    dialog = LumaErrorDialog(dialog)
                    errorMsg = self.trUtf8("Could not retrieve selected item.<br><br>Reason: ")
                    errorMsg.append(str(exceptionObject))
                    dialog.setErrorMessage(errorMsg)
                    dialog.exec_loop()

                    
            # search operation unsuccessful
            else:
                dialog = LumaErrorDialog(dialog)
                errorMsg = self.trUtf8("Could not retrieve selected item.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()

###############################################################################

    def enableAutomount(self):
        state = self.enableNFSBox.isChecked()
        
        self.nfsServerEdit.setEnabled(state)
        self.nfsArgumentsEdit.setEnabled(state)
        self.automountLocationEdit.setEnabled(state)
        self.browseAutomountButton.setEnabled(state)
        self.automountLabel.setEnabled(state)
        self.serverLabel.setEnabled(state)
        self.argLabel.setEnabled(state)
        self.locationLabel.setEnabled(state)
        
###############################################################################

    def browseAutomount(self):
        dialog = BrowserDialog(self)
        if dialog.result() == QDialog.Accepted:
            self.automountLocationEdit.setText(dialog.getItemPath())
    
    
    
    
    
    
