'''
Created on 16. mars 2011

@author: Simen
'''

from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex
from PyQt4.QtGui import QIcon

class AttributeTableModel(QAbstractTableModel):
    
    def __init__(self, parent = None):
        QAbstractTableModel.__init__(self)
        self.templateObject = None
        
    def setTemplateObject(self, templateObject = None):
        self.templateObject = templateObject
        self.reset()

    def addRow(self, name, must, single, binary, defaultValue):
        if self.templateObject:
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            self.templateObject.addAttribute(name, must, single, binary, defaultValue)
            self.endInsertRows()
            return True
        return False
    
    def removeRows(self, indexes):
        if self.templateObject:
            attributes = []
            for i in indexes:
                if i.column() == 0:
                    attr = self.getAttribute(i)
                    if not attr.must:
                        attributes.append(attr)
            for a in attributes:
                self.beginRemoveRows(QModelIndex(), self.getIndexRow(a), self.getIndexRow(a))
                if a:
                    self.templateObject.deleteAttribute(attributeName = a.attributeName)
                self.endRemoveRows()
            print self.templateObject.getCountAttributes()
            return True
        return False

    def getAttribute(self, index):
        if index.row() < self.templateObject.getCountAttributes() and index.column() == 0:
            return self.templateObject.attributes.items()[index.row()][1]
        return None
    
    def getIndexRow(self, attribute):
        return self.templateObject.attributeIndex(attribute)

    def setData(self, index, value, role = Qt.EditRole):
        """
        Handles updating data in the TemplateObjects
        """
        print "AttributeTableModel: setData()"
        if index.column() == 4:
            print "default value?"
            print value.toString()
            self.templateObject.attributes.items()[index.row()][1].defaultValue = value.toString()
            return True
        return False
    
    def rowCount(self,parent = QModelIndex()):
        #Number of objectclass
        if self.templateObject:
            return self.templateObject.getCountAttributes()
        return 0
    
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
        
        if role == Qt.DecorationRole and self.templateObject:
            if column == 1 or column == 2 or column == 3:
                if self.templateObject.attributes.items()[row][1].getList()[column]:
                    return QIcon(':/icons/ok')
                else:
                    return QIcon(':/icons/no')
        
        if (role == Qt.DisplayRole or role == Qt.EditRole) and self.templateObject:
            if column == 0 or column == 4:
                return self.templateObject.attributes.items()[row][1].getList()[column]