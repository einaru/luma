# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping                                      
#    <wido.depping@tu-clausthal.de>                                                             
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
        tmpAttribute = str(self.attributeEdit.text())
        
        self.filterDict[tmpAttribute] = None
        
        tmpItem = QListViewItem(self.attributeView, tmpAttribute)
        self.attributeView.insertItem(tmpItem)
        
        self.attributeEdit.clear()
        

###############################################################################

    def deleteAttribute(self):
        tmpSelected = self.attributeView.selectedItem()
        if tmpSelected == None:
            return
            
        del self.filterDict[str(tmpSelected.text(0))]
        self.attributeView.takeItem(tmpSelected)
        
###############################################################################

    def readSettings(self):
        config = ConfigParser()
        config.readfp(open(self.configFile, 'r'))
        
        filter = None
        
        if config.has_option('Addressbook', 'filter'):
            filter = config.get('Addressbook', 'filter')
            filterSplit = filter.split(",")
            if filterSplit[0] == "":
                config.set("Addressbook", "filter", "inetOrgPerson,cn,sn,givenName,mail")
                config.write(open(self.configFile, 'w'))
                filterSplit = "inetOrgPerson,cn,sn,givenName,mail".split(",")
            
            for x in filterSplit:
                tmpItem = QListViewItem(self.attributeView, x)
                self.attributeView.insertItem(tmpItem)
                self.filterDict[x] = None
                
        else:
            config.add_section("Addressbook")
            config.set("Addressbook", "load", "1")
            config.set("Addressbook", "filter", "inetOrgPerson,cn,sn,givenName,mail")
            config.write(open(self.configFile, 'w'))
        
###############################################################################

    def saveValues(self):
        config = ConfigParser()
        config.readfp(open(self.configFile, 'r'))
        
        val = ",".join(self.filterDict.keys())
        
        if not config.has_section("Addressbook"):
            config.add_section("Addressbook")
            config.set("Addressbook", "load", "1")
            
        config.set("Addressbook", "filter", val)
        
        config.write(open(self.configFile, 'w'))
        
        
