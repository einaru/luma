'''
Created on 16. mars 2011

@author: Simen
'''

from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex

class ObjectclassTableModel(QAbstractTableModel):
    
    def __init__(self, parent = None):
        QAbstractTableModel.__init__(self)
        self.templateObject = None
        
    def setTemplateObject(self, templateObject = None):
        self.templateObject = templateObject
        self.reset()
        
    def insertRow(self, objectclass):
        if self.templateObject:
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            self.templateObject.addObjectclass(objectclass)
            self.endInsertRows()
            return True
        return False
    
    def removeRows(self, indexes):
        if self.templateObject:
            objectclasses = map(self.getObjectclass, indexes)
            for o in objectclasses:
                self.beginRemoveRows(QModelIndex(), self.getIndexRow(o), self.getIndexRow(o))
                self.templateObject.deleteObjectclass(objectclass = o)
                self.endRemoveRows()
            return True
        return False
    
    def getObjectclass(self, index):
        if index.row() < self.templateObject.getCountObjectclasses:
            return self.templateObject.objectclasses[index.row()]

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
        
        if row >= len(self.templateObject.objectclasses):
            #TODO: See print...
            print "WHY index out of range?! second from the bottom deleted...?"
            print row, len(self.templateObject.objectclasses)
            row = row-1
        
        if role == Qt.DisplayRole and self.templateObject:
            # getTable() return a list of all the TemplateObjects
            return self.templateObject.objectclasses[row]

            # return the property set in the given column
            # correct painting/displaying of it is done by a delegate if needed


