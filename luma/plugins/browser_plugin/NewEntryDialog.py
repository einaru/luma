from PyQt4.QtGui import QDialog
from base.gui.design.WidgetPlusOkCancelDialog import Ui_NewEntryDialog

class NewEntryDialog(QDialog, Ui_NewEntryDialog):

    def __init__(self, parentIndex, templateSmartObject = None, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)
