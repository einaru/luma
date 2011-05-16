# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/einar/Desktop/luma-merging/resources/forms/plugins/template/AddObjectclassDialogDesign.ui'
#
# Created: Mon May 16 02:47:11 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AddObjectclassDialog(object):
    def setupUi(self, AddObjectclassDialog):
        AddObjectclassDialog.setObjectName(_fromUtf8("AddObjectclassDialog"))
        AddObjectclassDialog.resize(500, 300)
        self.gridLayout = QtGui.QGridLayout(AddObjectclassDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelMain = QtGui.QLabel(AddObjectclassDialog)
        self.labelMain.setWordWrap(True)
        self.labelMain.setObjectName(_fromUtf8("labelMain"))
        self.gridLayout.addWidget(self.labelMain, 0, 1, 1, 3)
        self.pushButtonCancel = QtGui.QPushButton(AddObjectclassDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonCancel.sizePolicy().hasHeightForWidth())
        self.pushButtonCancel.setSizePolicy(sizePolicy)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.gridLayout.addWidget(self.pushButtonCancel, 5, 3, 1, 1)
        self.pushButtonOk = QtGui.QPushButton(AddObjectclassDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonOk.sizePolicy().hasHeightForWidth())
        self.pushButtonOk.setSizePolicy(sizePolicy)
        self.pushButtonOk.setObjectName(_fromUtf8("pushButtonOk"))
        self.gridLayout.addWidget(self.pushButtonOk, 5, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 2)
        self.labelMainIcon = QtGui.QLabel(AddObjectclassDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMainIcon.sizePolicy().hasHeightForWidth())
        self.labelMainIcon.setSizePolicy(sizePolicy)
        self.labelMainIcon.setMinimumSize(QtCore.QSize(64, 64))
        self.labelMainIcon.setText(_fromUtf8(""))
        self.labelMainIcon.setObjectName(_fromUtf8("labelMainIcon"))
        self.gridLayout.addWidget(self.labelMainIcon, 0, 0, 1, 1)
        self.line = QtGui.QFrame(AddObjectclassDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 4, 0, 1, 4)
        self.line_2 = QtGui.QFrame(AddObjectclassDialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 1, 0, 1, 4)
        self.listWidgetObjectclasses = QtGui.QListWidget(AddObjectclassDialog)
        self.listWidgetObjectclasses.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidgetObjectclasses.setObjectName(_fromUtf8("listWidgetObjectclasses"))
        self.gridLayout.addWidget(self.listWidgetObjectclasses, 3, 0, 1, 4)

        self.retranslateUi(AddObjectclassDialog)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), AddObjectclassDialog.reject)
        QtCore.QObject.connect(self.pushButtonOk, QtCore.SIGNAL(_fromUtf8("clicked()")), AddObjectclassDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AddObjectclassDialog)
        AddObjectclassDialog.setTabOrder(self.pushButtonOk, self.pushButtonCancel)
        AddObjectclassDialog.setTabOrder(self.pushButtonCancel, self.listWidgetObjectclasses)

    def retranslateUi(self, AddObjectclassDialog):
        AddObjectclassDialog.setWindowTitle(QtGui.QApplication.translate("AddObjectclassDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMain.setText(QtGui.QApplication.translate("AddObjectclassDialog", "Please choose the objectclass you want to add to the template.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel.setText(QtGui.QApplication.translate("AddObjectclassDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOk.setText(QtGui.QApplication.translate("AddObjectclassDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))

