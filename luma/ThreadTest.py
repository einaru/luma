'''
Created on 15. feb. 2011

@author: Christian
'''
import threading
import time
from PyQt4.QtGui import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QCursor, QProgressBar
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import qApp

import sys

class qtThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        app.setOverrideCursor(Qt.WaitCursor)
        #s.setCursor(Qt.WaitCursor)
        time.sleep(2)
        #s.unsetCursor()
        app.restoreOverrideCursor()
        print "done"

class WorkerThreadTest(threading.Thread):
        
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        app.setOverrideCursor(Qt.WaitCursor)
        #s.setCursor(Qt.WaitCursor)
        time.sleep(2)
        #s.unsetCursor()
        app.restoreOverrideCursor()
        print "done"

t2 = qtThread()
app = QApplication(sys.argv)
s = QMainWindow()
bar = QProgressBar()

def lol():
    print "L O L"
    #t = WorkerThreadTest()
    #t.start()
    #t2 = qtThread()
    #t2.start()
    #bar.setRange(0,1)
    #time.sleep(4)
    while(1):
        pass
        #qApp.processEvents()
    print "R O F L"
        
if __name__ == "__main__":
    #app = QApplication(sys.argv)
    #s = QMainWindow()
    b = QPushButton("Click!")
    bar.setRange(0,0)
    #bar.setValue(50)
    l = QVBoxLayout()
    l.addWidget(bar)
    l.addWidget(b)
    w = QWidget()
    w.setLayout(l)
    s.setCentralWidget(w)
    #s.setCentralWidget(b)
    s.connect(b,QtCore.SIGNAL("clicked()"),lol)
    s.show()
    sys.exit(app.exec_())
    
