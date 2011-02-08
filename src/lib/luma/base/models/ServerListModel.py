# -*- coding: utf-8 -*-

from PyQt4 import  QtCore, QtGui
from base.backend.ServerObject import ServerObject

class ServerListModel(QtCore.QAbstractTableModel):
    
    def __init__(self, ServerList, parent = None):
        QtCore.QAbstractTableModel.__init__(self)
        
        self._ServerList = ServerList
        self.i = 0
        
    def setData(self, index, value, role = QtCore.Qt.EditRole):

        value = QtCore.QVariant.toPyObject(value)
        #value = index.internalPointer()
        print "setData:",value
        
        if not index.isValid(): 
            return False
        
        row = index.row()
        column = index.column()
        
        serverObject = self._ServerList.getTable()[row]
        serverObject.setIndexToValue(column,value)      
            
        self.emit(QtCore.SIGNAL("dataChanged( const QModelIndex&, const QModelIndex& )"), index, index)
        return True
        
    def rowCount(self,parent):
        return len(self._ServerList.getTable())
    
    def columnCount(self,parent):
        return ServerObject.numFields
    
    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
    
    def data(self,index,role = QtCore.Qt.DisplayRole):
        
        if not index.isValid(): 
            return QtCore.QVariant()
        
        row = index.row()
        column = index.column()
        
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            self.i = self.i + 1
            #print self.i
            serverObject = self._ServerList.getTable()[row]
            return serverObject.getList()[column]

