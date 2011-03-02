# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2008 by Vegar Westerlund
#    <vegarwe@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget, QAction
from PyQt4.QtCore import pyqtSlot, QModelIndex
import modeltest

#import environment
from base.backend.ServerList import ServerList
from model.LDAPTreeItemModel import LDAPTreeItemModel
from model.LDAPEntryModel import LDAPEntryModel
from item.LDAPTreeItem import LDAPTreeItem
from plugins.browser_plugin.item.ServerTreeItem import ServerTreeItem
from plugins.browser_plugin.AdvancedObjectView import AdvancedObjectView


class BrowserView(QWidget):

    def __init__(self, parent, configPrefix = None):
        QtGui.QWidget.__init__(self, parent)

        self.setObjectName("PLUGIN_BROWSER")
        
        # The serverlist used
        self.serverList = ServerList(configPrefix)

        self.mainLayout = QtGui.QHBoxLayout(self)
        self.splitter = QtGui.QSplitter(self)
        
        # The model for server-content
        self.ldaptreemodel = LDAPTreeItemModel(parent)
        self.ldaptreemodel.populateModel(self.serverList)
        
        # For testing ONLY
        # AND ONLY ON SMALL LDAP-SERVERS SINCE IT LOADS BASICALLY ALL ENTIRES
        #self.modeltest = modeltest.ModelTest(self.ldaptreemodel, self);
        
        # The view for server-content
        self.entryList = QtGui.QTreeView(self.splitter)
        self.entryList.setMinimumWidth(200)
        self.entryList.setUniformRowHeights(True) #Major optimalization for big lists
        self.entryList.setModel(self.ldaptreemodel)
        # For right-clicking in the tree
        self.entryList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.entryList.customContextMenuRequested.connect(self.rightClick)
        # When something is clicked, call self.initEntryView
        self.entryList.clicked.connect(self.initEntryView)
        
        # The editor for entries
        #self.entryView = TableView(self.splitter)
	self.entryView = AdvancedObjectView(self.splitter)

        self.mainLayout.addWidget(self.splitter)
        
        # Used to signal the ldaptreemodel with a index
        # which needs processing (reloading, clearing)
        self.reloadSignal.connect(self.ldaptreemodel.reloadItem)
        self.emptySignal.connect(self.ldaptreemodel.emptyItem)        
        
        # Working / needed?
        self.ldaptreemodel.dataChanged.connect(self.entryList.dataChanged)
        
    # Custom signals used
    reloadSignal = QtCore.pyqtSignal(QtCore.QModelIndex)
    emptySignal = QtCore.pyqtSignal(QtCore.QModelIndex)
    
    def rightClick(self, point):
        """
        Called when the view is right-clicked.
        Displays a menu with possible actions.
        """
        
        # Remember the index so it can be used from the method selected from the pop-up-menu
        self.clickedIndex = self.entryList.indexAt(point)
        #self.ldaptreemodel.currentIndex = self.clickedIndex #TODO REMOVE
        
        clickedItem = self.clickedIndex.internalPointer()
        if clickedItem != None:
            """
            TODO: Get supported actions from item and add them to menu
            """
            #menu = clickedItem.getContextMenu(QtGui.QMenu())
            menu = QtGui.QMenu()
            menu.addAction(u"Ikke alle operasjoner er mulig på alle items ennå.")
            menu.addAction(u"Når ferdig vil den sjekke hva som støttes og bare vise disse.")
            menu.addAction("Reload", self.reloadChoosen)
            menu.addAction("Clear", self.emptyChoosen)
            menu.addAction("Filter", self.filterChoosen)
            menu.addAction("Limit", self.limitChoosen)
            menu.exec_(self.entryList.mapToGlobal(point))
    
    
    """
    Following methods are called from a context-menu.
    self.clickedItem is set there.
    """
    def reloadChoosen(self):
        self.reloadSignal.emit(self.clickedIndex)
    def emptyChoosen(self):
        self.emptySignal.emit(self.clickedIndex)  
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
	self.model = LDAPEntryModel(index)
        self.entryView.setModel(self.model)
	self.entryView.displayValues()

    def buildToolBar(self, parent):
        # FIXME: qt4 migration needed
        #self.entryView.buildToolBar(parent)
        pass

class TableView(QtGui.QTableView):

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setShowGrid(False)



