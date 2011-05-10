# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Skole\it2901\resources\forms\SettingsDialogDesign.ui'
#
# Created: Tue May 10 19:41:52 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(_fromUtf8("SettingsDialog"))
        SettingsDialog.resize(550, 340)
        self.gridLayout = QtGui.QGridLayout(SettingsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.actionSave = QtGui.QPushButton(SettingsDialog)
        self.actionSave.setDefault(True)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.horizontalLayout.addWidget(self.actionSave)
        self.actionCancel = QtGui.QPushButton(SettingsDialog)
        self.actionCancel.setObjectName(_fromUtf8("actionCancel"))
        self.horizontalLayout.addWidget(self.actionCancel)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(SettingsDialog)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabGeneral = QtGui.QWidget()
        self.tabGeneral.setObjectName(_fromUtf8("tabGeneral"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabGeneral)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox = QtGui.QGroupBox(self.tabGeneral)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.showLoggerOnStart = QtGui.QCheckBox(self.groupBox)
        self.showLoggerOnStart.setChecked(False)
        self.showLoggerOnStart.setObjectName(_fromUtf8("showLoggerOnStart"))
        self.horizontalLayout_3.addWidget(self.showLoggerOnStart)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tabGeneral, _fromUtf8(""))
        self.tabPlugins = QtGui.QWidget()
        self.tabPlugins.setObjectName(_fromUtf8("tabPlugins"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tabPlugins)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.splitter = QtGui.QSplitter(self.tabPlugins)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.pluginListView = QtGui.QListView(self.splitter)
        self.pluginListView.setMaximumSize(QtCore.QSize(175, 16777215))
        self.pluginListView.setObjectName(_fromUtf8("pluginListView"))
        self.pluginTabs = QtGui.QTabWidget(self.splitter)
        self.pluginTabs.setObjectName(_fromUtf8("pluginTabs"))
        self.gridLayout_4.addWidget(self.splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabPlugins, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(SettingsDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsDialog.cancelSettings)
        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsDialog.saveSettings)
        QtCore.QObject.connect(self.pluginListView, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), SettingsDialog.pluginSelected)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)
        SettingsDialog.setTabOrder(self.tabWidget, self.pluginListView)
        SettingsDialog.setTabOrder(self.pluginListView, self.actionSave)
        SettingsDialog.setTabOrder(self.actionSave, self.actionCancel)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QtGui.QApplication.translate("SettingsDialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("SettingsDialog", "&Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCancel.setText(QtGui.QApplication.translate("SettingsDialog", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("SettingsDialog", "Logging", None, QtGui.QApplication.UnicodeUTF8))
        self.showLoggerOnStart.setText(QtGui.QApplication.translate("SettingsDialog", "Allways show the Logger on startup", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGeneral), QtGui.QApplication.translate("SettingsDialog", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPlugins), QtGui.QApplication.translate("SettingsDialog", "Plugins", None, QtGui.QApplication.UnicodeUTF8))

