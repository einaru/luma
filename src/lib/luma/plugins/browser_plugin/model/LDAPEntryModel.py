'''
Created on 18. feb. 2011

@author: Simen
'''
from PyQt4 import QtCore
from LDAPTreeItemModel import LDAPTreeItemModel
from ServerTreeItem import ServerTreeItem
class LDAPEntryModel(QtCore.QAbstractTableModel):
    def __init__(self, index, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        
        self.index = index
        self.itemData = []
        
        if isinstance(index.internalPointer(), ServerTreeItem):
            """
            Servers doesn't have a smartObject
            """
            return
        
        data = index.internalPointer().smartObject().data
        for key in data.keys():
            for value in data[key]:
                self.itemData.append([key, value])

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
