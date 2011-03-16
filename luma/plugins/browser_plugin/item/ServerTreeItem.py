
import ldap

from base.backend.LumaConnection import LumaConnection
from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from LDAPTreeItem import LDAPTreeItem
from PyQt4 import QtCore
from PyQt4.QtGui import QPixmap, QIcon
import logging
from plugins.browser_plugin.item.LDAPErrorItem import LDAPErrorItem

class ServerTreeItem(AbstractLDAPTreeItem):
    """
    Represents the servers in the model.
    """
    
    logger = logging.getLogger(__name__)

    def __init__(self, data, serverMeta=None, parent=None):
        AbstractLDAPTreeItem.__init__(self, parent)
        self.itemData = data
        self.serverMeta = serverMeta
        self.rootItem = parent

    def columnCount(self):
        return len(self.itemData)

    def data(self, column, role):
        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.DecorationRole:
            return QtCore.QVariant()
        
        if role == QtCore.Qt.DecorationRole:
            return QIcon(QPixmap(":/icons/network-server"))
        else:
            return self.itemData[column]

    def smartObject(self):
        return self.itemData[1]
    
    def fetchChildList(self):
        """
        Gets the list of baseDNs for the server and return them.
        """
                
        connection = LumaConnection(self.serverMeta)
        
        # If baseDNs are aleady spesified
        if self.serverMeta.autoBase == False:
            self.logger.debug("autoBase=False")
            tmpList = self.serverMeta.baseDN
            
            #Need to bind in order to fetch the data for the baseDNs
            bindSuccess, exceptionObject = connection.bind()
            if not bindSuccess:
                self.logger.debug("Bind failed.")
                self.displayError(exceptionObject)
                return
            
        # Else get them from the server
        else:
            self.logger.debug("Using getBaseDNList()")
            #self.isWorking.emit()
            success, tmpList, exceptionObject = connection.getBaseDNList()
        
            if not success:
                self.logger.debug("getBaseDNList failed")
                self.displayError(exceptionObject)
                return
            
            #getBaseDNList calles unbind(), so let's rebind
            connection.bind()
        
        self.logger.debug("Entering for-loop")

        # Get the info for the baseDNs
        newChildList = []
        for base in tmpList:
            success, resultList, exceptionObject = connection.search(base, \
                    scope=ldap.SCOPE_BASE,filter='(objectclass=*)', sizelimit=1)
            if not success:
                self.logger.debug("Couldn't search item")
                #self.displayError(str(base)+": "+str(exceptionObject))
                #tmp = LDAPTreeItem(resultList[0], self, self)    
                tmp = LDAPErrorItem(str(base+" [Error]"), self, self)
                newChildList.append(tmp)
                continue
            
            self.logger.debug("Found item")
            tmp = LDAPTreeItem(resultList[0], self, self)    
            newChildList.append(tmp)
            
        self.logger.debug("End populatItem")
        
        return newChildList
        
    def getSupportedOperations(self):
        return AbstractLDAPTreeItem.SUPPORT_CLEAR|AbstractLDAPTreeItem.SUPPORT_RELOAD
        