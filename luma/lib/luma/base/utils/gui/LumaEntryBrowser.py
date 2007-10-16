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
from base.utils.gui.LumaErrorDialog import LumaErrorDialog
from base.utils.backend.LogObject import LogObject

class LumaEntryBrowser (LumaEntryBrowserDesign):

    # FIXME: make the searchfilter configurable and possibly per server/base
    searchFilter = "(&(objectClass=inetOrgPerson)(|(cn=*)(sn=*)(givenName=*)(mail=*) ) )"
    searchFilterPrefix =  "(&(objectClass=inetOrgPerson)(|"
    searchFilterSuffix = "))"
        
    def __init__(self,parent = None,name = None,fl = 0):
        LumaEntryBrowserDesign.__init__(self,parent,name,fl)
        
        # dummies for the pre/post-processing functions which will be executed
        # when an item will be deleted
        self.deletePreProcess = None
        self.deletePostProcess = None
        
        self.iconPath = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons")
        
        listViewIcon = QPixmap(os.path.join(self.iconPath, "view_tree.png"))
        iconViewIcon = QPixmap(os.path.join(self.iconPath, "view_icon.png"))
        
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
        tmpFile  = os.path.join(self.iconPath, "secure.png")
        securePixmap = QPixmap(tmpFile)

        serverListObject = ServerList()
        serverListObject.readServerList()
        self.serverList = serverListObject.serverList
        
        self.serverBox.insertItem("")
        if not (self.serverList == None):
            tmpDict = {}
            for x in self.serverList:
                if not (x.encryptionMethod == u"None"):
                    tmpDict[x.name] = True
                else:
                    tmpDict[x.name] = False
                
            
            tmpList = tmpDict.keys()
            tmpList.sort()
            for x in tmpList:
                if tmpDict[x]:
                    self.serverBox.insertItem(securePixmap, x)
                else:
                    self.serverBox.insertItem(x)
        
        # metadata of the current server
        self.SERVERMETA = None
        
        # A string representing the currently selected baseDN
        self.currentBase = None
                    
###############################################################################

    def serverChanged(self, serverName):
        self.setEnabled(False)
        
        if self.serverList == None:
            return
        
        for x in self.serverList:
            if x.name == str(serverName):
                self.SERVERMETA = x
                self.lumaConnection = LumaConnection(x)
                break
        
        self.setEnabled(True)
        
        if not (self.SERVERMETA == None):
            self.initBaseBox()
        
            self.emit(PYSIGNAL("about_to_change"), ())
            self.emit(PYSIGNAL("server_changed"), ())
        
###############################################################################

    def initBaseBox(self):
        self.setEnabled(False)
        
        baseList = None
            
        if self.SERVERMETA.autoBase:
            success, baseList, exceptionObject = self.lumaConnection.getBaseDNList()
            
            if not success:
                self.setEnabled(True)
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not retrieve baseDN.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                
        else:
            baseList = self.SERVERMETA.baseDN
          
        self.setEnabled(True)
        
        if baseList == None:
            self.goButton.setEnabled(False)
            return
        else:
            self.goButton.setEnabled(True)
            
        self.baseBox.clear()
        for tmpBase in baseList:
            self.baseBox.insertItem(tmpBase)
            
        self.search()
            
        
###############################################################################

    def search(self, filter=None):
        if self.lumaConnection == None:
            return
        
        if self.lumaConnection.serverMeta == None:
            return
            
        self.setEnabled(False)
            
        if not(unicode(self.searchEdit.text()) == ''):
            filter = unicode(self.searchEdit.text())
          
        tmpFilter = None
        
        if (unicode(filter) == '') or (filter == None):
            filter = "*"
        else:
	    # If * is the first or last character.. do not add it
            if not(unicode(filter).startswith("*")):
                filter = "*" + unicode(filter)
            if not(unicode(filter).endswith("*")):
                filter = unicode(filter) + "*"
            # FIXME: should be replaced by gui-elements such as
            # 'Starts with', 'Ends with' and 'contains'
            
        tmpString = ""
        for x in self.filterElements:
            tmpString = tmpString + "(" + x + "=" + filter + ")"
                
        tmpFilter = self.searchFilterPrefix + tmpString + self.searchFilterSuffix
        
        self.SERVERMETA.currentBase = unicode(self.baseBox.currentText())
        
        bindSuccess, exceptionObject = self.lumaConnection.bind()
        
        if not bindSuccess:
            self.setEnabled(True)
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            self.setEnabled(True)
            return 
                
        success, resultList, exceptionObject = self.lumaConnection.search(self.SERVERMETA.currentBase, ldap.SCOPE_SUBTREE, tmpFilter.encode('utf-8'), [self.primaryKey, 'sn', 'givenName'], 0)
        self.lumaConnection.unbind()
        
        if success:
            self.setEnabled(True)
            self.processResults(resultList)
        else:
            self.setEnabled(True)
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not search entries.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            

###############################################################################

    def processResults(self, results):
        statusBar = qApp.mainWidget().statusBar()
        tmpMessage = self.trUtf8("Received %1 entries").arg(unicode(len(results)))
        statusBar.message(tmpMessage, 10000)
        self.data={}
        if not(results == None):
            for x in results:
                self.data[x.getDN()] = x
            
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
            if tmpData.hasAttribute(self.primaryKey):
                name = tmpData.getAttributeValue(self.primaryKey, 0)
            else:
                if tmpData.hasAttribute('sn') or tmpData.hasAttribute('givenName'):
                    if tmpData.hasAttribute('sn'):
                        name = tmpData.getAttributeValue('sn', 0)
                    if tmpData.hasAttribute('givenName'):
                        if not(name == ''):
                            name = name + ' '
                        name += tmpData.getAttributeValue('givenName', 0)
                
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
        bindSuccess, exceptionObject = self.lumaConnection.bind()
        
        if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                return 
                
        success, resultList, exceptionObject = self.lumaConnection.search(dn, ldap.SCOPE_BASE)
        self.lumaConnection.unbind()
        
        self.itemIconView.blockSignals(False)
        
        if success:
            if len(resultList) > 0:
                self.emit(PYSIGNAL("about_to_change"), ())
                self.emit(PYSIGNAL("ldap_result"), (deepcopy(resultList[0]),))
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not access entry.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
        
###############################################################################

    def listItemClicked(self, entry):
        self.itemListView.blockSignals(True)
        
        if entry == None:
            return
            
        dn = self.entryDict[entry]
        bindSuccess, exceptionObject = self.lumaConnection.bind()
        
        if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                return 
                
        success, resultList, exceptionObject = self.lumaConnection.search(dn, ldap.SCOPE_BASE)
        self.lumaConnection.unbind()
        
        self.itemListView.blockSignals(False)
        
        if success:
            if len(resultList) > 0:
                self.emit(PYSIGNAL("about_to_change"), ())
                self.emit(PYSIGNAL("ldap_result"), (deepcopy(resultList[0]),))
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not access entry.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()

    
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
        
        tmpDialog = QMessageBox(self.trUtf8("Delete contact"),
                self.trUtf8("Do your really want to delete the selected contact?"),
                QMessageBox.Critical,
                QMessageBox.Yes,
                QMessageBox.No,
                QMessageBox.NoButton,
                self)
        
        tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
        tmpDialog.exec_loop()
        
        if not tmpDialog.result() == 4:
            if not self.deletePreProcess == None:
                self.deletePreProcess(self.SERVERMETA, dn)
                
            bindSuccess, exceptionObject = self.lumaConnection.bind()
            
            if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                return
            
            success, exceptionObject = self.lumaConnection.delete(dn)
            self.lumaConnection.unbind()
            
            if success:
                self.itemListView.setSelected(self.itemListView.firstChild(), True)
                del self.data[dn]
                if not self.deletePostProcess == None:
                    self.deletePostProcess(self.SERVERMETA, dn)
                    
                self.showResults()
            else:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not delete entry.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()

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
            tmpString =  "Could not read configuration file. Reason:\n"
            tmpString += str(e)
            environment.logMessage(LogObject("Debug", tmpString))
            
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
        
###############################################################################

    def baseChanged(self, itemText):
        self.search()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
