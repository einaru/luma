# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2008 by Vegar Westerlund
#    <vegarwe@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4 import QtCore, QtGui
import modeltest

#import environment
from base.backend.ServerList import ServerList
from model.LDAPTreeItemModel import LDAPTreeItemModel
from model.LDAPEntryModel import LDAPEntryModel


class BrowserView(QtGui.QWidget):

    def __init__(self, parent=None, configPrefix = None):
        QtGui.QWidget.__init__(self, parent)

        self.setObjectName("PLUGIN_BROWSER")

        self.mainLayout = QtGui.QHBoxLayout(self)
        self.splitter = QtGui.QSplitter(self)

        self.entryList = QtGui.QTreeView(self.splitter)
        self.entryList.setMinimumWidth(200)

        self.entryView = QtGui.QTableView(self.splitter)

        self.connect(self.entryList, QtCore.SIGNAL("clicked(const QModelIndex &)"), self.initEntryView)
        self.mainLayout.addWidget(self.splitter)

        self.serverList = ServerList(configPrefix)

        self.initView(parent)
        
        self.entryList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.entryList, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.rightClick)
        
    def rightClick(self, point):
        clickedIndex = self.entryList.indexAt(point)
        clickedItem = clickedIndex.internalPointer()
        
        if clickedItem != None:
            menu = clickedItem.getContextMenu(QtGui.QMenu())
            menu.exec_(self.entryList.mapToGlobal(point))
            self.entryList.model().emit(QtCore.SIGNAL("layoutChanged()"))
        

###############################################################################
    
    def initView(self, parent=None):
        self.ldaptreemodel = LDAPTreeItemModel(parent)
        self.ldaptreemodel.populateModel(self.serverList)

        #OBS TODO 
        #self.modelTest = modeltest.ModelTest(self.ldaptreemodel, parent)
        
        #self.ldaptreemodel.populateSingleModel(self.serverList.getServerObject("abakus"))
        self.connect(self.ldaptreemodel, QtCore.SIGNAL("dataChanged"), self.entryList.dataChanged)

        self.entryList.setModel(self.ldaptreemodel)

    def initEntryView(self, index):
        print "initEntryView"
        self.model = LDAPEntryModel(index)
        self.entryView.setModel(self.model)

###############################################################################

    def buildToolBar(self, parent):
        # FIXME: qt4 migration needed
        #self.entryView.buildToolBar(parent)
        pass
