# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PluginListWidgetDesign.ui'
#
# Created: Tue Feb 22 15:15:05 2011
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
        self.listView = QtGui.QListView(pluginListWidget)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.gridLayout.addWidget(self.listView, 0, 0, 1, 1)

        self.retranslateUi(pluginListWidget)
        QtCore.QObject.connect(self.listView, QtCore.SIGNAL(_fromUtf8("activated(QModelIndex)")), pluginListWidget.pluginDoubleClicked)
        QtCore.QMetaObject.connectSlotsByName(pluginListWidget)

    def retranslateUi(self, pluginListWidget):
        pluginListWidget.setWindowTitle(QtGui.QApplication.translate("pluginListWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))

