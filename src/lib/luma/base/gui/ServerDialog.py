'''
Created on 2. feb. 2011

@author: Christian
'''

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtGui import QDialog, QDataWidgetMapper, QStandardItemModel, QStandardItem, QItemSelectionRange
from base.gui.ServerDialogDesign import Ui_ServerDialogDesign
from base.models.ServerListModel import ServerListModel
from base.backend.ServerObject import ServerObject
from PyQt4.QtGui import QPixmap
from ServerDelegate import ServerDelegate

class ServerDialog(QDialog, Ui_ServerDialogDesign):
    
    def __init__(self, serverList):
        """
        Note: the input-ServerList-object is used directly by both the methods here and the model so beware of changes to it.
        It's probably not a good idea to pass a ServerList if one of its ServerObjects are in use.
        """
        
        QDialog.__init__(self)
        self.setupUi(self)
        
        self._ServerList = serverList
        slm = ServerListModel(self._ServerList)
        
        self.listView.setModel(slm)
        #self.listView.setItemDelegate(BoxDelegate())
        
        # Select the first server in the list
        self.listView.selectionModel().select(self.listView.model().index(0,0), QtGui.QItemSelectionModel.ClearAndSelect)        
        
        #For testing
        #self.tableView = QtGui.QTableView()
        #self.tableView.setModel(slm)
        #self.tableView.show()
        #self.tableView.setSelectionModel(self.listView.selectionModel())
        
        # Maps columns of the model to fields in the gui (and back when they're edited)
        self.mapper = QtGui.QDataWidgetMapper()
        self.mapper.setModel(slm)
        self.mapper.setItemDelegate(ServerDelegate())

        self.mapper.addMapping(self.hostLineEdit, 1)
        self.mapper.addMapping(self.portSpinBox, 2)
        self.mapper.addMapping(self.bindAnonBox, 3)
        self.mapper.addMapping(self.baseBox, 4)        
        self.mapper.addMapping(self.baseDNView, 5)
        self.mapper.addMapping(self.bindLineEdit, 6)
        self.mapper.addMapping(self.passwordLineEdit, 7)
        self.mapper.addMapping(self.encryptionBox, 8)
        self.mapper.addMapping(self.methodBox, 9)
        self.mapper.addMapping(self.aliasBox, 10)
        self.mapper.addMapping(self.useClientCertBox, 11)
        self.mapper.addMapping(self.certFileEdit, 12)
        self.mapper.addMapping(self.certKeyfileEdit, 13)
        self.mapper.addMapping(self.validateBox, 14)
        self.mapper.setCurrentIndex(0)
        
        # Let the mapper know when another server is selected in the list
        self.listView.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex)

        # The model is reset in the baseDNView when it looses focus (which means the selection is lost)
        # so in order for the button to know which baseDN to remove, it needs to let it keep the focus
        self.removeBaseDN.setFocusPolicy(Qt.Qt.NoFocus)
        QtGui.QPushButton.connect(self.removeBaseDN, QtCore.SIGNAL("clicked()"), self.removeBaseDn)
        
        
    def addBaseDn(self):
        """
        Adds a new BaseDN to the list
        """
        if self.baseDNView.model() != None:
            m = self.baseDNView.model()
            m.insertRows(m.rowCount(), 1, QtCore.QModelIndex())
            index = m.index(m.rowCount()-1, 0) #the row we just inserted
            m.setData(index, QtCore.QVariant("<Fill inn to add>"))
        else:
            QtGui.QMessageBox.information(None, 'Error', self.tr("Choose a server first"))

    def removeBaseDn(self):
        """
        Removes a BaseDN from the list.
        """
        if not len(self.baseDNView.selectedIndexes()) > 0:
            QtGui.QMessageBox.information(None, 'Error', "Nothing selected")
            return 
        row = self.baseDNView.selectedIndexes()[0].row() #Single selection
        self.baseDNView.model().removeRow(row)
        
    def addServer(self):
        """
        Create a new ServerObject and add it to the model (thus the list)
        """
        name, ok = QtGui.QInputDialog.getText(self, 'Add server', 'Name:')
        if ok:
            if len(name) < 1 or self._ServerList.getServerObject(name) != None:
                QtGui.QMessageBox.information(self, 'Error', "Invalid name or already used.")
                return
            
            sO = ServerObject()
            sO.name = unicode(name)
            
            # Insert into the model
            m = self.listView.model() 
            m.beginInsertRows(QtCore.QModelIndex(), m.rowCount(QtCore.QModelIndex()),m.rowCount(QtCore.QModelIndex())+1)
            self._ServerList.addServer(sO)
            m.endInsertRows()
            
            s = m.index(m.rowCount(QtCore.QModelIndex)-1,0) #Index of the newly added server
            self.listView.selectionModel().select(s, QtGui.QItemSelectionModel.ClearAndSelect) #Select it
            self.mapper.setCurrentIndex(m.rowCount(QtCore.QModelIndex)-1) # Update the mapper
            
    def deleteServer(self):
        """
        Delete a server from the model/list
        """
        re = QtGui.QMessageBox.question(self, 'Delete', 
                     "Are you sure?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if re == QtGui.QMessageBox.Yes:
            index = self.listView.selectionModel().currentIndex() #Currently selected
            
            self.listView.model().beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
            self._ServerList.deleteServerByIndex(index.row())
            self.listView.model().endRemoveRows()
            
            newIndex = self.listView.selectionModel().currentIndex()
            self.mapper.setCurrentIndex(newIndex.row())
            
    def saveServer(self):
        self._ServerList.writeServerList()        
    
    def saveCloseDialog(self):
        #Called when OK-button is clicked
        print "saveCloseDialog()"
    
if __name__ == "__main__":
    import logging
    from base.backend.ServerList import ServerList
    l = logging.getLogger("base")
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())
    app = QtGui.QApplication(sys.argv)
    s = ServerDialog(ServerList("c:/luma/","serverlist.xml"))
    s.show()
    sys.exit(app.exec_())
    
    