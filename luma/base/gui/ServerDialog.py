# -*- coding: utf-8 -*-
#
# base.gui.ServerDialog
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
from PyQt4.QtGui import QMessageBox, QProgressDialog
from PyQt4.QtCore import QCoreApplication, Qt, pyqtSignal
from PyQt4.QtCore import pyqtSlot, QThread, QThreadPool, QRunnable

from ..backend.LumaConnection import LumaConnection
from ..backend.ServerList import ServerList
from ..backend.ServerObject import ServerEncryptionMethod
from ..backend.ServerObject import ServerObject
from ..gui.design.ServerDialogDesign import Ui_ServerDialogDesign
from ..model.ServerListModel import ServerListModel
from ..util.IconTheme import pixmapFromTheme
from .ServerDelegate import ServerDelegate

class ServerDialog(QDialog, Ui_ServerDialogDesign):
    
    # Used by TestConnection
    testReturnSignal = pyqtSignal(bool, str)

    def __init__(self, server=None, parent=None):
        """The `ServerDialog` constructor.

        Parameters:

        - `serverList`: a `ServerList` instance containing the list of
          available servers.
        - `server`: the name of a server. If provided, this server will
          be selected in the serverList view.
        """
        super(ServerDialog, self).__init__(parent)
        self.setupUi(self)

        self.networkIcon.setPixmap(pixmapFromTheme(
            'preferences-system-network',
            ':/icons/48/preferences-system-network')
        )
        self.authIcon.setPixmap(pixmapFromTheme(
            'preferences-other',
            ':/icons/48/preferences-other')
        )
        self.securityIcon.setPixmap(pixmapFromTheme(
            'preferences-system',
            ':/icons/48/preferences-system')
        )
        
        self.__serverList = ServerList() #Load the serverlist from disk.
        self.__serverListCopy = None # When we click "Save", the current list is saved here
        
        # The list actually returned to the caller. Could be the copy or current active list
        self.__returnList = None 

        # Create the model used by the views and connect signals
        self.slm = ServerListModel(self.__serverList, self)
        self.slm.dataChanged.connect(self.wasChanged)
        self.slm.rowsInserted.connect(self.wasChanged)
        self.slm.rowsRemoved.connect(self.wasChanged)
        
        # Used for determining if we should confirm cancel
        self.isChanged = False

        # The serverListView works on the servermodel
        self.serverListView.setModel(self.slm)

        # Enable/disable editing depending on if we have a server to edit
        if self.slm.rowCount(QModelIndex()) > 0:
            self.tabWidget.setEnabled(True)
        else:
            self.tabWidget.setEnabled(False)

        self.splitter.setStretchFactor(1, 0)
        
        # If a servername is supplied we try to get its index, 
        # And make it selected, else we select the first server
        # in the model)
        if not server is None:
            serverIndex = self.__serverList.getIndexByName(server)
            if serverIndex == -1:
                serverIndex = 0
            index = self.serverListView.model().index(serverIndex, 0)
        else:
            index = self.serverListView.model().index(0, 0)
        # Select it in the view
        self.serverListView.selectionModel().select(index, QItemSelectionModel.ClearAndSelect)
        self.serverListView.selectionModel().setCurrentIndex(index, QItemSelectionModel.ClearAndSelect)

        self.serverListView.selectionModel().selectionChanged.connect(self.setBaseDN) #Same as below

        # Map columns of the model to fields in the gui
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.slm)
        
        # The delegate handles the comboboxes and to-from the list of custom baseDNs
        # (delegate is used manually for the baseDNs)
        self.serverDelegate = ServerDelegate()
        self.mapper.setItemDelegate(self.serverDelegate)
        self.mapper.addMapping(self.hostEdit, 1)
        self.mapper.addMapping(self.portSpinBox, 2)
        self.mapper.addMapping(self.bindAnonBox, 3)
        self.mapper.addMapping(self.baseDNBox, 4)
        self.mapper.addMapping(self.bindAsEdit, 6)
        self.mapper.addMapping(self.passwordEdit, 7)
        self.mapper.addMapping(self.encryptionBox, 8)
        self.mapper.addMapping(self.mechanismBox, 9)
        self.mapper.addMapping(self.aliasBox, 10)
        self.mapper.addMapping(self.useClientCertBox, 11)
        self.mapper.addMapping(self.certFileEdit, 12)
        self.mapper.addMapping(self.certKeyfileEdit, 13)
        self.mapper.addMapping(self.validateBox, 14)

        # workaround to ensure model being updated (Mac OS X bug)
        self.aliasBox.clicked.connect(self.aliasBox.setFocus)
        self.baseDNBox.clicked.connect(self.baseDNBox.setFocus)
        self.bindAnonBox.clicked.connect(self.bindAnonBox.setFocus)
        self.useClientCertBox.clicked.connect(self.useClientCertBox.setFocus)

        # Select the first servers (as the serverlistview does)
        self.mapper.setCurrentIndex(0)
        self.setBaseDN()

        # Let the mapper know when another server is selected in the list
        self.serverListView.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex)
        
        # Checks for SSL enabled but with a non-standard port.
        self.encryptionBox.currentIndexChanged[int].connect(self.checkSSLport)

        # Used by TestConnection
        self.testReturnSignal.connect(self.testFinished)
        
    def checkSSLport(self, index):
        """ If SSL is choosen with a port other than 636, confirm this with the user
        """
        if index == ServerEncryptionMethod.SSL and self.portSpinBox.value() != 636:
            ans = QMessageBox.information(self, QCoreApplication.translate("ServerDialog","SSL")
                ,QCoreApplication.translate("ServerDialog","You have choosen to use SSL but with a port other than 636.\n Do you want this automatically changed?")
                ,QMessageBox.Yes|QMessageBox.No)
            if ans == QMessageBox.Yes:
                self.portSpinBox.setValue(636)

    def wasChanged(self):
        """Slot to register that some server settings is changed.
        """
        self.isChanged = True

    def addBaseDN(self):
        """Slot for adding a base DN
        """
        tmpBaseDN = unicode(self.baseDNEdit.text()).strip()
        if tmpBaseDN == u"":
            return
        self.baseDNListWidget.addItem(QListWidgetItem(tmpBaseDN)) #Add to list

        serverIndex = self.serverListView.selectedIndexes()
        index = self.slm.createIndex(serverIndex[0].row(), 5)
        self.serverDelegate.setModelData(self.baseDNListWidget, self.slm, index)
        self.baseDNEdit.clear() #Clear textfield
        self.mapper.submit() #Force push to model

    def deleteBaseDN(self):
        """Slot for deleting a base DN
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
        """Slot for setting the base DN.
        """
        serverIndex = self.serverListView.selectedIndexes()
        if len(serverIndex) > 0:
            index = self.slm.createIndex(serverIndex[0].row(), 5)
            self.serverDelegate.setEditorData(self.baseDNListWidget, index)

    def addServer(self):
        """Create a new ServerObject and add it to the model, and thus
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
            self.tabWidget.setEnabled(True) # Make sure editing is enabled

    def deleteServer(self):
        """Delete a server from the model/list
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
            self.tabWidget.setEnabled(False) #Disable editing if no servers left

    def saveServerlist(self):
        """Called when the Save-button is clicked
        """
        self.mapper.submit()

        if not self.baseDNsOK():
            if not self.isBaseDNsOkMessage():
                # If we got here, we DO NOT WANT TO SAVE/QUIT
                return False

        self.__serverList.writeServerList()
        self.__serverListCopy = copy.deepcopy(self.__serverList)

        return True

    def reject(self):
        """Called when the users clicks cancel or presses escape
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
        """Called when OK-button is clicked
        """
        if not self.saveServerlist():
            # DO NOT QUIT
            return
        self.__returnList = self.__serverList
        QDialog.accept(self)

    def isBaseDNsOkMessage(self):
        r = QMessageBox.question(self,
            self.tr("BaseDNs not defined"),
            self.tr("One or more server(s) are setup to use custom base DNs without specifying any.\nDo you still want to save?"),
            QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.No:
            return False
        else:
            return True

    def baseDNsOK(self):
        for server in self.__serverList.getTable(): 
            if server.autoBase == False and len(server.baseDN) < 1:
                return False
        return True

    def getResult(self):
        return self.__returnList

    def certFileDialog(self):
        """Slot for selecting a certificate file.
        """
        certFile = QFileDialog.getOpenFileName(self, self.trUtf8('Select certificate file'), '')

        if not certFile is None:
            self.certFileEdit.setText(certFile)
            self.mapper.submit()

    def certKeyfileDialog(self):
        """Slot for selecting a certificate keyfile.
        """
        certKeyfile = QFileDialog.getOpenFileName(self, self.trUtf8('Select certificate keyfile'), '')

        if not certKeyfile is None:
            self.certKeyfileEdit.setText(certKeyfile)
            self.mapper.submit()

    def testConnection(self):
        """
        Tries to bind to the currently selected server.
        """
        currentServerId = self.serverListView.currentIndex().row()
        sO = self.__serverList.getServerObjectByIndex(currentServerId)

        # Busy-dialog
        self.testProgress = QProgressDialog("Trying to connect to server.",
                "Abort",
                0, 0,
                self)
        self.testProgress.setWindowModality(Qt.WindowModal)
        self.testProgress.show()

        self.thread = TestConnection(sO, self)
        QThreadPool.globalInstance().start(self.thread)

    @pyqtSlot(bool, str)
    def testFinished(self, success, exceptionStr):
        self.testProgress.hide()
        # No message on cancel
        if self.testProgress.wasCanceled():
            return

        if success:
            # Success-message
            QMessageBox.information(self, "Status", "Connection successful!")
        else:
            # Error-message
            if exceptionStr == "Invalid credentials":
                QMessageBox.warning(self, "Status", "Connection failed:\n"+exceptionStr+"\n\n(You do not have to spesify passwords here -- you will be asked when needed.)")
                return
            QMessageBox.warning(self, "Status", "Connection failed:\n"+exceptionStr)

class TestConnection(QRunnable):
    def __init__(self, serverObject, target):
        super(TestConnection, self).__init__()
        self.target = target
        self.serverObject = serverObject
    def run(self):
        # Try bind -- do not display pw-input and do not use remembered passwords
        conn = LumaConnection(self.serverObject)
        success, exception = conn.bind(askForPw = False, noOverride = True)
        # Return status
        if success:
            self.target.testReturnSignal.emit(True, "")
        else:
            self.target.testReturnSignal.emit(False,str(exception[0]["desc"]))


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
