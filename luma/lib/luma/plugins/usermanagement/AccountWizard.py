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
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
import environment
from base.utils.gui.BrowserWidget import BrowserWidget
from plugins.usermanagement.UsermanagementWidget import UsermanagementWidget
from base.backend.LumaConnection import LumaConnection
from base.utils import lumaStringDecode, lumaStringEncode
from plugins.usermanagement import addPreProcess, addPostProcess


class AccountWizard(AccountWizardDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        AccountWizardDesign.__init__(self,parent,name,modal,fl)

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

    def updateLocation(self, server, data):
        self.locationServer = server
        self.locationDN = data[0][0].decode('utf-8')
        tmpString = self.locationDN + "@" + self.locationServer
        self.locationEdit.setText(tmpString)
        
###############################################################################

    def saveContact(self):
        uid = unicode(self.accountWidget.uidEdit.text()).strip()
        if len(uid) == 0:
            QMessageBox.warning(None,
                self.trUtf8("Save account"),
                self.trUtf8("""Please enter a username."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)
            return

        if self.accountWidget.uidBox.value() == 0:
            QMessageBox.warning(None,
                self.trUtf8("Save account"),
                self.trUtf8("""Please enter a uid number."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)
            return
            
        groupNumber = str(self.accountWidget.groupNumberEdit.text()).strip()
        if len(groupNumber) == 0:
            groupNumber = 0
        else: 
            groupNumber = int(groupNumber)
        if groupNumber == 0:
            QMessageBox.warning(None,
                self.trUtf8("Save account"),
                self.trUtf8("""Please assign the user to a group."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)
            return
        
        cn = unicode(self.accountWidget.nameEdit.text()).strip()
        if len(cn) == 0:
            QMessageBox.warning(None,
                self.trUtf8("Save account"),
                self.trUtf8("""Please enter a common name."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)
            return

        home = unicode(self.accountWidget.homeEdit.text()).strip()
        if len(home) == 0:
            QMessageBox.warning(None,
                self.trUtf8("Save account"),
                self.trUtf8("""Please enter a homeDirectory."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)
            return
        
        serverList = ServerList()
        serverList.readServerList()
        serverMeta = serverList.getServerObject(self.locationServer)
        dn = "uid=" + self.accountWidget.CURRENTDATA["uid"][0] + "," + self.locationDN
        values = self.accountWidget.CURRENTDATA
        
        objectClasses = ["posixAccount"]
        if values.has_key("shadowExpire"):
            objectClasses.append("shadowAccount")
        if values.has_key("mail"):
            objectClasses.append("inetOrgPerson")
            # UGLY HACK
            values["sn"] = values["uid"]
        else:
            objectClasses.append("account")
        
        values["objectClass"] = objectClasses
        #values["objectClass"] = ["posixAccount", "shadowAccount", 
        #    "organizationalPerson", "inetOrgPerson", "qmailUser"]
        #values["mailAlternateAddress"] = [values["uid"][0] + "@mail.in.tu-clausthal.de"]
        
        groupName = unicode(self.accountWidget.groupEdit.text())
        
        addPreProcess(serverMeta, dn, values, groupName)
        
        modlist = ldap.modlist.addModlist(values)
        
        connectionObject = LumaConnection(serverMeta)
        connectionObject.bind()
        
        result = connectionObject.add(dn, modlist)
        if result == 0:
            QMessageBox.warning(None,
                self.trUtf8("Create account"),
                self.trUtf8("""Could not create account. 
Please see console output for more information."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)
            return
        else:
            self.accountWidget.SERVERMETA = serverMeta
            self.accountWidget.saveOtherGroups()
        
        result = addPostProcess(serverMeta, dn, values, groupName)
        
        if result == 0:
            QMessageBox.warning(None,
                self.trUtf8("Create account"),
                self.trUtf8("""Could not create automount entry. 
Please see console output for more information."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)
            return
        
        self.accept()

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
            serverList = ServerList()
            serverList.readServerList()
            self.accountWidget.SERVERMETA = serverList.getServerObject(self.locationServer)
            self.next()
            
###############################################################################

    def checkUID(self):
        uid = unicode(self.accountWidget.uidEdit.text()).encode("utf-8")
        if len(uid) == 0:
            return
        else:
            self.accountWidget.editGroups()

        
