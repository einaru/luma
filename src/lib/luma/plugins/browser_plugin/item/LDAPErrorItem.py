from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from PyQt4.QtGui import QMessageBox, QInputDialog, QIcon, QPixmap
from PyQt4 import QtCore

"""
Currently not used.
"""

class LDAPErrorItem(AbstractLDAPTreeItem):
    
    def __init__(self, data, serverParent, parent=None, modelParent = None):
        AbstractLDAPTreeItem.__init__(self, parent, modelParent = modelParent)
        
        if data != None:
            self.error = data
        else:
            self.error = "Error!"
        
        self.populated = 1
        
    def data(self, column, role):
        if not role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return self.error
    
    def columnCount(self):
        return 1
    
    def smartObject(self):
        return None
    
    def getContextMenu(self, menu):
        menu.addAction("Nothing")
        return menu
        