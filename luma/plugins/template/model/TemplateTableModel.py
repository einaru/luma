'''
Created on 16. mars 2011

@author: Simen
'''
from PyQt4.QtCore import QAbstractTableModel, QModelIndex
from PyQt4.QtCore import Qt, SIGNAL, QVariant

from ..TemplateObject import TemplateObject

class TemplateTableModel(QAbstractTableModel):
    
    def __init__(self, templateList, parent = None):
        QAbstractTableModel.__init__(self)
        self._templateList = templateList
        
    def insertRow(self, tO):
        if tO:
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            self._templateList.addTemplate(tO)
            self.endInsertRows()
            return True
        return False
    
    def removeRow(self, index):
        self.beginRemoveRows(QModelIndex(), index.row(), index.row())
        self._templateList.deleteTemplateByIndex(index.row())
        self.endRemoveRows()
        return True
        
    def setData(self, index, value, role = Qt.EditRole):
        """
        Handles updating data in the TemplateObjects
        """
        
        if not index.isValid():
            return False

        value = value.toPyObject()
        #value = index.internalPointer()
        
        row = index.row()
        column = index.column()
        
        # Find the templateobject from the list of them
        templateObject = self._templateList.getTable()[row]
        
        # Update the correct field in it (given by the column) with the given data
        templateObject.setIndexToValue(column, value)      
        
        # Let other views know the underlying data is (possibly) changed
        self.emit(SIGNAL("dataChanged( const QModelIndex&, const QModelIndex& )"), index, index)
        return True
        
    def rowCount(self,parent = QModelIndex()):
        #Number of templates
        return len(self._templateList.getTable())
    
    def columnCount(self,parent):
        #Number of different settings for the templates
        return TemplateObject.numFields
    
    def flags(self, index):
        if not index.isValid(): 
            return QVariant()
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled
    
    def data(self,index,role = Qt.DisplayRole):
        """
        Handles getting the correct data from the TemplateObjects and returning it
        """
        
        if not index.isValid(): 
            return QVariant()
        
        row = index.row()
        column = index.column()
        
        if role == Qt.DisplayRole or role ==Qt.EditRole:
            # getTable() return a list of all the TemplateObjects
            templateObject = self._templateList.getTable()[row]

            # return the property set in the given column
            # correct painting/displaying of it is done by a delegate if needed
            return templateObject.getList()[column]

