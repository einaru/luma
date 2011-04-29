from PyQt4.QtGui import QDialog, QVBoxLayout
from .gui.NewEntryDialogDesign import Ui_Dialog
from AdvancedObjectWidget import AdvancedObjectWidget

class NewEntryDialog(QDialog, Ui_Dialog):

    def __init__(self, parentIndex, templateSmartObject = None, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)
        smartObject = AdvancedObjectWidget.smartObjectCopy(parentIndex.internalPointer().smartObject())
        x = AdvancedObjectWidget(smartObject, None, create=True)
        self.gridLayout.addWidget(x)
