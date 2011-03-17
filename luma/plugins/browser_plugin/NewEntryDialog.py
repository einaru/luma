
from base.gui.NewEntryDialogDesign import Ui_Dialog
from PyQt4 import QtGui

class NewEntryDialog(QtGui.QDialog, Ui_Dialog):

    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)