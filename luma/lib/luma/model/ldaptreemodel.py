#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2008 by Vegar Westerlund
#    <vegarwe@users.sourceforge.net>
###########################################################################

import ldap
from PyQt4 import QtCore
from base.backend.LumaConnection import LumaConnection

class LDAPItemModel(QtCore.QAbstractTableModel):
    def __init__(self, index, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)

        self.index = index
        self.itemData = []

        data = index.internalPointer().smartObject().data
        for key in data.keys():
            for value in data[key]:
                self.itemData.append([key, value])

    def rowCount(self, parent):
        return len(self.itemData)

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        return QtCore.QVariant(self.itemData[index.row()][index.column()])

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        if index.column() == 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

class LDAPTreeItem(object):

    def __init__(self, data, serverParent, parent=None):
        self.parentItem = parent
        self.serverParent = serverParent
        self.itemData = data
        self.childItems = []
        self.populated = 0

    def appendChild(self, item):
        self.populated = 1
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return 1

    def data(self, column):
        return self.itemData.getPrettyRDN()

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

    def smartObject(self):
        return self.itemData

    def populateItem(self):
        l = self.serverParent.connection
        success, resultList, exceptionObject = l.search(self.itemData.getDN(), \
                scope=ldap.SCOPE_ONELEVEL,filter='(objectclass=*)')

        if not success:
            return

        for x in resultList:
            tmp = LDAPTreeItem(x, self.serverParent, self)
            self.appendChild(tmp)

        self.populated = 1

class ServerTreeItem(object):

    def __init__(self, data, serverMeta=None, parent=None):
        self.itemData = data
        self.serverMeta = serverMeta
        self.parentItem = parent
        self.childItems = []
        self.populated = 0

    def appendChild(self, item):
        self.populated = 1
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        return self.itemData[column]

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

    def smartObject(self):
        return self.itemData[1]

    def populateItem(self):
        self.connection = LumaConnection(self.serverMeta)
        success, tmpList, exceptionObject = self.connection.getBaseDNList()

        for base in tmpList:
            success, resultList, exceptionObject = self.connection.search(base, \
                    scope=ldap.SCOPE_BASE,filter='(objectclass=*)', sizelimit=1)
            tmp = LDAPTreeItem(resultList[0], self, self)
            self.appendChild(tmp)

        self.populated = 1

class LDAPTreeItemModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()

        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        item = index.internalPointer()

        return QtCore.QVariant(item.data(index.column()))

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return QtCore.QVariant()

    def index(self, row, column, parent):
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        if not parentItem.populated:
            parentItem.populateItem()

        return parentItem.childCount()

    def hasChildren(self, parent):
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        if parentItem.populated:
            return parentItem.childCount() > 0

        return 1

    def populateModel(self, serverList):
        self.rootItem = ServerTreeItem([QtCore.QVariant("asdf")])
        self.rootItem.populated = 1

        for server in serverList.serverList:
            tmp = ServerTreeItem([server.name], server, self.rootItem)
            self.rootItem.appendChild(tmp)

    def populateSingleModel(self, server):
        self.rootItem = ServerTreeItem([QtCore.QVariant(server.name)], server)

    def setData(self, index, value, role):
        index.internalPointer().itemData[0] = "test"
        self.emit(QtCore.SIGNAL("dataChanged"), index, index)

