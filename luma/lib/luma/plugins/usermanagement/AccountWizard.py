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
from string import strip
import random

from plugins.usermanagement.AccountWizardDesign import AccountWizardDesign
from base.backend.ServerList import ServerList
import environment
from base.utils.gui.BrowserWidget import BrowserWidget
from plugins.usermanagement.UsermanagementWidget import UsermanagementWidget
from base.backend.LumaConnection import LumaConnection
from base.utils import lumaStringDecode, lumaStringEncode
from plugins.usermanagement import addPreProcess, addPostProcess
from base.backend.SmartDataObject import SmartDataObject
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.utils.gui.LumaErrorDialog import LumaErrorDialog


class AccountWizard(AccountWizardDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        AccountWizardDesign.__init__(self,parent,name,modal,fl)
        
        self.iconPath = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons")
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons","plugins", "addressbook")
        locationIcon = QPixmap (os.path.join (iconDir, "location.png"))
        self.locationLabel.setPixmap(locationIcon)
        
        layout = QHBoxLayout(self.browserFrame)
        self.browserWidget = BrowserWidget(self.browserFrame)
        layout.addWidget(self.browserWidget)
        
        self.connect(self.browserWidget, PYSIGNAL("ldap_result"), self.updateLocation)
        self.connect(self.finishButton(), SIGNAL("clicked()"), self.saveContact)
        
        self.locationServer = None
        self.locationDN = None
        self.serverMeta = None
        
        for x in range(0,self.pageCount()):
            self.setHelpEnabled(self.page(x), 0)
            
        self.setFinishEnabled(self.page(1), 1)
        self.disconnect(self.finishButton(), SIGNAL("clicked()"), self, SLOT("accept()"))
        self.disconnect(self.nextButton(), SIGNAL("clicked()"), self, SLOT("next()"))
        
        self.connect(self.nextButton(),SIGNAL("clicked()"), self.checkNext)
           
          
        self.accountWidget = UsermanagementWidget(self.accountFrame)
        tmpLayout = QHBoxLayout(self.accountFrame)
        tmpLayout.addWidget(self.accountWidget)
        
        
        self.accountWidget.NEWENTRY = True
        
        self.accountWidget.uidEdit.setReadOnly(False)
        self.disconnect(self.accountWidget.groupButton, SIGNAL("clicked()"), self.accountWidget.editGroups)
        self.connect(self.accountWidget.groupButton, SIGNAL("clicked()"), self.checkUID)
        self.accountWidget.setEnabled(1)
        
###############################################################################

    def updateLocation(self, dataObject):
        self.locationServer = dataObject.getServerMeta().name
        self.serverMeta = dataObject.getServerMeta()
        self.locationDN = dataObject.getPrettyDN()
        tmpString = self.locationDN + "@" + self.locationServer
        self.locationEdit.setText(tmpString)
        
###############################################################################

    def saveContact(self):
        dataObject = self.accountWidget.dataObject
        
        if not dataObject.hasAttribute('uid'):
            tmpDialog = QMessageBox(self.trUtf8("Save account"),
                self.trUtf8("Please enter a username."),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton,
                self)
        
            tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
            tmpDialog.exec_loop()
            return

        if not dataObject.hasAttribute('uidNumber'):
            tmpDialog = QMessageBox(self.trUtf8("Save account"),
                self.trUtf8("Please enter a uid number."),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton,
                self)
        
            tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
            tmpDialog.exec_loop()
            return
            
        if not dataObject.hasAttribute('gidNumber'):
            tmpDialog = QMessageBox(self.trUtf8("Save account"),
                self.trUtf8("Please assign the user to a group."),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton,
                self)
        
            tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
            tmpDialog.exec_loop()
            return
        
        if not dataObject.hasAttribute('cn'):
            tmpDialog = QMessageBox(self.trUtf8("Save account"),
                self.trUtf8("Please enter a common name."),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton,
                self)
        
            tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
            tmpDialog.exec_loop()
            return

        if not dataObject.hasAttribute('homeDirectory'):
            tmpDialog = QMessageBox(self.trUtf8("Save account"),
                self.trUtf8("Please enter a homeDirectory."),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton,
                self)
        
            tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
            tmpDialog.exec_loop()
            return
        
        if not dataObject.hasAttribute("userPassword"):
            tmpDialog = QMessageBox(self.trUtf8("Missing password"),
                self.trUtf8("""It is strongly recommended that you choose 
a password for the new user. Otherwise 
it might compromise the security of your system."""),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton,
                self)
        
            tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
            tmpDialog.exec_loop()
            return
        
        dn = "uid=" + dataObject.getAttributeValue('uid', 0) + "," + self.locationDN
        dataObject.setDN(dn)
        dataObject.addAttributeValue("sn", [dataObject.getAttributeValue("uid", 0)])

        # Start preprocessing of usercreation
        groupName = unicode(self.accountWidget.groupEdit.text())
        addPreProcess(self.serverMeta, dataObject.getDN(), dataObject.data, groupName)
        
        connectionObject = LumaConnection(self.serverMeta)
        bindSuccess, exceptionObject = connectionObject.bind()
        
        if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                return
        
        addSuccess, exceptionObject = connectionObject.addDataObject(dataObject)
        
        if addSuccess:
            self.accountWidget.saveOtherGroups()
            
            # Start postprocessing of usercreation
            addPostProcess(self.serverMeta, dataObject.getDN(), dataObject.data, groupName)
            self.accept()
            
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not create account.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()

###############################################################################

    def checkLocation(self):
        if self.currentPage() == None:
            return 1
        
        if (self.locationServer == None) or (self.locationDN == None):
            return 0
        else:
            return 1
            
###############################################################################

    def checkNext(self):
        result = self.checkLocation()
        
        if result == 0:
            tmpDialog = QMessageBox(self.trUtf8("Warning: Location"),
                self.trUtf8("""Please select a location where to store the contact."""),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton,
                self)
        
            tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
            tmpDialog.exec_loop()
            
        elif result ==1:
            dataObject = SmartDataObject(('', {'objectClass': self.getPossibleClasses()}), self.serverMeta)
            dataObject.addAttributeValue('uidNumber', ['1024'])
            dataObject.addAttributeValue('homeDirectory', ['/home'])
            dataObject.addAttributeValue('loginShell', ['/bin/bash'])
            
            self.accountWidget.initView(dataObject)
            
            self.next()
            
###############################################################################

    def checkUID(self):
        uid = unicode(self.accountWidget.uidEdit.text())
        if len(uid) > 0:
            self.accountWidget.dataObject.addAttributeValue('uid', [uid], True)
            self.accountWidget.editGroups()
            
###############################################################################

    def getPossibleClasses(self):
        objectClassList = ["top", "posixAccount", "shadowAccount", "inetOrgPerson",
            "organizationalPerson", "person"]
        metaInfo = ObjectClassAttributeInfo(self.serverMeta)
        
        self.availableClasses = []
        for x in objectClassList:
            if metaInfo.hasObjectClass(x):
                self.availableClasses.append(x)
        
        return self.availableClasses

        
