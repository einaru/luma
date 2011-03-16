'''
Created on 16. mars 2011

@author: Simen
'''

from PyQt4.QtCore import QAbstractTableModel

class ObjectclassTableModel(QAbstractTableModel):
    
    def __init__(self, templateList, parent = None):
        QAbstractTableModel.__init__(self)
        self._templateList = templateList