# -*- coding: <utf-8> -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path

import environment
from plugins.addressbook.ContactWizard import ContactWizard
from plugins.addressbook.AddressbookWidget import AddressbookWidget
from base.utils.gui.LumaIconView import LumaIconView


class AddressbookView(QWidget):

    def __init__(self, parent=None, name=None, fl=0):
        QWidget.__init__(self, parent, name, fl)


        self.splitter = QSplitter(self)
        self.mainLayout = QHBoxLayout(self)
        self.entryList = LumaIconView(self.splitter)
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons", "plugins", "addressbook")
        entryIcon = QPixmap (os.path.join (iconDir, "person.png"))
        self.entryList.setItemPixmap(entryIcon)
        self.entryList.initFilterConfig("Addressbook")
        self.entryList.setMinimumWidth(200)
        
        self.addressContainer = QWidget(self.splitter)
        containerLayout = QGridLayout(self.addressContainer,1,1,0,6,"AddressbookWidgetDesignLayout")
        self.saveButton = QPushButton(self.addressContainer,"saveButton")
        self.saveButton.setText(self.trUtf8("&Save"))
        containerLayout.addWidget(self.saveButton,1,1)
        spacer = QSpacerItem(320,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        containerLayout.addItem(spacer,1,0)
        
        self.addressBookWidget = AddressbookWidget(self.addressContainer)
        containerLayout.addMultiCellWidget(self.addressBookWidget,0,0,0,1)
        
        #self.addressBookWidget = AddressbookWidget(self.splitter)
        self.connect (self.entryList, PYSIGNAL("ldap_result"), self.addressBookWidget.initView)
        self.connect(self.entryList, PYSIGNAL("server_changed"), self.addressBookWidget.serverChanged)
        self.connect(self.addressBookWidget, PYSIGNAL("contact_saved"), self.entryList.search)
        self.connect(self.saveButton,SIGNAL("clicked()"), self.addressBookWidget.saveEntry)
        self.connect(self.addressBookWidget, PYSIGNAL("enable_save"), self.enableSave)
        self.connect(self.entryList, PYSIGNAL("add_entry"), self.addEntry)
        self.mainLayout.addWidget(self.splitter)
        
        self.enableSave(0)
        
###############################################################################

    def enableSave(self, val):
        self.saveButton.setEnabled(val)
        
###############################################################################

    def addEntry(self):
        dialog = ContactWizard()
        dialog.exec_loop()

        dialog.result()

###############################################################################

    def createDialog(self):
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons", "plugins", "addressbook")
        locationIcon = QPixmap (os.path.join (iconDir, "location.png"))
        dialog = ContactWizard()
        dialog.locationLabel.setPixmap(locationIcon)
        
        layout = QHBoxLayout(dialog.browserFrame)
        browserWidget = BrowserWidget(dialog.browserFrame)
        layout.addWidget(browserWidget)
        
        
        return dialog






