from PyQt4.QtGui import QWidget
from LoggerWidgetDesign import Ui_LoggerWidgetDesign

class LoggerWidget(QWidget, Ui_LoggerWidgetDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent)

        self.setupUi(self)
        
        self.parent = parent
        
        self.logObjectList = []
        
    def clearLogger(self):
        pass