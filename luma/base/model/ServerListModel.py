# -*- coding: utf-8 -*-

from PyQt4.QtCore import QAbstractTableModel
from PyQt4.QtCore import Qt, QVariant
from ..backend.ServerObject import ServerObject

class ServerListModel(QAbstractTableModel):
    """
    Defines a tablemodel where rows are the different servers and columns are the properties of it.
    """
    
    def __init__(self, serverList, parent = None):
        QAbstractTableModel.__init__(self, parent)
        self._serverList = serverList
        
    def removeRows(self, row, count):
        self._serverList.deleteServerByIndex(row)
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
        
        # Update the correct field in it (given by the column) with the given data
        serverObject.setIndexToValue(column, value)   
        
        # Let other views know the underlying data is changed
        self.dataChanged.emit(index, index)
        #self.emit(SIGNAL("dataChanged( const QModelIndex&, const QModelIndex& )"), index, index)
        return True
        
    def rowCount(self,parent):
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

