from PyQt4.QtGui import QDialog, QVBoxLayout
from .gui.NewEntryDialogDesign import Ui_Dialog
from AdvancedObjectWidget import AdvancedObjectWidget
from base.backend.SmartDataObject import SmartDataObject

class NewEntryDialog(QDialog, Ui_Dialog):

    def __init__(self, parentIndex, templateSmartObject = None, parent=None, entryTemplate = None):
        QDialog.__init__(self)
        self.setupUi(self)
        if templateSmartObject:
            smartObject = templateSmartObject 
        else:
            smartO = parentIndex.internalPointer().smartObject()
            serverMeta = smartO.getServerMeta()
            baseDN = smartO.getDN()
            data = {}
            smartObject = AdvancedObjectWidget.smartObjectCopy(SmartDataObject((baseDN, data), serverMeta))
        self.objectWidget = AdvancedObjectWidget(None, entryTemplate = entryTemplate)
        self.objectWidget.initModel(smartObject, create=True)
        self.gridLayout.addWidget(self.objectWidget)

    def accept(self):
        if self.objectWidget.saveObject():
            super(NewEntryDialog, self).accept()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
