'''
Created on 15. mars 2011

@author: Simen
'''

from PyQt4.QtGui import QDialog
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from .AddObjectclassDialogDesign import Ui_AddObjectclassDialog 

class AddObjectclassDialog(QDialog, Ui_AddObjectclassDialog):
    
    def __init__(self, ocai):
        QDialog.__init__(self)
        self.setupUi(self)
        
        self.ocai = ocai
        list = self.ocai.getObjectClasses()
        list.sort(key = str.lower)
        self.listWidgetObjectclasses.addItems(list)
        