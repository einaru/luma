# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import ldap
from qt import *
import base64
import re
import os.path
import string

from base.utils.gui.SearchResultViewDesign import SearchResultViewDesign
from base.utils.gui.AdvancedObjectWidget import AdvancedObjectWidget
from base.backend.ServerList import ServerList
import environment
from base.utils import isBinaryAttribute, encodeBase64
from base.backend.LumaConnection import LumaConnection
from base.utils import escapeSpecialChars
from base.utils import explodeDN
from base.utils import getSortedDnList
from base.utils.gui.LumaErrorDialog import LumaErrorDialog
from base.utils.gui.DeleteDialog import DeleteDialog
from base.utils import getSortedDnList




class SearchResultView(SearchResultViewDesign):

    def __init__(self, parent=None, name=None, fl=0):
        SearchResultViewDesign.__init__(self,parent,name,fl)

        self.SERVER = None
        self.RESULT = {}
        self.childWidgets = []
        self.childsToClean = []
        self.FILTER_COLUMN_POS = {}
        self.FILTER_LIST = []
        
        self.iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        delIconFile = os.path.join(self.iconPath, "deleteEntry.png")
        exportIconFile = os.path.join(self.iconPath, "exportLdif.png")
        
        self.popupMenu = QPopupMenu()
        self.popupMenu.insertItem(QIconSet(QPixmap(exportIconFile)), self.trUtf8("Export selected"), self.exportItems)
        self.popupMenu.insertSeparator()
        self.popupMenu.insertItem(QIconSet(QPixmap(delIconFile)), self.trUtf8("Delete selected"), self.deleteItems)
        
        self.connect(self.resultListView, SIGNAL("rightButtonPressed(QListViewItem*, const QPoint&, int)"), self.showPopup)
        
        self.resultListView.setSorting(-1, False) 

###############################################################################

    def showEntry(self, listItem):
        """ Show the double-clicked listitem in an own window.
        """

        floatingWidget = ChildWindow(None, unicode(listItem.text(0)).encode('utf-8'))
        widget = AdvancedObjectWidget(floatingWidget, unicode(listItem.text(0)).encode('utf-8'), 0)
    
        floatingWidget.setCentralWidget(widget)
        widget.buildToolBar(floatingWidget)
        
        tmpString = unicode(listItem.text(0)).encode('utf-8')
        tmpList = explodeDN(tmpString)
        newList = map(escapeSpecialChars, tmpList)
        tmpString = ",".join(newList)
        
        widget.initView(self.RESULT[tmpString])
        
        # needed if window is closed. gets deletetd from the list
        self.connect(floatingWidget, PYSIGNAL("child_closed"), self.cleanChildren)
        
        #widget.show()
        widget.setCaption(listItem.text(0))
        floatingWidget.show()
        
        # don't loose reference. normally window will disappear if function is completed
        self.childWidgets.append(floatingWidget)
        
###############################################################################

    def cleanChildren(self, child):
        """ Delete window of closed ldap item.
        """
        
        index = self.childWidgets.index(child)
        del self.childWidgets[index]

###############################################################################

    def setResult(self, server=None, resultData=None, filterList=None):
        self.SERVER = server
        self.rawResultList = resultData
        self.processData(resultData)
        self.FILTER_LIST = filterList
        self.displayResults()

###############################################################################

    def processData(self, data):
        self.RESULT = {}
        if not(data == None):
            for x in data:
                self.RESULT[x.getDN()] = x

###############################################################################

    def displayResults(self):
        self.resultListView.clear()
        
        while self.resultListView.columns():
            self.resultListView.removeColumn(0)
            
        self.FILTER_COLUMN_POS = {}
        position = self.resultListView.addColumn("dn")
        self.FILTER_COLUMN_POS["dn"] = position
        
        for x in self.FILTER_LIST:
            position = self.resultListView.addColumn(x)
            self.FILTER_COLUMN_POS[x] = position
            
        tmpList = self.RESULT.keys()
        tmpList = getSortedDnList(tmpList)
        for x in tmpList[::-1]:
            dataObject = self.RESULT[x]
            listItem = QListViewItem(self.resultListView, dataObject.getDN())
            listItem.setText(0, dataObject.getPrettyDN())
            
            for x in self.FILTER_COLUMN_POS.keys():
                if 'dn' == x:
                    continue
                    
                if "objectclass" == string.lower(x):
                    valueList = dataObject.getObjectClasses()
                    listItem.setText(self.FILTER_COLUMN_POS[x], ",".join(valueList))
                        
                if dataObject.hasAttribute(x):
                    if dataObject.isAttributeBinary(x):
                        listItem.setText(self.FILTER_COLUMN_POS[x], self.trUtf8("<u>Binary value</u>"))
                    else:
                        valueList = dataObject.getAttributeValueList(x)
                        listItem.setText(self.FILTER_COLUMN_POS[x], ",".join(valueList))
            
            self.resultListView.insertItem(listItem)
            
        self.resultListView.setColumnWidth(0, 250)
        self.resultListView.triggerUpdate()


###############################################################################

    def eventFilter(self, object, event):
        if (event.type() == QEvent.Close):
            self.childsToClean.append(object)
            
        return 0

###############################################################################

    def deleteItems(self):
        itemList = self.getSelectedItems()
        
        dnList = []
        itemDict = {}
        for x in itemList:
            # create the real string of the dn.
            tmpString = unicode(x.text(0)).encode('utf-8')
            tmpList = explodeDN(tmpString)
            newList = map(escapeSpecialChars, tmpList)
            tmpString = ",".join(newList)
            
            dnList.append(tmpString)
            itemDict[tmpString] = x
            
            
        deleteList = map(lambda x: self.RESULT[x], dnList)
        deleteDialog = DeleteDialog()
        deleteDialog.initData(deleteList)
        deleteDialog.exec_loop()
        
        realDeletedEntries = deleteDialog.getDeletedItems()
        
        for x in realDeletedEntries:
            self.resultListView.takeItem(itemDict[x])
            del self.RESULT[x]
        
        #serverList = ServerList()
        #serverList.readServerList()
        #serverMeta = serverList.getServerObject(self.SERVER)

        
        #connectionObject = LumaConnection(serverMeta)
        #bindSuccess, exceptionObject = connectionObject.bind()
        
        #if not bindSuccess:
        #        dialog = LumaErrorDialog()
        #        errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
        #        errorMsg.append(str(exceptionObject))
        #        dialog.setErrorMessage(errorMsg)
        #        dialog.exec_loop()
        #        environment.setBusy(False)
        #        return
        
        #deleteFailure = False
        #deleteException = None
        #failedDN = None
        
        ## delete items from directory
        #for x in getSortedDnList(dnList)[::-1]:
        #    success, exceptionObject = connectionObject.delete(x)
        #    if success:
        #        # remove items from widget
        #        self.resultListView.takeItem(itemDict[x])
        #    else:
        #        deleteFailure = True
        #        deleteException = exceptionObject
        #        failedDN = x
        #        break
                
        #connectionObject.unbind()
    
        
###############################################################################
    
    def showPopup(self, tmpItem=None, point=None, itemId=None):
        if not (tmpItem == None):
            self.popupMenu.exec_loop(point)

###############################################################################

    def exportItems(self):
        itemList = self.getSelectedItems()
        
        tmpList = map(lambda x: self.RESULT[unicode(x.text(0))], itemList)
        ldifList = map(lambda x: x.convertToLdif(), tmpList)
        
        fileName = unicode(QFileDialog.getSaveFileName())
        if fileName == '':
            return
        try:
            fileHandler = open(fileName, 'w')
            fileHandler.write("".join(ldifList))
            fileHandler.close()
        except IOError, e:
            print "Could not save Data"
            print "Reason: " + unicode(e)
        
###############################################################################

    def getSelectedItems(self):
        tmpList = []
        
        child = self.resultListView.firstChild()
        if child.isSelected():
                tmpList.append(child)
        
        while child.nextSibling():
            child = child.nextSibling()
            if child.isSelected():
                tmpList.append(child)
                
        return tmpList
    
###############################################################################

class ChildWindow(QMainWindow):
    
    def __init__(self, parent = None, name= None):
        QMainWindow.__init__(self, parent, name)
        
        
    def closeEvent(self, event):
        self.emit(PYSIGNAL("child_closed"), (self,))
        self.deleteLater()
