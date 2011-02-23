
import ldap

from base.backend.LumaConnection import LumaConnection
from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from LDAPTreeItem import LDAPTreeItem
from PyQt4 import QtCore
from PyQt4.QtGui import QPixmap, QIcon

class ServerTreeItem(AbstractLDAPTreeItem):
    """
    Represents the servers in the model.
    """

    def __init__(self, data, serverMeta=None, parent=None, modelParent = None):
        AbstractLDAPTreeItem.__init__(self, parent, modelParent = modelParent)
        self.itemData = data
        self.serverMeta = serverMeta
        self.rootItem = parent
        
        self.isWorking.connect(self.rootItem.isWorking)
        self.doneWorking.connect(self.rootItem.doneWorking)


    def columnCount(self):
        return len(self.itemData)

    def data(self, column, role):
        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.DecorationRole:
            return QtCore.QVariant()
        
        if role == QtCore.Qt.DecorationRole:
            return QIcon(QPixmap(":/images/server.png"))
        else:
            return self.itemData[column]

    def smartObject(self):
        return self.itemData[1]

    def populateItem(self):
        """
        Gets the list of baseDNs for the server and adds them as children.
        """
        self.isWorking.emit()

        self.connection = LumaConnection(self.serverMeta)
        success, tmpList, exceptionObject = self.connection.getBaseDNList()
        
        self.doneWorking.emit()
        
        if not success:
            self.displayError(exceptionObject)
            return
        
        self.isWorking.emit()
        
        # Clear list of baseDNs
        self.childItems = []
        for base in tmpList:
            success, resultList, exceptionObject = self.connection.search(base, \
                    scope=ldap.SCOPE_BASE,filter='(objectclass=*)', sizelimit=1)
            if not success:
                    self.displayError(exceptionObject)
                    continue
            tmp = LDAPTreeItem(resultList[0], self, self, modelParent = self.modelParent)            
            self.appendChild(tmp)
            
        self.doneWorking.emit()
        self.populated = 1
        