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
        
        restObjectclass = []
        for objectclass in tO.objectclasses:
            if not objectclass in dOc:
                restObjectclass.append(objectclass)
        
        rest, rest2 = ocai.getAllAttributes(restObjectclass)
        rest |= rest2
        remove, remove2 = ocai.getAllAttributes(dOc)
        remove |= remove2
        print remove
        for name in remove:
            if name in oldAttributes and not name in rest:
                a = oldAttributes[name]
                attributeTM.addRow(a.attributeName, a.must, a.single, a.binary, a.defaultValue, a.customMust)
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
