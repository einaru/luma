'''
Created on 18. feb. 2011

@author: Simen
'''

from base.backend.LumaConnection import LumaConnection
import ldap
from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from LDAPTreeItem import LDAPTreeItem

class ServerTreeItem(AbstractLDAPTreeItem):

    def __init__(self, data, serverMeta=None, parent=None):
        AbstractLDAPTreeItem.__init__(self, parent)
        self.itemData = data
        self.serverMeta = serverMeta
        self.rootItem = parent
        
        self.isWorking.connect(self.rootItem.isWorking)
        self.doneWorking.connect(self.rootItem.doneWorking)


    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        return self.itemData[column]

    def smartObject(self):
        return self.itemData[1]

    def populateItem(self):
        
        self.isWorking.emit()

        self.connection = LumaConnection(self.serverMeta)
        success, tmpList, exceptionObject = self.connection.getBaseDNList()
        
        self.doneWorking.emit()
        
        if not success:
            self.displayError(exceptionObject)
            return
        
        self.isWorking.emit()
        for base in tmpList:
            success, resultList, exceptionObject = self.connection.search(base, \
                    scope=ldap.SCOPE_BASE,filter='(objectclass=*)', sizelimit=1)
            if not success:
                    self.displayError(exceptionObject)
                    continue
            tmp = LDAPTreeItem(resultList[0], self, self)            
            self.appendChild(tmp)
        self.doneWorking.emit()

        self.populated = 1
        
    def getContextMenu(self, menu):
        menu.addAction("...")
        return menu
    