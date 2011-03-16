'''
Created on 15. mars 2011

@author: Simen
'''

from PyQt4.QtGui import QDialog
from AddObjectclassDialogDesign import Ui_AddObjectclassDialog 

class AddObjectclassDialog(QDialog, Ui_AddObjectclassDialog):
    
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)