# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path

from base.utils.gui.DeleteDialogDesign import DeleteDialogDesign
from base.backend.LumaConnection import LumaConnection
import environment


class DeleteDialog(DeleteDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        DeleteDialogDesign.__init__(self,parent,name,modal,fl)
        
        self.iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        self.deleteIcon = QPixmap(os.path.join(self.iconPath, "trashcan.png"))
        self.iconLabel.setPixmap(self.deleteIcon)
        
        self.okIcon = QPixmap(os.path.join(self.iconPath, "ok.png"))
        self.failureIcon = QPixmap(os.path.join(self.iconPath, "no.png"))
        
        self.itemView.setColumnText(0, "")
        self.itemView.setColumnWidth(0, 32)
        self.itemView.setSorting(-1, False) 
        
        # Dictionary of items which should be deleted
        # Key is the dn; value is as list with the SmartDataObject 
        # and the QListViewItem
        self.deleteDictionary = {}
        
        # List of entries which have been deleted
        self.deletedEntries = []
        
        
        
###############################################################################

    def initData(self, tmpList):
        """ Initializaion of the dialog with data.
        """
        
        for x in tmpList[::-1]:
            prettyDN = x.getPrettyDN()
            tmpItem = QListViewItem(self.itemView)
            tmpItem.setText(1, prettyDN)
            self.deleteDictionary[prettyDN] = [x, tmpItem]
            
###############################################################################

    def removeItems(self):
        """ Remove the currently selected items from the list of items to 
        be deleted.
        """
        
        selectedList = []
        
        listIterator = QListViewItemIterator(self.itemView)
        while listIterator.current():
            item = listIterator.current()
            if item.isSelected():
                selectedList.append(item)
            listIterator += 1
        
        for x in selectedList:
            name = unicode(x.text(1))
            self.itemView.takeItem(self.deleteDictionary[name][1])
            del self.deleteDictionary[name]
            
###############################################################################

    def deleteItems(self):
        """ Delete items from server and display statusmessages.
        """
        
        environment.setBusy(True)
        
        connectionObject = None
        currentServerMeta = None
        connected = False
        
        deleteList = map(lambda x: self.deleteDictionary[x][0], self.deleteDictionary.keys())
        deleteList.sort()
        
        
        for x in deleteList[::-1]:
            prettyDN = x.getPrettyDN()
            normalDN = x.getDN()
            
            if None == connectionObject:
                currentServerMeta = x.getServerMeta()
                connectionObject = LumaConnection(currentServerMeta)
                
            tmpServerMeta = x.getServerMeta()
            if not (tmpServerMeta.name == currentServerMeta.name):
                if connected:
                    connectionObject.unbind()
                    
                currentServerMeta = tmpServerMeta
                connectionObject = LumaConnection(currentServerMeta)
                
            if not connected:
                success, exceptionObject = connectionObject.bind()
                self.displayItemStatus(self.deleteDictionary[prettyDN][1], success, exceptionObject)
                
                if not success:
                    continue
                    
            success, exceptionObject = connectionObject.delete(normalDN)
            self.displayItemStatus(self.deleteDictionary[prettyDN][1], success, exceptionObject)
            
            if success:
                self.deletedEntries.append(normalDN)
                
        environment.setBusy(False)
            
###############################################################################

    def displayItemStatus(self, listItem, success, exceptionObject):
        if success:
            listItem.setPixmap(0, self.okIcon)
            listItem.setText(2, self.trUtf8("Item deleted successfully."))
        else:
            listItem.setPixmap(0, self.failureIcon)
            listItem.setText(2, str(exceptionObject))
        
###############################################################################

    def getDeletedItems(self):
        """ Returns a list of items which have been deleted.
        """
        
        return self.deletedEntries
        
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
