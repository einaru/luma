# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/debris/devel/git/luma/resources/forms/SettingsDialogDesign.ui'
#
# Created: Fri Apr  1 20:53:00 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(550, 340)
        self.gridLayout = QtGui.QGridLayout(SettingsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.actionSave = QtGui.QPushButton(SettingsDialog)
        self.actionSave.setDefault(True)
        self.actionSave.setObjectName("actionSave")
        self.horizontalLayout.addWidget(self.actionSave)
        self.actionCancel = QtGui.QPushButton(SettingsDialog)
        self.actionCancel.setObjectName("actionCancel")
        self.horizontalLayout.addWidget(self.actionCancel)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(SettingsDialog)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tabGeneral = QtGui.QWidget()
        self.tabGeneral.setObjectName("tabGeneral")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabGeneral)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtGui.QGroupBox(self.tabGeneral)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.showLoggerOnStart = QtGui.QCheckBox(self.groupBox)
        self.showLoggerOnStart.setChecked(False)
        self.showLoggerOnStart.setObjectName("showLoggerOnStart")
        self.horizontalLayout_3.addWidget(self.showLoggerOnStart)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tabGeneral, "")
        self.tabPlugins = QtGui.QWidget()
        self.tabPlugins.setObjectName("tabPlugins")
        self.gridLayout_4 = QtGui.QGridLayout(self.tabPlugins)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.splitter = QtGui.QSplitter(self.tabPlugins)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.pluginListView = QtGui.QListView(self.splitter)
        self.pluginListView.setMaximumSize(QtCore.QSize(175, 16777215))
        self.pluginListView.setObjectName("pluginListView")
        self.pluginTabs = QtGui.QTabWidget(self.splitter)
        self.pluginTabs.setObjectName("pluginTabs")
        self.gridLayout_4.addWidget(self.splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabPlugins, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(SettingsDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionCancel, QtCore.SIGNAL("clicked()"), SettingsDialog.cancelSettings)
        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL("clicked()"), SettingsDialog.saveSettings)
        QtCore.QObject.connect(self.pluginListView, QtCore.SIGNAL("clicked(QModelIndex)"), SettingsDialog.pluginSelected)
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

