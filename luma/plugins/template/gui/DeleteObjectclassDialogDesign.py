# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Skole\it2901\resources\forms\plugins\template\DeleteObjectclassDialogDesign.ui'
#
# Created: Thu May 05 14:02:44 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AddAttributeDialog(object):
    def setupUi(self, AddAttributeDialog):
        AddAttributeDialog.setObjectName(_fromUtf8("AddAttributeDialog"))
        AddAttributeDialog.resize(452, 288)
        self.gridLayout_2 = QtGui.QGridLayout(AddAttributeDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButtonNo = QtGui.QPushButton(AddAttributeDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonNo.sizePolicy().hasHeightForWidth())
        self.pushButtonNo.setSizePolicy(sizePolicy)
        self.pushButtonNo.setObjectName(_fromUtf8("pushButtonNo"))
        self.gridLayout_2.addWidget(self.pushButtonNo, 4, 3, 1, 1)
        self.pushButtonYes = QtGui.QPushButton(AddAttributeDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonYes.sizePolicy().hasHeightForWidth())
        self.pushButtonYes.setSizePolicy(sizePolicy)
        self.pushButtonYes.setObjectName(_fromUtf8("pushButtonYes"))
        self.gridLayout_2.addWidget(self.pushButtonYes, 4, 2, 1, 1)
        self.line = QtGui.QFrame(AddAttributeDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 3, 0, 1, 4)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 2)
        self.line_2 = QtGui.QFrame(AddAttributeDialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_2.addWidget(self.line_2, 1, 0, 1, 4)
        self.labelMainIcon = QtGui.QLabel(AddAttributeDialog)
        self.labelMainIcon.setText(_fromUtf8(""))
        self.labelMainIcon.setObjectName(_fromUtf8("labelMainIcon"))
        self.gridLayout_2.addWidget(self.labelMainIcon, 0, 0, 1, 1)
        self.labelMain = QtGui.QLabel(AddAttributeDialog)
        self.labelMain.setWordWrap(True)
        self.labelMain.setObjectName(_fromUtf8("labelMain"))
        self.gridLayout_2.addWidget(self.labelMain, 0, 1, 1, 3)
        self.tableView = QtGui.QTableView(AddAttributeDialog)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setShowGrid(False)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.tableView, 2, 0, 1, 4)

        self.retranslateUi(AddAttributeDialog)
        QtCore.QObject.connect(self.pushButtonNo, QtCore.SIGNAL(_fromUtf8("clicked()")), AddAttributeDialog.reject)
        QtCore.QObject.connect(self.pushButtonYes, QtCore.SIGNAL(_fromUtf8("clicked()")), AddAttributeDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AddAttributeDialog)
        AddAttributeDialog.setTabOrder(self.pushButtonYes, self.pushButtonNo)
        AddAttributeDialog.setTabOrder(self.pushButtonNo, self.tableView)

    def retranslateUi(self, AddAttributeDialog):
        AddAttributeDialog.setWindowTitle(QtGui.QApplication.translate("AddAttributeDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNo.setText(QtGui.QApplication.translate("AddAttributeDialog", "No", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonYes.setText(QtGui.QApplication.translate("AddAttributeDialog", "Yes", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMain.setText(QtGui.QApplication.translate("AddAttributeDialog", "Warning: The following attributes will be removed when deleting all selected objectclasses. Do you want to continue?", None, QtGui.QApplication.UnicodeUTF8))

