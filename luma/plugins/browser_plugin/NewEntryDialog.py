from PyQt4.QtGui import QDialog, QVBoxLayout
from .gui.NewEntryDialogDesign import Ui_Dialog
from AdvancedObjectWidget import AdvancedObjectWidget

class NewEntryDialog(QDialog, Ui_Dialog):

    def __init__(self, parentIndex, templateSmartObject = None, parent=None, entryTemplate = None):
        QDialog.__init__(self)
        self.setupUi(self)
        if templateSmartObject:
            smartObject = templateSmartObject 
        else:
            smartObject = AdvancedObjectWidget.smartObjectCopy(parentIndex.internalPointer().smartObject())
        self.objectWidget = AdvancedObjectWidget(smartObject, None, create=True, entryTemplate = entryTemplate)
        self.gridLayout.addWidget(self.objectWidget)

    def accept(self):
        if self.objectWidget.saveObject():
            super(NewEntryDialog, self).accept()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
