'''
Created on 15. feb. 2011

@author: Christian
'''
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, QObject
from PyQt4.QtGui import QListWidgetItem, qApp, QDialog
from base.backend.LumaConnection import LumaConnection
from base.backend.ServerList import ServerList

class BrowseTest(QtGui.QWidget):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.list = QtGui.QListWidget()
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.addWidget(self.list)
        self.setLayout(self.hboxlayout)
        
    # SLOT
    def addItems(self, item):
        print "Fikk liste"
        item = item.toPyObject()
        print len(item)
        #print "addItems()"
        #import thread
        #print "add",thread.get_ident()
        #item = item.toPyObject()
        #self.list.setModel(item)
        #print item
        ok = QtGui.QMessageBox.question(self,"?","Fortsette? oO\nFikk "+str(len(item)),QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel)
        print ok
        if not ok == 1024:
            return
        x=0
        for i in item:
            x = x+1
            self.list.addItem(QListWidgetItem(str(i)+str(x)))
        #    if (x % 10000) == 0:
                #pass
        #        qApp.processEvents()
        #print "startprocess"
        #qApp.processEvents()
        #print "processed"
        #import time
        #time.sleep(0.2)
        #print "addItem finished"
    
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    b = BrowseTest()
    b.show()
    class qtThread(QtCore.QThread):
        def __init__(self):
            QtCore.QThread.__init__(self)
            self.i = 0
        
        def run(self):
            import ldap
            l = ldap.open("at.ntnu.no")
            l.protocol_version = ldap.VERSION3    
            baseDN = "dc=ntnu,dc=no"
            searchScope = ldap.SCOPE_SUBTREE
            retrieveAttributes = ["cn"] 
            searchFilter = "(objectClass=*)"
            ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
            result_set = []
            data = []
            while 1:
                #if len(data) > 10000:
                #    break
                result_type, result_data = l.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
            ## here you don't have to append to a list
            ## you could do whatever you want with the individual entry
            ## The appending to list is just for illustration. 
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        data.append(result_data)
                    #if len(data) > 100000:
                        #print "EMITTING Oo"
                        #print "data:",data
                        #for i in data:
                        #    self.emit(QtCore.SIGNAL('lol(QString)'),str(i))
                        #data = []
                        #import time
                        #time.sleep(5)
                        #qApp.processEvents()
                    #result_set.append(result_data)
                #print result_set
            #for i in data:
            print "FERDIG"
            #list = QtCore.QStringList()
            #for i in data:
            #    list.append(str(i))
            #data = QtGui.QStringListModel(list)
            self.emit(QtCore.SIGNAL('lol(QVariant)'),data)
    t = qtThread()
    QObject.connect(t, QtCore.SIGNAL('lol(QVariant)'),b.addItems)
    t.start()
    #lc = LumaConnection(ServerList("/tmp").getTable()[0])
    #print lc.getBaseDNList()
    sys.exit(app.exec_())