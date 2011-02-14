# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoggerWidgetDesign.ui'
#
# Created: Mon Feb 14 17:28:20 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LoggerWidgetDesign(object):
    def setupUi(self, LoggerWidgetDesign):
        LoggerWidgetDesign.setObjectName(_fromUtf8("LoggerWidgetDesign"))
        LoggerWidgetDesign.resize(516, 217)
        self.vboxlayout = QtGui.QVBoxLayout(LoggerWidgetDesign)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.messageEdit = QtGui.QTextEdit(LoggerWidgetDesign)
        self.messageEdit.setReadOnly(True)
        self.messageEdit.setObjectName(_fromUtf8("messageEdit"))
        self.vboxlayout.addWidget(self.messageEdit)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.textLabel1 = QtGui.QLabel(LoggerWidgetDesign)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName(_fromUtf8("textLabel1"))
        self.hboxlayout.addWidget(self.textLabel1)
        self.errorBox = QtGui.QCheckBox(LoggerWidgetDesign)
        self.errorBox.setChecked(True)
        self.errorBox.setObjectName(_fromUtf8("errorBox"))
        self.hboxlayout.addWidget(self.errorBox)
        self.debugBox = QtGui.QCheckBox(LoggerWidgetDesign)
        self.debugBox.setChecked(True)
        self.debugBox.setObjectName(_fromUtf8("debugBox"))
        self.hboxlayout.addWidget(self.debugBox)
        self.infoBox = QtGui.QCheckBox(LoggerWidgetDesign)
        self.infoBox.setChecked(True)
        self.infoBox.setObjectName(_fromUtf8("infoBox"))
        self.hboxlayout.addWidget(self.infoBox)
        spacerItem = QtGui.QSpacerItem(141, 21, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.clearButton = QtGui.QToolButton(LoggerWidgetDesign)
        self.clearButton.setAutoRaise(True)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.hboxlayout.addWidget(self.clearButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(LoggerWidgetDesign)
        QtCore.QObject.connect(self.clearButton, QtCore.SIGNAL(_fromUtf8("clicked()")), LoggerWidgetDesign.clearLogger)
        QtCore.QObject.connect(self.debugBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), LoggerWidgetDesign.rebuildLog)
        QtCore.QObject.connect(self.errorBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), LoggerWidgetDesign.rebuildLog)
        QtCore.QObject.connect(self.infoBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), LoggerWidgetDesign.rebuildLog)
        QtCore.QMetaObject.connectSlotsByName(LoggerWidgetDesign)

    def retranslateUi(self, LoggerWidgetDesign):
        LoggerWidgetDesign.setWindowTitle(QtGui.QApplication.translate("LoggerWidgetDesign", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setText(QtGui.QApplication.translate("LoggerWidgetDesign", "Display message types:", None, QtGui.QApplication.UnicodeUTF8))
        self.errorBox.setText(QtGui.QApplication.translate("LoggerWidgetDesign", "Errors", None, QtGui.QApplication.UnicodeUTF8))
        self.debugBox.setText(QtGui.QApplication.translate("LoggerWidgetDesign", "Debug", None, QtGui.QApplication.UnicodeUTF8))
        self.infoBox.setText(QtGui.QApplication.translate("LoggerWidgetDesign", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setToolTip(QtGui.QApplication.translate("LoggerWidgetDesign", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setText(QtGui.QApplication.translate("LoggerWidgetDesign", "Clear log", None, QtGui.QApplication.UnicodeUTF8))

