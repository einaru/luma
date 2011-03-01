#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2008 by Vegar Westerlund
#    <vegarwe@users.sourceforge.net>
###########################################################################

import ldap
from plugins.browser_plugin.item.ServerTreeItem import ServerTreeItem
from plugins.browser_plugin.item.RootTreeItem import RootTreeItem
from plugins.browser_plugin.item.LDAPErrorItem import LDAPErrorItem
from PyQt4 import QtCore
from PyQt4.QtCore import QAbstractItemModel
from base.backend.LumaConnection import LumaConnection

class LDAPTreeItemModel(QAbstractItemModel):
    """
    The model used by the QTreeView in the BrowserPlugin.
    """
       
    def __init__(self, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        
    def columnCount(self, parent):
        """
        Given a parent, how many children.
        """
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        """
        Returns data given an index and role.
        """
        
        if not index.isValid():
            return QtCore.QVariant()

        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.DecorationRole:
            return QtCore.QVariant()

        item = index.internalPointer()
        return QtCore.QVariant(item.data(index.column(), role))

    def flags(self, index):
        """
        Items are enabled and selectable.
        """
        
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        """
        The root defines the header.
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return QtCore.QVariant()

    def index(self, row, column, parent):
        """
        Creates and index given a row, column and parent.
        If the parent is invalid, use the root-item.
        """
        
        # Really needed? Should avoid calls to rowCount() where possible
        #if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
        #    return QtCore.QModelIndex()
        
        #print "Spør etter index for row",row," column",column,"parent",parent

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
        """
        Returns the index to the parent of a given index.
        """
        
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            # The root has no parent
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        """
        Returns the number of rows under the given parent (i.e. children)
        This should not be called to determine IF a parent has children, and
        it has to look up the exact number, that's what hasChildren() is for.
        """
        
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        if not parentItem.populated:
            parentItem.populateItem()
            # Updates the |>-icon to show if the item has children
            self.layoutChanged.emit()
        
        return parentItem.childCount()
        
    def hasChildren(self, parent):
        """
        Used to avoid (expensive) calls to rowCount()
        to find out it an item has children.
        
        Return True unless it's known to not have children
        (ie. it has already been loaded).
        """
        
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        if parentItem.populated:
            return parentItem.childCount() > 0
        
        # True
        return 1
    
    def populateModel(self, serverList):
        """
        Called after the model is initialized. Adds the servers to the root.
        """
        
        print "populateModel in Model"
        
        self.rootItem = RootTreeItem("Servere", self, self) # Also provides the header
        
        if not len(serverList.getTable()) > 0:
            # If there's no servers :(
            return

        for server in serverList.getTable():
            tmp = ServerTreeItem([server.name], server, self.rootItem, modelParent = self)
            self.rootItem.appendChild(tmp)
                
    def setData(self, index, value, role):
        # Not used.
        index.internalPointer().itemData[0] = "test"
        self.dataChanged.emit(index, index)
        #self.emit(QtCore.SIGNAL("dataChanged"), index, index)

