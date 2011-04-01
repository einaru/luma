# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/debris/devel/git/luma/resources/forms/WidgetPlusOkCancelDialog.ui'
#
# Created: Fri Apr  1 20:41:51 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NewEntryDialog(object):
    def setupUi(self, NewEntryDialog):
        NewEntryDialog.setObjectName("NewEntryDialog")
        NewEntryDialog.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(NewEntryDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtGui.QWidget(NewEntryDialog)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtGui.QDialogButtonBox(NewEntryDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(NewEntryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewEntryDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewEntryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewEntryDialog)

    def retranslateUi(self, NewEntryDialog):
        NewEntryDialog.setWindowTitle(QtGui.QApplication.translate("NewEntryDialog", "Add new entry", None, QtGui.QApplication.UnicodeUTF8))

