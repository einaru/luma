# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2008 by Vegar Westerlund
#    <vegarwe@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget#, QAction
#from PyQt4.QtCore import pyqtSlot, QModelIndex
#import modeltest

#import environment
from base.backend.ServerList import ServerList
from model.LDAPTreeItemModel import LDAPTreeItemModel
from item.AbstractLDAPTreeItem import AbstractLDAPTreeItem
from plugins.browser_plugin.item.ServerTreeItem import ServerTreeItem
from plugins.browser_plugin.AdvancedObjectView import AdvancedObjectView


class BrowserView(QWidget):

    def __init__(self, parent, configPrefix = None):
        """
        Configprefix defines the location of serverlist.xml
        """
        QtGui.QWidget.__init__(self, parent)

        self.setObjectName("PLUGIN_BROWSER")
        self.openSmartObjects = []
        
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
        # For right-clicking in the tree
        self.entryList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.entryList.customContextMenuRequested.connect(self.rightClick)
        # When something is clicked, call self.initEntryView
        self.entryList.doubleClicked.connect(self.initEntryView)
        
        # The editor for entries
        self.tabWidget = QtGui.QTabWidget(self)
        self.setMinimumWidth(200)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.tabCloseClicked)

            
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
                    menu.addAction("Reload", self.reloadChoosen)
                if supports & AbstractLDAPTreeItem.SUPPORT_FILTER:
                    menu.addAction("Filter", self.filterChoosen)
                if supports & AbstractLDAPTreeItem.SUPPORT_LIMIT:
                    menu.addAction("Limit", self.limitChoosen)
                if supports & AbstractLDAPTreeItem.SUPPORT_CLEAR:
                    menu.addAction("Clear", self.clearChoosen)
            
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


    def initEntryView(self, index):
        """
        Loads the entry-viewer with the content from the index clicked
        """
        
        # If we clicked a server -- ignore
        if isinstance(index.internalPointer(), ServerTreeItem):
            """
            Servers doesn't have a smartObject
            """
            return
        
        # If it's an ErrorItem
        if index.internalPointer().smartObject() == None:
            return
        
        # Elso, gogo
        self.viewItem(index)
        
    def viewItem(self, index):
        smartObject = index.internalPointer().smartObject()
        
        if smartObject == None:
            return
        
        # Saves a representation of the opened entry to avoid opening duplicates
        serverName = smartObject.getServerAlias()
        dn = smartObject.getDN()
        rep = (serverName,dn)
        
        if self.openSmartObjects.count(rep) > 0:
            """Already open"""
            return
        
        self.openSmartObjects.append( (serverName,dn) )

        x = AdvancedObjectView(smartObject)
        self.tabWidget.addTab(x, x.ldapDataObject.getPrettyRDN())
        self.tabWidget.setCurrentWidget(x)
    
        
    def tabCloseClicked(self, index):
        #TODO Check if should save etc etc
        sO = self.tabWidget.widget(index).getSmartObject()

        # Remove the representation of the opened entry from the list
        serverName = sO.getServerAlias()
        dn = sO.getDN()
        rep = (serverName,dn)
        self.openSmartObjects.remove(rep)
        
        self.tabWidget.removeTab(index)

    def buildToolBar(self, parent):
        # FIXME: qt4 migration needed
        #self.entryView.buildToolBar(parent)
        pass


