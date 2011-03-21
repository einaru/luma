'''
Created on 16. mars 2011

@author: Simen
'''

from PyQt4 import QtCore
from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex

class ObjectclassTableModel(QAbstractTableModel):
    
    def __init__(self, parent = None):
        QAbstractTableModel.__init__(self)
        self._templateObject = None
        
    def setTemplateObject(self, templateObject = None):
        self._templateObject = templateObject
        self.reset()
        
    def addRow(self, objectclass):
        if self._templateObject:
            self._templateObject.addObjectclass(objectclass)
    
    def removeRow(self, objectclass):
        if self._templateObject:
            self._templateObject.deleteObjectclass(objectclass)
            return True
        return False
    
    def getObjectclass(self, index):
        if index.row() < self._templateObject.getCountObjectclasses:
            return self._templateObject.objectclasses[index.row()]
        
    def setData(self, index, value, role = Qt.EditRole):
        """
        Handles updating data in the TemplateObjects
        """
        return False
#            if not index.isValid():
#                return False
#    
#            value = value.toPyObject()
#            #value = index.internalPointer()
#            
#            row = index.row()
#            column = index.column()
#            
#            # Find the templateobject from the list of them
#            templateObject = self._templateList.getTable()[row]
#            
#            # Update the correct field in it (given by the column) with the given data
#            templateObject.setIndexToValue(column, value)
#            
#            # Let other views know the underlying data is (possibly) changed
#            self.emit(QtCore.SIGNAL("dataChanged( const QModelIndex&, const QModelIndex& )"), index, index)
#            return True
        
    def rowCount(self,parent = QModelIndex()):
        #Number of objectclass
        if self._templateObject:
            return self._templateObject.getCountObjectclasses()
        return 0
    
    def columnCount(self,parent = QModelIndex()):
        return 1
    
    def flags(self, index):
        if not index.isValid(): 
            return QVariant()
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
    
    def data(self,index,role = Qt.DisplayRole):
        """
        Handles getting the correct data from the TemplateObjects and returning it
        """
        if not index.isValid():
            return QVariant()
        
        row = index.row()
        column = index.column()
        
        if role == Qt.DisplayRole and self._templateObject:
            # getTable() return a list of all the TemplateObjects
            return self._templateObject.objectclasses[row]

            # return the property set in the given column
            # correct painting/displaying of it is done by a delegate if needed


