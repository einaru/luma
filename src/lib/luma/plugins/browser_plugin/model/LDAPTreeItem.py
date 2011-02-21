

import ldap
from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from PyQt4.QtGui import QMessageBox, QInputDialog

class LDAPTreeItem(AbstractLDAPTreeItem):
    
    ASK_TO_DISPLAY = 1000

    def __init__(self, data, serverParent, parent=None):
        AbstractLDAPTreeItem.__init__(self, parent)
        self.serverParent = serverParent
        self.itemData = data
        
        self.limit = 0
        self.isWorking.connect(self.serverParent.isWorking)
        self.doneWorking.connect(self.serverParent.doneWorking)


    def columnCount(self):
        return 1
    
    def data(self, column):
        return self.itemData.getPrettyRDN()

    def smartObject(self):
        return self.itemData
    
    def populateItem(self):
        
        self.isWorking.emit()
        
        l = self.serverParent.connection
        success, resultList, exceptionObject = l.search(self.itemData.getDN(), \
                scope=ldap.SCOPE_ONELEVEL,filter='(objectclass=*)')
        
        self.doneWorking.emit()
        
        if not success:
            self.displayError(exceptionObject)
            return
        
        print "limit",self.limit
        
        if self.limit > 0 and len(resultList) > self.limit:
            print "over limit",self.limit
            self.childItems = []
            for i in xrange(self.limit):
                self.childItems.append(LDAPTreeItem(resultList[i], self.serverParent, self))
            self.populated = 1
            return
              
        if len(resultList) > self.ASK_TO_DISPLAY:
            """
            Todo: specify how many to load and "remembers"/"always yes"-function
            """
            svar = QMessageBox.question(None, "Got many results", "Got "+str(len(resultList))+" items. Do you want to display them all?",QMessageBox.Yes|QMessageBox.No)
            if not svar == QMessageBox.Yes:
                self.childItems = []
                for i in xrange(50):
                    self.childItems.append(LDAPTreeItem(resultList[i], self.serverParent, self))
                self.populated = 1
                return
        """
        for x in resultList:
            tmp = LDAPTreeItem(x, self.serverParent, self)
            self.appendChild(tmp)
        """
        self.childItems = [LDAPTreeItem(x, self.serverParent, self) for x in resultList]
        self.populated = 1
    
    def setLimit(self):
        r = QInputDialog.getInt(None, "Limit","Enter the limit:",self.limit)
        if r[1] == True:
            self.limit = r[0]
            self.populateItem()
    
    def setFilter(self):
        #Todo
        self.populateItem()
    
    def getContextMenu(self, menu):
        menu.addAction("Reload", self.populateItem)
        menu.addAction("Set search limit", self.setLimit)
        menu.addAction("Set search filter", self.setFilter)
        return menu
    