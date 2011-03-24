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
from string import replace

from PyQt4 import (QtCore, QtGui)
from PyQt4.QtGui import (QWidget, QMessageBox, QMenu, QAction)

from base.backend.LumaConnection import LumaConnection
from base.backend.ServerList import ServerList
from base.util.IconTheme import (pixmapFromThemeIcon, iconFromTheme)
from base.util.Paths import getUserHomeDir

from .gui.ExportDialogDesign import Ui_ExportDialog
from .item.AbstractLDAPTreeItem import AbstractLDAPTreeItem
from .model.LDAPTreeItemModel import LDAPTreeItemModel
from .NewEntryDialog import NewEntryDialog
from .AdvancedObjectWidget import AdvancedObjectWidget


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
        QtGui.QWidget.__init__(self, parent)
        super(BrowserView, self).__init__(parent)

        self.setObjectName("PLUGIN_BROWSER")

        # The serverlist used
        self.serverList = ServerList(configPrefix)
        self.mainLayout = QtGui.QHBoxLayout(self)

        self.splitter = QtGui.QSplitter(self)

        # The model for server-content
        self.ldaptreemodel = LDAPTreeItemModel(self)
        self.ldaptreemodel.populateModel(self.serverList)

        # For testing ONLY
        # AND ONLY ON SMALL LDAP-SERVERS SINCE IT LOADS BASICALLY ALL ENTIRES
        #self.modeltest = modeltest.ModelTest(self.ldaptreemodel, self);

        # The view for server-content
        self.entryList = QtGui.QTreeView(self)
        self.entryList.setMinimumWidth(200)
        self.entryList.setMaximumWidth(400)
        #self.entryList.setAlternatingRowColors(True)
        self.entryList.setAnimated(True) # Somewhat cool, but should be removed if deemed too taxing
        self.entryList.setUniformRowHeights(True) #Major optimalization for big lists
        self.entryList.setModel(self.ldaptreemodel)
        self.entryList.setMouseTracking(True)
        self.entryList.viewport().setMouseTracking(True)
        # For right-clicking in the tree
        self.entryList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.entryList.customContextMenuRequested.connect(self.rightClick)
        # When something is activated (doubleclick, <enter> etc.)
        self.entryList.activated.connect(self.viewItem)

        self.entryList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

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

        self.__createContextMenu()
        self.retranslateUi()

    def __createContextMenu(self):
        """Creates the context menu for the tree view.
        """
        self.contextMenu = QMenu()
        self.contextMenuServerSettings = QAction(self)
        self.contextMenu.addAction(self.contextMenuServerSettings)
        self.contextMenu.addSeparator()
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

        # Connect the context menu actions to the correct slots
        self.contextMenuServerSettings.triggered.connect(self.editServerSettings)
        self.contextMenuReload.triggered.connect(self.reloadChoosen)
        self.contextMenuClear.triggered.connect(self.clearChoosen)
        self.contextMenuFilter.triggered.connect(self.filterChoosen)
        self.contextMenuLimit.triggered.connect(self.limitChoosen)

    def rightClick(self, point):
        """ Called when the view is right-clicked.
        Displays a context menu with possible actions.
        
        @param point: 
        """
        # This is a list of QModelIndex objects, which will be used by
        # the various context menu slots.
        # We therfore store it as a class member
        self.selection = self.entryList.selectedIndexes()

        reloadSupport = True
        clearSupport = True
        filterSupport = True
        limitSupport = True
        addSupport = True
        deleteSupport = True
        exportSupport = True

        # The number of selected items is used for naming of the actions
        # added to the submenues
        numselected = len(self.selection)

        # Iterate through the list of selected indexes, and
        # validate what operations are supported. That is, 
        # if one of the selected indexes do not support an
        # operation, we cannot allow to apply that operation
        # on the whole selection
        for index in self.selection:
            item = index.internalPointer()
            operations = item.getSupportedOperations()
            
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
        
        # Now we just use the *Support variables to enable|disable
        # the context menu actions.
        self.contextMenuReload.setEnabled(reloadSupport)
        self.contextMenuClear.setEnabled(clearSupport)
        self.contextMenuFilter.setEnabled(filterSupport)
        self.contextMenuLimit.setEnabled(limitSupport)

        # For the submenues in the context menu, we add appropriate
        # actions, based on single|multi selection, or disable the menu
        # altogether if there is no support for the operation.
        if addSupport:
            self.contextMenuAdd.setEnabled(True)
            self.contextMenuAdd.addAction(self.str_ENTRY, self.addEntryChoosen)
            self.contextMenuAdd.addAction(self.str_TEMPLATE, self.addTemplateChoosen)
        else:
            self.contextMenuAdd.setEnabled(False)

        if deleteSupport:
            self.contextMenuDelete.setEnabled(True)
            if numselected == 1:
                self.contextMenuDelete.addAction(self.str_ITEM, self.deleteSelection)
                self.contextMenuDelete.addAction(self.str_SUBTREE, self.deleteSelection)
                self.contextMenuDelete.addAction(self.str_SUBTREE_PARENTS, self.deleteSelection)
            else:
                self.contextMenuDelete.addAction(self.str_ITEMS, self.deleteSelection)
                self.contextMenuDelete.addAction(self.str_SUBTREES, self.deleteSelection)
                self.contextMenuDelete.addAction(self.str_SUBTREES_PARENTS, self.deleteSelection)
        else:
            self.contextMenuDelete.setEnabled(False)

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

#        else:
#            # Remember the index so it can be used from the method
#            # selected from the pop-up-menu
#            self.clickedIndex = self.selection[0]
#            clickedItem = self.clickedIndex.internalPointer()
#
#            if clickedItem == None:
#                return
#            else:
#                # Find out what the item supports
#                supports = clickedItem.getSupportedOperations()
#
#                if supports == 0:
#                    pass#menu.addAction("No actions available")
#
#                else:
#                    if clickedItem.smartObject() != None:
#                        pass#menu.addAction("Open", self.openChoosen)
#
#                    # Add avaiable methods
#                    if supports & AbstractLDAPTreeItem.SUPPORT_RELOAD:
#                        menu.addAction(self.tr("Reload children"), self.reloadChoosen)
#                    if supports & AbstractLDAPTreeItem.SUPPORT_FILTER:
#                        menu.addAction(self.tr("Filter"), self.filterChoosen)
#                    if supports & AbstractLDAPTreeItem.SUPPORT_LIMIT:
#                        menu.addAction(self.tr("Limit"), self.limitChoosen)
#                    if supports & AbstractLDAPTreeItem.SUPPORT_CLEAR:
#                        menu.addAction(self.tr("Clear"), self.clearChoosen)
#                    if supports & AbstractLDAPTreeItem.SUPPORT_ADD:
#                        m = QMenu("Add", menu)
#                        m.addAction(self.tr("Entry"), self.entryChoosen)
#                        m.addAction(self.tr("Template"), self.addTemplateChoosen)
#                        menu.addMenu(m)
#                    if supports & AbstractLDAPTreeItem.SUPPORT_DELETE:
#                        m = QMenu("Delete", menu)
#                        m.addAction(self.tr("Entry"), self.entryChosen)
#                        m.addAction(self.tr("Template"), self.addTemplateChoosen)
#                    if supports & AbstractLDAPTreeItem.SUPPORT_EXPORT:
#                        m = QMenu("Export", menu)
#                        m.addAction(self.tr("Item"), self.exportSelection)
#                        m.addAction(self.tr("Subtree"), self.exportSelection)
#                        m.addAction(self.tr("Subtree with parent"), self.exportSelection)
#                        menu.addMenu(m)
                        
        # Finally we execute the context menu
        self.contextMenu.exec_(self.entryList.mapToGlobal(point))
        
        # We need to clear all the submenues after each right click
        # selection, if not; the submenu actions will be added and 
        # thus duplicated for every selection the user makes.
        # FIXME: Find a better way of handling this issue.
        self.contextMenuAdd.clear()
        self.contextMenuDelete.clear()
        self.contextMenuExport.clear()

    """
    Following methods are called from a context-menu.
    self.clickedItem is set there.
    """
    def openChoosen(self):
        self.viewItem(self.clickedIndex)

    def reloadChoosen(self):
        for index in self.selection:
            self.reloadSignal.emit(index)

    def clearChoosen(self):
        for index in self.selection:
            self.clearSignal.emit(index)

    def limitChoosen(self):
        # Have the item set the limit for us, the reload
        for index in self.selection():
            index.internalPointer().setLimit()
            self.reloadSignal.emit(index)

    def filterChoosen(self):
        # Have the item set the filter, then reload
        for index in self.selection:
            index.internalPointer().setFilter()
            self.reloadSignal.emit(index)

    def addEntryChoosen(self):
        for index in self.selection:
            self.addNewEntry(index)

    def addTemplateChoosen(self):
        pass

    def addNewEntry(self, parentIndex, defaultSmartObject=None):
        tmp = NewEntryDialog(parentIndex, defaultSmartObject)
        if tmp.exec_():
            print "La til ny entry"
            # TODO Do something. (Reload?)

    def viewItem(self, index):

        smartObject = index.internalPointer().smartObject()

        # We need to have tried to open an items with a smartobject to proceed
        if smartObject == None:
            return

        # Saves a representation of the opened entry to avoid opening duplicates
        serverName = smartObject.getServerAlias()
        dn = smartObject.getDN()
        rep = (serverName, dn)

        if self.openTabs.has_key(str(rep)):
            x = self.openTabs[str(rep)]
            self.tabWidget.setCurrentWidget(x)
            return

        x = AdvancedObjectWidget(smartObject, QtCore.QPersistentModelIndex(index))
        self.openTabs[str(rep)] = x
        self.tabWidget.addTab(x, smartObject.getPrettyRDN())
        self.tabWidget.setCurrentWidget(x)

    def deleteSelection(self, selection=[]):
        """Slot for the context menu.
        
        Opens the DeleteDialog with the selected entries, giving the
        user the option to validate the selection before deleting.
        """
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
        serverListObject = ServerList()
        
        for index in self.selection:
            smartObject = index.internalPointer().smartObject()
            
            serverName = smartObject.getServerAlias()
            dn = smartObject.getDN()
            con = LumaConnection(serverListObject.getServerObject(serverName))
            
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
        dialog.exec_()

    def editServerSettings(self):
        """Slot for the context menu.
        
        Opens the ServerDialog with the selected server.
        """
        pass

    def tabCloseClicked(self, index):
        #TODO Check if should save etc etc
        clicked = self.tabWidget.widget(index).aboutToChange()
        if clicked == QMessageBox.Cancel:
            return
        sO = self.tabWidget.widget(index).getSmartObject()

        if not (sO == None):
            # Remove the representation of the opened entry from the list
            serverName = sO.getServerAlias()
            dn = sO.getDN()
            rep = (serverName, dn)
            self.openTabs.pop(str(rep))

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
        self.contextMenuReload.setText(QtCore.QCoreApplication.translate("BrowserView", "Reload"))
        self.contextMenuClear.setText(QtCore.QCoreApplication.translate("BrowserView", "Clear"))
        self.contextMenuFilter.setText(QtCore.QCoreApplication.translate("BrowserView", "Set Filter"))
        self.contextMenuLimit.setText(QtCore.QCoreApplication.translate("BrowserView", "Set Limit"))
        self.contextMenuAdd.setTitle(QtCore.QCoreApplication.translate("BrowserView", "Add"))
        self.contextMenuDelete.setTitle(QtCore.QCoreApplication.translate("BrowserView", "Delete"))
        self.contextMenuExport.setTitle(QtCore.QCoreApplication.translate("BrowserView", "Export"))
        
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


import dsml
import StringIO

class ExportDialog(QtGui.QDialog, Ui_ExportDialog):
    """The dialog for exporting ldap entries to disk.
    
    TODO: enable|disable export button when filename|nofilename is defined
    TODO: better feedback if something goes wrong, perhaps not accept(), if
          not all checked items get exported ?
    """
    
    __logger = logging.getLogger(__name__)
    
    def __init__(self, msg='', parent=None):
        """
        @param items:
            The list of items to export.
        @param msg:
            A message to display in the dialog. Might be information
            about problems with fetching all the LDAP entries, etc.
        """
        super(ExportDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.iconLabel.setPixmap(pixmapFromThemeIcon('document-save', ':/icons/export_big'))
        self.fileButton.setIcon(iconFromTheme('document-open', ':/icons/folder'))
        self.messageLabel.setText(msg)
        
        self.model = QtGui.QStandardItemModel()
        self.exportItemView.setModel(self.model)
        self.exportItemView.setAlternatingRowColors(True)
        self.exportItemView.setUniformItemSizes(True)
        self.exportDict = {}
    
    def __utf8(self, text):
        """Helper method for encoding in unicode utf-8.
        
        This is helpful in particular when working with QStrings.
        
        @param text: 
            the text object to encode.
        @return: 
            the text in unicode utf-8 encoding.
        """
        return unicode(text).encode('utf-8').strip()
    
    def setExportItems(self, data):
        """Sets the items to be exported.
        
        Populates the model.
        """
        self.data = data
        for item in self.data:
            prettyDN = item.getPrettyDN()
            modelItem = QtGui.QStandardItem(prettyDN)
            modelItem.setEditable(False)
            modelItem.setCheckable(True)
            
            self.exportDict[prettyDN] = [item, modelItem]
            modelItem.setCheckState(QtCore.Qt.Checked)
            self.model.appendRow(modelItem)
    
    def openFileDialog(self):
        """Slot for the file button.
        
        Opens a File Dialog to let the user choose where to export.
        """
        userdir = getUserHomeDir()
        filter = "LDIF files (*.ldif);;DSML files (*dsml)"
        filename = QtGui.QFileDialog.getSaveFileName(self,
                                                     caption='Select export file',
                                                     directory=userdir,
                                                     filter=filter)
        filename = self.__utf8(filename)
        filter = self.__utf8(self.formatBox.currentText())
        if filter.startswith('LDIF') and not filename.endswith('.ldif'):
            filename = '%s.ldif' % filename
        elif filter.startswith('DSML') and not filename.endswith('.dsml'):
            filename = '%s.dsml' % filename
 
        self.outputEdit.setText(filename)
        self.exportButton.setEnabled(True)
    
    def onFormatChanged(self, format):
        """Slot for the format combobox.
        
        Checks if the output file is defined and wether its filending
        matches the choosen export format. If not defined the method
        returns. If the filening doesn't match, it is switched.
        """
        if self.outputEdit.text() == '':
            return
        format = self.__utf8(format)
        oldname = self.outputEdit.text()
        if format == 'LDIF':
            newname = replace(oldname, '.dsml', '.ldif')
        elif format == 'DSML':
            newname = replace(oldname, '.ldif', '.dsml')
        self.outputEdit.setText(newname)

    def export(self):
        """Slot for the export button.
        
        Exports all checked items to the file defined in the outputEdit
        widget.
        """
        # Iterate through the modelitems and remove unchekced items
        # from the export dictionary, which will be used later.
        for i in xrange(self.model.rowCount()):
            item = self.model.itemFromIndex(self.model.index(i, 0))
            if item.checkState() != QtCore.Qt.Checked:
                del self.exportDict[self.__utf8(item.text())]
        
        # Map the dictionary keys
        #
        itemList = map(lambda x: self.exportDict[x][0], self.exportDict.keys())
        itemList.sort()
        try:
            filename = self.outputEdit.text()
            fileHandler = open(filename, 'w')
            format = self.__utf8(self.formatBox.currentText())
            
            
            # DSML need some header info.
            if format == 'DSML':
                tmp = StringIO.StringIO()
                dsmlWriter = dsml.DSMLWriter(tmp)
                dsmlWriter.writeHeader()
                fileHandler.write(tmp.getvalue())
            
            # Write the LDAP entries to file
            for x in itemList:
                try:
                    if format == 'LDIF':
                        fileHandler.write(x.convertToLdif())
                    
                    elif format == 'DSML':
                        fileHandler.write(x.convertToDsml())
                except IOError, e:
                    msg = 'Could not export %s. Reason\n%s' % (str(x), str(e))
                    self.__logger.error(msg)
            
            # DSML need additional footer info, to close the format
            if format == 'DSML':
                tmp = StringIO.StringIO()
                dsml.DSMLWriter(tmp)
                dsmlWriter.writeFooter()
                fileHandler.write(tmp.getvalue())
            
            fileHandler.close()
        except IOError, e:
            msg = 'Problems writing to %s. Reason:\n%s' % (filename, str(e))
            self.__logger.error(msg)
        
        self.accept()
    
    def cancel(self):
        """Slot for the cancel button.
        """
        del self.exportDict
        self.reject()
        