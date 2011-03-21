

import ldap
from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from LDAPErrorItem import LDAPErrorItem
from PyQt4.QtGui import QMessageBox, QInputDialog, QIcon, QPixmap
from PyQt4 import QtCore
from base.backend.LumaConnection import LumaConnection

class LDAPTreeItem(AbstractLDAPTreeItem):
    """
    Used by LDAP-entries (as opposed to servers or rootitems).
    """
    
    # Defaults
    LIMIT_DEFAULT = 0
    FILTER_DEFAULT = "(objectClass=*)"
    
    # How many aquired entries before a messagebox 
    # pops up asking if the user want to load them all?
    ASK_TO_DISPLAY = 1000

    def __init__(self, data, serverParent, parent=None):
        AbstractLDAPTreeItem.__init__(self, parent)
        
        self.serverParent = serverParent
        self.itemData = data
        
        self.limit = LDAPTreeItem.LIMIT_DEFAULT
        self.filter = LDAPTreeItem.FILTER_DEFAULT

    def columnCount(self):
        """
        Has only one column = the name of the item.
        """
        return 1
    
    def data(self, column, role):
        """
        Returns the name and possibly an icon for the item.
        """
        
        # Return an icon if the item has been configured
        if role == QtCore.Qt.DecorationRole:
            if self.filter != LDAPTreeItem.FILTER_DEFAULT or self.limit != LDAPTreeItem.LIMIT_DEFAULT:
                return QIcon(QPixmap(":/icons/filter"))
            else:
                return None
        # Return applicable status-tip-role
        elif role == QtCore.Qt.StatusTipRole:
            if self.limit != LDAPTreeItem.LIMIT_DEFAULT and self.filter != LDAPTreeItem.FILTER_DEFAULT:
                return QtCore.QCoreApplication.translate("LDAPTreeItem","This item has both a filter and limit applied.")
            if self.filter != LDAPTreeItem.FILTER_DEFAULT:
                return QtCore.QCoreApplication.translate("LDAPTreeItem","This item have a filter applied.")
            if self.limit != LDAPTreeItem.LIMIT_DEFAULT:
                return QtCore.QCoreApplication.translate("LDAPTreeItem","This item have a limit applied.")
            return None
        # If DisplayRole (most common case)
        elif role == QtCore.Qt.DisplayRole:
            #return self.itemData.getPrettyDN() # The whole name
            return self.itemData.getPrettyRDN()
        else:
            return None

    def smartObject(self):
        return self.itemData
    
    def fetchChildList(self):
        """
        (Re)aquire the list of childs for this item (if any).
        """       
        
        l = LumaConnection(self.serverParent.serverMeta)
        
        bindSuccess, exceptionObject = l.bind()
        
        if not bindSuccess:
            self.displayError(exceptionObject)
            return None
        
        
        # Search for items at the level under this one
        success, resultList, exceptionObject = l.search(self.itemData.getDN(), \
                scope=ldap.SCOPE_ONELEVEL, filter=self.filter)
        l.unbind()
        
        if not success:
            self.displayError(exceptionObject)
            return None

        
        # If a limit is specified, only display the chosen amount        
        if self.limit > 0 and len(resultList) > self.limit:
            returnList = []
            for i in xrange(self.limit):
                returnList.append(LDAPTreeItem(resultList[i], self.serverParent, self))
            return returnList
        
        """
        # If there are ALOT of returned entries, confirm displaying them all
        if len(resultList) > self.ASK_TO_DISPLAY:
            #Todo: specify how many to load and "remembers"/"always yes"-function in the dialog
            # TODO Translate
            svar = QMessageBox.question(None, self.tr("Got many results"), "Got " +str(len(resultList))+" items. Do you want to display them all?", QMessageBox.Yes|QMessageBox.No)
            if not svar == QMessageBox.Yes:
                self.beginUpdateModel()
                self.childItems = []
                for i in xrange(50):
                    self.childItems.append(LDAPTreeItem(resultList[i], self.serverParent, self))
                self.populated = 1
                self.endUpdateModel()
                return
        """
        
        # Default behavior: return all
        return [LDAPTreeItem(x, self.serverParent, self) for x in resultList]
    
    def setLimit(self):
        """
        Asks for the users limit.
        """
        r = QInputDialog.getInt(None, QtCore.QCoreApplication.translate("LDAPTreeItem","Limit"),QtCore.QCoreApplication.translate("LDAPTreeItem","Enter the limit (0 = none):"), self.limit)
        if r[1] == True:
            self.limit = r[0]
    
    def setFilter(self):
        """
        Asks the user for the filter.
        """
        r = QInputDialog.getText(None, QtCore.QCoreApplication.translate("LDAPTreeItem","Filter"), QtCore.QCoreApplication.translate("LDAPTreeItem","Enter the filter (with parentheses -- none for default):"), text=self.filter)
        if r[1] == True:
            if len(str(r[0])) > 0:
                self.filter = str(r[0])
            else:
                self.filter = LDAPTreeItem.FILTER_DEFAULT

        
    def getSupportedOperations(self):
        return AbstractLDAPTreeItem.SUPPORT_CLEAR|AbstractLDAPTreeItem.SUPPORT_RELOAD|AbstractLDAPTreeItem.SUPPORT_FILTER|AbstractLDAPTreeItem.SUPPORT_LIMIT|AbstractLDAPTreeItem.SUPPORT_ADD
        
