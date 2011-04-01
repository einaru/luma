
import ldap
from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from PyQt4.QtGui import QInputDialog, QIcon, QPixmap
from PyQt4 import QtCore
from base.backend.LumaConnection import LumaConnection
from plugins.browser_plugin.item.AbstractLDAPTreeItem import AbstractLDAPTreeItem

class LDAPTreeItem(AbstractLDAPTreeItem):
    """
    Used by LDAP-entries (as opposed to servers or rootitems).
    """
    
    # Defaults
    LIMIT_DEFAULT = 0
    FILTER_DEFAULT = "(objectClass=*)"
    
    # How many aquired entries before a messagebox 
    # pops up asking if the user want to load them all?
    # Not used currently.
    # See commented-out code.
    #ASK_TO_DISPLAY = 1000

    def __init__(self, data, serverParent, parent):
        AbstractLDAPTreeItem.__init__(self, parent)
        
        self.serverParent = serverParent
        self.itemData = data
        
        self.limit = LDAPTreeItem.LIMIT_DEFAULT
        self.filter = LDAPTreeItem.FILTER_DEFAULT
        
        self.error = False
	self.loading = False

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
	    if self.loading:
		#return QIcon(QPixmap(":/icons/loading"))
		return QIcon(QPixmap(":/icons/luma-16"))
            if self.error:
                return QIcon(QPixmap(":/icons/no"))
            if self.filter != LDAPTreeItem.FILTER_DEFAULT or self.limit != LDAPTreeItem.LIMIT_DEFAULT:
                return QIcon(QPixmap(":/icons/filter"))
            else:
                return None
        # Return applicable status-tip-role
        elif role == QtCore.Qt.StatusTipRole:
	    if self.loading:
		return QtCore.QCoreApplication.translate("LDAPTreeItem","Fetching items...")
            if self.error:
                return QtCore.QCoreApplication.translate("LDAPTreeItem","Couldn't fetch list of children.")
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
            self.error = True
            return (False, None, exceptionObject)
        
        
        # Search for items at the level under this one
        success, resultList, exceptionObject = l.search(self.itemData.getDN(), \
                scope=ldap.SCOPE_ONELEVEL, filter=self.filter, sizelimit=self.limit)
        l.unbind()
        
        if not success:
            self.error = True
            return (False, None, exceptionObject)
        
        self.error = False
        
        # If a limit is specified, only display the chosen amount     
        """
        SIzelimit is used instead
        if self.limit > 0 and len(resultList) > self.limit:
            returnList = []
            for i in xrange(self.limit):
                returnList.append(LDAPTreeItem(resultList[i], self.serverParent, self))
            return (True, returnList, exceptionObject)
        """
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
        return (True, [LDAPTreeItem(x, self.serverParent, self) for x in resultList], exceptionObject)
    
    def setLimit(self):
        """
        Asks for the users limit.
        """
        (value, ok) = QInputDialog.getInt(None, QtCore.QCoreApplication.translate("LDAPTreeItem","Limit"),QtCore.QCoreApplication.translate("LDAPTreeItem","Enter the limit (0 = none):"), self.limit)
        if ok == True:
            self.limit = value
        return ok
    
    def setFilter(self):
        """
        Asks the user for the filter.
        """
        (value, ok) = QInputDialog.getText(None, QtCore.QCoreApplication.translate("LDAPTreeItem","Filter"), QtCore.QCoreApplication.translate("LDAPTreeItem","Enter the filter (with parentheses -- none for default):"), text=self.filter)
        if ok == True:
            if len(str(value)) > 0:
                self.filter = str(value)
            else:
                self.filter = LDAPTreeItem.FILTER_DEFAULT
        return ok
                
    def delete(self):
        """ Tries to delete the item on the server
        """
        
        lumaConnection = LumaConnection(self.serverParent.serverMeta)
        bindSuccess, exceptionObject = lumaConnection.bind()
        
        if not bindSuccess:
            message = QtCore.QCoreApplication.translate("LDAPTreeItem","Could not bind to server.")
            return (False, message, exceptionObject)
        
        success, exceptionObject = lumaConnection.delete(self.smartObject().getDN())
        lumaConnection.unbind()
        
        if success:
            self.childItems = []
            self.populated = True
            return (True, None, None)
        else:
            message = QtCore.QCoreApplication.translate("LDAPTreeItem","Could not delete entry: "+exceptionObject[0]["desc"])
            return (False, message, exceptionObject)
        
    def getSupportedOperations(self):
        return AbstractLDAPTreeItem.SUPPORT_CLEAR | \
               AbstractLDAPTreeItem.SUPPORT_RELOAD | \
               AbstractLDAPTreeItem.SUPPORT_FILTER | \
               AbstractLDAPTreeItem.SUPPORT_LIMIT | \
               AbstractLDAPTreeItem.SUPPORT_ADD | \
               AbstractLDAPTreeItem.SUPPORT_EXPORT | \
               AbstractLDAPTreeItem.SUPPORT_DELETE | \
               AbstractLDAPTreeItem.SUPPORT_OPEN
