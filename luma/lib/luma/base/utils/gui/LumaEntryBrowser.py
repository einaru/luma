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
from base.utils.gui.LumaEntryBrowserDesign import LumaEntryBrowserDesign
from base.backend.ServerObject import ServerObject
from base.backend.ServerList import ServerList
from base.backend.LumaConnection import LumaConnection

class LumaEntryBrowser (LumaEntryBrowserDesign):

    searchFilter = "(&(objectClass=inetOrgPerson)(|(cn=*)(sn=*)(givenName=*)(mail=*) ) )"
    searchFilterPrefix =  "(&(objectClass=inetOrgPerson)(|"
    searchFilterSuffix = "))"
        
    def __init__(self,parent = None,name = None,fl = 0):
        LumaEntryBrowserDesign.__init__(self,parent,name,fl)
        
        # dummies for the pre/post-processing functions which will be executed
        # when an item will be deleted
        self.deletePreProcess = None
        self.deletePostProcess = None
        
        lumaIconPath = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons")
        
        listViewIcon = QPixmap(os.path.join(lumaIconPath, "view_tree.png"))
        iconViewIcon = QPixmap(os.path.join(lumaIconPath, "view_icon.png"))
        
        self.listViewButton.setIconSet(QIconSet(listViewIcon))
        QToolTip.add(self.listViewButton, self.trUtf8("Tree"))
        
        self.iconViewButton.setIconSet(QIconSet(iconViewIcon))
        QToolTip.add(self.iconViewButton, self.trUtf8("Icons"))
        
        self.widgetStack.raiseWidget(1)
        
        
        self.searchFilter = "(&(objectClass=inetOrgPerson)(|(cn=*)(sn=*)(givenName=*)(mail=*) ) )"
        self.searchFilterPrefix =  "(&(objectClass=inetOrgPerson)(|"
        self.searchFilterSuffix = "))"
        
        self.filterElements = ["cn", "sn", "givenName", "mail"]
        
        self.primaryKey = "cn"
        
        self.data = {}
        self.entryDict = {}
        
        searchFilter = "(objectClass=inetOrgPerson)"
        self.lumaConnection = None
        
        # the id of the widget which should be used to display the results
        # the id is defined by the widgetstack
        self.RESULTVIEWID = 1
        
        # Setting up server box
        tmpFile  = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons", "secure.png")
        securePixmap = QPixmap(tmpFile)

        serverListObject = ServerList()
        serverListObject.readServerList()
        self.serverList = serverListObject.serverList
        
        self.serverBox.insertItem("")
        if not (self.serverList == None):
            for x in self.serverList:
                if x.tls == 1:
                    self.serverBox.insertItem(securePixmap, x.name)
                else:
                    self.serverBox.insertItem(x.name)
        
        # metadata of the current server
        self.SERVERMETA = None
        
        # A string representing the currently selected baseDN
        self.currentBase = None
                    
###############################################################################

    def serverChanged(self, serverName):
        if self.serverList == None:
            return
        
        for x in self.serverList:
            if x.name == str(serverName):
                self.SERVERMETA = x
                self.lumaConnection = LumaConnection(x)
                break
        
        self.initBaseBox()
        
        self.emit(PYSIGNAL("about_to_change"), ())
        self.emit(PYSIGNAL("server_changed"), ())
        
###############################################################################

    def initBaseBox(self):
        baseList = None
        if self.SERVERMETA.autoBase:
            baseList = self.lumaConnection.getBaseDNList()
        else:
            baseList = self.SERVERMETA.baseDN
            
        if None == baseList:
            return
            
        self.baseBox.clear()
        for tmpBase in baseList:
            self.baseBox.insertItem(tmpBase)
            
        
###############################################################################

    def search(self, filter = None):
        if self.lumaConnection.serverMeta == None:
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
        
        self.SERVERMETA.currentBase = unicode(self.baseBox.currentText())
        
        self.lumaConnection.bind()
        results = self.lumaConnection.search(self.SERVERMETA.currentBase, ldap.SCOPE_SUBTREE, tmpFilter.encode('utf-8'), [self.primaryKey, 'sn', 'givenName'], 0)
        self.lumaConnection.unbind()
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
        self.entryDict = {}
        self.itemIconView.clear()
        self.itemListView.clear()
        
        if len(self.data.keys()) == 0:
                return
        
        nameList = []
        
        for x in self.data.keys():
            tmpData = self.data[x]
            name = ''
            if tmpData.has_key(self.primaryKey):
                name = tmpData[self.primaryKey][0]                
            else:
                if tmpData.has_key('sn') or tmpData.has_key('givenName'):
                    if tmpData.has_key('sn'):
                        name = tmpData['sn'][0]
                    if tmpData.has_key('givenName'):
                        if not(name == ''):
                            name = name + ' '
                        name = name + tmpData['givenName'][0]
                        
            name = name.decode('utf-8')
                
            nameList.append((name, x))
        
        nameList.sort()
        
        for x in nameList:
            if self.RESULTVIEWID == 0:
                iconTmp = QIconViewItem(self.itemIconView, x[0], self.entryIcon)
                self.entryDict[iconTmp] = x[1]
            elif self.RESULTVIEWID == 1:
                entryTmp = QListViewItem(self.itemListView, x[0])
                self.entryDict[entryTmp] = x[1]
        
                
            
###############################################################################

    def iconClicked(self, icon):
        self.itemIconView.blockSignals(True)
        
        if icon == None:
            return
            
        dn = self.entryDict[icon]
        self.lumaConnection.bind()
        tmpData = self.lumaConnection.search(dn, ldap.SCOPE_BASE)[0][1]
        self.lumaConnection.unbind()
        
        self.itemIconView.blockSignals(False)
        
        self.emit(PYSIGNAL("about_to_change"), ())
        self.emit(PYSIGNAL("ldap_result"), (deepcopy(dn), deepcopy(tmpData), deepcopy(self.lumaConnection.serverMeta),))
        
###############################################################################

    def listItemClicked(self, entry):
        self.itemListView.blockSignals(True)
        
        if entry == None:
            return
            
        dn = self.entryDict[entry]
        self.lumaConnection.bind()
        tmpData = self.lumaConnection.search(dn, ldap.SCOPE_BASE)[0][1]
        self.lumaConnection.unbind()
        
        self.itemListView.blockSignals(False)
        
        self.emit(PYSIGNAL("about_to_change"), ())
        self.emit(PYSIGNAL("ldap_result"), (deepcopy(dn), deepcopy(tmpData), deepcopy(self.lumaConnection.serverMeta),))

    
###############################################################################

    def deleteItem(self):
        item = None
        
        for x in self.entryDict.keys():
            if x.isSelected():
                item = x
                break
            
        
        if item == None:
            return
            
        dn = self.entryDict[item]
        
        dialogResult = QMessageBox.warning(None,
            self.trUtf8("Delete contact"),
            self.trUtf8("""Do you really want to delete the selected contact?"""),
            self.trUtf8("&Yes"),
            self.trUtf8("&No"),
            None,
            0, -1)
            
        if dialogResult == 0:
            if not self.deletePreProcess == None:
                self.deletePreProcess(self.SERVERMETA, dn)
                
            self.lumaConnection.bind()
            result = self.lumaConnection.delete(dn)
            self.lumaConnection.unbind()
            if result == 0:
                QMessageBox.warning(None,
                    self.trUtf8("Error"),
                    self.trUtf8("""Could not delete contact. See console output for more information."""),
                    self.trUtf8("&OK"),
                    None,
                    None,
                    0, -1)
            else:
                self.itemListView.setSelected(self.itemListView.firstChild(), True)
                del self.data[dn]
                if not self.deletePostProcess == None:
                    self.deletePostProcess(self.SERVERMETA, dn)
                    
                self.showResults()

###############################################################################

    def addItem(self):
        self.emit(PYSIGNAL("add_entry"), ())
            
###############################################################################

    def initFilterConfig(self, pluginName):
        configFile = os.path.join(environment.userHomeDir,  ".luma", "plugins")
        config = ConfigParser()
        try:
            config.readfp(open(configFile, 'r'))
        except IOError, e:
            print "Could not read configuration file. Reason: "
            print e
        
        self.filterElements = ["cn", "sn", "givenName", "mail"]
        
        if config.has_option(pluginName, 'filter'):
            filter = config.get(pluginName, 'filter')
            foo = filter.split(",")
            if not(foo[0] == ''):
                self.filterElements = foo

###############################################################################

    def setItemPixmap(self, pixmap):
        self.entryIcon = pixmap

###############################################################################

    def raiseIconView(self):
        self.RESULTVIEWID = 0
        self.widgetStack.raiseWidget(0)
        self.showResults()
        
        
###############################################################################

    def raiseListView(self):
        self.RESULTVIEWID = 1
        self.widgetStack.raiseWidget(1)
        self.showResults()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
