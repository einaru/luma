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

import environment
from plugins.usermanagement.UsermanagementWidget import UsermanagementWidget
from plugins.usermanagement.AccountWizard import AccountWizard
from base.utils.gui.LumaEntryBrowser import LumaEntryBrowser
from plugins.usermanagement import deletePreProcess, deletePostProcess

class Usermanagement(QWidget):

    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        self.splitter = QSplitter(self)
        self.mainLayout = QHBoxLayout(self)
        self.entryList = LumaEntryBrowser(self.splitter)
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons", "plugins", "usermanagement")
        entryIcon = QPixmap (os.path.join (iconDir, "entry.png"))
        self.entryList.setItemPixmap(entryIcon)
        self.entryList.initFilterConfig("Usermanagement")
        self.entryList.setMinimumWidth(200)
        self.entryList.searchFilterPrefix =  "(&(|(objectClass=posixAccount)(objectClass=shadowAccount))(|"
        self.entryList.filterElements = ["cn", "sn", "givenName", "uid", "mail"]
        self.entryList.primaryKey = "uid"
        # assign functions which will be executed when an object will be deleted
        self.entryList.deletePreProcess = deletePreProcess
        self.entryList.deletePostProcess = deletePostProcess
    
        self.entryView = UsermanagementWidget(self.splitter)
        self.connect (self.entryList, PYSIGNAL("ldap_result"), self.entryView.initView)
        self.connect (self.entryList, PYSIGNAL("about_to_change"), self.entryView.aboutToChange)
        self.connect(self.entryList, PYSIGNAL("server_changed"), self.entryView.serverChanged)
        self.connect(self.entryList, PYSIGNAL("add_entry"), self.addEntry)
        self.mainLayout.addWidget(self.splitter)

###############################################################################

    def addEntry(self):
        dialog = AccountWizard()
        dialog.exec_loop()

        dialog.result()
