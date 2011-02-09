'''
Created on 2. feb. 2011

@author: Christian
'''

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtGui import QDialog, QPixmap, QDataWidgetMapper, QStandardItemModel, QStandardItem, QItemSelectionRange
from base.gui.ServerDialogDesign import Ui_ServerDialogDesign
from base.models.ServerListModel import ServerListModel
from base.backend.ServerObject import ServerObject
from PyQt4.QtCore import QModelIndex
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
        
        if slm.rowCount(QModelIndex()) > 0:
            self.serverWidget.setEnabled(True)
            
        
        # Select the first server in the list
        index = self.listView.model().index(0,0)
        self.listView.selectionModel().select(index, QtGui.QItemSelectionModel.ClearAndSelect) 
        self.listView.selectionModel().setCurrentIndex(index, QtGui.QItemSelectionModel.ClearAndSelect)       
        
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
        self.mapper.addMapping(self.baseDNWidget, 5)
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
        self.deleteBaseDNButton.setFocusPolicy(Qt.Qt.NoFocus)
        
    """
    def manageBaseDn(self):

        d = BaseSelector()
        d.exec_()
        print d.getList()
    """
    
    def addBaseDN(self):
        tmpBase = unicode(self.baseEdit.text()).strip()
        if tmpBase == u"":
            return      
        self.baseDNWidget.addItem(QtGui.QListWidgetItem(tmpBase))
        self.baseEdit.clear()
        self.mapper.submit()
    
    def deleteBaseDN(self):
        for tmpItem in self.baseDNWidget.selectedItems():
            if not (None == tmpItem):
                index = self.baseDNWidget.indexFromItem(tmpItem)
                d = self.baseDNWidget.takeItem(index.row())
                if d != 0:
                    del d
        self.mapper.submit()

    def addServer(self):
        """
        Create a new ServerObject and add it to the model (thus the list)
        """
        name, ok = QtGui.QInputDialog.getText(self, 'Add server', 'Name:')
        if ok:
            if len(name) < 1 or self._ServerList.getServerObject(name) != None:
                QtGui.QMessageBox.information(self, 'Error', "Invalid name or already used.")
                return
            
            self.serverWidget.setEnabled(True)
            
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
            self.listView.model().removeRows(index.row(),1)
            self.listView.model().endRemoveRows()
            
            newIndex = self.listView.selectionModel().currentIndex()
            self.mapper.setCurrentIndex(newIndex.row())
            
    def saveServer(self):
        self._ServerList.writeServerList()        
    
    def saveCloseDialog(self):
        #Called when OK-button is clicked
        print self._ServerList.getTable()[0]
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
    
    