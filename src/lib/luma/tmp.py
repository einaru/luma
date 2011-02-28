'''
Created on 2. feb. 2011

@author: Christian
'''

from PyQt4 import QtGui, QtCore
import sys

class TestModel(QtCore.QAbstractTableModel):
    
    def __init__ (self):
        QtCore.QAbstractTableModel.__init__(self)
        self.i = [[0,1,2],[1,2,3],[2,3,4]]
        
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        print "setData"
        #QtCore.QAbstractTableModel.setData(self, index, value, role)
        row = index.row()
        column = index.column()
        self.i[row][column] = value
        self.emit(QtCore.SIGNAL("dataChanged( const QModelIndex&, const QModelIndex& )"), index, index)
        return True
        
    def rowCount(self,parent):
        return 3
    
    def columnCount(self,parent):
        return 3
    
    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
    
    def data(self,index,role):
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.i[row][column]
       
        
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    
    splitter = QtGui.QSplitter()
    
    m = TestModel()
    index = m.index(0, 0)
    
    v = QtGui.QTableView(splitter)
    v.setModel(m)
    
    x = QtGui.QTreeView(splitter)
    x.setModel(m)

    splitter.show()
    #m.setData(index, "LOL")
    sys.exit(app.exec_())