from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from PyQt4.QtGui import QIcon, QPixmap
from PyQt4 import QtCore

class LDAPErrorItem(AbstractLDAPTreeItem):
    """
    Used to indicate an error.
    """
    
    def __init__(self, data, serverParent, parent):
        AbstractLDAPTreeItem.__init__(self, serverParent, parent)
                
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
        return (None, None, None)
    
    def getSupportedOperations(self):
        return AbstractLDAPTreeItem.SUPPORT_NONE
        
