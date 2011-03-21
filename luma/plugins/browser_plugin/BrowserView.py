# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2008 by Vegar Westerlund
#    <vegarwe@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget, QMessageBox #, QAction
#from PyQt4.QtCore import pyqtSlot, QModelIndex
#import modeltest

#import environment
from base.backend.ServerList import ServerList
from model.LDAPTreeItemModel import LDAPTreeItemModel
from item.AbstractLDAPTreeItem import AbstractLDAPTreeItem
from plugins.browser_plugin.item.ServerTreeItem import ServerTreeItem
from plugins.browser_plugin.AdvancedObjectView import AdvancedObjectView
from plugins.browser_plugin.NewEntryDialog import NewEntryDialog

class BrowserView(QWidget):
    
    def retranslateUi(self): 
        print "RETRANSLATE"
        self.tabWidget.setStatusTip(QtCore.QCoreApplication.translate("BrowserView","This is where entries are displayed when opened."))
        self.tabWidget.setToolTip(QtCore.QCoreApplication.translate("BrowserView","This is where entries are displayed when opened."))
        
    def changeEvent(self, e):
        if e.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi()
        else:
            QWidget.changeEvent(self, e)

    def __init__(self, parent = None, configPrefix = None):
        """
        Configprefix defines the location of serverlist.xml
        """
        QtGui.QWidget.__init__(self, parent)
        
        self.setObjectName("PLUGIN_BROWSER")
            
        # The serverlist used
        self.serverList = ServerList(configPrefix)
        self.mainLayout = QtGui.QHBoxLayout(self)
        
        self.splitter = QtGui.QSplitter(self)
        
        # The model for server-content
        self.ldaptreemodel = LDAPTreeItemModel(self)
        self.ldaptreemodel.populateModel(self.serverList)
        
        # For testing ONLY
        # AND ONLY ON SMALL LDAP-SERVERS SINCE IT LOADS BASICALLY ALL ENTIRES
        #self.modeltest = modeltest.ModelTest(self.ldaptreemodel, self);
        
        # The view for server-content
        self.entryList = QtGui.QTreeView(self)
        self.entryList.setMinimumWidth(200)
        self.entryList.setMaximumWidth(400)
        #self.entryList.setAlternatingRowColors(True)
        self.entryList.setAnimated(True) # Somewhat cool, but should be removed if deemed too taxing
        self.entryList.setUniformRowHeights(True) #Major optimalization for big lists
        self.entryList.setModel(self.ldaptreemodel)
        self.entryList.setMouseTracking(True)
        self.entryList.viewport().setMouseTracking(True)
        # For right-clicking in the tree
        self.entryList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.entryList.customContextMenuRequested.connect(self.rightClick)
        # When something is activated (doubleclick, <enter> etc.)
        self.entryList.activated.connect(self.viewItem)
        
        # The editor for entries
        self.tabWidget = QtGui.QTabWidget(self)
        self.tabWidget.setStatusTip(QtCore.QCoreApplication.translate("BrowserView","This is where entries are displayed when opened."))
        self.tabWidget.setToolTip(QtCore.QCoreApplication.translate("BrowserView","This is where entries are displayed when opened."))
        #self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        #self.tabWidget.setStyleSheet("QTabWidget::pane {border: 0; border-top: 30px solid qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 red, stop: 1 yellow); background: yellow; } QTabWidget::tab-bar { top: 30px; }")
        self.setMinimumWidth(200)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.tabCloseClicked)
        
        # Remember and looks up open tabs
        self.openTabs = {}

            
        self.splitter.addWidget(self.entryList)
        self.splitter.addWidget(self.tabWidget)
        self.mainLayout.addWidget(self.splitter)

        # Used to signal the ldaptreemodel with a index
        # which needs processing (reloading, clearing)
        self.reloadSignal.connect(self.ldaptreemodel.reloadItem)
        self.clearSignal.connect(self.ldaptreemodel.clearItem)        

        
    # Custom signals used
    reloadSignal = QtCore.pyqtSignal(QtCore.QModelIndex)
    clearSignal = QtCore.pyqtSignal(QtCore.QModelIndex)

    def rightClick(self, point):
        """
        Called when the view is right-clicked.
        Displays a menu with possible actions.
        """
        
        # Remember the index so it can be used from the method selected from the pop-up-menu
        self.clickedIndex = self.entryList.indexAt(point)
        
        clickedItem = self.clickedIndex.internalPointer()
        if clickedItem != None:
            
            menu = QtGui.QMenu()
            
            # Find out what the item supports
            supports = clickedItem.getSupportedOperations()
            
            if supports == 0:
                menu.addAction("No actions available")
                
            else:
                if clickedItem.smartObject() != None:
                    menu.addAction("Open", self.openChosen)
                # Add avaiable methods
                if supports & AbstractLDAPTreeItem.SUPPORT_RELOAD:
                    menu.addAction(self.tr("Reload children"), self.reloadChoosen)
                if supports & AbstractLDAPTreeItem.SUPPORT_FILTER:
                    menu.addAction(self.tr("Filter"), self.filterChoosen)
                if supports & AbstractLDAPTreeItem.SUPPORT_LIMIT:
                    menu.addAction(self.tr("Limit"), self.limitChoosen)
                if supports & AbstractLDAPTreeItem.SUPPORT_CLEAR:
                    menu.addAction(self.tr("Clear"), self.clearChoosen)
                if supports & AbstractLDAPTreeItem.SUPPORT_ADD:
                    m = QtGui.QMenu("Add", menu)
                    m.addAction(self.tr("Entry"), self.addEntryChosen)
                    m.addAction(self.tr("Template"), self.addTemplateChosen)
                    menu.addMenu(m)
                if supports & AbstractLDAPTreeItem.SUPPORT_DELETE:
                    m = QtGui.QMenu(self.tr("Delete"), menu)
                    m.addAction(self.tr("Entry"), self.addEntryChosen)
                    m.addAction(self.tr("Template"), self.addTemplateChosen)
                    menu.addMenu(m)

            
            menu.exec_(self.entryList.mapToGlobal(point))
    
    
    """
    Following methods are called from a context-menu.
    self.clickedItem is set there.
    """
    def openChosen(self):
        self.viewItem(self.clickedIndex)
    def reloadChoosen(self):
        self.reloadSignal.emit(self.clickedIndex)
    def clearChoosen(self):
        self.clearSignal.emit(self.clickedIndex)  
    def limitChoosen(self):
        # Have the item set the limit for us, the reload
        self.clickedIndex.internalPointer().setLimit()
        self.reloadSignal.emit(self.clickedIndex)
    def filterChoosen(self):
        # Have the item set the filter, then reload
        self.clickedIndex.internalPointer().setFilter()
        self.reloadSignal.emit(self.clickedIndex)
    def addEntryChosen(self):
        self.addNewEntry(self.clickedIndex)
    def addTemplateChosen(self):
        pass

    def addNewEntry(self, parentIndex, defaultSmartObject = None):
        tmp = NewEntryDialog(parentIndex, defaultSmartObject)
        if tmp.exec_():
            print "La til ny entry"
            # TODO Do something. (Reload?)
        
    def viewItem(self, index):
        
        smartObject = index.internalPointer().smartObject()
        
        # We need to have tried to open an items with a smartobject to proceed
        if smartObject == None:
            return
        
        # Saves a representation of the opened entry to avoid opening duplicates
        serverName = smartObject.getServerAlias()
        dn = smartObject.getDN()
        rep = (serverName,dn)
        
        if self.openTabs.has_key(str(rep)):
            x = self.openTabs[str(rep)]
            self.tabWidget.setCurrentWidget(x)
            return
        
        x = AdvancedObjectView(smartObject, QtCore.QPersistentModelIndex(index))
        self.openTabs[str(rep)] = x
        self.tabWidget.addTab(x, x.ldapDataObject.getPrettyRDN())
        self.tabWidget.setCurrentWidget(x)
    
        
    def tabCloseClicked(self, index):
        #TODO Check if should save etc etc
        clicked = self.tabWidget.widget(index).aboutToChange()
        if clicked == QMessageBox.Cancel:
            return
        sO = self.tabWidget.widget(index).getSmartObject()

        if not (sO == None):
            # Remove the representation of the opened entry from the list
            serverName = sO.getServerAlias()
            dn = sO.getDN()
            rep = (serverName,dn)
            self.openTabs.pop(str(rep))
        
        self.tabWidget.removeTab(index)

    def buildToolBar(self, parent):
        # Not used
        pass


