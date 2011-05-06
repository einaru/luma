# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Christian Forfang, <cforfang@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

from PyQt4.QtGui import QMessageBox

class AbstractLDAPTreeItem(object):
    """
    This is an abstract class which the items of the LDAPTreeItemModel should subclass.
    """
    
    # Used from getSupportedOperations()
    # which returns the result of or-ing (|) the supported operations
    # e.g. "return SUPPORT_FILTER | SUPPORT_LIMIT"
    # to indicate what the item supports.
    SUPPORT_NONE = 0 # Should only be used alone
    SUPPORT_RELOAD = 1 # Probably works on all items
    SUPPORT_FILTER = 2 # Indicates the item has implement setFilter
    SUPPORT_LIMIT = 4 # Indicates the item has implement setLimit
    SUPPORT_CLEAR = 8 # Probably works on all items
    SUPPORT_ADD = 16 # Can add child-items
    SUPPORT_DELETE = 32 # Can remove this item
    SUPPORT_EXPORT = 64 # Can be exported
    SUPPORT_OPEN = 128 # Can be opened (has smartdataobject)
    SUPPORT_CANCEL = 256 # Can be canceled
    
    def __init__(self, serverParent, parent):
        """
        serverParent = the LDAPServerItem this item is under
        parent = the item above this
        """
        self.serverParent = serverParent
        self.parentItem = parent
        
        # The list of childs to this item
        self.childItems = []
        
        # Indicated if the item's list of childs has been populate
        # (i.e. one can use rowCount() without the additional penalty
        # of aquiring the items.
        self.populated = 0
        self.loading = False
        
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
        Should NOT use this in new code.
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

    def getParentServerItem(self):
        return self.serverParent
