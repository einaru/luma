'''
Created on 15. mars 2011

@author: Simen
'''

from PyQt4.QtGui import QDialog
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from .AddObjectclassDialogDesign import Ui_AddObjectclassDialog 

class AddObjectclassDialog(QDialog, Ui_AddObjectclassDialog):
    
    def __init__(self, serverMeta):
        QDialog.__init__(self)
        self.setupUi(self)
        
        self.serverMeta = serverMeta
        list = self.getObjectclassList()
        
        self.listWidgetObjectclasses.addItems(list)
        
        
    def getObjectclassList(self):
        ocai = ObjectClassAttributeInfo(self.serverMeta)
        return ocai.getObjectClasses()