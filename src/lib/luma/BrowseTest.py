'''
Created on 15. feb. 2011

@author: Christian
'''
from PyQt4 import QtGui
from base.backend.LumaConnection import LumaConnection
from base.backend.ServerList import ServerList

class BrowseTest(QtGui.QWidget):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.list = QtGui.QListWidget()
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.addWidget(self.list)
        self.setLayout(self.hboxlayout)
    
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    b = BrowseTest()
    b.show()
    lc = LumaConnection(ServerList("/tmp").getTable()[0])
    print lc.getBaseDNList()
    sys.exit(app.exec_())