# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2008 by Vegar Westerlund
#    <vegarwe@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4 import QtCore, QtGui

import environment
from base.backend.ServerList import ServerList
from base.backend.LumaConnection import LumaConnection
from modules.ldaptreemodel import LDAPTreeItemModel, LDAPItemModel

class BrowserView(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setObjectName("PLUGIN_BROWSER")

        self.mainLayout = QtGui.QHBoxLayout(self)
        self.splitter = QtGui.QSplitter(self)

        self.entryList = QtGui.QTreeView(self.splitter)
        self.entryList.setMinimumWidth(200)

        self.entryView = QtGui.QTableView(self.splitter)

        self.connect(self.entryList, QtCore.SIGNAL("clicked(const QModelIndex &)"), self.initEntryView)
        self.mainLayout.addWidget(self.splitter)

        self.serverList = ServerList()
        self.serverList.readServerList()

        self.initView(parent)


###############################################################################
    
    def initView(self, parent=None):
        # TODO: Need a way to select server
        serverMeta = self.serverList.getServerObject('abakus')
        connectionObject = LumaConnection(serverMeta)
        bindSuccess, exceptionObject = connectionObject.bind()
            
        if not bindSuccess:
            environment.setBusy(False)
            ## TODO: Warn user    
            return

        # TODO: Determine base according to config, not this way
        success, tmpList, exceptionObject = connectionObject.getBaseDNList()

        self.ldaptreemodel = LDAPTreeItemModel(parent, serverMeta, connectionObject)
        self.ldaptreemodel.populateModel(tmpList)
        self.connect(self.ldaptreemodel, QtCore.SIGNAL("dataChanged"), self.entryList.dataChanged)

        self.entryList.setModel(self.ldaptreemodel)

    def initEntryView(self, index):
        self.model = LDAPItemModel(index)
        self.entryView.setModel(self.model)

###############################################################################

    def buildToolBar(self, parent):
        # FIXME: qt4 migration needed
        #self.entryView.buildToolBar(parent)
        pass
