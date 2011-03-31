from PyQt4.QtGui import QDialog
from NewEntryDialogDesign import Ui_Dialog

class NewEntryDialog(QDialog, Ui_Dialog):

    def __init__(self, parentIndex, templateSmartObject = None, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)
