
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

    def __init__(self, data, serverMeta=None, parent=None, modelParent = None):
        AbstractLDAPTreeItem.__init__(self, parent, modelParent = modelParent)
        self.itemData = data
        self.serverMeta = serverMeta
        self.rootItem = parent
        
        self.isWorking.connect(self.rootItem.isWorking)
        self.doneWorking.connect(self.rootItem.doneWorking)

        # When True we have and index we can used to update the model with
        self.hasIndex = False

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
    
    def fetchChildList(self):
        """
        Gets the list of baseDNs for the server and adds them as children.
        """
        print "ServerTreeItem - fetchCHildList"
                
        connection = LumaConnection(self.serverMeta)
        
        if self.serverMeta.autoBase == False:
            self.logger.debug("autoBase=False")
            tmpList = self.serverMeta.baseDN
            
            #Need to bind in order to fetch the data for the baseDNs
            bindSuccess, exceptionObject = connection.bind()
            if not bindSuccess:
                self.logger.debug("Bind failed.")
                self.displayError(exceptionObject)
                return
        else:
            self.logger.debug("Using getBaseDNList()")
            #self.isWorking.emit()
            success, tmpList, exceptionObject = connection.getBaseDNList()
        
            if not success:
                self.logger.debug("getBaseDNList failed")
                self.displayError(exceptionObject)
                #self.populated = 1
                return
        
        #self.isWorking.emit()
        
        # Will be overriden if we mange to add some data
        #self.populated = 0
        
        self.logger.debug("Entering for-loop")

        newChildList = []
        for base in tmpList:
            success, resultList, exceptionObject = connection.search(base, \
                    scope=ldap.SCOPE_BASE,filter='(objectclass=*)', sizelimit=1)
            if not success:
                self.logger.debug("Couldn't search item")
                #self.displayError(str(base)+": "+str(exceptionObject))
                #tmp = LDAPTreeItem(resultList[0], self, self, modelParent = self.modelParent)    
                tmp = LDAPErrorItem(str(base+" [Error]"), self, self, self.modelParent)
                newChildList.append(tmp)
                continue
            
            self.logger.debug("Found item")
            tmp = LDAPTreeItem(resultList[0], self, self, modelParent = self.modelParent)    
            newChildList.append(tmp)
            
        # Replace with new list
        #self.beginUpdateModel()        
        #self.childItems = newChildList
        #self.populated = 1
        #self.endUpdateModel()        
            
        #self.doneWorking.emit()
        self.logger.debug("End populatItem")
        print "ServerTreeItem - populateItem- END"
        return newChildList
        
    def getContextMenu(self, menu):
        #Remember the index so the methods can use it for notifying the model
        # of changes.
        self.index = self.modelParent.currentIndex
        self.hasIndex = True
        
        #menu.addAction("Reload", self.populateItem)
        return menu
        