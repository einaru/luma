'''
Created on 18. feb. 2011

@author: Simen
'''
#from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox
#from PyQt4.QtCore import QObject

class AbstractLDAPTreeItem(object):
    """
    This is an abstract class which the items of the LDAPTreeItemModel should subclass.
    """
    
    # Used from getSupportedOperations()
    # which returns the result of or-ing (|) the supported operations
    # e.g. "return SUPPORT_FILTER | SUPPORT_LIMIT"
    SUPPORT_NONE = 0 # Should only be used alone
    SUPPORT_RELOAD = 1 # Probably works on all items
    SUPPORT_FILTER = 2 # Indicates the item has implement setFilter
    SUPPORT_LIMIT = 4 # Indicates the item has implement setLimit
    SUPPORT_CLEAR = 8 # Probably works on all items
    SUPPORT_ADD = 16 # Can add child-items
    SUPPORT_DELETE = 32 # Can remove this item
    SUPPORT_EXPORT = 64 # Can be exported
    SUPPORT_OPEN = 128 # Can be opened (has smartdataobject)
    
    def __init__(self, parent):
        """
        parent = the item above this
        """
        #QObject.__init__(self, parent)
        self.parentItem = parent
        
        # The list of childs to this item
        self.childItems = []
        
        # Indicated if the item's list of childs has been populate
        # (i.e. one can use rowCount() without the additional penalty
        # of aquiring the items.
        self.populated = 0
        
    def appendChild(self, item):
        """
        Adds a child to this item, and marks it as populated
        """
        self.childItems.append(item)
        self.populated = 1
        
    def removeChild(self, item):
        self.childItems.remove(item)
        
    def emptyChildren(self):
        """
        Drops list of children, but keep it marked populated
        """
        self.childItems = []
        self.populated = 1
    
    def child(self, row):
        """
        Returns the childs item at the given row
        """
        return self.childItems[row]

    def childCount(self):
        """
        Returns the number of children
        """
        return len(self.childItems)

    def parent(self):
        """
        Return this items parent-item.
        """
        return self.parentItem

    def row(self):
        """
        Returns this items rowNumber at its parent
        """
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    def displayError(self, exceptionObject):
        """
        Displays an error-box if populating it's child list fails.
        """
        QMessageBox.information(None,"Error","Couldn't populate list.\nError was: "+str(exceptionObject))

    def columnCount(self):
        """
        Returns the number of columns in this item.
        """
        raise NotImplementedError("Should be implemented")

    def data(self, column, role):
        """
        Returns the data for this item given an column and role.
        """
        raise NotImplementedError("Should be implemented")

    def smartObject(self):
        """
        Returns the smartObject related to this item.
        """
        raise NotImplementedError("Should be implemented")

    def fetchChildList(self):
        """
        Fetches the list of children from server. (Used for lazy-loading.)
        """
        raise NotImplementedError("Should be implemented")
        
    def getSupportedOperations(self):
        """
        Returns the result of or-ing (|) the supported operations (AbstractLDAPTreeItem.SUPPORT_X) for this item
        """
        raise NotImplementedError("Should be implemented")
