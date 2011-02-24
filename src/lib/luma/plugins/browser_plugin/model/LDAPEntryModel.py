'''
Created on 18. feb. 2011

@author: Simen
'''
import os

from PyQt4 import QtCore, QtGui
from LDAPTreeItemModel import LDAPTreeItemModel
from ServerTreeItem import ServerTreeItem
class LDAPEntryModel(QtCore.QAbstractTableModel):
    def __init__(self, index, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        
        self.index = index
        self.itemData = []

        iconPath = "./icons"
        self.editPicture = QtGui.QPixmap(os.path.join(iconPath, "edit.png"))
        self.deletePicture = QtGui.QPixmap(os.path.join(iconPath, "delete.png"))
        
        if isinstance(index.internalPointer(), ServerTreeItem):
            """
            Servers doesn't have a smartObject
            """
            return
        self.initData()
#       data = index.internalPointer().smartObject().data
#       for key in data.keys():
#           for value in data[key]:
#               self.itemData.append([key, value])
    def initData(self):
        self.itemData.extend([['Distinguished Name: ', self.getRootDN()]])
        self.itemData.extend([['ObjectClasses', '']])
        self.itemData.extend(self.getObjectClasses())
        self.attributesIndex = len(self.itemData)
        self.itemData.extend([['Attributes', '']])
        self.itemData.extend(self.getAttributes())



    def getRootDN(self):
        return self.index.internalPointer().smartObject().getDN()

    def getObjectClasses(self):
        smartObject = self.index.internalPointer().smartObject()
        classList = []
        for objectClass in smartObject.getObjectClasses():
            classList.append([objectClass, ''])
        return classList
        

    def getAttributes(self):
        smartObject = self.index.internalPointer().smartObject()
        attributeList = []
        for attribute in smartObject.getAttributeList():
            for value in smartObject.getAttributeValueList(attribute):
                attributeList.append([attribute, value])
        attributeList.sort()
        return attributeList



    def rowCount(self, parent):
        return len(self.itemData)

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role == QtCore.Qt.BackgroundRole:
            if index.row() == 0:
                return QtCore.QVariant(QtGui.QBrush(QtGui.QColor('#B3CAE7')))
            elif index.row() == 1 or index.row() == self.attributesIndex:
                return QtCore.QVariant(QtGui.QBrush(QtGui.QColor('#C4DFFF')))
            else: 
                return QtCore.QVariant(QtGui.QBrush(QtGui.QColor('#E5E5E5')))

        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        elif index.column() >= 2:
            return self.itemData[index.row()][index.column()]
        return QtCore.QVariant(self.itemData[index.row()][index.column()])

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        if index.column() == 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
