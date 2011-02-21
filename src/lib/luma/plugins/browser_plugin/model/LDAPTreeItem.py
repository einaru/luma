'''
Created on 18. feb. 2011

@author: Simen
'''

import ldap
from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from PyQt4 import QtCore
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
        
        import PyQt4.QtGui
        if len(resultList) > 50:
            svar = PyQt4.QtGui.QMessageBox.question(None, "Got many results", "Got "+str(len(resultList))+" items. Do you want to display them all?",PyQt4.QtGui.QMessageBox.Yes|PyQt4.QtGui.QMessageBox.No)
            if svar == PyQt4.QtGui.QMessageBox.No:
                for i in xrange(10):
                    self.appendChild(LDAPTreeItem(resultList[i], self.serverParent, self))
                self.populated = 1
                return

        for x in resultList:
            tmp = LDAPTreeItem(x, self.serverParent, self)
            self.appendChild(tmp)

        self.populated = 1
        
    def getContextMenu(self, menu):
        menu.addAction("Reload/repopulate", self.populateItem)
        return menu
    