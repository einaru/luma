'''
Created on 18. mars 2011

@author: Simen
'''
from PyQt4.QtGui import QDialog
from .AddTemplateDialogDesign import Ui_AddTemplateDialog

class AddTemplateDialog(QDialog, Ui_AddTemplateDialog):
    
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)