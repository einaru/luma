
from PyQt4 import QtCore, QtGui

class Model(QtCore.QAbstractListModel):
    
    def __init__(self):
        QtCore.QAbstractTableModel.__init__(self)
        self.table = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        self.i = 0
        
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        value = QtCore.QVariant.toPyObject(value)
        print "setData:",value
        
        row = index.row()
        self.table[row] = value
            
        self.emit(QtCore.SIGNAL("dataChanged( const QModelIndex&, const QModelIndex& )"), index, index)
        return True
        
    def rowCount(self,parent):
        return 5
    
    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
    
    def data(self,index,role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            row = index.row()
            self.i = self.i + 1
            print self.i
            return self.table[row]
            
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    
    m = Model()
    
    view = QtGui.QListView()
    view.setModel(m)
    view.show()
    
    view2 = QtGui.QTableView()
    view2.setModel(m)
    
    view.show()
    view2.show()
    sys.exit(app.exec_())
    
