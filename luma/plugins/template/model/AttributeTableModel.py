'''
Created on 16. mars 2011

@author: Simen
'''

from PyQt4 import QtCore
from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex
from PyQt4.QtGui import QIcon, QPixmap

class AttributeTableModel(QAbstractTableModel):
    
    def __init__(self, parent = None):
        QAbstractTableModel.__init__(self)
        self.templateObject = None
        
    def setTemplateObject(self, templateObject = None):
        self.templateObject = templateObject
        self.reset()

    def addRow(self, name, must, single, binary, defaultValue):
        if self.templateObject:
            self.templateObject.addAttribute(name, must, single, binary, defaultValue)
    
    def removeRow(self, attribute):
        if self.templateObject:
            self.templateObject.deleteAttribute(attribute)
            return True
        return False
    
    def getAttribute(self, index):
        if index.row() < self.templateObject.getCountAttributes():
            self.templateObject.attributes.keys()[index.row()]
        
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