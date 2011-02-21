'''
Created on 18. feb. 2011

@author: Simen
'''
#from PyQt4.QtCore import QObject
class AbstractLDAPTreeItem:

    def __init__(self):
        raise NotImplementedError("Should be implemented")

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


    def columnCount(self):
        raise NotImplementedError("Should be implemented")

    def data(self, column):
        raise NotImplementedError("Should be implemented")

    def smartObject(self):
        raise NotImplementedError("Should be implemented")

    def populateItem(self):
        raise NotImplementedError("Should be implemented")
    
    def getContextMenu(self):
        raise NotImplementedError("Should be implemented")