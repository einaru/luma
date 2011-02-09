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
        """
        Specifies how the given editor should be filled out with the data from the model (at the index)
        """
        
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
                    newList.append(unicode(x)) 
           
            # the view (editor) is a QListView in this case, so lets give it a model to display
            if editor.model() == None:
                editor.setModel(QStringListModel(newList))
                return
            m = editor.model()
            m.setStringList(QStringList(newList))
            return
        
        # if QComboBox, just set the index it should display (the strings displayed is in the .ui-file)
        if editor.property("currentIndex").isValid(): #QComboBoxes has currentIndex
            editor.setProperty("currentIndex", index.data()) # just give it the data (the int)
            return
        
        # else - default
        QStyledItemDelegate.setEditorData(self, editor, index) #if not, do as you always do
        
    def setModelData(self, editor, model, index):
        """
        Specifies how the model should be filled out with data from the editor
        """
    
        # if the baseDNs
        if index.column() == 5:
            
            # get strings from the model of the QListView displaying the baseDNs
            m = editor.model()
            
            # Populate the list again
            d = []
            for i in xrange(m.rowCount()):
                data = m.data(m.index(i,0), Qt.DisplayRole)
                d.append(data)
            
            # now that we have constructed the list, give it to the model
            model.setData(index,QVariant(d))
            return 
        
        # if a combobox
        value = editor.property("currentIndex") #get the index and give it to the model
        if value.isValid():
            model.setData(index, value)
            return
        
        # else - default
        QStyledItemDelegate.setModelData(self, editor, model, index)
        