'''
Created on 2. feb. 2011

@author: Christian
'''
from PyQt4 import QtGui, QtCore, Qt
import sys
from PyQt4.QtGui import QDialog, QDataWidgetMapper, QStandardItemModel, QStandardItem, QItemSelectionRange
from base.gui.ServerDialogDesign import Ui_ServerDialogDesign
from base.models.ServerListModel import ServerListModel
from base.backend.ServerObject import ServerObject
from PyQt4.QtGui import QPixmap

class ServerDialog(QDialog, Ui_ServerDialogDesign):
    
    def __init__(self, serverList):
        """
        Note: the input-ServerList-object is used directly by both the methods here and the model so beware of changes to it.
        Don't pass a ServerList if one of its ServerObjects are in use.
        """
        
        QDialog.__init__(self)
        self.setupUi(self)
        
        p = QPixmap("D:\\Dropbox\\Git\\rep\\src\\share\\luma\\icons\\server.png")
        self.networkLabel.setPixmap(p)    
        
        self._ServerList = serverList
        slm = ServerListModel(self._ServerList)
        
        #self.tableView = QtGui.QTableView()
        #self.tableView.setModel(slm)
        #self.tableView.show()
        
        self.listView.setModel(slm)
        self.listView.setItemDelegate(BoxDelegate())
        #self.listView.setSelectionModel(self.tableView.selectionModel())
        
        self.mapper = QtGui.QDataWidgetMapper()
        
        self.mapper.setModel(slm)
        self.mapper.setItemDelegate(BoxDelegate())
        
        #self.mapper.addMapping(self.listView, 0)
        self.mapper.addMapping(self.hostLineEdit, 1)
        self.mapper.addMapping(self.portSpinBox, 2)
        self.mapper.addMapping(self.bindAnonBox, 3)
        self.mapper.addMapping(self.baseBox, 4)
        
        # OBS
        #self.mapper.addMapping(self.listWidget, 5)
        #self.mapper.addMapping(self.tableView, 5)
        #self.mapper.addMapping(self.testView, 5)
        
        self.mapper.addMapping(self.baseDNView, 5)
        #self.baseDNView = QtGui.QListView()
        #self.baseDNView.setModel(slm)
        #self.baseDNView.setModelColumn(5)

        
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
        m = self.listView.model()
        s = m.index(0,0)
        self.listView.selectionModel().select(s,QtGui.QItemSelectionModel.ClearAndSelect)

        
        #QtCore.QObject.connect(self.listView.selectionModel(),
        #                      QtCore.SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"), self.mapper,
        #                       QtCore.SLOT("setCurrentModelIndex(QModelIndex)"))
        #self.listView.clicked.connect(self.mapper.setCurrentModelIndex)
        self.listView.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex)

        #QtCore.QObject.connect(self.listView.selectionModel(),
        #                      QtCore.SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"), self.listBaseDNs)   
        self.removeBaseDN.setFocusPolicy(Qt.Qt.NoFocus)
        QtGui.QPushButton.connect(self.removeBaseDN, QtCore.SIGNAL("clicked()"), self.removeBaseDn)
    """
    TODO: Improve the handeling of baseDNs. Maybe set up a custom model which deals directly with the list.
    """
    """
    def listBaseDNs(self, index):
        
        self.addBaseDN.setEnabled(True)
        self.removeBaseDN.setEnabled(True)
        
        self.baseDNView.clear() #Slett gammel liste
        
        model = self.listView.model() #Modellen som gir data
        dnIndex = model.index(index.row(), 5) #Indeks til listen over baseDNs i modellen
        
        dnList = model.data(dnIndex) #Listen over baseDNs fra modellen
        self.baseDNView.addItems(dnList)     
        """
    def addBaseDn(self):
        if self.baseDNView.model() != None:
            m = self.baseDNView.model()
            m.insertRows(m.rowCount(),1, QtCore.QModelIndex())
            index = m.index(m.rowCount()-1,0)
            m.setData(index,QtCore.QVariant("<Fill inn to add>"))
        else:
            QtGui.QMessageBox.information(None, 'Error', self.tr("Choose a server first"))
        
        #index = self.baseDNView.selectionModel().selectedRows()[0]
       # m.removeRows(index.row(), 1, QtCore.QModelIndex())
        """
        dn, ok = QtGui.QInputDialog.getText(self, 'Add baseDN', 'Base DN:')
        
        if not ok:
            return
        
        if not len(self.baseDNView.findItems(dn, QtCore.Qt.MatchExactly)) < 1:
            QtGui.QMessageBox.information(None, 'Error', "Item already in list")
            return
            
        model = self.listView.model() #Modellen som gir data
        index = self.listView.selectedIndexes()[0]
        dnIndex = model.index(index.row(), 5)
        dnList = model.data(dnIndex) #Listen over baseDNs fra modellen
        dnList.append(dn)
        #self.emit(QtCore.SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"),dnIndex,dnIndex)
        self.listBaseDNs(index)
        """
    

    def removeBaseDn(self):
        if not len(self.baseDNView.selectedIndexes()) > 0:
            QtGui.QMessageBox.information(None, 'Error', "Nothing selected")
            return 
        row = self.baseDNView.selectedIndexes()[0].row()
        self.baseDNView.model().removeRow(row)
        
        
        """
        selectedIndex = self.baseDNView.selectedIndexes()[0]
        dn = selectedIndex.data().toPyObject()
        
        model = self.listView.model() #Modellen som gir data
        index = self.listView.selectedIndexes()[0]
        dnIndex = model.index(index.row(), 5)
        dnList = model.data(dnIndex) #Listen over baseDNs fra modellen
        dnList.remove(dn)
        
        self.listBaseDNs(index)
        """
        
    def addServer(self):
        print "addServer()"
        name, ok = QtGui.QInputDialog.getText(self, 'Add server', 'Name:')
        if ok:
            if len(name) < 1 or self._ServerList.getServerObject(name) != None:
                QtGui.QMessageBox.information(self, 'Error', "Invalid name or already used.")
                return
            sO = ServerObject()
            sO.name = name
            m = self.listView.model()
            m.beginInsertRows(QtCore.QModelIndex(), m.rowCount(QtCore.QModelIndex()),m.rowCount(QtCore.QModelIndex())+1)
            self._ServerList.addServer(sO)
            m.endInsertRows()
            s = m.index(m.rowCount(QtCore.QModelIndex)-1,0)
            #s = QtCore.QModelIndex(m.rowCount(QtCore.QModelIndex()))#QModelIndex som skal bli valgt
            self.listView.selectionModel().select(s,QtGui.QItemSelectionModel.ClearAndSelect)
            self.mapper.setCurrentIndex(m.rowCount(QtCore.QModelIndex)-1)
            
    def deleteServer(self):
        print "deleteServer()"  
        re = QtGui.QMessageBox.question(self, 'Delete', 
                     "Are you sure?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if re == QtGui.QMessageBox.Yes:
            index = self.listView.selectionModel().currentIndex()
            name = self.listView.model().data(index)
            m = self.listView.model()
            print index.row(),index.column()
            m.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
            #print index.data().toPyObject()
            self._ServerList.deleteServerByIndex(index.row())
            m.endRemoveRows()
            self.mapper.setCurrentIndex(0)
            
    def saveServer(self):
        print "saveServer()"
        self._ServerList.writeServerList()        
    
    def saveCloseDialog(self):
        #Called when OK-button is clicked
        print "saveCloseDialog()"
        
class loldelegate(QtGui.QStyledItemDelegate):
    def __init__(self):
        QtGui.QStyledItemDelegate.__init__(self)
        
    def setEditorData(self, editor, index):
        #QtGui.QItemDelegate.setEditorData(self, editor, index)
        print "setEditorData"
        #if editor.model() == None:
        #        editor.setModel(QtGui.QStringListModel())
        m = editor.model()
        m.setStringList(QtCore.QStringList(d))
        return
    
    def setModelData(self, editor, model, index):
        print "setModelData"
        QtGui.QStyledItemDelegate.setModelData(self, editor, model, index)
    
    
class BoxDelegate(QtGui.QStyledItemDelegate):
    """
    Maps QComboBoxes with set content (descriptions) to the model (saved as ints)
    """
    def __init__(self):
        QtGui.QStyledItemDelegate.__init__(self)
        
    def setEditorData(self, editor, index):
        if not index.isValid():
            return
          
        if index.column() == 5:
            #print "setEditorData"
            d = index.data().toPyObject()
            
            newList = []
            for x in d:
                x = x.trimmed() #QString
                if not len(x) == 0:
                    newList.append(x) 
            #stringModel = QtGui.QStringListModel(QtCore.QStringList(newList))
            #editor.setModel(stringModel)
            
            if editor.model() == None:
                editor.setModel(QtGui.QStringListModel(newList))
                return
            m = editor.model()
            print m
            m.setStringList(QtCore.QStringList(newList))
            return
        
        if editor.property("currentIndex").isValid(): #QComboBoxes has currentIndex
            editor.setProperty("currentIndex", index.data()) # just give it the data (the int)
            return
        QtGui.QStyledItemDelegate.setEditorData(self, editor, index) #if not, do as you always do
        
    def setModelData(self, editor, model, index):

        if index.column() == 5:
            #print "setModelData()"
            m = editor.model()
            d = []
            for i in xrange(m.rowCount()):
                d.append(m.data(m.index(i,0),QtCore.Qt.DisplayRole))
            model.setData(index,QtCore.QVariant(d))
            return 
        
        value = editor.property("currentIndex") #get the index and give it to the model
        if value.isValid():
            model.setData(index, value)
            return
        QtGui.QStyledItemDelegate.setModelData(self, editor, model, index)
        
    
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
    
    