# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Dropbox\Git\it2901\resources\forms\WidgetPlusOkCancelDialog.ui'
#
# Created: Mon Mar 21 14:19:52 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NewEntryDialog(object):
    def setupUi(self, NewEntryDialog):
        NewEntryDialog.setObjectName(_fromUtf8("NewEntryDialog"))
        NewEntryDialog.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(NewEntryDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(NewEntryDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtGui.QDialogButtonBox(NewEntryDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(NewEntryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewEntryDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewEntryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewEntryDialog)

    def retranslateUi(self, NewEntryDialog):
        NewEntryDialog.setWindowTitle(QtGui.QApplication.translate("NewEntryDialog", "Add new entry", None, QtGui.QApplication.UnicodeUTF8))

