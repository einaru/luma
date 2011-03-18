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
from PyQt4.QtGui import QPixmap

from base.gui.ServerDialogDesign import Ui_ServerDialogDesign
from base.model.ServerListModel import ServerListModel
from base.backend.ServerObject import ServerObject
from ServerDelegate import ServerDelegate
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
        
        self.networkLabel.setPixmap(QPixmap(':/icons/network-server'))
        self.authLabel.setPixmap(QPixmap(':/icons/passwordmedium'))
        self.securityLabel.setPixmap(QPixmap(':/icons/config'))

        
        self._serverList = copy.deepcopy(serverList)
        self._serverListCopy = None
        self._returnList = None
        
        # Create the model used by the views
        self.slm = ServerListModel(self._serverList)
        
        # Add the model to the list of servers
        self.serverListView.setModel(self.slm)

        # Enable/disable editing depending on if we have a server to edit
        if self.slm.rowCount(QModelIndex()) > 0:
            self.serverWidget.setEnabled(True)
        else:
            self.serverWidget.setEnabled(False)
            
        self.splitter.setStretchFactor(0, 1)
        
        # Select the first server in the model)
        index = self.serverListView.model().index(0,0)
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
        name, ok = QInputDialog.getText(self, self.tr('Add server'), self.tr('Name:'))
        if ok:
            if len(name) < 1 or self._serverList.getServerObject(name) != None:
                QMessageBox.information(self, self.tr('Error'), self.tr("Invalid name or already used."))
                return
            
            sO = ServerObject()
            sO.name = unicode(name)
            
            # Insert into the model
            m = self.serverListView.model() 
            m.beginInsertRows(QModelIndex(), m.rowCount(QModelIndex()),m.rowCount(QModelIndex())+1)
            self._serverList.addServer(sO)
            m.endInsertRows()
            
            s = m.index(m.rowCount(QModelIndex)-1,0) #Index of the newly added server
            self.serverListView.selectionModel().select(s, QItemSelectionModel.ClearAndSelect) #Select it
            self.serverListView.selectionModel().setCurrentIndex(s, QItemSelectionModel.ClearAndSelect) #Mark it as current      
            self.mapper.setCurrentIndex(s.row()) # Update the mapper
            self.serverWidget.setEnabled(True) # Make sure editing is enabled
            
    def deleteServer(self):
        """
        Delete a server from the model/list
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
            self.serverListView.model().removeRows(index.row(),1)
            self.serverListView.model().endRemoveRows()
            
            # When deleting, the view gets updated and selects a new current.
            # Get it and give it to the mapper
            newIndex = self.serverListView.selectionModel().currentIndex()
            self.mapper.setCurrentIndex(newIndex.row())
            
        if self.slm.rowCount(QModelIndex()) == 0:
            self.serverWidget.setEnabled(False) #Disable editing if no servers left
            
    def saveServers(self):
        """
        Called when the Save-button is clicked
        """
        self.mapper.submit()
        self._serverList.writeServerList()
        self._serverListCopy = copy.deepcopy(self._serverList)     
        
    def reject(self):
        """
        Called when the users clicks cancel or presses escape
        """
        # Really quit?
        r = QMessageBox.question(self, self.tr("Exit?"), self.tr("Are you sure you want to exit the server editor?\n Any unsaved changes will be lost!"), QMessageBox.Ok|QMessageBox.Cancel)
        if not r == QMessageBox.Ok:
            # Don't quit
            return
        
        # If "save" has been clicked, return the saved list by calling accept()
        if self._serverListCopy: #This is non-None if Save has been clicked.
            self._returnList = self._serverListCopy #Return the saved on instead
            self.accept() #accept() returns _returnList to the caller
            return
        QDialog.reject(self)
    
    def accept(self):
        """
        Called when OK-button is clicked
        """
        self.mapper.submit()
        self._serverList.writeServerList()
        self._returnList = self._serverList
        QDialog.accept(self)
        
    def getResult(self):
        return self._returnList
        
    def certFileDialog(self):
        filename = QFileDialog.getOpenFileName(self, self.tr('Open file'),
                    '')
        self.certFileEdit.setText(filename)
        self.mapper.submit()

    def certKeyFileDialog(self):
        filename = QFileDialog.getOpenFileName(self, self.tr('Open file'), '')
        self.certKeyFileEdit.setText(filename)
        self.mapper.submit()
    
    
