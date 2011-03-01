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


class BrowserView(QWidget):

    def __init__(self, parent, configPrefix = None):
        QtGui.QWidget.__init__(self, parent)

        self.setObjectName("PLUGIN_BROWSER")

        self.mainLayout = QtGui.QHBoxLayout(self)
        self.splitter = QtGui.QSplitter(self)

        self.entryList = QtGui.QTreeView(self.splitter)
        self.entryList.setMinimumWidth(200)

        self.entryView = TableView(self.splitter)

        #self.entryList.clicked.connect(self.initEntryView)
        #self.connect(self.entryList, QtCore.SIGNAL("clicked(const QModelIndex &)"), self.initEntryView)
                
        self.mainLayout.addWidget(self.splitter)

        self.serverList = ServerList(configPrefix)

        self.initView(parent)
        
        self.entryList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.connect(self.entryList, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.rightClick)
        self.entryList.customContextMenuRequested.connect(self.rightClick)

        
    def rightClick(self, point):
        self.clickedIndex = self.entryList.indexAt(point)
        self.ldaptreemodel.currentIndex = self.clickedIndex
        clickedItem = self.clickedIndex.internalPointer()
        
        if clickedItem != None:
            """
            TODO: Get supported actions from item and add them to menu
            """
            #menu = clickedItem.getContextMenu(QtGui.QMenu())
            menu = QtGui.QMenu()
            #someSignal = QtCore.pyqtSignal(QtCore.QPoint)
            #someSignal.connect(self.ldaptreemodel.reloadPoint)
            menu.addAction("Reload", self.reloadChoosen)
            menu.exec_(self.entryList.mapToGlobal(point))
    
    reloadSignal = QtCore.pyqtSignal(QtCore.QModelIndex)
    
    def reloadChoosen(self):
        self.reloadSignal.connect(self.ldaptreemodel.populateItem)
        self.reloadSignal.emit(self.clickedIndex)
            
    def initView(self, parent=None):
        self.ldaptreemodel = LDAPTreeItemModel(parent)
        self.ldaptreemodel.populateModel(self.serverList)

        self.entryList.setUniformRowHeights(True) #Major optimalization for big lists
        self.entryList.setModel(self.ldaptreemodel)

        #self.ldaptreemodel.dataChanged.connect(self.entryList.dataChanged)
        #self.connect(self.ldaptreemodel, QtCore.SIGNAL("dataChanged"), self.entryList.dataChanged)
        

    def initEntryView(self, index):
        if isinstance(index.internalPointer(), ServerTreeItem):
            """
            Servers doesn't have a smartObject
            """
            return
        if index.internalPointer().smartObject() == None:
            return
        self.model = LDAPEntryModel(index)
        self.entryView.setModel(self.model)

    def buildToolBar(self, parent):
        # FIXME: qt4 migration needed
        #self.entryView.buildToolBar(parent)
        pass

class TableView(QtGui.QTableView):

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setShowGrid(False)



