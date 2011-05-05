# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Skole\it2901\resources\forms\plugins\browser_plugin\StandardEditorDesign.ui'
#
# Created: Thu May 05 14:43:15 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_StandardEditorDesign(object):
    def setupUi(self, StandardEditorDesign):
        StandardEditorDesign.setObjectName(_fromUtf8("StandardEditorDesign"))
        StandardEditorDesign.resize(441, 216)
        self.gridlayout = QtGui.QGridLayout(StandardEditorDesign)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.iconLabel = QtGui.QLabel(StandardEditorDesign)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconLabel.sizePolicy().hasHeightForWidth())
        self.iconLabel.setSizePolicy(sizePolicy)
        self.iconLabel.setMinimumSize(QtCore.QSize(64, 64))
        self.iconLabel.setWordWrap(False)
        self.iconLabel.setObjectName(_fromUtf8("iconLabel"))
        self.gridlayout.addWidget(self.iconLabel, 0, 0, 1, 1)
        self.attributeLabel = QtGui.QLabel(StandardEditorDesign)
        self.attributeLabel.setWordWrap(False)
        self.attributeLabel.setObjectName(_fromUtf8("attributeLabel"))
        self.gridlayout.addWidget(self.attributeLabel, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(21, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridlayout.addItem(spacerItem, 1, 1, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem1 = QtGui.QSpacerItem(390, 21, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.okButton = QtGui.QPushButton(StandardEditorDesign)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(StandardEditorDesign)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.hboxlayout.addWidget(self.cancelButton)
        self.gridlayout.addLayout(self.hboxlayout, 5, 0, 1, 2)
        self.line2 = QtGui.QFrame(StandardEditorDesign)
        self.line2.setFrameShape(QtGui.QFrame.HLine)
        self.line2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line2.setObjectName(_fromUtf8("line2"))
        self.gridlayout.addWidget(self.line2, 4, 0, 1, 2)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.textLabel3 = QtGui.QLabel(StandardEditorDesign)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel3.sizePolicy().hasHeightForWidth())
        self.textLabel3.setSizePolicy(sizePolicy)
        self.textLabel3.setWordWrap(False)
        self.textLabel3.setObjectName(_fromUtf8("textLabel3"))
        self.hboxlayout1.addWidget(self.textLabel3)
        self.valueEdit = QtGui.QLineEdit(StandardEditorDesign)
        self.valueEdit.setObjectName(_fromUtf8("valueEdit"))
        self.hboxlayout1.addWidget(self.valueEdit)
        self.gridlayout.addLayout(self.hboxlayout1, 2, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 90, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem2, 2, 0, 2, 1)
        spacerItem3 = QtGui.QSpacerItem(21, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem3, 3, 1, 1, 1)

        self.retranslateUi(StandardEditorDesign)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), StandardEditorDesign.accept)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), StandardEditorDesign.reject)
        QtCore.QObject.connect(self.valueEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), StandardEditorDesign.updateValue)
        QtCore.QMetaObject.connectSlotsByName(StandardEditorDesign)
        StandardEditorDesign.setTabOrder(self.valueEdit, self.okButton)
        StandardEditorDesign.setTabOrder(self.okButton, self.cancelButton)

    def retranslateUi(self, StandardEditorDesign):
        StandardEditorDesign.setWindowTitle(QtGui.QApplication.translate("StandardEditorDesign", "Edit attribute", None, QtGui.QApplication.UnicodeUTF8))
        self.iconLabel.setText(QtGui.QApplication.translate("StandardEditorDesign", "IT", None, QtGui.QApplication.UnicodeUTF8))
        self.attributeLabel.setText(QtGui.QApplication.translate("StandardEditorDesign", "Please enter a new value for the attribute <b>%1</b>.", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("StandardEditorDesign", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setShortcut(QtGui.QApplication.translate("StandardEditorDesign", "Alt+O", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("StandardEditorDesign", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setShortcut(QtGui.QApplication.translate("StandardEditorDesign", "Alt+C", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel3.setText(QtGui.QApplication.translate("StandardEditorDesign", "Value:", None, QtGui.QApplication.UnicodeUTF8))

