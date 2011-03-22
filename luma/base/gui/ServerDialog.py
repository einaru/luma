# -*- coding: utf-8 -*-
#
# base.gui.Dialog
#
# Copyright (c) 2011
#     Christian Forfang, <cforfang@gmail.com>
#     Simen Natvig, <simen.natvig@gmail.com>
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
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
import copy

from PyQt4.QtCore import QModelIndex
from PyQt4.QtGui import QDialog, QDataWidgetMapper
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QInputDialog, QItemSelectionModel
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QMessageBox

from .ServerDelegate import ServerDelegate
from ..backend.ServerObject import ServerObject
from ..gui.design.ServerDialogDesign import Ui_ServerDialogDesign
from ..model.ServerListModel import ServerListModel
from ..util.IconTheme import pixmapFromThemeIcon

class ServerDialog(QDialog, Ui_ServerDialogDesign):

    def __init__(self, serverList, parent=None):
        """ Note:
        the input-ServerList-object is used directly by both the methods
        here and the model so beware of changes to it. It's probably not
        a good idea to pass a ServerList if one of its ServerObjects are
        in use.
        """
        super(ServerDialog, self).__init__(parent)
        self.setupUi(self)

        self.networkIcon.setPixmap(pixmapFromThemeIcon('network-server', ':/icons/network-server'))
        self.authIcon.setPixmap(pixmapFromThemeIcon('dialog-password', ':/icons/passwordmedium'))
        self.securityIcon.setPixmap(pixmapFromThemeIcon('preferences-system', ':/icons/config'))

        self.__serverList = copy.deepcopy(serverList)
        self.__serverListCopy = None
        self.__returnList = None

        # Create the model used by the views
        self.slm = ServerListModel(self.__serverList)
        self.slm.dataChanged.connect(self.wasChanged)
        self.slm.rowsInserted.connect(self.wasChanged)
        self.slm.rowsRemoved.connect(self.wasChanged)
        self.isChanged = False

        # Add the model to the list of servers
        self.serverListView.setModel(self.slm)

        # Enable/disable editing depending on if we have a server to edit
        if self.slm.rowCount(QModelIndex()) > 0:
            self.tabWidget.setEnabled(True)
        else:
            self.tabWidget.setEnabled(False)

        self.splitter.setStretchFactor(0, 1)

        # Select the first server in the model)
        index = self.serverListView.model().index(0, 0)
        # Select it in the view
        self.serverListView.selectionModel().select(index, QItemSelectionModel.ClearAndSelect)
        self.serverListView.selectionModel().setCurrentIndex(index, QItemSelectionModel.ClearAndSelect)

        self.serverListView.selectionModel().selectionChanged.connect(self.setBaseDN) #Same as below
        #self.connect(self.serverListView.selectionModel(),  QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'), self.setBaseDN)

        # Map columns of the model to fields in the gui
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.slm)
        # Handles the comboboxes and to-from the list of custom baseDNs
        self.serverDelegate = ServerDelegate()
        self.mapper.setItemDelegate(self.serverDelegate)

        self.mapper.addMapping(self.hostEdit, 1)
        self.mapper.addMapping(self.portSpinBox, 2)
        self.mapper.addMapping(self.bindAnonBox, 3)
        self.mapper.addMapping(self.baseDNBox, 4)
        #self.mapper.addMapping(self.baseDNListWidget, 5)

        self.mapper.addMapping(self.bindAsEdit, 6)
        self.mapper.addMapping(self.passwordEdit, 7)
        self.mapper.addMapping(self.encryptionBox, 8)
        self.mapper.addMapping(self.mechanismBox, 9)
        self.mapper.addMapping(self.aliasBox, 10)
        self.mapper.addMapping(self.useClientCertBox, 11)
        self.mapper.addMapping(self.certFileEdit, 12)
        self.mapper.addMapping(self.certKeyfileEdit, 13)
        self.mapper.addMapping(self.validateBox, 14)

        # Select the first servers (as the serverlistview does)
        self.mapper.setCurrentIndex(0)

        # Let the mapper know when another server is selected in the list
        self.serverListView.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex)

        # Workaround to avoid the button stealing the focus from the baseDNView thus invalidating it's selection
        # maning we don't know what do delete
        #self.deleteBaseDNButton.setFocusPolicy(Qt.NoFocus)
        self.setBaseDN()

    def wasChanged(self):
        """ Slot to register that some server settings is changed.
        """
        self.isChanged = True

    def addBaseDN(self):
        """ Slot for adding a base DN
        """
        tmpBase = unicode(self.baseEdit.text()).strip()
        if tmpBase == u"":
            return
        self.baseDNListWidget.addItem(QListWidgetItem(tmpBase)) #Add to list

        serverIndex = self.serverListView.selectedIndexes()
        index = self.slm.createIndex(serverIndex[0].row(), 5)
        self.serverDelegate.setModelData(self.baseDNListWidget, self.slm, index)
        self.baseEdit.clear() #Clear textfield
        self.mapper.submit() #Force push to model

    def deleteBaseDN(self):
        """ Slot for deleting a base DN
        """
        # Delete every selected baseDN
        for tmpItem in self.baseDNListWidget.selectedItems():
            if not (None == tmpItem):
                index = self.baseDNListWidget.indexFromItem(tmpItem) #get the index to the basedn
                d = self.baseDNListWidget.takeItem(index.row()) #delete (actually steal) the baseDN from the list
                if d != 0:
                    del d # Per the QT-docs, someone needs to delete it

        serverIndex = self.serverListView.selectedIndexes()
        index = self.slm.createIndex(serverIndex[0].row(), 5)
        self.serverDelegate.setModelData(self.baseDNListWidget, self.slm, index)
        self.mapper.submit() #Force push changes to model

    def setBaseDN(self):
        """ Slot for setting the base DN.
        """
        serverIndex = self.serverListView.selectedIndexes()
        if len(serverIndex) > 0:
            index = self.slm.createIndex(serverIndex[0].row(), 5)
            self.serverDelegate.setEditorData(self.baseDNListWidget, index)

    def addServer(self):
        """ Create a new ServerObject and add it to the model, and thus
        the server list.
        """
        name, ok = QInputDialog.getText(self, self.tr('Add server'), self.tr('Name:'))
        if ok:
            if len(name) < 1 or self.__serverList.getServerObject(name) != None:
                QMessageBox.information(self, self.tr('Error'), self.tr("Invalid name or already used."))
                return

            sO = ServerObject()
            sO.name = unicode(name)

            # Insert into the model
            m = self.serverListView.model()
            m.beginInsertRows(QModelIndex(), m.rowCount(QModelIndex()), m.rowCount(QModelIndex()) + 1)
            self.__serverList.addServer(sO)
            m.endInsertRows()

            s = m.index(m.rowCount(QModelIndex) - 1, 0) #Index of the newly added server
            self.serverListView.selectionModel().select(s, QItemSelectionModel.ClearAndSelect) #Select it
            self.serverListView.selectionModel().setCurrentIndex(s, QItemSelectionModel.ClearAndSelect) #Mark it as current      
            self.mapper.setCurrentIndex(s.row()) # Update the mapper
            self.serverWidget.setEnabled(True) # Make sure editing is enabled

    def deleteServer(self):
        """ Delete a server from the model/list
        """
        if self.serverListView.selectionModel().currentIndex().row() < 0:
            #No server selected
            return

        re = QMessageBox.question(self, self.tr('Delete'),
                     self.tr("Are you sure?"), QMessageBox.Yes, QMessageBox.No)
        if re == QMessageBox.Yes:
            index = self.serverListView.selectionModel().currentIndex() #Currently selected

            # Delete the server
            self.serverListView.model().beginRemoveRows(QModelIndex(), index.row(), index.row())
            self.serverListView.model().removeRows(index.row(), 1)
            self.serverListView.model().endRemoveRows()

            # When deleting, the view gets updated and selects a new current.
            # Get it and give it to the mapper
            newIndex = self.serverListView.selectionModel().currentIndex()
            self.mapper.setCurrentIndex(newIndex.row())

        if self.slm.rowCount(QModelIndex()) == 0:
            self.serverWidget.setEnabled(False) #Disable editing if no servers left

    def saveServerlist(self):
        """ Called when the Save-button is clicked
        """
        self.mapper.submit()
        self.__serverList.writeServerList()
        self.__serverListCopy = copy.deepcopy(self.__serverList)

    def reject(self):
        """ Called when the users clicks cancel or presses escape
        """
        # If no changes: just quit
        if not self.isChanged:
            QDialog.reject(self)
            return

        # Really quit?
        r = QMessageBox.question(self, self.tr("Exit?"), self.tr("Are you sure you want to exit the server editor?\n Any unsaved changes will be lost!"), QMessageBox.Ok | QMessageBox.Cancel)
        if not r == QMessageBox.Ok:
            # Don't quit
            return

        # If "save" has been clicked, return the saved list by calling accept()
        if self.__serverListCopy: #This is non-None if Save has been clicked.
            self.__returnList = self.__serverListCopy # Return the saved on instead
            QDialog.accept(self) # Closes the window while indicating the caller needs to get the new list (self.__returnList)
            return
        QDialog.reject(self)

    def accept(self):
        """ Called when OK-button is clicked
        """
        self.mapper.submit()
        self.__serverList.writeServerList()
        self.__returnList = self.__serverList
        QDialog.accept(self)

    def getResult(self):
        return self.__returnList

    def certFileDialog(self):
        """ Slot for selecting a certificate file.
        """
        certFile = QFileDialog.getOpenFileName(self, self.trUtf8('Select certificate file'), '')

        if not certFile is None:
            self.certFileEdit.setText(certFile)
            self.mapper.submit()

    def certKeyfileDialog(self):
        """ Slot for selecting a certificate keyfile.
        """
        certKeyfile = QFileDialog.getOpenFileName(self, self.trUtf8('Select certificate keyfile'), '')

        if not certKeyfile is None:
            self.certKeyfileEdit.setText(certKeyfile)
            self.mapper.submit()
