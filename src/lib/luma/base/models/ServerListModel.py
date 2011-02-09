# -*- coding: utf-8 -*-

from PyQt4 import  QtCore, QtGui
from base.backend.ServerObject import ServerObject

class ServerListModel(QtCore.QAbstractTableModel):
    """
    Defines a tablemodel where rows are different servers and columns are the properties of it
    """
    
    def __init__(self, ServerList, parent = None):
        QtCore.QAbstractTableModel.__init__(self)
        self._ServerList = ServerList
        
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        """
        Handles updating data in the ServerObjects
        """

        value = value.toPyObject()
        #value = index.internalPointer()
        
        if not index.isValid(): 
            return False
        
        row = index.row()
        column = index.column()
        
        # Find the serverobject from the list of them
        serverObject = self._ServerList.getTable()[row]
        
        # Update the correct field in it (given by the column) with the given data
        serverObject.setIndexToValue(column, value)      
        
        # Let other views know the underlying data is (possibly) changed
        self.emit(QtCore.SIGNAL("dataChanged( const QModelIndex&, const QModelIndex& )"), index, index)
        return True
        
    def rowCount(self,parent):
        #Number of servers
        return len(self._ServerList.getTable())
    
    def columnCount(self,parent):
        #Number of different settings for the servers
        return ServerObject.numFields
    
    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
    
    def data(self,index,role = QtCore.Qt.DisplayRole):
        """
        Handles getting the correct data from the ServerObjects and returning it
        """
        
        if not index.isValid(): 
            return QtCore.QVariant()
        
        row = index.row()
        column = index.column()
        
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            # getTable() return a list of all the ServerObjects
            serverObject = self._ServerList.getTable()[row]

            # return the property set in the given column
            # correct painting/displaying of it is done by a delegate if needed
            # (e.g. the list of baseDNs is returned as a list and is splitted and displayed by the delegate)
            return serverObject.getList()[column]

