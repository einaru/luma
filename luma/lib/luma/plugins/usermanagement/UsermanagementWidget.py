# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path
import ldap

import environment
from plugins.usermanagement.UsermanagementWidgetDesign import UsermanagementWidgetDesign
from plugins.usermanagement.NameDialog import NameDialog
from base.backend.LumaConnection import LumaConnection
from base.utils.gui.PasswordDialog import PasswordDialog
from base.utils.gui.MailDialog import MailDialog
from plugins.usermanagement.GroupDialog import GroupDialog
from base.utils.gui.LumaErrorDialog import LumaErrorDialog

from sets import Set



class UsermanagementWidget(UsermanagementWidgetDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        UsermanagementWidgetDesign.__init__(self,parent,name,fl)
        
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons", "plugins", "usermanagement")
        lumaIconPath = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons")

        accountPixmap = QPixmap(os.path.join(iconDir, "entry.png"))
        groupPixmap = QPixmap(os.path.join(iconDir, "group.png"))
        shellPixmap = QPixmap(os.path.join(iconDir, "shell.png"))
        homePixmap = QPixmap(os.path.join(iconDir, "home.png"))
        passwordPixmap = QPixmap(os.path.join(iconDir, "password.png"))
        mailPixmap = QPixmap(os.path.join(iconDir, "email.png"))
        self.savePixmap = QPixmap(os.path.join(lumaIconPath, "save.png"))
        deletePixmap = QPixmap(os.path.join(lumaIconPath, "editdelete.png"))
        
        self.accountLabel.setPixmap(accountPixmap)
        self.groupLabel.setPixmap(groupPixmap)
        self.shellLabel.setPixmap(shellPixmap)
        self.homeLabel.setPixmap(homePixmap)
        self.passwordLabel.setPixmap(passwordPixmap)
        self.mailLabel.setPixmap(mailPixmap)
        

        self.otherGroups = {}
        
        self.ENABLED = False
        self.dataObject = None
        self.enableWidget()
        
        self.EDITED = False
        self.ENABLEDELETE = True
        
        # Indicates if were are creating a new entry.
        self.NEWENTRY = False
        
        # a list of user ids which are stored in the ldap tree
        self.usedUserIds = None
        
        
        

###############################################################################

    def initView(self, dataObject):
        self.dataObject = dataObject
        
        self.ENABLED = True
        self.EDITED = False
        self.usedUserIds = None
        
        self.enableWidget()
        self.displayValues()
        
###############################################################################

    def enableWidget(self):
        if self.ENABLED:
            self.setEnabled(True)
            
            self.expireEdit.setEnabled(self.dataObject.hasObjectClass('shadowAccount'))
            
            posixBool = self.dataObject.hasObjectClass('posixAccount')
            self.uidEdit.setEnabled(posixBool)
            self.uidBox.setEnabled(posixBool)
            self.nameEdit.setEnabled(posixBool)
            self.groupNumberEdit.setEnabled(posixBool)
            self.shellEdit.setEnabled(posixBool)
            self.homeEdit.setEnabled(posixBool)
            self.passwordEdit.setEnabled(posixBool)
            self.passwordButton.setEnabled(posixBool)
        
            inetOrgBool = self.dataObject.hasObjectClass('inetOrgPerson') or self.dataObject.hasAttribute('mail')
            self.mailBox.setEnabled(inetOrgBool)
            self.deleteMailButton.setEnabled(inetOrgBool)
            self.addMailButton.setEnabled(inetOrgBool)
        else:
            self.setEnabled(False)
        
        
        
###############################################################################

    def serverChanged(self):
        self.ENABLED = False
        self.enableWidget()
        self.clearValues()
        self.usedUserIds = None
        
###############################################################################

    def displayValues(self):
        self.uidEdit.blockSignals(True)
        if self.dataObject.hasAttribute('uid'):
            value = self.dataObject.getAttributeValue('uid', 0)
            self.uidEdit.setText(value)
        else:
            self.uidEdit.setText("")
        self.uidEdit.blockSignals(False)
        
        
        self.uidBox.blockSignals(True)
        if self.dataObject.hasAttribute('uidNumber'):
            value = int(self.dataObject.getAttributeValue('uidNumber',0))
            self.uidBox.setValue(value)
        else:
            self.uidBox.setValue(1024)
        self.uidBox.blockSignals(False)
        
        
        self.nameEdit.blockSignals(True)
        if self.dataObject.hasAttribute('cn'):
            value = self.dataObject.getAttributeValue('cn', 0)
            self.nameEdit.setText(value)
        else:
            self.nameEdit.setText("")
        self.nameEdit.blockSignals(False)
        
        
        self.expireEdit.blockSignals(True)
        if self.dataObject.hasAttribute('shadowExpire'):
            days = int(self.dataObject.getAttributeValue('shadowExpire',0))
            date = QDate(1970, 1, 1)
            date = date.addDays(days)
            self.expireEdit.setDate(date)
        else:
            self.expireEdit.setDate(QDate(0, 0, 0))
        self.expireEdit.blockSignals(False)
           
          
        self.shellEdit.blockSignals(True)
        if self.dataObject.hasAttribute('loginShell'):
            value = self.dataObject.getAttributeValue('loginShell', 0)
            self.shellEdit.setText(value)
        else:
            self.shellEdit.setText("")
        self.shellEdit.blockSignals(False)
            
            
        self.homeEdit.blockSignals(True)
        if self.dataObject.hasAttribute('homeDirectory'):
            value = self.dataObject.getAttributeValue('homeDirectory', 0)
            self.homeEdit.setText(value)
        else:
            self.homeEdit.setText("")
        self.homeEdit.blockSignals(False)


        self.passwordEdit.blockSignals(True)
        if self.dataObject.hasAttribute('userPassword'):
            value = self.dataObject.getAttributeValue('userPassword', 0)
            self.passwordEdit.setText(value)
        else:
            self.passwordEdit.setText("")
        self.passwordEdit.blockSignals(False)
            
        self.displayGroupInfo()
        self.displayMailInfo()
        
        self.enableToolBar()
            
###############################################################################

    def clearValues(self):
        pass

###############################################################################

    def displayGroupInfo(self):
        self.groupNumberEdit.blockSignals(True)
        
        if self.dataObject.hasAttribute('gidNumber'):
            value = self.dataObject.getAttributeValue('gidNumber', 0)
            self.groupNumberEdit.setText(value)
            self.groupNumberEdit.blockSignals(False)
            
            connectionObject = LumaConnection(self.dataObject.getServerMeta())
            bindSuccess, exceptionObject = connectionObject.bind()
            
            if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                self.groupNumberEdit.blockSignals(False)
                return
            
            filter = "(&(objectClass=posixGroup)(gidNumber=" + self.dataObject.getAttributeValue('gidNumber', 0) + "))"
            success, resultList, exceptionObject = connectionObject.search(self.dataObject.getServerMeta().currentBase, 
                        ldap.SCOPE_SUBTREE, filter)
            
            if success:
                if len(resultList) > 0:
                    groupName = ''
                    tmpObject = resultList[0]
                    if tmpObject.hasAttribute('cn'):
                        groupName = tmpObject.getAttributeValue('cn', 0)
                    self.groupEdit.setText(groupName)
            else:
                self.groupEdit.setText("")
                
        else:
            self.groupNumberEdit.setText("")
            self.groupEdit.setText("")
            
        self.groupNumberEdit.blockSignals(False)
            
            
        
###############################################################################
    
    def displayMailInfo(self):
        self.mailBox.clear()
        
        self.mailBox.blockSignals(True)
        
        if self.dataObject.hasAttribute('mail'):
            tmpList = self.dataObject.getAttributeValueList('mail')
            tmpList.sort()
            map(self.mailBox.insertItem, tmpList)
                
        self.mailBox.blockSignals(False)
            
###############################################################################

    def editPassword(self):
        dialog = PasswordDialog()
        dialog.exec_loop()
        
        if dialog.result() == 1:
            passwordHash = dialog.passwordHash
            if self.dataObject.isAttributeAllowed("userPassword"):
                self.dataObject.addAttributeValue('userPassword', [passwordHash], True)
            
            self.EDITED = True
            self.displayValues()
            
###############################################################################

    def deleteMail(self):
        if not self.dataObject.hasAttribute('mail'):
            return
            
        mail = unicode(self.mailBox.currentText())
        position = self.dataObject.getAttributeValueList('mail').index(mail)
        self.dataObject.deleteAttributeValue('mail', position)
        
        self.EDITED = True
        self.displayValues()

###############################################################################
    def addMail(self):
        dialog = MailDialog()
        dialog.exec_loop()
        
        if (dialog.result() == QDialog.Accepted):
            mail = unicode(dialog.mailEdit.text()).strip().encode("utf-8")
            
            if mail == '':
                return
                
            if self.dataObject.isAttributeAllowed('mail'):
                if self.dataObject.hasAttribute('mail'):
                    # We only want to have each email address one time.
                    if not (mail in self.dataObject.getAttributeValueList('mail')):
                        self.dataObject.addAttributeValue('mail', [mail])
                else:
                    self.dataObject.addAttributeValue('mail', [mail])
                
            self.EDITED = True
            self.displayValues()
                
###############################################################################

    def editGroups(self):
        dialog = GroupDialog()
        dialog.serverMeta = self.dataObject.getServerMeta()
        dialog.userName = self.dataObject.getAttributeValue('uid', 0)
        dialog.retrieveGroups()
        
        if self.dataObject.hasAttribute("gidNumber"):
            value = int(self.dataObject.getAttributeValue('gidNumber', 0))
            dialog.groupNumberBox.setValue(value)
        dialog.exec_loop()
        
        if (dialog.result() == QDialog.Accepted):
            gid = str(dialog.groupNumberBox.value())
            if self.dataObject.isAttributeAllowed('gidNumber'):
                self.dataObject.addAttributeValue('gidNumber', [gid], True)
            
            self.otherGroups = {}
            
            listIterator = QListViewItemIterator(dialog.groupView)
            while listIterator.current():
                item = listIterator.current()
                self.otherGroups[unicode(item.text(2))] = item.isOn()
                
                listIterator += 1
            
            self.EDITED = True
            self.displayValues()

###############################################################################

    def enableToolBar(self):
        if not self.NEWENTRY:
            self.saveButton.setEnabled(self.EDITED)
        
###############################################################################

    def homeChanged(self, newHome):
        newHome = unicode(newHome)
        
        if self.dataObject.isAttributeAllowed('homeDirectory'):
            self.dataObject.addAttributeValue('homeDirectory', [newHome], True)
            
        self.EDITED = True
        self.enableToolBar()
      
###############################################################################

        
    def shellChanged(self, newShell):
        newShell = unicode(newShell)
        
        if self.dataObject.isAttributeAllowed('loginShell'):
            self.dataObject.addAttributeValue('loginShell', [newShell], True)
            
        self.EDITED = True
        self.enableToolBar()
    
###############################################################################
        
    def expireChanged(self, newDate):
        newExpire = str(QDate(1970, 1, 1).daysTo(newDate))
        
        if self.dataObject.isAttributeAllowed('shadowExpire'):
            self.dataObject.addAttributeValue('shadowExpire', [newExpire], True)
        
        self.EDITED = True
        self.enableToolBar()
        
###############################################################################
        
    def commonNameChanged(self, newName):
        newName = unicode(newName)
        
        if self.dataObject.isAttributeAllowed('cn'):
            self.dataObject.addAttributeValue('cn', [newName], True)
            
        self.EDITED = True
        self.enableToolBar()
    
###############################################################################

    def uidChanged(self, newID):
        newID= unicode(newID)
        
        if self.dataObject.isAttributeAllowed('uidNumber'):
            self.dataObject.addAttributeValue('uidNumber', [newID], True)
            
        self.EDITED = True
        self.enableToolBar()
        
###############################################################################

    def uidNameChanged(self, newName):
        newName= unicode(newName)
        
        if self.dataObject.isAttributeAllowed('uid'):
            self.dataObject.addAttributeValue('uid', [newName], True)
            
        self.EDITED = True
        self.enableToolBar()

###############################################################################

    def saveAccount(self):
        connectionObject = LumaConnection(self.dataObject.getServerMeta())
        bindSuccess, exceptionObject = connectionObject.bind()
        
        if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                return 
                
        success, exceptionObject = connectionObject.updateDataObject(self.dataObject)
        connectionObject.unbind()
        
        if success:
            self.saveOtherGroups()

            self.EDITED = False
            self.enableToolBar()
            self.usedUserIds = None
            self.emit(PYSIGNAL("account_saved"), ())
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not save entry.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
        
###############################################################################

    def saveOtherGroups(self):
        connectionObject = LumaConnection(self.dataObject.getServerMeta())
        bindSuccess, exceptionObject = connectionObject.bind()
        
        if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                return 
    
        groupUpdateSuccess = True
        failureException = None
        userName = self.dataObject.getAttributeValue('uid', 0)
        
        for x in self.otherGroups.keys():
            success, resultList, exceptionObject = connectionObject.search(x)
            
            if success:
                if len(resultList) > 0:
                    tmpObject = resultList[0]
            
                    if tmpObject.hasAttribute("memberUid"):
                        if userName in tmpObject.getAttributeValueList("memberUid"):
                            if not(self.otherGroups[x]):
                                index = tmpObject.getAttributeValueList("memberUid").index(userName)
                                tmpObject.deleteAttributeValue('memberUid', index)
                        else:
                            if self.otherGroups[x]:
                                tmpObject.addAttributeValue('memberUid', [userName])
                    else:
                        if self.otherGroups[x]:
                            tmpObject.addAttributeValue("memberUid", [userName])
                        
            
                    updateSuccess, exceptionObject = connectionObject.updateDataObject(tmpObject)
            
                    if not updateSuccess:
                        groupUpdateSuccess = False
                        failureException = exceptionObject
                    
            else:
                groupUpdateSuccess = False
                failureException = exceptionObject
                    
                
        if not groupUpdateSuccess:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not update all group information.<br><br>Reason: ")
            errorMsg.append(str(failureException))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
        
        connectionObject.unbind()
        
        
###############################################################################

    def nextFreeUserID(self):
        if self.usedUserIds == None:
            result = self.retrieveUserIDs()
            if result == None:
                return
            else:
                self.usedUserIds = result
            
        uid = self.uidBox.value() + 1
        while uid in self.usedUserIds:
            uid = uid + 1
            
        self.uidBox.setValue(uid)
        
###############################################################################

    def retrieveUserIDs(self):
        connectionObject = LumaConnection(self.dataObject.getServerMeta())
        bindSuccess, exceptionObject = connectionObject.bind()
        
        if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                return []
        
        success, resultList, exceptionObject = connectionObject.search(self.dataObject.getServerMeta().currentBase, ldap.SCOPE_SUBTREE,
                "(&(objectClass=*)(uidNumber=*))", ["uidNumber"], 0)
        connectionObject.unbind()
        
        if success:
            uidList = []
            for x in resultList:
                for y in x.getAttributeValueList("uidNumber"):
                    uidList.append(int(y))
            
            return uidList
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not retrieve used userids.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            
            return []
    
###############################################################################

    def aboutToChange(self):
        """Is called as a slot when new data arrives. 
        
        This way we are able to save the changed values.
        """
    
        if not self.EDITED:
            return
            
        value =QMessageBox.question(None,
            self.trUtf8("Save entry"),
            self.trUtf8("""The account has been modified. Do you want to save it?"""),
            self.trUtf8("&Yes"),
            self.trUtf8("&No"),
            None,
            0, -1)
            
        # button order says, that 'yes' is zero
        if value == 0:
            self.saveAccount()
        
###############################################################################

    def buildToolBar(self, parent):
        toolBar = QToolBar(parent)
    
        self.saveButton = QToolButton(toolBar, "saveValues")
        self.saveButton.setIconSet(QIconSet(self.savePixmap))
        self.saveButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.saveButton.setAutoRaise(True)
        self.saveButton.setBackgroundMode(self.backgroundMode())
        QToolTip.add(self.saveButton, self.trUtf8("Save"))
        self.connect(self.saveButton, SIGNAL("clicked()"), self.saveAccount)
    
        self.enableToolBar()
    
    
    
    
    
    
    
    
    
    
