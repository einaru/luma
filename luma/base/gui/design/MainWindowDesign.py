# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\Dropbox\Git\it2901\resources\forms\MainWindowDesign.ui'
#
# Created: Mon May 09 00:51:20 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(700, 500)
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.mainTabs = QtGui.QTabWidget(self.centralwidget)
        self.mainTabs.setObjectName(_fromUtf8("mainTabs"))
        self.gridLayout.addWidget(self.mainTabs, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuLanguage = QtGui.QMenu(self.menuEdit)
        self.menuLanguage.setObjectName(_fromUtf8("menuLanguage"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menu_View = QtGui.QMenu(self.menubar)
        self.menu_View.setObjectName(_fromUtf8("menu_View"))
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionShowLogger = QtGui.QAction(MainWindow)
        self.actionShowLogger.setCheckable(True)
        self.actionShowLogger.setObjectName(_fromUtf8("actionShowLogger"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionEditServerList = QtGui.QAction(MainWindow)
        self.actionEditServerList.setObjectName(_fromUtf8("actionEditServerList"))
        self.actionReloadPlugins = QtGui.QAction(MainWindow)
        self.actionReloadPlugins.setObjectName(_fromUtf8("actionReloadPlugins"))
        self.actionConfigurePlugins = QtGui.QAction(MainWindow)
        self.actionConfigurePlugins.setObjectName(_fromUtf8("actionConfigurePlugins"))
        self.actionAboutLuma = QtGui.QAction(MainWindow)
        self.actionAboutLuma.setObjectName(_fromUtf8("actionAboutLuma"))
        self.actionEditSettings = QtGui.QAction(MainWindow)
        self.actionEditSettings.setObjectName(_fromUtf8("actionEditSettings"))
        self.actionShowPluginList = QtGui.QAction(MainWindow)
        self.actionShowPluginList.setCheckable(False)
        self.actionShowPluginList.setObjectName(_fromUtf8("actionShowPluginList"))
        self.actionShowWelcomeTab = QtGui.QAction(MainWindow)
        self.actionShowWelcomeTab.setCheckable(False)
        self.actionShowWelcomeTab.setEnabled(False)
        self.actionShowWelcomeTab.setObjectName(_fromUtf8("actionShowWelcomeTab"))
        self.actionShowToolbar = QtGui.QAction(MainWindow)
        self.actionShowToolbar.setCheckable(True)
        self.actionShowToolbar.setObjectName(_fromUtf8("actionShowToolbar"))
        self.actionShowStatusbar = QtGui.QAction(MainWindow)
        self.actionShowStatusbar.setCheckable(True)
        self.actionShowStatusbar.setChecked(True)
        self.actionShowStatusbar.setObjectName(_fromUtf8("actionShowStatusbar"))
        self.actionFullscreen = QtGui.QAction(MainWindow)
        self.actionFullscreen.setCheckable(True)
        self.actionFullscreen.setObjectName(_fromUtf8("actionFullscreen"))
        self.actionSet_Temporary_Password = QtGui.QAction(MainWindow)
        self.actionSet_Temporary_Password.setObjectName(_fromUtf8("actionSet_Temporary_Password"))
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionEditServerList)
        self.menuEdit.addAction(self.actionSet_Temporary_Password)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionReloadPlugins)
        self.menuEdit.addAction(self.actionConfigurePlugins)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.menuLanguage.menuAction())
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionEditSettings)
        self.menuHelp.addAction(self.actionAboutLuma)
        self.menu_View.addAction(self.actionShowPluginList)
        self.menu_View.addAction(self.actionShowWelcomeTab)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.actionShowStatusbar)
        self.menu_View.addAction(self.actionShowLogger)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.actionFullscreen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.actionAboutLuma, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.showAboutLuma)
        QtCore.QObject.connect(self.actionConfigurePlugins, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.configurePlugins)
        QtCore.QObject.connect(self.actionReloadPlugins, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.reloadPlugins)
        QtCore.QObject.connect(self.actionShowLogger, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), MainWindow.toggleLoggerWindow)
        QtCore.QObject.connect(self.actionEditServerList, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.showServerEditor)
        QtCore.QObject.connect(self.actionEditSettings, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.showSettingsDialog)
        QtCore.QObject.connect(self.mainTabs, QtCore.SIGNAL(_fromUtf8("tabCloseRequested(int)")), MainWindow.tabClose)
        QtCore.QObject.connect(self.actionShowPluginList, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.showPlugins)
        QtCore.QObject.connect(self.actionShowWelcomeTab, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.showWelcome)
        QtCore.QObject.connect(self.actionShowStatusbar, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), MainWindow.toggleStatusbar)
        QtCore.QObject.connect(self.actionFullscreen, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), MainWindow.toggleFullscreen)
        QtCore.QObject.connect(self.actionSet_Temporary_Password, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.showTempPasswordDialog)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Luma", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuLanguage.setTitle(QtGui.QApplication.translate("MainWindow", "Language", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_View.setTitle(QtGui.QApplication.translate("MainWindow", "&View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowLogger.setText(QtGui.QApplication.translate("MainWindow", "Logger Window", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowLogger.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+L", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditServerList.setText(QtGui.QApplication.translate("MainWindow", "Server List", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditServerList.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReloadPlugins.setText(QtGui.QApplication.translate("MainWindow", "Reload Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReloadPlugins.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfigurePlugins.setText(QtGui.QApplication.translate("MainWindow", "Configure Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAboutLuma.setText(QtGui.QApplication.translate("MainWindow", "About Luma", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAboutLuma.setShortcut(QtGui.QApplication.translate("MainWindow", "F12", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditSettings.setText(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowPluginList.setText(QtGui.QApplication.translate("MainWindow", "Show Plugin List", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowPluginList.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowWelcomeTab.setText(QtGui.QApplication.translate("MainWindow", "Show Welcome Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowWelcomeTab.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+W", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowToolbar.setText(QtGui.QApplication.translate("MainWindow", "Toolbar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowStatusbar.setText(QtGui.QApplication.translate("MainWindow", "Statusbar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFullscreen.setText(QtGui.QApplication.translate("MainWindow", "Fullscreen", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFullscreen.setShortcut(QtGui.QApplication.translate("MainWindow", "F11", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSet_Temporary_Password.setText(QtGui.QApplication.translate("MainWindow", "Use temporary password", None, QtGui.QApplication.UnicodeUTF8))

