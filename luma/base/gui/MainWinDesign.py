# -*- coding: utf-8 -*-

<<<<<<< HEAD
# Form implementation generated from reading ui file '/mnt/debris/devel/git/luma/src/lib/luma/resources/forms/MainWinDesign.ui'
#
# Created: Fri Feb 25 12:12:02 2011
=======
# Form implementation generated from reading ui file '/mnt/debris/devel/git/luma-playground/resources/forms/MainWinDesign.ui'
#
# Created: Mon Mar 14 12:54:09 2011
>>>>>>> S3-installation-v2
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 550)
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.mainStack = QtGui.QStackedWidget(self.centralwidget)
        self.mainStack.setObjectName("mainStack")
        self.page = QtGui.QWidget()
        self.page.setObjectName("page")
        self.mainStack.addWidget(self.page)
        self.gridLayout.addWidget(self.mainStack, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuLanguage = QtGui.QMenu(self.menuEdit)
        self.menuLanguage.setObjectName("menuLanguage")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionShowLogger = QtGui.QAction(MainWindow)
        self.actionShowLogger.setCheckable(True)
        self.actionShowLogger.setObjectName("actionShowLogger")
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionEditServerList = QtGui.QAction(MainWindow)
        self.actionEditServerList.setObjectName("actionEditServerList")
        self.actionReloadPlugins = QtGui.QAction(MainWindow)
        self.actionReloadPlugins.setObjectName("actionReloadPlugins")
        self.actionConfigurePlugins = QtGui.QAction(MainWindow)
        self.actionConfigurePlugins.setObjectName("actionConfigurePlugins")
        self.actionAboutLuma = QtGui.QAction(MainWindow)
        self.actionAboutLuma.setObjectName("actionAboutLuma")
        self.actionEditSettings = QtGui.QAction(MainWindow)
        self.actionEditSettings.setObjectName("actionEditSettings")
        self.menuFile.addAction(self.actionShowLogger)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionEditServerList)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionReloadPlugins)
        self.menuEdit.addAction(self.actionConfigurePlugins)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.menuLanguage.menuAction())
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionEditSettings)
        self.menuHelp.addAction(self.actionAboutLuma)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.mainStack.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QObject.connect(self.actionAboutLuma, QtCore.SIGNAL("triggered()"), MainWindow.showAboutLuma)
        QtCore.QObject.connect(self.actionConfigurePlugins, QtCore.SIGNAL("triggered()"), MainWindow.configurePlugins)
        QtCore.QObject.connect(self.actionReloadPlugins, QtCore.SIGNAL("triggered()"), MainWindow.reloadPlugins)
        QtCore.QObject.connect(self.actionShowLogger, QtCore.SIGNAL("triggered(bool)"), MainWindow.showLoggerWindow)
        QtCore.QObject.connect(self.actionEditServerList, QtCore.SIGNAL("triggered()"), MainWindow.showServerEditor)
        QtCore.QObject.connect(self.actionEditSettings, QtCore.SIGNAL("triggered()"), MainWindow.showSettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Luma", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuLanguage.setTitle(QtGui.QApplication.translate("MainWindow", "Language", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowLogger.setText(QtGui.QApplication.translate("MainWindow", "Show logger", None, QtGui.QApplication.UnicodeUTF8))
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

