'''
Created on 15. mars 2011

@author: Simen
'''

from PyQt4.QtGui import QDialog, QPixmap
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from .AddObjectclassDialogDesign import Ui_AddObjectclassDialog 

class AddObjectclassDialog(QDialog, Ui_AddObjectclassDialog):
    
    def __init__(self, ocai, templateObject):
        QDialog.__init__(self)
        self.setupUi(self)
        
        self.ocai = ocai
        objectclassesList = templateObject.objectclasses
        list = []
        for objectclasses in self.ocai.getObjectClasses():
            if not objectclasses in objectclassesList:
                list.append(objectclasses)
        list.sort(key = str.lower)
        self.listWidgetObjectclasses.addItems(list)
        self.labelMainIcon.setPixmap(QPixmap(':/icons/64/objectclass'))