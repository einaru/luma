'''
Created on 15. mars 2011

@author: Simen
'''

from PyQt4.QtGui import QDialog
from .AddAttributeDialogDesign import Ui_AddAttributeDialog
from ..model.AttributeTableModel import AttributeTableModel 

class AddAttributeDialog(QDialog, Ui_AddAttributeDialog):
    
    def __init__(self, ocai, templateObject):
        QDialog.__init__(self)
        self.setupUi(self)
        self.attributeTM = AttributeTableModel()
        self.tableView.setModel(self.attributeTM)
        self.ocai = ocai
        objectclassesList = templateObject.objectclasses
        attributeNameList = self.ocai.getAllMays(objectclassesList)
        
        for name in attributeNameList:
            if not name in templateObject.attributes.keys():
                single = self.ocai.isSingle(name)
                binary = self.ocai.isBinary(name)
                self.attributeTM.addRow(name, False, single, binary, "", False)
            
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()