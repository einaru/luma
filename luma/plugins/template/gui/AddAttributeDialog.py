'''
Created on 15. mars 2011

@author: Simen
'''

from PyQt4.QtGui import QDialog
from .AddAttributeDialogDesign import Ui_AddAttributeDialog 

class AddAttributeDialog(QDialog, Ui_AddAttributeDialog):
    
    def __init__(self, ocai, templateObject):
        QDialog.__init__(self)
        self.setupUi(self)
        
        self.ocai = ocai
        objectclassesList = templateObject.objectclasses
        list = self.ocai.getAllAttributes(objectclassesList)
        #self.listWidgetObjectclasses.addItems(list)
        print list