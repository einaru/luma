# -*- coding: utf-8 -*-
#
# plugins.browser_plugin.BrowserView
#
# Copyright (c) 2011
#     Christian Forfang, <cforfang@gmail.com>
#     Simen Natvig, <simen.natvig@gmail.com>
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# Copyright (c) 2008
#     Vegar Westerlund, <vegarwe@users.sourceforge.net> 
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

import logging

from PyQt4 import (QtCore, QtGui)
from PyQt4.QtGui import (QWidget, QMessageBox, QMenu, QAction, qApp, QTableWidget, QKeySequence)
from PyQt4.QtCore import Qt, QPersistentModelIndex, QModelIndex, QObject, QEvent

from .AdvancedObjectWidget import AdvancedObjectWidget
from .NewEntryDialog import NewEntryDialog
from .gui.BrowserDialogs import ExportDialog, DeleteDialog
from .item.AbstractLDAPTreeItem import AbstractLDAPTreeItem
from .model.LDAPTreeItemModel import LDAPTreeItemModel
from base.backend.LumaConnection import LumaConnection
from ..template.TemplateList import TemplateList
from base.backend.ServerList import ServerList
from base.gui.ServerDialog import ServerDialog


class BrowserView(QWidget):
    """Luma LDAP Browser plugin
    """

    # Custom signals used
    reloadSignal = QtCore.pyqtSignal(QtCore.QModelIndex)
    clearSignal = QtCore.pyqtSignal(QtCore.QModelIndex)
    
    __logger = logging.getLogger(__name__)

    def __init__(self, parent=None, configPrefix=None):
        """
        @param configPrefix:
            defines the location of serverlist
        """
        super(BrowserView, self).__init__(parent)
        
        self.__logger = logging.getLogger(__name__)

        self.setObjectName("PLUGIN_BROWSER")

        # The serverlist used
        self.serverList = ServerList(configPrefix)
        self.serversChangedMessage = QtGui.QErrorMessage()
        self.mainLayout = QtGui.QHBoxLayout(self)

        self.splitter = QtGui.QSplitter(self)

        # The templatelist
        self.templateList = TemplateList()

        # Create the model
        self.ldaptreemodel = LDAPTreeItemModel(self.serverList, self)
        self.ldaptreemodel.workingSignal.connect(self.setBusy)
    
        # Set up the entrylist (uses the model)
        self.__setupEntryList()

        # The editor for entries
        self.tabWidget = QtGui.QTabWidget(self)
        #self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        #self.tabWidget.setStyleSheet("QTabWidget::pane {border: 0; border-top: 30px solid qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 red, stop: 1 yellow); background: yellow; } QTabWidget::tab-bar { top: 30px; }")
        self.setMinimumWidth(200)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.tabCloseClicked)

        # Remember and looks up open tabs
        self.openTabs = {}

        self.splitter.addWidget(self.entryList)
        self.splitter.addWidget(self.tabWidget)
        self.mainLayout.addWidget(self.splitter)

        # Used to signal the ldaptreemodel with a index
        # which needs processing (reloading, clearing)
        self.reloadSignal.connect(self.ldaptreemodel.reloadItem)
        self.clearSignal.connect(self.ldaptreemodel.clearItem)

        self.cancelList = []
    
        eventFilter = BrowserPluginEventFilter(self)
        self.installEventFilter(eventFilter)

        self.__createContextMenu()
        self.progress = QMessageBox(
            1,"Please wait",
            "Please wait, fetching data...\nThis message will automatically close when done...",
            QMessageBox.Ignore, parent = self
        )
        self.retranslateUi()
        
        # For testing ONLY
        # AND ONLY ON SMALL LDAP-SERVERS SINCE IT LOADS BASICALLY ALL ENTIRES
        #import modeltest
        #self.modeltest = modeltest.ModelTest(self.ldaptreemodel, self);
        
    def setBusy(self, status):
        """
        Helper-method.
        """
        if status == True:
            self.progress.show()
            qApp.setOverrideCursor(Qt.WaitCursor)
        else:
            if not self.progress.isHidden():
                self.progress.hide()
            qApp.restoreOverrideCursor()

    def __setupEntryList(self):
        # The view for server-content
        self.entryList = QtGui.QTreeView(self)
        self.entryList.setMinimumWidth(200)
        self.entryList.setMaximumWidth(400)
        #self.entryList.setAlternatingRowColors(True)
        self.entryList.setAnimated(True) # Somewhat cool, but should be removed if deemed too taxing
        self.entryList.setUniformRowHeights(True) #MAJOR optimalization for big lists
        #self.entryList.setExpandsOnDoubleClick(False)
        self.entryList.setModel(self.ldaptreemodel)
        self.entryList.setMouseTracking(True)
        self.entryList.viewport().setMouseTracking(True)
        # For right-clicking in the tree
        self.entryList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.entryList.customContextMenuRequested.connect(self.rightClick)
        # When something is activated (doubleclick, <enter> etc.)
        self.entryList.activated.connect(self.viewItem)
        self.delegate = LoadingDelegate(self.entryList)
        self.entryList.setItemDelegate(self.delegate)
        self.entryList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
    def __createContextMenu(self):
        """Creates the context menu for the tree view.
        """
        self.contextMenu = QMenu()
        self.contextMenuServerSettings = QAction(self)
        self.contextMenu.addAction(self.contextMenuServerSettings)
        self.contextMenu.addSeparator()
        self.contextMenuOpen = QAction(self)
        self.contextMenu.addAction(self.contextMenuOpen)
        self.contextMenuReload = QAction(self)
        self.contextMenu.addAction(self.contextMenuReload)
        self.contextMenuClear = QAction(self)
        self.contextMenu.addAction(self.contextMenuClear)
        self.contextMenuFilter = QAction(self)
        self.contextMenu.addAction(self.contextMenuFilter)
        self.contextMenuLimit = QAction(self)
        self.contextMenu.addAction(self.contextMenuLimit)
        self.contextMenu.addSeparator()
        self.contextMenuAdd = QMenu()
        self.contextMenu.addMenu(self.contextMenuAdd)
        self.contextMenuDelete = QMenu()
        self.contextMenu.addMenu(self.contextMenuDelete)
        self.contextMenuExport = QMenu()
        self.contextMenu.addMenu(self.contextMenuExport)
        self.contextMenuCancel = QAction(self)
        self.contextMenu.addAction(self.contextMenuCancel)

        # Connect the context menu actions to the correct slots
        self.contextMenuServerSettings.triggered.connect(self.editServerSettings)
        self.contextMenuOpen.triggered.connect(self.openChoosen)
        self.contextMenuReload.triggered.connect(self.reloadChoosen)
        self.contextMenuClear.triggered.connect(self.clearChoosen)
        self.contextMenuFilter.triggered.connect(self.filterChoosen)
        self.contextMenuLimit.triggered.connect(self.limitChoosen)
        self.contextMenuCancel.triggered.connect(self.cancelChoosen)

    def rightClick(self, point):
        """ Called when the view is right-clicked.
        Displays a context menu with possible actions.
        
        @param point: 
        """        
        # This is a list of QModelIndex objects, which will be used by
        # the various context menu slots.
        # We therfore store it as a class member
        self.selection = self.entryList.selectedIndexes()

        openSupport = True
        reloadSupport = True
        clearSupport = True
        filterSupport = True
        limitSupport = True
        addSupport = True
        deleteSupport = True
        exportSupport = True
        editServerSupport = True

        # The number of selected items is used for naming of the actions
        # added to the submenues
        numselected = len(self.selection)
        
        # View disabled menu if nothing selected
        self.contextMenu.setEnabled(True) # Remember to enable in case we have a selection
        if not numselected > 0: # If nothing is selected
            self.contextMenu.setEnabled(False) # Disable..
            self.contextMenu.exec_(self.entryList.mapToGlobal(point)) #.. then show.
            return

        # Iterate through the list of selected indexes, and
        # validate what operations are supported. That is, 
        # if one of the selected indexes do not support an
        # operation, we cannot allow to apply that operation
        # on the whole selection
        self.cancelList = []
        for index in self.selection:
            item = index.internalPointer()
            operations = item.getSupportedOperations()
            if not AbstractLDAPTreeItem.SUPPORT_OPEN & operations:
                openSupport = False
            if not AbstractLDAPTreeItem.SUPPORT_RELOAD & operations:
                reloadSupport = False
            if not AbstractLDAPTreeItem.SUPPORT_CLEAR & operations:
                clearSupport = False
            if not AbstractLDAPTreeItem.SUPPORT_FILTER & operations:
                filterSupport = False
            if not AbstractLDAPTreeItem.SUPPORT_LIMIT & operations:
                limitSupport = False
            if not AbstractLDAPTreeItem.SUPPORT_ADD & operations:
                addSupport = False
            if not AbstractLDAPTreeItem.SUPPORT_DELETE & operations:
                deleteSupport = False
            if not AbstractLDAPTreeItem.SUPPORT_EXPORT & operations:
                exportSupport = False
            if index.internalPointer().getParentServerItem() == None:
                editServerSupport = False
            if AbstractLDAPTreeItem.SUPPORT_CANCEL & operations:
                if item.canCancelSearch():
                    self.cancelList.append(item)

        
        # Now we just use the *Support variables to enable|disable
        # the context menu actions.
        self.contextMenuOpen.setEnabled(openSupport)
        self.contextMenuReload.setEnabled(reloadSupport)
        self.contextMenuClear.setEnabled(clearSupport)
        self.contextMenuFilter.setEnabled(filterSupport)
        self.contextMenuLimit.setEnabled(limitSupport)
        self.contextMenuServerSettings.setEnabled(editServerSupport)

        # For the submenues in the context menu, we add appropriate
        # actions, based on single|multi selection, or disable the menu
        # altogether if there is no support for the operation.
        if (limitSupport or filterSupport or openSupport) and not numselected == 1:
                self.contextMenuLimit.setEnabled(False)
                self.contextMenuFilter.setEnabled(False)
                self.contextMenuOpen.setEnabled(False)
        if addSupport and numselected == 1:
            self.contextMenuAdd.setEnabled(True)
            self.contextMenuAdd.addAction(self.str_ENTRY, self.addEntryChoosen)
            #template
            templateMenu = QMenu(self.str_TEMPLATE)
            self.contextMenuAdd.addMenu(templateMenu)
            index = self.selection[0]
            for template in self.templateList.getTable():
                if template.server == index.internalPointer().smartObject().serverMeta.name:
                    method = lambda name = template.templateName, i = index : self.addTemplateChoosen(name, i)
                    templateMenu.addAction(template.templateName, method)
            
            
            
        else:
            self.contextMenuAdd.setEnabled(False)

        if numselected != 1:
            self.contextMenuServerSettings.setEnabled(False)

        if deleteSupport:
            self.contextMenuDelete.setEnabled(True)
            if numselected == 1:
                self.contextMenuDelete.addAction(self.str_ITEM, self.deleteSelection)
                #self.contextMenuDelete.addAction(self.str_SUBTREE, self.deleteSelection)
                #self.contextMenuDelete.addAction(self.str_SUBTREE_PARENTS, self.deleteSelection)
            else:
                self.contextMenuDelete.addAction(self.str_ITEMS, self.deleteSelection)
                #self.contextMenuDelete.addAction(self.str_SUBTREES, self.deleteSelection)
                #self.contextMenuDelete.addAction(self.str_SUBTREES_PARENTS, self.deleteSelection)
        else:
            self.contextMenuDelete.setEnabled(False)

        if len(self.cancelList) > 0:
            self.contextMenuCancel.setEnabled(True)
        else:
            self.contextMenuCancel.setEnabled(False)

        if exportSupport:
            self.contextMenuExport.setEnabled(True)
            if numselected == 1:
                self.contextMenuExport.addAction(self.str_ITEM, self.exportItems)
                self.contextMenuExport.addAction(self.str_SUBTREE, self.exportSubtrees)
                self.contextMenuExport.addAction(self.str_SUBTREE_PARENTS, self.exportSubtreeWithParents)
            else:
                self.contextMenuExport.addAction(self.str_ITEMS, self.exportItems)
                self.contextMenuExport.addAction(self.str_SUBTREES, self.exportSubtrees)
                self.contextMenuExport.addAction(self.str_SUBTREES_PARENTS, self.exportSubtreeWithParents)
        else:
            self.contextMenuExport.setEnabled(False)

        # Finally we execute the context menu
        self.contextMenu.exec_(self.entryList.mapToGlobal(point))
        
        # We need to clear all the submenues after each right click
        # selection, if not; the submenu actions will be added and 
        # thus duplicated for every selection the user makes.
        # FIXME: Find a better way of handling this issue.
        self.contextMenuAdd.clear()
        self.contextMenuDelete.clear()
        self.contextMenuExport.clear()

    def cancelChoosen(self):
        for item in self.cancelList:
            item.cancelSearch()
        self.cancelList = []
    """
    Following methods are called from a context-menu.
    """
    def openChoosen(self):
        if len(self.selection) == 1:
            self.viewItem(self.selection[0])
    def reloadChoosen(self):
        for index in self.selection:
            self.reloadSignal.emit(index)
    def clearChoosen(self):
        for index in self.selection:
            self.clearSignal.emit(index)
    def limitChoosen(self):
        # Have the item set the limit for us, the reload
        for index in self.selection:
            ok = index.internalPointer().setLimit()
            if ok:
                self.reloadSignal.emit(index)
    def filterChoosen(self):
        # Have the item set the filter, then reload
        for index in self.selection:
            ok = index.internalPointer().setFilter()
            if ok:
                self.reloadSignal.emit(index)
    def addEntryChoosen(self):
        for index in self.selection:
            self.addNewEntry(index)
    def addTemplateChoosen(self, templateName, index):
        serverMeta = index.internalPointer().smartObject().serverMeta
        baseDN = index.internalPointer().smartObject().getDN()
        template = self.templateList.getTemplateObject(templateName)
        smartO = template.getDataObject(serverMeta, baseDN)
        self.addNewEntry(index, smartO, template)
        
    def addNewEntry(self, parentIndex, defaultSmartObject=None, template = None):
        tmp = NewEntryDialog(parentIndex, defaultSmartObject, entryTemplate = template)
        if tmp.exec_():
            print "La til ny entry"
            # TODO Do something. (Reload?)
            
    """
    Utility-methods
    """
    def isOpen(self, smartObject):
        rep = self.getRepForSmartObject(smartObject)
        if self.openTabs.has_key(str(rep)):
            return True
        else:
            return False
    def getRepForSmartObject(self, smartObject):
        serverName = smartObject.getServerAlias()
        dn = smartObject.getDN()
        return (serverName,dn)
        

    def viewItem(self, index):
        """
        Opens items for viewing.
        """
        item = index.internalPointer()
        supports = item.getSupportedOperations()
        
        # If we can't open this item, then don't
        if not supports & AbstractLDAPTreeItem.SUPPORT_OPEN:
            self.__logger.debug("Item didn't support open.")
            return
        
        smartObject = index.internalPointer().smartObject()
        rep = self.getRepForSmartObject(smartObject)
        
        # If the smartobject is already open, switch to it
        if self.isOpen(smartObject):
            x = self.openTabs[str(rep)]
            self.tabWidget.setCurrentWidget(x)
            return
            
        # Saves a representation of the opened entry to avoid opening duplicates  
        # and open it
        x = AdvancedObjectWidget(smartObject, QtCore.QPersistentModelIndex(index))
        self.openTabs[str(rep)] = x
        self.tabWidget.addTab(x, smartObject.getPrettyRDN())
        self.tabWidget.setCurrentWidget(x)
        
    
    def deleteIndex(self, index):
        # Remember the smartObject for later
        sO = index.internalPointer().smartObject()
        # Try to delete
        (success, message) = self.ldaptreemodel.deleteItem(index)
        if success:
            # Close open edit-windows if any
            self.__closeTabIfOpen(sO)
            # Notify success
            return (True, message)
        else:
            # Notify fail
            return (False,message)
        
    def __closeTabIfOpen(self, sO):
        if self.isOpen(sO):
                rep = self.getRepForSmartObject(sO)
                x = self.openTabs.pop(str(rep))
                i = self.tabWidget.indexOf(x)
                if i != -1:
                    self.tabWidget.removeTab(i)

    def deleteSelection(self, alsoSubTree = False):
        """Slot for the context menu.
        
        Opens the DeleteDialog with the selected entries, giving the
        user the option to validate the selection before deleting.
        
        This is for deleting the item + possibly it's subtree.
        See deleteOnlySubtreeOfSelection() for only subtree.
        """
        
        # Only one item
        if len(self.selection) == 1:
            # Confirmation-message
            ok = QMessageBox.question(self, QtCore.QCoreApplication.translate("BrowserView","Delete"), QtCore.QCoreApplication.translate("BrowserView", "Really delete?"), QMessageBox.Yes|QMessageBox.No)
            if ok == QMessageBox.No:
                return
            (status, message) = self.deleteIndex(self.selection[0])
            if not status:
                QMessageBox.critical(self, QtCore.QCoreApplication.translate("BrowserView","Error"), "On "+self.selection[0].data().toPyObject()+":\n"+message)
            return
        
        if alsoSubTree:
            # Not done yet
            return
        
        # Make persistent indexes and list of smartObjects to be deleted
        persistenSelection = []
        sOList = []
        for x in self.selection:
            persistenSelection.append(QPersistentModelIndex(x))
            sOList.append(x.internalPointer().smartObject())
        
        # Create gui
        deleteDialog = DeleteDialog(sOList, 0) #0 = not subtree
        status = deleteDialog.exec_()
        
        if status: # the dialog was not canceled
            
            # If all rows were removed successfully, just call removeRows on all selected items
            # (reloading all items of the parent can be expensive)
            if deleteDialog.passedItemsWasDeleted:
                for x in persistenSelection:
                    if x.isValid:
                        i = x.sibling(x.row(), 0) #QModelIndex
                        self.__closeTabIfOpen(i.internalPointer().smartObject())
                        self.ldaptreemodel.removeRow(x.row(), x.parent())
                return
                
            # If not, call reload on the parent of all the items?
            else:
                tmp = QMessageBox.question(self, 
                    QtCore.QCoreApplication.translate("BrowserView", "Deletion"),
                    QtCore.QCoreApplication.translate("BrowserView", "It's possible some of the selected items might not have been deleted, while others were.\nDo you wan't to update the list to reflect the changes?"),
                    buttons=QMessageBox.Yes|QMessageBox.No, defaultButton=QMessageBox.Yes)
                
                if tmp == QMessageBox.Yes:
                    for x in persistenSelection:
                        # index might not be valid if the parent was reloaded by a previous item
                        if x.isValid():
                            self.ldaptreemodel.reloadItem(x.parent())
                        return
            
        # Was cancelled so do nothing
        else:
            pass
        
            
    def deleteOnlySubtreeOfSelection(self, selection):
            pass
        
    def exportItems(self):
        """Slot for the context menu.
        """
        self.__exportSelection(scope=0)
    
    def exportSubtrees(self):
        """Slot for the context menu.
        """
        self.__exportSelection(scope=1)

    def exportSubtreeWithParents(self):
        """Slot for the context menu.
        """
        self.__exportSelection(scope=2)

    def __exportSelection(self, scope=0):
        """Slot for the context menu.
        
        Opens the ExportDialog with the selected entries, giving the
        user the option to validate the selection before exporting.
        
        @param scope:
            The scope selection.
            0 = SCOPE_BASE -> Item(s);
            1 = SCOPE_ONELEVEL -> Subtree(s); 
            2 = SCOPE_SUBTREE -> Subtree(s) with parent 
        """
        exportObjects = []
        msg = ''
        
        self.setBusy(True)
        for index in self.selection:
            smartObject = index.internalPointer().smartObject()
            
            serverName = smartObject.getServerAlias()
            dn = smartObject.getDN()
            serverObject = self.serverList.getServerObject(serverName)
            con = LumaConnection(serverObject)
            
            if scope == 1:
                pass
            
            # Do a search on the whole subtree
            # 2 = ldap.SCOPE_SUBTREE
            elif scope == 2:

                success, e = con.bind()
                
                if not success:
                    self.__logger.error(str(e))
                    continue
                success, result, e = con.search(base=dn, scope=2)

                if success:
                    exportObjects.extend(result)
                else:
                    self.__logger.error(str(e))
                    
            # For scope == 0 we need not do any LDAP search operation
            # because we already got what we need
            else:
                exportObjects.append(smartObject)
        
        # Initialize the export dialog
        # and give it the items for export
        dialog = ExportDialog(msg)
        dialog.setExportItems(exportObjects)
        self.setBusy(False)
        dialog.exec_()

    def editServerSettings(self):
        """Slot for the context menu.
        Opens the ServerDialog with the selected server.
        """
        try:
            items = self.selection
            serverItem = items[0].internalPointer().getParentServerItem()
            serverName = serverItem.serverMeta.name
            serverDialog = ServerDialog(serverName)
            r = serverDialog.exec_()
            if r:
                self.serversChangedMessage.showMessage(QtCore.QCoreApplication.translate("BrowserView","You need to restart the plugin for changes to take effect."))
        except Exception, e:
            self.__logger.error(str(e))
            QMessageBox.information(self, "Error","See log for details")

    def tabCloseClicked(self, index):

        clicked = self.tabWidget.widget(index).aboutToChange()
        if clicked == False:
            return
        sO = self.tabWidget.widget(index).getSmartObject()

        if not (sO == None):
            # Remove the representation of the opened entry from the list
            rep = self.getRepForSmartObject(sO)
            try:
                self.openTabs.pop(str(rep))
            except:
                # Don't care
                pass
        self.tabWidget.removeTab(index)

    def buildToolBar(self, parent):
        # Not used
        pass

    def retranslateUi(self):
        """Retranslates all translatable strings.
        
        This method is called when the LanguageChange event is caught.
        """
        self.tabWidget.setStatusTip(QtCore.QCoreApplication.translate("BrowserView", "This is where entries are displayed when opened."))
        self.tabWidget.setToolTip(QtCore.QCoreApplication.translate("BrowserView", "This is where entries are displayed when opened."))
        self.contextMenuServerSettings.setText(QtCore.QCoreApplication.translate("BrowserView", "Edit Server Settings"))
        self.contextMenuOpen.setText(QtCore.QCoreApplication.translate("BrowserView", "Open"))
        self.contextMenuReload.setText(QtCore.QCoreApplication.translate("BrowserView", "Reload"))
        self.contextMenuClear.setText(QtCore.QCoreApplication.translate("BrowserView", "Clear"))
        self.contextMenuFilter.setText(QtCore.QCoreApplication.translate("BrowserView", "Set Filter"))
        self.contextMenuLimit.setText(QtCore.QCoreApplication.translate("BrowserView", "Set Limit"))
        self.contextMenuAdd.setTitle(QtCore.QCoreApplication.translate("BrowserView", "Add"))
        self.contextMenuDelete.setTitle(QtCore.QCoreApplication.translate("BrowserView", "Delete"))
        self.contextMenuExport.setTitle(QtCore.QCoreApplication.translate("BrowserView", "Export"))
        self.contextMenuCancel.setText(QtCore.QCoreApplication.translate("BrowserView", "Cancel"))
        
        self.str_ENTRY = QtCore.QCoreApplication.translate("BrowserView", "Entry")
        self.str_TEMPLATE = QtCore.QCoreApplication.translate("BrowserView", "Template")
        self.str_ITEM = QtCore.QCoreApplication.translate("BrowserView", "Item")
        self.str_SUBTREE = QtCore.QCoreApplication.translate("BrowserView", "Subtree")
        self.str_SUBTREE_PARENTS = QtCore.QCoreApplication.translate("BrowserView", "Subtree with parents")
        self.str_ITEMS = QtCore.QCoreApplication.translate("BrowserView", "Items")
        self.str_SUBTREES = QtCore.QCoreApplication.translate("BrowserView", "Subtrees")
        self.str_SUBTREES_PARENTS = QtCore.QCoreApplication.translate("BrowserView", "Subtrees with parents")

    def changeEvent(self, e):
        """Overloaded so we can catch the LanguageChange event, and at 
        translation support to the plugin
        """
        if e.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi()
        else:
            QWidget.changeEvent(self, e)

class BrowserPluginEventFilter(QObject):

    def eventFilter(self, target, event):
        if event.type() == QEvent.KeyPress:
            index = target.tabWidget.currentIndex()
            if event.matches(QKeySequence.Close):
                if index >= 0:
                    target.tabWidget.tabCloseRequested.emit(index)
                return True
        return QObject.eventFilter(self, target, event)

class LoadingDelegate(QtGui.QStyledItemDelegate):
    """
    Draws "Loading..." on items currently loading data.
    """

    def __init__(self, view):
        super(LoadingDelegate, self).__init__()
        from PyQt4.QtCore import QTimer
        self.t = QTimer()
        self.t.setInterval(1000)
        self.t.timeout.connect(view.model().layoutChanged)

    def paint(self, painter, option, index):
        item = index.internalPointer()
        if item.loading == True:
            self.t.start()
            # When loading
            self.initStyleOption(option, index)
            QtGui.QStyledItemDelegate.paint(self, painter, option, index)
            #painter.drawText(option.rect, QtCore.Qt.AlignRight, "Loading...  ")
            painted = False
            if hasattr(item, "lumaConnection"):
                connection = item.lumaConnection
                if not(connection == None):
                    resultCount = connection.resultCount
                    if not(resultCount == None):
                        painted = True
                        painter.drawText(option.rect, QtCore.Qt.AlignRight, "Loading...  " + str(resultCount))
                        return
            if not painted:
                painter.drawText(option.rect, QtCore.Qt.AlignRight, "Loading...  ")
        else:
            # Default
            QtGui.QStyledItemDelegate.paint(self, painter, option, index)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
