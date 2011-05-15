# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Christian Forfang, <cforfang@gmail.com>
#
# Luma is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public Licence as published by 
# the Free Software Foundation; either version 2 of the Licence, or 
# (at your option) any later version.
#
# Luma is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence 
# for more details.
#
# You should have received a copy of the GNU General Public Licence along 
# with Luma; if not, write to the Free Software Foundation, Inc., 
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

from PyQt4.QtCore import QAbstractTableModel
from PyQt4.QtCore import Qt, QVariant, QModelIndex
from ..backend.ServerObject import ServerObject
from plugins.template.TemplateList import TemplateList

class ServerListModel(QAbstractTableModel):
    """
    Defines a tablemodel where rows are the different servers and columns are the properties of it.
    """
    
    def __init__(self, serverList, parent = None):
        QAbstractTableModel.__init__(self, parent)
        self._serverList = serverList

    def hasServers(self):
        return (self.rowCount(QModelIndex()) > 0)

    def addServer(self, serverObject):
        """ Adds server to model.

        @returns:
            tuple with (bool, QModelIndex)
            where bool = success/false on add
            and the QModelIndex is the position of the added server
        """
        # Insert into the model
        self.beginInsertRows(QModelIndex(), self.rowCount(QModelIndex()), self.rowCount(QModelIndex()) + 1) # Insert at end
        self._serverList.addServer(serverObject)
        self.endInsertRows()
        return (True, self.index(self.rowCount(QModelIndex())-1,0))

    def delServerAtIndex(self, index):
        if not index.isValid():
            return False

        self.beginRemoveRows(QModelIndex(), index.row(), index.row())
        self._serverList.deleteServerByIndex(index.row())
        self.endRemoveRows()
        return True
        
    def setData(self, index, value, role = Qt.EditRole):
        """
        Handles updating data in the ServerObjects
        """
        
        if not index.isValid(): 
            return False
        
        value = value.toPyObject()
        
        row = index.row()
        column = index.column()
        
        # Find the serverobject from the list of them
        serverObject = self._serverList.getTable()[row]
        
        # Check for an actual change
        if serverObject.getList()[column] == value:
            """
            No change so do nothing.
            """
            return True
        
        #name or hostname changed check the list of templates if it should be updated.
        if index.column() == 0:
            templateList = TemplateList()
            server = self._serverList.getTable()[index.row()]
            for template in templateList.getTable():
                if server.name == template.server:
                    if index.column() == 0:
                        template.server = value
                        
            templateList.save()
            
        # Update the correct field in it (given by the column) with the given data
        serverObject.setIndexToValue(column, value)   
        
        # Let other views know the underlying data is changed
        self.dataChanged.emit(index, index)
        return True
        
    def rowCount(self, parent):
        #Number of servers
        return len(self._serverList.getTable())

    def columnCount(self,parent):
        #Number of different settings for the servers
        return ServerObject.numFields
    
    def flags(self, index):
        if not index.isValid(): 
            return QVariant()
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled
    
    def data(self,index,role = Qt.DisplayRole):
        """
        Handles getting the correct data from the ServerObjects and returning it
        """
        
        if not index.isValid(): 
            return QVariant()
        
        row = index.row()
        column = index.column()
        
        if role == Qt.DisplayRole or role ==Qt.EditRole:
            # getTable() return a list of all the ServerObjects
            serverObject = self._serverList.getTable()[row]

            # return the property set in the given column
            # correct painting/displaying of it is done by a delegate if needed
            return serverObject.getList()[column]


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
