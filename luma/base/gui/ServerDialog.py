'''
Created on 2. feb. 2011

@author: Christian Forfang and Simen Natvig
'''

from PyQt4 import QtCore
from PyQt4.QtCore import QModelIndex
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog, QDataWidgetMapper
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QInputDialog, QItemSelectionModel
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QMessageBox

from base.gui.ServerDialogDesign import Ui_ServerDialogDesign
from base.model.ServerListModel import ServerListModel
from base.backend.ServerObject import ServerObject
from ServerDelegate import ServerDelegate
from base.util.icontheme import pixmapFromThemeIcon
import copy

class ServerDialog(QDialog, Ui_ServerDialogDesign):

    def __init__(self, serverList):
        """
        Note: the input-ServerList-object is used directly by both the 
        methods here and the model so beware of changes to it.
        It's probably not a good idea to pass a ServerList if one of its 
        ServerObjects are in use.
        """

        QDialog.__init__(self)
        self.setupUi(self)

        self.networkLabel.setPixmap(pixmapFromThemeIcon('network-server', ':/icons/network-server'))
        self.authLabel.setPixmap(pixmapFromThemeIcon('dialog-password', ':/icons/passwordmedium'))
        self.securityLabel.setPixmap(pixmapFromThemeIcon('preferences-system', ':/icons/config'))


        self.__serverList = copy.deepcopy(serverList)
        self._serverListCopy = None
        self._returnList = None

        # Create the model used by the views
        self.slm = ServerListModel(self.__serverList)

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

        self.connect(self.serverListView.selectionModel(), QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'), self.setBaseDN)

        # Map columns of the model to fields in the gui
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.slm)
        # Handles the comboboxes and to-from the list of custom baseDNs
        self.serverDelegate = ServerDelegate()
        self.mapper.setItemDelegate(self.serverDelegate)

        self.mapper.addMapping(self.hostLineEdit, 1)
        self.mapper.addMapping(self.portSpinBox, 2)
        self.mapper.addMapping(self.bindAnonBox, 3)
        self.mapper.addMapping(self.baseBox, 4)
        #self.mapper.addMapping(self.baseDNWidget, 5)

        self.mapper.addMapping(self.bindLineEdit, 6)
        self.mapper.addMapping(self.passwordLineEdit, 7)
        self.mapper.addMapping(self.encryptionBox, 8)
        self.mapper.addMapping(self.methodBox, 9)
        self.mapper.addMapping(self.aliasBox, 10)
        self.mapper.addMapping(self.useClientCertBox, 11)
        self.mapper.addMapping(self.certFileEdit, 12)
        self.mapper.addMapping(self.certKeyFileEdit, 13)
        self.mapper.addMapping(self.validateBox, 14)

        # Select the first servers (as the serverlistview does)
        self.mapper.setCurrentIndex(0)

        # Let the mapper know when another server is selected in the list
        self.serverListView.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex)

        # Workaround to avoid the button stealing the focus from the baseDNView thus invalidating it's selection
        # maning we don't know what do delete
        #self.deleteBaseDNButton.setFocusPolicy(Qt.NoFocus)
        self.setBaseDN()

    def addBaseDN(self):
        tmpBase = unicode(self.baseEdit.text()).strip()
        if tmpBase == u"":
            return
        self.baseDNWidget.addItem(QListWidgetItem(tmpBase)) #Add to list

        serverIndex = self.serverListView.selectedIndexes()
        index = self.slm.createIndex(serverIndex[0].row(), 5)
        self.serverDelegate.setModelData(self.baseDNWidget, self.slm, index)
        self.baseEdit.clear() #Clear textfield
        self.mapper.submit() #Force push to model

    def deleteBaseDN(self):
        # Delete every selected baseDN
        for tmpItem in self.baseDNWidget.selectedItems():
            if not (None == tmpItem):
                index = self.baseDNWidget.indexFromItem(tmpItem) #get the index to the basedn
                d = self.baseDNWidget.takeItem(index.row()) #delete (actually steal) the baseDN from the list
                if d != 0:
                    del d # Per the QT-docs, someone needs to delete it

        serverIndex = self.serverListView.selectedIndexes()
        index = self.slm.createIndex(serverIndex[0].row(), 5)
        self.serverDelegate.setModelData(self.baseDNWidget, self.slm, index)
        self.mapper.submit() #Force push changes to model

    def setBaseDN(self):
        serverIndex = self.serverListView.selectedIndexes()
        if len(serverIndex) > 0:
            index = self.slm.createIndex(serverIndex[0].row(), 5)
            self.serverDelegate.setEditorData(self.baseDNWidget, index)

    def addServer(self):
        """
        Create a new ServerObject and add it to the model (thus the list)
        """
        name, ok = QInputDialog.getText(self, 'Add server', 'Name:')
        if ok:
            if len(name) < 1 or self.__serverList.getServerObject(name) != None:
                QMessageBox.information(self, 'Error', "Invalid name or already used.")
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
        """
        Delete a server from the model/list
        """
        if self.serverListView.selectionModel().currentIndex().row() < 0:
            #No server selected
            return

        re = QMessageBox.question(self, 'Delete',
                     "Are you sure?", QMessageBox.Yes, QMessageBox.No)
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

    def saveServers(self):
        """
        Called when the Save-button is clicked.
        
        What should happen when the user clicks Save then Cancel?
        """
        self.__serverList.writeServerList()
        self._serverListCopy = copy.deepcopy(self.__serverList)

    def reject(self):
        """
        Called when the users clicks cancel or presses escape
        
        SOMETHING LOGICAL SHOULD PROBABLY BE DONE HER
        """
        r = QMessageBox.question(self, "Exit?", "Are you sure you want to exit the server editor?\n Any unsaved changes will be lost!", QMessageBox.Ok | QMessageBox.Cancel)
        if not r == QMessageBox.Ok:
            return
        if self._serverListCopy:
            self._returnList = self._serverListCopy
            QDialog.accept(self)
            return
        QDialog.reject(self)

    def accept(self):
        """
        Called when OK-button is clicked
        
        SOMETHING LOGICAL SHOULD PROBABLY BE DONE HER
        """
        self.__serverList.writeServerList()
        self._returnList = self.__serverList
        QDialog.accept(self)

    def getResult(self):
        return self._returnList

    def certFileDialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file',
                    '')
        self.certFileEdit.setText(filename)
        self.mapper.submit()

    def certKeyFileDialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file',
                    '')
        self.certKeyFileEdit.setText(filename)
        self.mapper.submit()

if __name__ == "__main__":
    import logging
    import sys
    from base.backend.ServerList import ServerList
    l = logging.getLogger("base")
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())
    app = QApplication(sys.argv)
    s = ServerDialog(ServerList("c:/luma/", "serverlist.xml"))
    s.show()
    sys.exit(app.exec_())


