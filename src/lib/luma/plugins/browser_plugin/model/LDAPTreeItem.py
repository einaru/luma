'''
Created on 18. feb. 2011

@author: Simen
'''

import ldap
from AbstractLDAPTreeItem import AbstractLDAPTreeItem

class LDAPTreeItem(AbstractLDAPTreeItem):

    def __init__(self, data, serverParent, parent=None):
        self.parentItem = parent
        self.serverParent = serverParent
        self.itemData = data
        self.childItems = []
        self.populated = 0


    def columnCount(self):
        return 1
    
    def data(self, column):
        return self.itemData.getPrettyRDN()

    def smartObject(self):
        return self.itemData

    def populateItem(self):
        l = self.serverParent.connection
        success, resultList, exceptionObject = l.search(self.itemData.getDN(), \
                scope=ldap.SCOPE_ONELEVEL,filter='(objectclass=*)')

        if not success:
            return

        for x in resultList:
            tmp = LDAPTreeItem(x, self.serverParent, self)
            self.appendChild(tmp)

        self.populated = 1
        
    def getContextMenu(self, menu):
        menu.addAction("Sup?")
        return menu
    