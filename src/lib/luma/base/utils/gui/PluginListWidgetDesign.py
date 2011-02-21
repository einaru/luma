# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PluginListWidgetDesign.ui'
#
# Created: Mon Feb 21 13:08:43 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_pluginListWidget(object):
    def setupUi(self, pluginListWidget):
        pluginListWidget.setObjectName(_fromUtf8("pluginListWidget"))
        pluginListWidget.resize(444, 313)
        self.gridLayout = QtGui.QGridLayout(pluginListWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listWidget = QtGui.QListWidget(pluginListWidget)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)

        self.retranslateUi(pluginListWidget)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), pluginListWidget.pluginDoubleClicked)
        QtCore.QMetaObject.connectSlotsByName(pluginListWidget)

    def retranslateUi(self, pluginListWidget):
        pluginListWidget.setWindowTitle(QtGui.QApplication.translate("pluginListWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))

