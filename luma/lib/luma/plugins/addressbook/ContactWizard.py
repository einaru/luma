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
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo


class ContactWizard(ContactWizardDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        ContactWizardDesign.__init__(self,parent,name,modal,fl)

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
        
        self.addressWidget.data = {'cn': [''], 'sn': ['']}
        
###############################################################################

    def updateLocation(self, server, data):
        self.locationServer = server
        self.locationDN = data[0][0].decode('utf-8')
        tmpString = self.locationDN + "@" + self.locationServer
        self.locationEdit.setText(tmpString)
        
###############################################################################

    def saveContact(self):
        values = self.addressWidget.getValues()
        
        for x in values.keys():
            if len(values[x]) == 0:
                del values[x]
                
        values['objectClass'] = self.availableClasses
        if (values.has_key('cn')) and (values.has_key('sn')):
            description = lumaStringEncode(strip(values['cn'][0]))
            description = description + strftime('%Y%m%d') + str(random.randint(0,100))
            values['description'] = description
            
            modlist = ldap.modlist.addModlist(values)
            serverList = ServerList()
            serverList.readServerList()
            serverMeta = serverList.getServerObject(self.locationServer)
            connection = LumaConnection(serverMeta)
    
            dn = 'description=' + description + ',' + self.locationDN.encode('utf-8')

            connection.bind()
            result = connection.add(dn, modlist)
            connection.unbind()
            
            if result == 1:
                self.accept()
            elif result == 0:
                QMessageBox.warning(None,
                    self.trUtf8("Error"),
                    self.trUtf8("""Could not save entry. Please see console for more infomation."""),
                    self.trUtf8("&OK"),
                    None,
                    None,
                    0, -1)

        else:
            QMessageBox.warning(None,
                self.trUtf8("Incomplete Information"),
                self.trUtf8("""Your contact needs at least a surname."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)


            
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
            QMessageBox.warning(None,
                self.trUtf8("Warning: Location"),
                self.trUtf8("""Please select a location where to store the contact."""),
                None,
                None,
                None,
                0, -1)
        elif result ==1:
            allowedAttributes = self.getAllowedAttributes()
            self.addressWidget.enableContactFields(allowedAttributes)
            self.next()
            
###############################################################################

    def getAllowedAttributes(self):
        objectClassList = ['person', 'organizationalPerson', 'inetOrgPerson', 'evolutionPerson']
        metaInfo = ObjectClassAttributeInfo(self.locationServer)
        
        self.availableClasses = []
        for x in objectClassList:
            if metaInfo.hasObjectClass(x):
                self.availableClasses.append(x)
        
        must, may = metaInfo.getAllAttributes(objectClassList)
        return must | may
