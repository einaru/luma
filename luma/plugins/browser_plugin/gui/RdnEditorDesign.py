# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/debris/devel/git/luma/resources/forms/plugins/browser_plugin/RdnEditorDesign.ui'
#
# Created: Thu May  5 00:01:02 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RdnEditorDesign(object):
    def setupUi(self, RdnEditorDesign):
        RdnEditorDesign.setObjectName(_fromUtf8("RdnEditorDesign"))
        RdnEditorDesign.resize(436, 268)
        self.gridlayout = QtGui.QGridLayout(RdnEditorDesign)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.iconLabel = QtGui.QLabel(RdnEditorDesign)
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
        self.gridlayout.addItem(spacerItem, 1, 0, 5, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem1 = QtGui.QSpacerItem(390, 21, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.okButton = QtGui.QPushButton(RdnEditorDesign)
        self.okButton.setDefault(True)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(RdnEditorDesign)
        self.cancelButton.setDefault(False)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.hboxlayout.addWidget(self.cancelButton)
        self.gridlayout.addLayout(self.hboxlayout, 7, 0, 1, 3)
        self.line2 = QtGui.QFrame(RdnEditorDesign)
        self.line2.setFrameShape(QtGui.QFrame.HLine)
        self.line2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line2.setObjectName(_fromUtf8("line2"))
        self.gridlayout.addWidget(self.line2, 6, 0, 1, 3)
        self.textLabel3 = QtGui.QLabel(RdnEditorDesign)
        self.textLabel3.setWordWrap(False)
        self.textLabel3.setObjectName(_fromUtf8("textLabel3"))
        self.gridlayout.addWidget(self.textLabel3, 3, 1, 1, 1)
        self.textLabel2 = QtGui.QLabel(RdnEditorDesign)
        self.textLabel2.setWordWrap(False)
        self.textLabel2.setObjectName(_fromUtf8("textLabel2"))
        self.gridlayout.addWidget(self.textLabel2, 4, 1, 1, 1)
        self.attributeLabel = QtGui.QLabel(RdnEditorDesign)
        self.attributeLabel.setAlignment(QtCore.Qt.AlignVCenter)
        self.attributeLabel.setWordWrap(True)
        self.attributeLabel.setObjectName(_fromUtf8("attributeLabel"))
        self.gridlayout.addWidget(self.attributeLabel, 0, 1, 1, 2)
        self.attributeBox = QtGui.QComboBox(RdnEditorDesign)
        self.attributeBox.setObjectName(_fromUtf8("attributeBox"))
        self.gridlayout.addWidget(self.attributeBox, 2, 2, 1, 1)
        self.valueEdit = QtGui.QLineEdit(RdnEditorDesign)
        self.valueEdit.setObjectName(_fromUtf8("valueEdit"))
        self.gridlayout.addWidget(self.valueEdit, 3, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridlayout.addItem(spacerItem2, 1, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(21, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem3, 5, 2, 1, 1)
        self.dnLabel = QtGui.QLabel(RdnEditorDesign)
        self.dnLabel.setText(_fromUtf8(""))
        self.dnLabel.setWordWrap(False)
        self.dnLabel.setObjectName(_fromUtf8("dnLabel"))
        self.gridlayout.addWidget(self.dnLabel, 4, 2, 1, 1)
        self.textLabel1 = QtGui.QLabel(RdnEditorDesign)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName(_fromUtf8("textLabel1"))
        self.gridlayout.addWidget(self.textLabel1, 2, 1, 1, 1)

        self.retranslateUi(RdnEditorDesign)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), RdnEditorDesign.accept)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), RdnEditorDesign.reject)
        QtCore.QObject.connect(self.valueEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), RdnEditorDesign.updateValue)
        QtCore.QObject.connect(self.attributeBox, QtCore.SIGNAL(_fromUtf8("activated(QString)")), RdnEditorDesign.updateValue)
        QtCore.QMetaObject.connectSlotsByName(RdnEditorDesign)
        RdnEditorDesign.setTabOrder(self.valueEdit, self.okButton)
        RdnEditorDesign.setTabOrder(self.okButton, self.cancelButton)

    def retranslateUi(self, RdnEditorDesign):
        RdnEditorDesign.setWindowTitle(QtGui.QApplication.translate("RdnEditorDesign", "Edit DN", None, QtGui.QApplication.UnicodeUTF8))
        self.iconLabel.setText(QtGui.QApplication.translate("RdnEditorDesign", "IT", "DO NOT TRANSLATE", QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("RdnEditorDesign", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setShortcut(QtGui.QApplication.translate("RdnEditorDesign", "Alt+O", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("RdnEditorDesign", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setShortcut(QtGui.QApplication.translate("RdnEditorDesign", "Alt+C", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel3.setText(QtGui.QApplication.translate("RdnEditorDesign", "Value:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel2.setText(QtGui.QApplication.translate("RdnEditorDesign", "DN:", None, QtGui.QApplication.UnicodeUTF8))
        self.attributeLabel.setText(QtGui.QApplication.translate("RdnEditorDesign", "Please choose an attribute and enter a value for it. These values will be part of distinguished name for the new object.", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setText(QtGui.QApplication.translate("RdnEditorDesign", "Attribute:", None, QtGui.QApplication.UnicodeUTF8))

