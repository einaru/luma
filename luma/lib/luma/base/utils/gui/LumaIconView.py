# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *
from copy import deepcopy
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
        
        self.emit(PYSIGNAL("server_changed"), ())
        
###############################################################################

    def search(self, filter = None):
        if self.lumaConnection.server == None:
            return
            
        if not(unicode(self.searchEdit.text()) == ''):
            filter = unicode(self.searchEdit.text())
          
        tmpFilter = None
        
        if (unicode(filter) == '') or (filter == None):
            filter = "*"
        else:
            filter = "*" + unicode(filter) + "*"
            
        tmpString = ""
        for x in self.filterElements:
            tmpString = tmpString + "(" + x + "=" + filter + ")"
                
        tmpFilter = self.searchFilterPrefix + tmpString + self.searchFilterSuffix
        
        results = self.lumaConnection.search(self.lumaConnection.server.baseDN, ldap.SCOPE_SUBTREE, tmpFilter.encode('utf-8'), ['cn', 'sn', 'givenName'], 0)
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
                        
            name = name.decode('utf-8')
            #name = lumaStringDecode(name)
                
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
        tmpData = self.lumaConnection.search(dn, ldap.SCOPE_BASE)[0][1]
        
        self.emit(PYSIGNAL("ldap_result"), (deepcopy(dn), deepcopy(tmpData), deepcopy(self.lumaConnection.server),))
        
###############################################################################

    def deleteItem(self):
        item = None
        
        for x in self.iconDict.keys():
            if x.isSelected():
                item = x
                break
            
        
        if item == None:
            return
            
        dn = self.iconDict[item]
        
        dialogResult = QMessageBox.warning(None,
            self.trUtf8("Delete contact"),
            self.trUtf8("""Do you really want to delete the selected contact?"""),
            self.trUtf8("&No"),
            self.trUtf8("&Yes"),
            None,
            0, -1)
            
            
            
        if dialogResult == 1:
            result = self.lumaConnection.delete_s(dn)
            if result == 0:
                QMessageBox.warning(None,
                    self.trUtf8("Error"),
                    self.trUtf8("""Could not delete contact. See console output for more information."""),
                    self.trUtf8("&OK"),
                    None,
                    None,
                    0, -1)
            else:
                del self.data[dn]
                self.showResults()

###############################################################################

    def addItem(self):
        self.emit(PYSIGNAL("add_entry"), ())
            
            
