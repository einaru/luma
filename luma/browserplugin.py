import sys, gc
from PyQt4 import QtGui, QtCore

def getPluginWidget():
    x = QtGui.QWidget()
    for i in xrange(1000000):
        QtCore.QObject(x)
    return x

def addTabTo(x):
    #tmp = getPluginWidget()
    tmp = test()
    print "TMP-parent:",tmp.parent()
    x.addTab(tmp, "...")
    print "TMP-parent:",tmp.parent()

def removeTabFrom(x):
    rem = x.currentIndex()
    tmp = x.widget(0)
    #del tmp.model.rootItem
    print tmp
    print "TMP-parent:",tmp.parent()
    x.removeTab(0)
    tmp.setParent(None)
    print "TMP-parent:",tmp.parent()
    tmp.deleteLater()
    print "REM",rem
    if rem == 1:
        addTabTo(x)
    else:
        pass
        #gc.collect()
    
    
def test():
    from plugins.browser_plugin.BrowserView import BrowserView
    x = BrowserView(None,None)
    return x

def test2():
    from plugins import lolplugin
    return lolplugin.getPluginWidget(None, None)

def dest():
    print "dest"

def wait():
    raw_input("Waiting...")
    
def tabClose(i):
    x = QtCore.QObject.sender(QtGui.qApp)
    removeTabFrom(x)
    print "gar:",gc.garbage
    
if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    
    x = QtGui.QTabWidget()
    x.setTabsClosable(True)
    x.tabCloseRequested.connect(tabClose)
    print x.children()
    addTabTo(x)
    print x.children()
    #removeTabFrom(x)
    addTabTo(x)
    x.show()
    print x.children()
    
        
    sys.exit(app.exec_())