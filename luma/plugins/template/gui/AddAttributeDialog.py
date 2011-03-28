'''
Created on 15. mars 2011

@author: Simen
'''

from PyQt4.QtGui import QDialog
from .AddAttributeDialogDesign import Ui_AddAttributeDialog 

class AddAttributeDialog(QDialog, Ui_AddAttributeDialog):
    
    def __init__(self, serverMeta):
        QDialog.__init__(self)
        self.setupUi(self)