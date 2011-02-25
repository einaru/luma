'''
Created on 2. feb. 2011

@author: Christian
'''

from plugins.browser_plugin.BrowserView import BrowserView
from PyQt4 import QtGui, QtCore
import sys, logging
import luma_rc       
        
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    
    l = logging.getLogger("base")
    l.setLevel(logging.DEBUG)  
    
    # Log to the loggerwidget
    l.addHandler(logging.StreamHandler())
    
    b = BrowserView(None,"/tmp")
    b.show()

    splitter.show()
    #m.setData(index, "LOL")
    sys.exit(app.exec_())