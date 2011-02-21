'''
Created on 18. feb. 2011

@author: Simen
'''

import ldap
from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import qApp, QCursor, QMessageBox

class LDAPTreeItem(AbstractLDAPTreeItem):
    
    ASK_TO_DISPLAY = 1000

    def __init__(self, data, serverParent, parent=None):
        AbstractLDAPTreeItem.__init__(self, parent)
        self.serverParent = serverParent
        self.itemData = data
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
              
        if len(resultList) > self.ASK_TO_DISPLAY:
            """
            Todo: specify how many to load and "remembers"/"always yes"-function
            """
            svar = QMessageBox.question(None, "Got many results", "Got "+str(len(resultList))+" items. Do you want to display them all?",QMessageBox.Yes|QMessageBox.No)
            if not svar == QMessageBox.Yes:
                for i in xrange(10):
                    tmp = LDAPTreeItem(resultList[i], self.serverParent, self)
                    self.appendChild(tmp)
                self.populated = 1
                return
        """
        for x in resultList:
            tmp = LDAPTreeItem(x, self.serverParent, self)
            self.appendChild(tmp)
        """
        self.childItems = [LDAPTreeItem(x, self.serverParent, self) for x in resultList]
        self.populated = 1
    
    def lol(self):
        print "lol"
        
    def getContextMenu(self, menu):
        menu.addAction("Reload", self.populateItem)
        return menu
    