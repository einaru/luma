from PyQt4.QtGui import QStyledItemDelegate, QStringListModel
from PyQt4.QtCore import QStringList, QVariant
from PyQt4.QtCore import Qt

class ServerDelegate(QStyledItemDelegate):
    """
    Maps QComboBoxes with set content (descriptions) to the model (ints),
    as well as populating a QListView with strings from a list (baseDNs).
    """
    
    def __init__(self):
        QStyledItemDelegate.__init__(self)
        
    def setEditorData(self, editor, index):
        
        if not index.isValid():
            return
        
        # if BaseDNs
        if index.column() == 5:
            
            # List of strings
            d = index.data().toPyObject()
            
            # Get rid of empty strings
            newList = []
            for x in d:
                x = x.trimmed() #QString
                if not len(x) == 0:
                    newList.append(x) 
           
            if editor.model() == None:
                editor.setModel(QStringListModel(newList))
                return
            
            m = editor.model()
            m.setStringList(QStringList(newList))
            return
        
        # if QComboBox
        if editor.property("currentIndex").isValid(): #QComboBoxes has currentIndex
            editor.setProperty("currentIndex", index.data()) # just give it the data (the int)
            return
        
        # else - default
        QStyledItemDelegate.setEditorData(self, editor, index) #if not, do as you always do
        
    def setModelData(self, editor, model, index):

        # if the baseDNs
        if index.column() == 5:
            m = editor.model()
            
            # Populate the list again
            d = []
            for i in xrange(m.rowCount()):
                d.append(m.data(m.index(i,0), Qt.DisplayRole))
            model.setData(index,QVariant(d))
            return 
        
        # if a combobox
        value = editor.property("currentIndex") #get the index and give it to the model
        if value.isValid():
            model.setData(index, value)
            return
        
        # else - default
        QStyledItemDelegate.setModelData(self, editor, model, index)
        