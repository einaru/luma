'''
Created on 16. mars 2011

@author: Simen
'''

from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex

class ObjectclassTableModel(QAbstractTableModel):
    
    def __init__(self, parent = None):
        QAbstractTableModel.__init__(self, parent)
        self.templateObject = None
        
    def setTemplateObject(self, templateObject = None):
        self.beginResetModel()
        self.templateObject = templateObject
        self.endResetModel()
        
    def insertRow(self, objectclass):
        if self.templateObject:
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            self.templateObject.addObjectclass(objectclass)
            self.endInsertRows()
            return True
        return False
    
    def removeRows(self, indexes):
        # We must get the objectclasses before we make any of their indexes invalid 
        if self.templateObject:
            objectclasses = map(self.getObjectclass, indexes)
            for o in objectclasses:
                self.beginRemoveRows(QModelIndex(), self.getIndexRow(o), self.getIndexRow(o))
                self.templateObject.deleteObjectclass(objectclass = o)
                self.endRemoveRows()
            return True
        return False
    
    def getObjectclass(self, index):
        if index.isValid():
            return index.internalPointer()
        return QVariant()

    def getIndexRow(self, objectclass):
        return self.templateObject.objectclassIndex(objectclass)
        
    def rowCount(self,parent = QModelIndex()):
        #Number of objectclass
        if self.templateObject:
            return self.templateObject.getCountObjectclasses()
        return 0
    
    def columnCount(self,parent = QModelIndex()):
        return 1
    
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
    
    def data(self,index,role = Qt.DisplayRole):
        """
        Handles getting the correct data from the TemplateObject and returning it
        """
        if not index.isValid():
            return QVariant()
        row = index.row()
        if role == Qt.DisplayRole and self.templateObject:
            # return the objectclass in the given row
            return self.templateObject.objectclasses[row]

    def index(self, row, column, parent):
        if row < 0 or column < 0:
            return QModelIndex()
        if row >= self.rowCount() or column >= self.columnCount():
            return QModelIndex()
        internalPointer = self.templateObject.objectclasses[row]
        return self.createIndex(row, column, internalPointer)
    
    
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
