

import ldap
from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from PyQt4.QtGui import QMessageBox, QInputDialog, QIcon, QPixmap
from PyQt4 import QtCore

class LDAPTreeItem(AbstractLDAPTreeItem):
    
    # Defaults
    LIMIT_DEFAULT = 0
    FILTER_DEFAULT = "(objectClass=*)"
    
    # How many before a messagebox asks if you want to load them all?
    ASK_TO_DISPLAY = 1000

    def __init__(self, data, serverParent, parent=None, modelParent = None):
        AbstractLDAPTreeItem.__init__(self, parent, modelParent = modelParent)
        self.serverParent = serverParent
        self.itemData = data
        
        self.limit = LDAPTreeItem.LIMIT_DEFAULT
        self.filter = LDAPTreeItem.FILTER_DEFAULT
        
        self.isWorking.connect(self.serverParent.isWorking)
        self.doneWorking.connect(self.serverParent.doneWorking)


    def columnCount(self):
        return 1
    
    def data(self, column, role):
        
        # Probably unessecary
        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.DecorationRole:
            return QtCore.QVariant()
        
        # Return an icon if the item has been configured
        if role == QtCore.Qt.DecorationRole:
            if self.filter != LDAPTreeItem.FILTER_DEFAULT or self.limit != LDAPTreeItem.LIMIT_DEFAULT:
                return QIcon(QPixmap(":/images/config.png"))
            else:
                return QtCore.QVariant()
        # If DisplayRole
        else:
            return self.itemData.getPrettyRDN()

    def smartObject(self):
        return self.itemData
    
    def populateItem(self):  
        
#        parent = self.parent()
#        parentIndex = self.modelParent.index(0,0, parent)
#        self.modelParent.beginRemoveRows(parentIndex, 0, parent.childCount()-1)
        self.childItems = []    
#        self.modelParent.endRemoveRows()          

        self.isWorking.emit()
        
        # Search for items at the level under this one
        # TODO: What if they're already spesified
        l = self.serverParent.connection
        success, resultList, exceptionObject = l.search(self.itemData.getDN(), \
                scope=ldap.SCOPE_ONELEVEL, filter=self.filter)
        
        self.doneWorking.emit()
        
        if not success:
            self.displayError(exceptionObject)
            return
        
        # If a limit is spesified, only display the choosen amount        
        if self.limit > 0 and len(resultList) > self.limit:
            self.childItems = []
            for i in xrange(self.limit):
                self.childItems.append(LDAPTreeItem(resultList[i], self.serverParent, self))
            self.populated = 1
            return
        
        # If there are ALOT of returned entries, confirm displaying them all
        if len(resultList) > self.ASK_TO_DISPLAY:
            """
            Todo: specify how many to load and "remembers"/"always yes"-function in the dialog
            """
            svar = QMessageBox.question(None, "Got many results", "Got "+str(len(resultList))+" items. Do you want to display them all?",QMessageBox.Yes|QMessageBox.No)
            if not svar == QMessageBox.Yes:
                self.childItems = []
                for i in xrange(50):
                    self.childItems.append(LDAPTreeItem(resultList[i], self.serverParent, self, modelParent = self.modelParent))
                self.populated = 1
                return

        # Default, load all
        self.childItems = [LDAPTreeItem(x, self.serverParent, self) for x in resultList]
        print "Added",self.childItems
        print "To",self.data(0,0)
        self.populated = 1
        
        #self.modelParent.dataChanged.emit()
        print "populateItems end"
    
    def setLimit(self):
        r = QInputDialog.getInt(None, "Limit","Enter the limit (0 = none):", self.limit)
        if r[1] == True:
            self.limit = r[0]
            self.populateItem()
    
    def setFilter(self):
        r = QInputDialog.getText(None, "Filter", "Enter the filter (with parentheses):", text=self.filter)
        if r[1] == True:
            if len(str(r[0])) > 0:
                self.filter = str(r[0])
            else:
                self.filter = LDAPTreeItem.FILTER_DEFAULT
            print self.filter
            self.populateItem()
    
    def getContextMenu(self, menu):
        # Not used
        return menu
    