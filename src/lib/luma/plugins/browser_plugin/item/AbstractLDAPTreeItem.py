'''
Created on 18. feb. 2011

@author: Simen
'''
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject

class AbstractLDAPTreeItem(QObject):
    """
    This is an abstract class which the items of the LDAPTreeItemModel should subclass.
    """
    
    # Used to signal the item is working on something which can take time.
    isWorking = QtCore.pyqtSignal()
    doneWorking = QtCore.pyqtSignal()
    
    def __init__(self, parent, modelParent):
        """
        parent = the item above this
        modelParent = the model the item is part of (possible unneccessary)
        """
        QObject.__init__(self, parent)
        self.modelParent = modelParent
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
        print "appendChild start"
        self.populated = 1
        self.childItems.append(item)
        print "appendChild end"
        
    def emptyChildren(self):
        """
        Drops list of children.
        """
        self.childItems = []
        self.populated = 0
    
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
        QtGui.QMessageBox.information(None,"Error","Couldn't populate list.\nError was: "+str(exceptionObject))

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

    def populateItem(self):
        """
        Populates the child-list of this item. (Used for lazy-loading.)
        """
        raise NotImplementedError("Should be implemented")
        
    def getContextMenu(self):
        raise NotImplementedError("Should be implemented")
    
    """
    Used to have the model signal changes.
    """
    def beginUpdateModel(self):
        if self.hasIndex:
            self.modelParent.beginRemoveRows(self.index, 0, self.childCount()-1)
        
    def endUpdateModel(self):
        if self.hasIndex:
            self.modelParent.endRemoveRows()
            self.hasIndex = False
