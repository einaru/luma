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
from sets import Set



class UsermanagementWidget(UsermanagementWidgetDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        UsermanagementWidgetDesign.__init__(self,parent,name,fl)
        
        self.optionLine1.hide()
        self.deleteButton.hide()
        
        
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons", "plugins", "usermanagement")
        lumaIconPath = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons")

        accountPixmap = QPixmap(os.path.join(iconDir, "entry.png"))
        groupPixmap = QPixmap(os.path.join(iconDir, "group.png"))
        shellPixmap = QPixmap(os.path.join(iconDir, "shell.png"))
        homePixmap = QPixmap(os.path.join(iconDir, "home.png"))
        passwordPixmap = QPixmap(os.path.join(iconDir, "password.png"))
        mailPixmap = QPixmap(os.path.join(iconDir, "email.png"))
        savePixmap = QPixmap(os.path.join(lumaIconPath, "save.png"))
        deletePixmap = QPixmap(os.path.join(lumaIconPath, "editdelete.png"))
        
        self.accountLabel.setPixmap(accountPixmap)
        self.groupLabel.setPixmap(groupPixmap)
        self.shellLabel.setPixmap(shellPixmap)
        self.homeLabel.setPixmap(homePixmap)
        self.passwordLabel.setPixmap(passwordPixmap)
        self.mailLabel.setPixmap(mailPixmap)
        
        self.saveButton.setIconSet(QIconSet(savePixmap))
        QToolTip.add(self.saveButton, self.trUtf8("Save"))
        self.saveButton.setBackgroundMode(self.backgroundMode())
        
        self.deleteButton.setIconSet(QIconSet(deletePixmap))
        QToolTip.add(self.deleteButton, self.trUtf8("Delete entry"))
        self.deleteButton.setBackgroundMode(self.backgroundMode())
        
        self.DN = None
        self.CURRENTDATA = {}
        self.SERVERMETA = None
        self.OTHERGROUPS = {}
        
        self.ENABLED = False
        self.enableWidget()
        
        self.EDITED = False
        self.ENABLEDELETE = True
        

###############################################################################

    def initView(self, dn, data, server):
        self.DN = dn
        self.CURRENTDATA = data
        self.SERVERMETA = server
        self.ENABLED = True
        self.EDITED = False
        
        self.enableWidget()
        self.displayValues()
        
###############################################################################

    def enableWidget(self):
        self.setEnabled(self.ENABLED)
        
        objectClasses = None
        if self.CURRENTDATA.has_key("objectClass"):
            objectClasses = self.CURRENTDATA["objectClass"]
        
        if objectClasses == None:
            return
            
        shadowBool = False
        if "shadowAccount" in objectClasses:
            shadowBool = True
        self.expireEdit.setEnabled(shadowBool)
                
                
        posixBool = False
        if "posixAccount" in objectClasses:
            posixBool = True
        self.uidEdit.setEnabled(posixBool)
        self.uidBox.setEnabled(posixBool)
        self.nameEdit.setEnabled(posixBool)
        self.groupNumberEdit.setEnabled(posixBool)
        self.shellEdit.setEnabled(posixBool)
        self.homeEdit.setEnabled(posixBool)
        self.passwordEdit.setEnabled(posixBool)
        self.passwordButton.setEnabled(posixBool)
        
        inetOrgBool = False
        if ("inetOrgPerson" in objectClasses) or (self.CURRENTDATA.has_key("mail")):
            inetOrgBool = True
        self.mailBox.setEnabled(inetOrgBool)
        self.deleteMailButton.setEnabled(inetOrgBool)
        self.addMailButton.setEnabled(inetOrgBool)
        
        
        
###############################################################################

    def serverChanged(self):
        self.ENABLED = False
        self.enableWidget()
        self.clearValues()
        
###############################################################################

    def displayValues(self):
        self.uidEdit.blockSignals(True)
        if self.CURRENTDATA.has_key('uid'):
            self.uidEdit.setText(self.CURRENTDATA['uid'][0])
        else:
            self.uidEdit.setText("")
        self.uidEdit.blockSignals(False)
        
        
        self.uidBox.blockSignals(True)
        if self.CURRENTDATA.has_key('uidNumber'):
            self.uidBox.setValue(int(self.CURRENTDATA['uidNumber'][0]))
        else:
            self.uidBox.setValue(0)
        self.uidBox.blockSignals(False)
        
        
        self.nameEdit.blockSignals(True)
        if self.CURRENTDATA.has_key('cn'):
            self.nameEdit.setText(self.CURRENTDATA['cn'][0].decode('utf-8'))
        else:
            self.nameEdit.setText("")
        self.nameEdit.blockSignals(False)
        
        
        self.expireEdit.blockSignals(True)
        if self.CURRENTDATA.has_key('shadowExpire'):
            days = int(self.CURRENTDATA['shadowExpire'][0])
            date = QDate(1970, 1, 1)
            date = date.addDays(days)
            self.expireEdit.setDate(date)
        else:
            self.expireEdit.setDate(QDate(0, 0, 0))
        self.expireEdit.blockSignals(False)
           
          
        self.shellEdit.blockSignals(True)
        if self.CURRENTDATA.has_key('loginShell'):
            self.shellEdit.setText(self.CURRENTDATA['loginShell'][0])
        else:
            self.shellEdit.setText("")
        self.shellEdit.blockSignals(False)
            
            
        self.homeEdit.blockSignals(True)
        if self.CURRENTDATA.has_key('homeDirectory'):
            self.homeEdit.setText(self.CURRENTDATA['homeDirectory'][0])
        else:
            self.homeEdit.setText("")
        self.homeEdit.blockSignals(False)


        self.passwordEdit.blockSignals(True)
        if self.CURRENTDATA.has_key('userPassword'):
            self.passwordEdit.setText(self.CURRENTDATA['userPassword'][0])
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
        
        if self.CURRENTDATA.has_key('gidNumber'):
            self.groupNumberEdit.setText(self.CURRENTDATA['gidNumber'][0])
            self.groupNumberEdit.blockSignals(False)
            
            connectionObject = LumaConnection(self.SERVERMETA)
            connectionObject.bind()
            filter = "(&(objectClass=posixGroup)(gidNumber=" + self.CURRENTDATA['gidNumber'][0] + "))"
            result = connectionObject.search(self.SERVERMETA.baseDN, 
                        ldap.SCOPE_SUBTREE, filter)
            
            if result == None:
                self.groupEdit.setText("")
                return
                
            groupName = result[0][1]['cn'][0]
            self.groupEdit.setText(groupName)
        else:
            self.groupNumberEdit.setText("")
            self.groupEdit.setText("")
            
        self.groupNumberEdit.blockSignals(False)
            
            
        
###############################################################################
    
    def displayMailInfo(self):
        self.mailBox.clear()
        
        self.mailBox.blockSignals(True)
        
        if self.CURRENTDATA.has_key('mail'):
            tmpList = self.CURRENTDATA['mail']
            tmpList.sort()
            for y in tmpList:
                self.mailBox.insertItem(y.decode('utf-8'))
                
        self.mailBox.blockSignals(False)
            
###############################################################################

    def editPassword(self):
        dialog = PasswordDialog()
        dialog.exec_loop()
        
        if dialog.result() == 1:
            passwordHash = dialog.passwordHash
            if self.CURRENTDATA.has_key("userPassword"):
                self.CURRENTDATA["userPassword"][0] = passwordHash
            else:
                self.CURRENTDATA["userPassword"] = [passwordHash]
            
            self.EDITED = True
            self.displayValues()
            
###############################################################################

    def deleteMail(self):
        if not(self.CURRENTDATA.has_key('mail')):
            return
            
        if len(self.CURRENTDATA['mail']) == 0:
            return
            
        mail = unicode(self.mailBox.currentText())
        position = self.CURRENTDATA['mail'].index(mail)
        del self.CURRENTDATA['mail'][position]
        
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
                
            if self.CURRENTDATA.has_key("mail"):
                if not(mail in self.CURRENTDATA['mail']):
                    self.CURRENTDATA['mail'].append(mail)
            else:
                self.CURRENTDATA['mail'] = [mail]
                
            self.EDITED = True
            self.displayValues()
                
###############################################################################

    def editGroups(self):
        dialog = GroupDialog()
        dialog.SERVERMETA = self.SERVERMETA
        dialog.userName = self.CURRENTDATA['uid'][0]
        dialog.retrieveGroups()
        if self.CURRENTDATA.has_key("gidNumber"):
            dialog.groupNumberBox.setValue(int(self.CURRENTDATA['gidNumber'][0]))
        dialog.exec_loop()
        
        if (dialog.result() == QDialog.Accepted):
            gid = str(dialog.groupNumberBox.value())
            if self.CURRENTDATA.has_key("gidNumber"):
                self.CURRENTDATA['gidNumber'][0] = gid
            else:
                self.CURRENTDATA['gidNumber'] = [gid]
            
            self.OTHERGROUPS = {}
            
            listIterator = QListViewItemIterator(dialog.groupView)
            while listIterator.current():
                item = listIterator.current()
                self.OTHERGROUPS[unicode(item.text(2)).encode("utf-8")] = item.isOn()

                listIterator.__iadd__(1)
            
            self.EDITED = True
            self.displayValues()

###############################################################################

    def enableToolBar(self):
        self.saveButton.setEnabled(self.EDITED)
        self.deleteButton.setEnabled(self.ENABLEDELETE)
        
###############################################################################

    def homeChanged(self, newHome):
        newHome = unicode(newHome).encode("utf-8")
        
        if self.CURRENTDATA.has_key('homeDirectory'):
            self.CURRENTDATA['homeDirectory'][0] = newHome
        else:
            self.CURRENTDATA['homeDirectory'] = [newHome]
            
        self.EDITED = True
        self.enableToolBar()
      
###############################################################################

        
    def shellChanged(self, newShell):
        newShell = unicode(newShell).encode("utf-8")
        
        if self.CURRENTDATA.has_key('loginShell'):
            self.CURRENTDATA['loginShell'][0] = newShell
        else:
            self.CURRENTDATA['loginShell'] = [newShell]
            
        self.EDITED = True
        self.enableToolBar()
    
###############################################################################
        
    def expireChanged(self, newDate):
        newExpire = str(QDate(1970, 1, 1).daysTo(newDate))
        
        if self.CURRENTDATA.has_key('shadowExpire'):
            self.CURRENTDATA['shadowExpire'][0] = newExpire
        else:
            self.CURRENTDATA['shadowExpire'] = [newExpire]
        
        self.EDITED = True
        self.enableToolBar()
        
###############################################################################
        
    def commonNameChanged(self, newName):
        newName = unicode(newName).encode('utf-8')
        
        if self.CURRENTDATA.has_key('cn'):
            self.CURRENTDATA['cn'][0] = newName
        else:
            self.CURRENTDATA['cn'] = [newName]
            
        self.EDITED = True
        self.enableToolBar()
    
###############################################################################

    def uidChanged(self, newID):
        newID= unicode(newID).encode("utf-8")
        
        if self.CURRENTDATA.has_key('uidNumber'):
            self.CURRENTDATA['uidNumber'][0] = newID
        else:
            self.CURRENTDATA['uidNumber'] = [newID]
            
        self.EDITED = True
        self.enableToolBar()
        
###############################################################################

    def uidNameChanged(self, newName):
        newName= unicode(newName).encode("utf-8")
        
        if self.CURRENTDATA.has_key('uid'):
            self.CURRENTDATA['uid'][0] = newName
        else:
            self.CURRENTDATA['uid'] = [newName]
            
        self.EDITED = True
        self.enableToolBar()

###############################################################################

    def saveAccount(self):
        connectionObject = LumaConnection(self.SERVERMETA)
        connectionObject.bind()
        
        oldValues = connectionObject.search(self.DN)
        oldValues = oldValues[0][1]
        
        
        modlist =  ldap.modlist.modifyModlist(oldValues, self.CURRENTDATA, [], 1)
        entryResult = connectionObject.modify_s(self.DN, modlist)
        
        if not(entryResult == 0):
            self.saveOtherGroups()

        connectionObject.unbind()
        
        if entryResult == 0:
            QMessageBox.warning(None,
            self.trUtf8("Error"),
            self.trUtf8("""Could not save account data. 
Please read console output for more information."""),
            None,
            None,
            None,
            0, -1)
        else:
            self.EDITED = False
            self.enableToolBar()
            self.emit(PYSIGNAL("account_saved"), ())
        
###############################################################################

    def saveOtherGroups(self):
        connectionObject = LumaConnection(self.SERVERMETA)
        connectionObject.bind()
    
        groupResult = 1
        userName = self.CURRENTDATA['uid'][0]
        for x in self.OTHERGROUPS.keys():
            searchResult = connectionObject.search(x)
            dn = searchResult[0][0]
            data = searchResult[0][1]
            if data.has_key("memberUid"):
                if userName in data["memberUid"]:
                    if not(self.OTHERGROUPS[x]):
                        index = data["memberUid"].index(userName)
                        del data["memberUid"][index]
                else:
                    if self.OTHERGROUPS[x]:
                        data["memberUid"].append(userName)
            else:
                if self.OTHERGROUPS[x]:
                    data["memberUid"] = [userName]
                        
            oldData = connectionObject.search(x)[0][1]
            modlist =  ldap.modlist.modifyModlist(oldData, data, [], 1)
            result = connectionObject.modify_s(x, modlist)
            if result == 0:
                groupResult = 0
                
        if groupResult == 0:
            QMessageBox.warning(None,
                self.trUtf8("Error"),
                self.trUtf8("""Could not group information. 
Please read console output for more information."""),
                None,
                None,
                None,
                0, -1)
        
        connectionObject.unbind()
        
        
        
        
        
        
        
        
        
        
