# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *
import os.path
import ldap
from ConfigParser import *

import environment
from base.utils.gui.LumaIconViewDesign import LumaIconViewDesign
from base.backend.ServerObject import ServerObject
from base.backend.ServerList import ServerList
from base.backend.LumaConnection import LumaConnection

class LumaIconView (LumaIconViewDesign):

    searchFilter = "(&(objectClass=inetOrgPerson)(|(cn=*)(sn=*)(givenName=*)(mail=*) ) )"
    searchFilterPrefix =  "(&(objectClass=inetOrgPerson)(|"
    searchFilterSuffix = "))"
        
    def __init__(self,parent = None,name = None,fl = 0):
        LumaIconViewDesign.__init__(self,parent,name,fl)
        
        configFile = os.path.join(environment.userHomeDir,  ".luma", "plugins")
        config = ConfigParser()
        config.readfp(open(configFile, 'r'))
        
        self.filterElements = ["cn", "sn", "givenName", "mail"]
        
        if config.has_option('Addressbook', 'filter'):
            filter = config.get('Addressbook', 'filter')
            foo = filter.split(",")
            if not(foo[0] == ''):
                self.filterElements = foo
            
        
        self.data = {}
        self.iconDict = {}
        
        searchFilter = "(objectClass=inetOrgPerson)"
        self.lumaConnection = LumaConnection()
        
        iconDir = os.path.join (environment.lumaInstallationPrefix, "lib", "luma", "plugins", "addressbook", "icons")
        
        self.entryIcon = QPixmap (os.path.join (iconDir, "person.png"))
        
        # Setting up server box
        tmpFile  = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons", "secure.png")
        securePixmap = QPixmap(tmpFile)

        serverListObject = ServerList()
        serverListObject.readServerList()
        self.serverList = serverListObject.SERVERLIST
        
        self.serverBox.insertItem("")
        if not (self.serverList == None):
            for x in self.serverList:
                if x.tls == 1:
                    self.serverBox.insertItem(securePixmap, x.name)
                else:
                    self.serverBox.insertItem(x.name)
                    
###############################################################################

    def serverChanged(self, serverName):
        if self.serverList == None:
            return
        
        for x in self.serverList:
            if x.name == str(serverName):
                self.lumaConnection.server = x
        
        self.search()
        
###############################################################################

    def search(self, filter = None):
        if self.lumaConnection.server == None:
            return
            
        if not(str(self.searchEdit.text()) == ''):
            filter = str(self.searchEdit.text())
          
        tmpFilter = None
        
        if (str(filter) == '') or (filter == None):
            filter = "*"
        else:
            filter = "*" + str(filter) + "*"
            
        tmpString = ""
        for x in self.filterElements:
            tmpString = tmpString + "(" + x + "=" + filter + ")"
                
        tmpFilter = self.searchFilterPrefix + tmpString + self.searchFilterSuffix
        
        results = self.lumaConnection.search(self.lumaConnection.server.baseDN, ldap.SCOPE_SUBTREE, tmpFilter)
        self.processResults(results)

###############################################################################

    def processResults(self, results):
        self.data={}
        if not(results == None):
            for x in results:
                self.data[x[0]] = x[1]
            
        self.showResults()
            
###############################################################################

    def showResults(self):
        self.iconDict = {}
        self.resultView.clear()
        
        if len(self.data.keys()) == 0:
            return
        
        nameList = []
        
        for x in self.data.keys():
            tmpData = self.data[x]
            name = ''
            if tmpData.has_key('cn'):
                name = tmpData['cn'][0]
            else:
                if tmpData.has_key('sn') or tmpData.has_key('givenName'):
                    if tmpData.has_key('sn'):
                        name = tmpData['sn'][0]
                    if tmpData.has_key('givenName'):
                        if not(name == ''):
                            name = name + ' '
                        name = name + tmpData['givenName'][0]
                
            nameList.append((name, x))
        
        nameList.sort()
        
        for x in nameList:
            iconTmp = QIconViewItem(self.resultView, x[0], self.entryIcon)
            self.iconDict[iconTmp] = x[1]
            
###############################################################################

    def iconClicked(self, icon):
        if icon == None:
            return
            
        dn = self.iconDict[icon]
        tmpData = self.data[dn]
        
        self.emit(PYSIGNAL("ldap_result"), (dn, tmpData, self.lumaConnection.server,))
