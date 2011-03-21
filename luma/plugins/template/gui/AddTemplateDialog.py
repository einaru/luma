'''
Created on 18. mars 2011

@author: Simen
'''
from PyQt4.QtGui import QDialog
from .AddTemplateDialogDesign import Ui_AddTemplateDialog

class AddTemplateDialog(QDialog, Ui_AddTemplateDialog):
    
    def __init__(self, serverList):
        QDialog.__init__(self)
        self.setupUi(self)
        
        i = 0
        for server in serverList.getTable():
            self.comboBoxServer.insertItem(i, server.name)