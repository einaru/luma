'''
Created on 16. mars 2011

@author: Simen
'''

from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex
from PyQt4.QtGui import QIcon
from ..TemplateObject import AttributeObject

class AttributeTableModel(QAbstractTableModel):
    
    def __init__(self, parent = None):
        QAbstractTableModel.__init__(self)
        self.attributes = {}
        
    def setTemplateObject(self, templateObject = None):
        if templateObject:
            self.attributes = templateObject.attributes
        else:
            self.attributes = {}
        self.reset()

    def addRow(self, name, must, single, binary, defaultValue):
        if not name in self.attributes or not self.attributes[name].must:
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            self.attributes[name] = AttributeObject(name, must, single, binary, defaultValue)
            self.endInsertRows()
            return True
        else:
            self.attributes[name].defaultValue = defaultValue
        return False


    def removeRows(self, indexes):
        attributes = []
        for i in indexes:
            if i.column() == 0:
                attr = self.getAttribute(i)
                if not attr.must:
                    attributes.append(attr)
        for a in attributes:
            self.beginRemoveRows(QModelIndex(), self.getIndexRow(a), self.getIndexRow(a))
            if a:
                self.attributes.pop(a.attributeName)
            self.endRemoveRows()

    def removeAlways(self, attribute):
        self.beginRemoveRows(QModelIndex(), self.getIndexRow(attribute), self.getIndexRow(attribute))
        self.attributes.pop(attribute.attributeName)
        self.endRemoveRows()

    def getAttribute(self, index):
        if index.row() < len(self.attributes) and index.column() == 0:
            return self.attributes.items()[index.row()][1]
        return None
    
    def getIndexRow(self, attribute):
        return self.attributes.values().index(attribute)

    def setData(self, index, value, role = Qt.EditRole):
        """
        Handles updating data in the TemplateObjects
        """
        print "AttributeTableModel: setData()"
        if index.column() == 4:
            print "default value?"
            print value.toString()
            self.attributes.items()[index.row()][1].defaultValue = value.toString()
            return True
        return False
    
    def rowCount(self,parent = QModelIndex()):
        #Number of objectclass
        return len(self.attributes)
    
    def columnCount(self,parent = QModelIndex()):
        return 5
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Attribute"
                if section == 1:
                    return "Must"
                if section == 2:
                    return "Single"
                if section == 3:
                    return "Binary"
                if section == 4:
                    return "Default value"

    def flags(self, index):
        if not index.isValid():
            return QVariant()
        if index.column() == 4:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def data(self,index,role = Qt.DisplayRole):
        """
        Handles getting the correct data from the TemplateObjects and returning it
        """
        if not index.isValid():
            return QVariant()
        
        row = index.row()
        column = index.column()
        
        if role == Qt.DecorationRole:
            if column == 1 or column == 2 or column == 3:
                if self.attributes.items()[row][1].getList()[column]:
                    return QIcon(':/icons/ok')
                else:
                    return QIcon(':/icons/no')
        
        if (role == Qt.DisplayRole or role == Qt.EditRole):
            if column == 0 or column == 4:
                return self.attributes.items()[row][1].getList()[column]
            
    def index(self, row, column, parent):
        if row < 0 or column < 0:
            return QModelIndex()
        if row >= self.rowCount() or column >= self.columnCount():
            return QModelIndex()
        internalPointer = self.attributes.items()[row][1].getList()[column]
        return self.createIndex(row, column, internalPointer)
