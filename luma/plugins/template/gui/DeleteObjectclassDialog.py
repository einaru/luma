'''
Created on 7. apr. 2011

@author: Simen
'''

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QModelIndex 
from .DeleteObjectclassDialogDesign import Ui_AddAttributeDialog
from ..model.AttributeTableModel import AttributeTableModel

class DeleteObjectclassDialog(QDialog, Ui_AddAttributeDialog):

    def __init__(self, ocai, tO, dOc, oldAttributes):
        QDialog.__init__(self)
        self.setupUi(self)
        attributeTM = AttributeTableModel()
        self.tableView.setModel(attributeTM)
        
        dOc = map(QModelIndex.internalPointer, dOc)
        
        must, may = ocai.getAllAttributes(dOc)
        for name in must:
            if name in oldAttributes:
                a = oldAttributes[name]
                attributeTM.addRow(a.attributeName, a.must, a.single, a.binary, a.defaultValue, a.customMust)
            
        for name in may:
            if name in oldAttributes:
                a = oldAttributes[name]
                attributeTM.addRow(a.attributeName, a.must, a.single, a.binary, a.defaultValue, a.customMust)