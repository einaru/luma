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

from plugins.addressbook.ContactWizardDesign import ContactWizardDesign
from base.backend.ServerList import ServerList
import environment
from base.utils.gui.BrowserWidget import BrowserWidget
from plugins.addressbook.AddressbookWidget import AddressbookWidget
from base.backend.LumaConnection import LumaConnection
from base.utils import lumaStringDecode, lumaStringEncode
from time import strftime
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.backend.SmartDataObject import SmartDataObject
from base.utils.gui.LumaErrorDialog import LumaErrorDialog


class ContactWizard(ContactWizardDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        ContactWizardDesign.__init__(self,parent,name,modal,fl)
        
        self.iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        iconDir = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons","plugins", "addressbook")
        locationIcon = QPixmap(os.path.join (iconDir, "location.png"))
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
            self.setHelpEnabled(self.page(x), False)
            
        self.setFinishEnabled(self.page(1), 1)
        self.disconnect(self.finishButton(), SIGNAL("clicked()"), self, SLOT("accept()"))
        self.disconnect(self.nextButton(), SIGNAL("clicked()"), self, SLOT("next()"))
        
        self.connect(self.nextButton(),SIGNAL("clicked()"), self.checkNext)
            
        tmpWidget = self.page(1)
        self.addressWidget = AddressbookWidget(self.contactFrame)
        tmpLayout = QHBoxLayout(self.contactFrame)
        tmpLayout.addWidget(self.addressWidget)
        self.addressWidget.setEnabled(1)
        
###############################################################################

    def updateLocation(self, dataObject):
        self.locationServer = dataObject.getServerMeta().name
        self.serverMeta = dataObject.getServerMeta()
        self.locationDN = dataObject.getPrettyDN()
        tmpString = self.locationDN + "@" + self.locationServer
        self.locationEdit.setText(tmpString)
        
###############################################################################

    def saveContact(self):
        dataObject = self.addressWidget.dataObject
        
        if (dataObject.hasAttribute('cn')) and (dataObject.hasAttribute('sn')):
            description = dataObject.getAttributeValue('cn', 0)
            description = description + strftime('%Y%m%d') + str(random.randint(0,100))
            dataObject.addAttributeValue('description', [description], True)
            dataObject.setDN('description=' + description + ',' + self.locationDN)
            
            connection = LumaConnection(dataObject.getServerMeta())
            bindSuccess, exceptionObject = connection.bind()
            
            if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                return
            
            success, exceptionObject = connection.addDataObject(dataObject)
            connection.unbind()
            
            if success:
                self.accept()
            else:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not add entry.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()

        else:
            tmpDialog = QMessageBox(self.trUtf8("Incomplete information."),
                self.trUtf8("Your contact needs at least a surname."),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton,
                self)
        
            tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
            tmpDialog.exec_loop()
            
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
                self.trUtf8("Please select a location where to store the contact."),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.NoButton,
                QMessageBox.NoButton,
                self)
        
            tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
            tmpDialog.exec_loop()
        
        elif result ==1:
            allowedAttributes = self.getAllowedAttributes()
            dataObject = SmartDataObject(('', {'objectClass': self.getPossibleClasses()}), self.serverMeta)
            self.addressWidget.initView(dataObject)
            self.addressWidget.enableContactFields(allowedAttributes)
            self.next()
            
###############################################################################

    def getAllowedAttributes(self):
        objectClassList = ['person', 'organizationalPerson', 'inetOrgPerson', 'evolutionPerson']
        metaInfo = ObjectClassAttributeInfo(self.serverMeta)
        
        self.availableClasses = []
        for x in objectClassList:
            if metaInfo.hasObjectClass(x):
                self.availableClasses.append(x)
        
        must, may = metaInfo.getAllAttributes(self.availableClasses)
        return must | may
        
###############################################################################

    def getPossibleClasses(self):
        objectClassList = ['person', 'organizationalPerson', 'inetOrgPerson', 'evolutionPerson']
        metaInfo = ObjectClassAttributeInfo(self.serverMeta)
        
        self.availableClasses = []
        for x in objectClassList:
            if metaInfo.hasObjectClass(x):
                self.availableClasses.append(x)
        
        return self.availableClasses
