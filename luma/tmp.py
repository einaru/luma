# -*- coding: utf-8 -*-
'''
Created on 2. feb. 2011

@author: Christian
'''

from plugins.browser_plugin.BrowserView import BrowserView
from PyQt4 import QtGui, QtCore
import sys, logging
from luma import LumaApp
import luma_rc


class W(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        
        self.layout = QtGui.QHBoxLayout(self)
        
        # Hvorfor er denne "stygg" (svart høyre halvdel)? Bare på Windows?
        x = QtGui.QProgressBar()
        x.setRange(0,0)
        self.layout.addWidget(x)
        
        # Hvis en gjør lengden på labelen mindre, så blir progressbaren penere. Har tydligvis noe å gjøre med
        # tilgjengelig plass....
        s = QtGui.QLabel("<------------ WTF?")
        self.layout.addWidget(s)
        
        #Hvis en bruker en vertikal-layout så er alt OK. (Sikkert pga. baren får all horisontal plass.)
        
        

if __name__ == "__main__":
    
    #app = LumaApp(sys.argv)
    app = QtGui.QApplication(sys.argv)
    
    l = logging.getLogger("")
    l.setLevel(logging.DEBUG)  
    
    # Log to the loggerwidget
    l.addHandler(logging.StreamHandler())
    
    b = BrowserView(None,"/tmp")
    b.show()
    
    w = W()
    w.show()
    
    #m.setData(index, "LOL")
    sys.exit(app.exec_())
    
    