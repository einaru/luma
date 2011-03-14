'''
Created on 18. feb. 2011

@author: Simen
'''
import os

from PyQt4 import QtCore, QtGui
from LDAPTreeItemModel import LDAPTreeItemModel
from plugins.browser_plugin.item.ServerTreeItem import ServerTreeItem

class LDAPEntryModel(QtCore.QAbstractTableModel):
    """
    Used by the LDAP-entry-viewer/editor.
    """
    
    def __init__(self, index, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        
        self.index = index
        self.itemData = []

        
        data = index.internalPointer().smartObject().data
        for key in data.keys():
            for value in data[key]:
                self.itemData.append([key, value])


    
    def getRootDN(self):
        return self.index.internalPointer().smartObject().getPrettyDN()

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
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.itemData[index.row()][index.column()])


    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        if index.column() == 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
