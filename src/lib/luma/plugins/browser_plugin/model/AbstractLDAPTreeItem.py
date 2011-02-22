'''
Created on 18. feb. 2011

@author: Simen
'''
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject

class AbstractLDAPTreeItem(QObject):
    
    isWorking = QtCore.pyqtSignal()
    doneWorking = QtCore.pyqtSignal()
    
    def __init__(self, parent, modelParent):
        QObject.__init__(self, parent)
        self.modelParent = modelParent
        self.childItems = []
        self.parentItem = parent
        self.populated = 0
        
    def appendChild(self, item):
        self.populated = 1
        self.childItems.append(item)
    
    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    def displayError(self, exceptionObject):
        QtGui.QMessageBox.information(None,"Error","Couldn't populate list.\nError was: "+str(exceptionObject))

    def columnCount(self):
        raise NotImplementedError("Should be implemented")

    def data(self, column, role):
        raise NotImplementedError("Should be implemented")

    def smartObject(self):
        raise NotImplementedError("Should be implemented")

    def populateItem(self):
        raise NotImplementedError("Should be implemented")
    
    def getContextMenu(self):
        raise NotImplementedError("Should be implemented")