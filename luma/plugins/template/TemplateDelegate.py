'''
Created on 16. mars 2011

@author: Simen
'''

from PyQt4.QtGui import  QStyledItemDelegate, QListWidgetItem

import copy

class TemplateDelegate(QStyledItemDelegate):
    """
    Maps QComboBoxes with set content (descriptions) to the model (ints),
    as well as populating a QListView with strings from a list (baseDNs).
    """
    
    def __init__(self):
        QStyledItemDelegate.__init__(self)
        
    def setEditorData(self, editor, index):
        """
        Specifies how the given editor should be filled out with the data from the model (at the index)
        """
        if not index.isValid():
            return
        
        # if BaseDNs
        if index.column() == 3:
            editor.model().resetAndFill() 
            return

        # if QComboBox, just set the index it should display (the strings displayed is in the .ui-file)
        if editor.property("currentIndex").isValid(): #QComboBoxes has currentIndex
            index.data().toString()
            i = editor.findText(index.data().toString)
            print i
            editor.setProperty("currentIndex", i) # just give it the data (the int)
            return
        
        # else - default
        QStyledItemDelegate.setEditorData(self, editor, index) #if not, do as you always do
        
    def setModelData(self, editor, model, index):
        """
        Specifies how the model should be filled out with data from the editor
        """
        # if the baseDNs
        if index.column() == 3:
            print "setModelData column = 3"
            return 
        
        # if a combobox
        value = editor.property("currentText") #get the index and give it to the model
        if value.isValid():
            model.setData(index, value)
            return
        
        # else - default
        QStyledItemDelegate.setModelData(self, editor, model, index)
        