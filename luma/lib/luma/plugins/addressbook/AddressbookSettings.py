# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *
from ConfigParser import *
import os.path

from plugins.addressbook.AddressbookSettingsDesign import AddressbookSettingsDesign
import environment

class AddressbookSettings(AddressbookSettingsDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        AddressbookSettingsDesign.__init__(self,parent,name,fl)
        
        self.configFile = os.path.join(environment.userHomeDir,  ".luma", "plugins")
        
        self.filterDict = {}
        
        self.readSettings()

###############################################################################

    def addAttribute(self):
        result = QInputDialog.getText(\
            self.trUtf8("New search criteria"),
            self.trUtf8("Attribute:"),
            QLineEdit.Normal)
        
        if result[1]:
            tmpAttribute = str(result[0])
        
            self.filterDict[tmpAttribute] = None
        
            tmpItem = QListViewItem(self.attributeView, tmpAttribute)
            self.attributeView.insertItem(tmpItem)
            
            self.saveValues()

###############################################################################

    def deleteAttribute(self):
        tmpSelected = self.attributeView.selectedItem()
        if tmpSelected == None:
            return
            
        del self.filterDict[str(tmpSelected.text(0))]
        self.attributeView.takeItem(tmpSelected)
        
        self.saveValues()
        
###############################################################################

    def readSettings(self):
        config = ConfigParser()
        try:
            config.readfp(open(self.configFile, 'r'))
        except IOError, e:
            print "Could not read addressbook settings. Reason: "
            print e
        
        filter = None
        
        if not config.has_section("Addressbook"):
            config.add_section("Addressbook")
        
        if not config.has_option("Addressbook", "filter"):
            config.set("Addressbook", "filter", "mail,givenName,cn,sn,uid")
        
        filter = config.get("Addressbook", "filter").strip()
        
        if (filter.split(",")[0] == "") or (filter == None):
            config.set("Addressbook", "filter", "mail,givenName,cn,sn,uid")
        
        try:
            config.write(open(self.configFile, 'w'))
        except IOError, e:
            print "Error: Could not write to " + self.configFile + ". Reason:"
            print e
        
        filterSplit = filter.split(",")
        for x in filterSplit:
                tmpItem = QListViewItem(self.attributeView, x)
                self.attributeView.insertItem(tmpItem)
                self.filterDict[x] = None
###############################################################################

    def saveValues(self):
        config = ConfigParser()
        
        try:
            config.readfp(open(self.configFile, 'r'))
        
            val = ",".join(self.filterDict.keys())
        
            if not config.has_section("Addressbook"):
                config.add_section("Addressbook")
            
            config.set("Addressbook", "filter", val)
        
            config.write(open(self.configFile, 'w'))
        except IOError, e:
            print "Error: Could not read/write to " + self.configFile + ". Reason:"
            print e
        
        
