# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/debris/devel/git/luma/resources/forms/plugins/browser_plugin/BinaryEditorDesign.ui'
#
# Created: Thu May  5 17:00:03 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BinaryEditorDesign(object):
    def setupUi(self, BinaryEditorDesign):
        BinaryEditorDesign.setObjectName(_fromUtf8("BinaryEditorDesign"))
        BinaryEditorDesign.resize(602, 208)
        self.gridlayout = QtGui.QGridLayout(BinaryEditorDesign)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.iconLabel = QtGui.QLabel(BinaryEditorDesign)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconLabel.sizePolicy().hasHeightForWidth())
        self.iconLabel.setSizePolicy(sizePolicy)
        self.iconLabel.setMinimumSize(QtCore.QSize(64, 64))
        self.iconLabel.setWordWrap(False)
        self.iconLabel.setObjectName(_fromUtf8("iconLabel"))
        self.gridlayout.addWidget(self.iconLabel, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 201, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 1, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem1 = QtGui.QSpacerItem(390, 21, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.okButton = QtGui.QPushButton(BinaryEditorDesign)
        self.okButton.setDefault(True)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(BinaryEditorDesign)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.hboxlayout.addWidget(self.cancelButton)
        self.gridlayout.addLayout(self.hboxlayout, 3, 0, 1, 2)
        self.line2 = QtGui.QFrame(BinaryEditorDesign)
        self.line2.setFrameShape(QtGui.QFrame.HLine)
        self.line2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line2.setObjectName(_fromUtf8("line2"))
        self.gridlayout.addWidget(self.line2, 2, 0, 1, 2)
        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.fileButton = QtGui.QPushButton(BinaryEditorDesign)
        self.fileButton.setObjectName(_fromUtf8("fileButton"))
        self.gridlayout1.addWidget(self.fileButton, 2, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(21, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridlayout1.addItem(spacerItem2, 1, 1, 1, 1)
        self.valueEdit = QtGui.QLineEdit(BinaryEditorDesign)
        self.valueEdit.setObjectName(_fromUtf8("valueEdit"))
        self.gridlayout1.addWidget(self.valueEdit, 2, 1, 1, 1)
        self.attributeLabel = QtGui.QLabel(BinaryEditorDesign)
        self.attributeLabel.setWordWrap(False)
        self.attributeLabel.setObjectName(_fromUtf8("attributeLabel"))
        self.gridlayout1.addWidget(self.attributeLabel, 0, 0, 1, 3)
        spacerItem3 = QtGui.QSpacerItem(21, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem3, 4, 1, 1, 1)
        self.informationLabel = QtGui.QLabel(BinaryEditorDesign)
        self.informationLabel.setMinimumSize(QtCore.QSize(0, 30))
        self.informationLabel.setAlignment(QtCore.Qt.AlignVCenter)
        self.informationLabel.setWordWrap(True)
        self.informationLabel.setObjectName(_fromUtf8("informationLabel"))
        self.gridlayout1.addWidget(self.informationLabel, 3, 0, 1, 2)
        self.textLabel3 = QtGui.QLabel(BinaryEditorDesign)
        self.textLabel3.setWordWrap(False)
        self.textLabel3.setObjectName(_fromUtf8("textLabel3"))
        self.gridlayout1.addWidget(self.textLabel3, 2, 0, 1, 1)
        self.gridlayout.addLayout(self.gridlayout1, 0, 1, 2, 1)

        self.retranslateUi(BinaryEditorDesign)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), BinaryEditorDesign.accept)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), BinaryEditorDesign.reject)
        QtCore.QObject.connect(self.valueEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), BinaryEditorDesign.updateValue)
        QtCore.QObject.connect(self.fileButton, QtCore.SIGNAL(_fromUtf8("clicked()")), BinaryEditorDesign.showFileDialog)
        QtCore.QMetaObject.connectSlotsByName(BinaryEditorDesign)
        BinaryEditorDesign.setTabOrder(self.valueEdit, self.fileButton)
        BinaryEditorDesign.setTabOrder(self.fileButton, self.okButton)
        BinaryEditorDesign.setTabOrder(self.okButton, self.cancelButton)

    def retranslateUi(self, BinaryEditorDesign):
        BinaryEditorDesign.setWindowTitle(QtGui.QApplication.translate("BinaryEditorDesign", "Edit attribute", None, QtGui.QApplication.UnicodeUTF8))
        self.iconLabel.setText(QtGui.QApplication.translate("BinaryEditorDesign", "IT", "DO NOT TRANSLATE", QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("BinaryEditorDesign", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setShortcut(QtGui.QApplication.translate("BinaryEditorDesign", "Alt+O", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("BinaryEditorDesign", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setShortcut(QtGui.QApplication.translate("BinaryEditorDesign", "Alt+C", None, QtGui.QApplication.UnicodeUTF8))
        self.fileButton.setText(QtGui.QApplication.translate("BinaryEditorDesign", "F", "DO NOT TRANSLATE", QtGui.QApplication.UnicodeUTF8))
        self.attributeLabel.setText(QtGui.QApplication.translate("BinaryEditorDesign", "Please enter a file location from where to load binary data for the attribute <b>%1</b>.", None, QtGui.QApplication.UnicodeUTF8))
        self.informationLabel.setText(QtGui.QApplication.translate("BinaryEditorDesign", "IL", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel3.setText(QtGui.QApplication.translate("BinaryEditorDesign", "Location:", None, QtGui.QApplication.UnicodeUTF8))

