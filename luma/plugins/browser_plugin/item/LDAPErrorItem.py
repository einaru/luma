from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from PyQt4.QtGui import QMessageBox, QInputDialog, QIcon, QPixmap, qApp
from PyQt4 import QtCore

"""
Currently not used.
"""

class LDAPErrorItem(AbstractLDAPTreeItem):
    
    
    def __init__(self, data, serverParent, parent=None):
        AbstractLDAPTreeItem.__init__(self, parent)
                
        if data != None:
            self.error = data
        else:
            self.error = "Error!"
        
        self.populated = 1
        
    def data(self, column, role):
        if role == QtCore.Qt.StatusTipRole:
            return QtCore.QCoreApplication.translate("LDAPErrorItem","There was an error receiving this item or it's parent. See the attached error-message and/or the log for details.")
        if role == QtCore.Qt.DecorationRole:
            return QIcon(QPixmap(":/icons/no"))
        if not role == QtCore.Qt.DisplayRole:
            return None
        return self.error
    
    def columnCount(self):
        return 1
    
    def smartObject(self):
        return None
    
    def fetchChildList(self):
        return None
    
    def getSupportedOperations(self):
        return AbstractLDAPTreeItem.SUPPORT_NONE
        