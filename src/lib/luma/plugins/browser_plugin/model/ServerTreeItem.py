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
        self.itemData = data
        self.serverMeta = serverMeta
        self.parentItem = parent
        self.childItems = []
        self.populated = 0

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        return self.itemData[column]

    def smartObject(self):
        return self.itemData[1]

    def populateItem(self):
        self.connection = LumaConnection(self.serverMeta)
        success, tmpList, exceptionObject = self.connection.getBaseDNList()

        for base in tmpList:
            success, resultList, exceptionObject = self.connection.search(base, \
                    scope=ldap.SCOPE_BASE,filter='(objectclass=*)', sizelimit=1)
            tmp = LDAPTreeItem(resultList[0], self, self)
            self.appendChild(tmp)

        self.populated = 1
        
    def getContextMenu(self, menu):
        menu.addAction("Skjera?")
        return menu
    