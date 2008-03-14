# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/luma/base/gui/MainWinDesign.ui'
#
# Created: Wed Mar 12 22:43:36 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWinDesign(object):
    def setupUi(self, MainWinDesign):
        MainWinDesign.setObjectName("MainWinDesign")
        MainWinDesign.resize(QtCore.QSize(QtCore.QRect(0,0,479,321).size()).expandedTo(MainWinDesign.minimumSizeHint()))

        self.widget = QtGui.QWidget(MainWinDesign)
        self.widget.setGeometry(QtCore.QRect(0,26,479,295))
        self.widget.setObjectName("widget")

        self.gridlayout = QtGui.QGridLayout(self.widget)
        self.gridlayout.setObjectName("gridlayout")

        self.taskStack = QtGui.QStackedWidget(self.widget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.taskStack.sizePolicy().hasHeightForWidth())
        self.taskStack.setSizePolicy(sizePolicy)
        self.taskStack.setObjectName("taskStack")

        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0,0,461,277))
        self.page.setObjectName("page")
        self.taskStack.addWidget(self.page)
        self.gridlayout.addWidget(self.taskStack,0,0,1,1)
        MainWinDesign.setCentralWidget(self.widget)

        self.menubar = QtGui.QMenuBar(MainWinDesign)
        self.menubar.setGeometry(QtCore.QRect(0,0,479,26))
        self.menubar.setObjectName("menubar")

        self.Program = QtGui.QMenu(self.menubar)
        self.Program.setObjectName("Program")

        self.Settings = QtGui.QMenu(self.menubar)
        self.Settings.setObjectName("Settings")

        self.Help = QtGui.QMenu(self.menubar)
        self.Help.setObjectName("Help")
        MainWinDesign.setMenuBar(self.menubar)

        self.about = QtGui.QAction(MainWinDesign)
        self.about.setIcon(QtGui.QIcon("image0"))
        self.about.setProperty("name",QtCore.QVariant(QtGui.QApplication.translate("MainWinDesign", "about", None, QtGui.QApplication.UnicodeUTF8)))
        self.about.setObjectName("about")

        self.editServerList = QtGui.QAction(MainWinDesign)
        self.editServerList.setIcon(QtGui.QIcon("image1"))
        self.editServerList.setProperty("name",QtCore.QVariant(QtGui.QApplication.translate("MainWinDesign", "editServerList", None, QtGui.QApplication.UnicodeUTF8)))
        self.editServerList.setObjectName("editServerList")

        self.exitItem = QtGui.QAction(MainWinDesign)
        self.exitItem.setIcon(QtGui.QIcon("image2"))
        self.exitItem.setProperty("name",QtCore.QVariant(QtGui.QApplication.translate("MainWinDesign", "exitItem", None, QtGui.QApplication.UnicodeUTF8)))
        self.exitItem.setObjectName("exitItem")

        self.menuConfigurePlugins = QtGui.QAction(MainWinDesign)
        self.menuConfigurePlugins.setIcon(QtGui.QIcon("image3"))
        self.menuConfigurePlugins.setProperty("name",QtCore.QVariant(QtGui.QApplication.translate("MainWinDesign", "menuConfigurePlugins", None, QtGui.QApplication.UnicodeUTF8)))
        self.menuConfigurePlugins.setObjectName("menuConfigurePlugins")

        self.reload = QtGui.QAction(MainWinDesign)
        self.reload.setIcon(QtGui.QIcon("image4"))
        self.reload.setProperty("name",QtCore.QVariant(QtGui.QApplication.translate("MainWinDesign", "reload", None, QtGui.QApplication.UnicodeUTF8)))
        self.reload.setObjectName("reload")

        self.selectLanguage = QtGui.QAction(MainWinDesign)
        self.selectLanguage.setIcon(QtGui.QIcon("image5"))
        self.selectLanguage.setProperty("name",QtCore.QVariant(QtGui.QApplication.translate("MainWinDesign", "selectLanguage", None, QtGui.QApplication.UnicodeUTF8)))
        self.selectLanguage.setObjectName("selectLanguage")

        self.showLogger = QtGui.QAction(MainWinDesign)
        self.showLogger.setCheckable(False)
        self.showLogger.setIcon(QtGui.QIcon("image6"))
        self.showLogger.setProperty("name",QtCore.QVariant(QtGui.QApplication.translate("MainWinDesign", "showLogger", None, QtGui.QApplication.UnicodeUTF8)))
        self.showLogger.setObjectName("showLogger")
        self.Program.addAction(self.showLogger)
        self.Program.addAction(self.reload)
        self.Program.addSeparator()
        self.Program.addAction(self.exitItem)
        self.Program.addSeparator()
        self.Settings.addAction(self.editServerList)
        self.Settings.addAction(self.menuConfigurePlugins)
        self.Settings.addAction(self.selectLanguage)
        self.Help.addAction(self.about)
        self.menubar.addAction(self.Program.menuAction())
        self.menubar.addAction(self.Settings.menuAction())
        self.menubar.addAction(self.Help.menuAction())

        self.retranslateUi(MainWinDesign)
        QtCore.QObject.connect(self.about,QtCore.SIGNAL("activated()"),MainWinDesign.showAboutLuma)
        QtCore.QObject.connect(self.exitItem,QtCore.SIGNAL("activated()"),MainWinDesign.quitApplication)
        QtCore.QObject.connect(self.editServerList,QtCore.SIGNAL("activated()"),MainWinDesign.showServerEditor)
        QtCore.QObject.connect(self.menuConfigurePlugins,QtCore.SIGNAL("activated()"),MainWinDesign.configurePlugins)
        QtCore.QObject.connect(self.reload,QtCore.SIGNAL("activated()"),MainWinDesign.reloadPlugins)
        QtCore.QObject.connect(self.selectLanguage,QtCore.SIGNAL("activated()"),MainWinDesign.showLanguageDialog)
        QtCore.QObject.connect(self.showLogger,QtCore.SIGNAL("activated()"),MainWinDesign.showLoggerWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWinDesign)

    def retranslateUi(self, MainWinDesign):
        MainWinDesign.setWindowTitle(QtGui.QApplication.translate("MainWinDesign", "Luma", None, QtGui.QApplication.UnicodeUTF8))
        self.Program.setTitle(QtGui.QApplication.translate("MainWinDesign", "&Program", None, QtGui.QApplication.UnicodeUTF8))
        self.Settings.setTitle(QtGui.QApplication.translate("MainWinDesign", "&Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.Help.setTitle(QtGui.QApplication.translate("MainWinDesign", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.about.setText(QtGui.QApplication.translate("MainWinDesign", "About Luma...", None, QtGui.QApplication.UnicodeUTF8))
        self.about.setIconText(QtGui.QApplication.translate("MainWinDesign", "About Luma...", None, QtGui.QApplication.UnicodeUTF8))
        self.editServerList.setText(QtGui.QApplication.translate("MainWinDesign", "Edit Server List...", None, QtGui.QApplication.UnicodeUTF8))
        self.editServerList.setIconText(QtGui.QApplication.translate("MainWinDesign", "Edit Server List...", None, QtGui.QApplication.UnicodeUTF8))
        self.editServerList.setShortcut(QtGui.QApplication.translate("MainWinDesign", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.exitItem.setText(QtGui.QApplication.translate("MainWinDesign", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.exitItem.setIconText(QtGui.QApplication.translate("MainWinDesign", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.exitItem.setShortcut(QtGui.QApplication.translate("MainWinDesign", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.menuConfigurePlugins.setText(QtGui.QApplication.translate("MainWinDesign", "Configure Plugins...", None, QtGui.QApplication.UnicodeUTF8))
        self.menuConfigurePlugins.setIconText(QtGui.QApplication.translate("MainWinDesign", "Configure Plugins...", None, QtGui.QApplication.UnicodeUTF8))
        self.reload.setText(QtGui.QApplication.translate("MainWinDesign", "Reload Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.reload.setIconText(QtGui.QApplication.translate("MainWinDesign", "Reload Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.selectLanguage.setText(QtGui.QApplication.translate("MainWinDesign", "Language...", None, QtGui.QApplication.UnicodeUTF8))
        self.selectLanguage.setIconText(QtGui.QApplication.translate("MainWinDesign", "Language...", None, QtGui.QApplication.UnicodeUTF8))
        self.showLogger.setIconText(QtGui.QApplication.translate("MainWinDesign", "Show logger", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWinDesign = QtGui.QMainWindow()
    ui = Ui_MainWinDesign()
    ui.setupUi(MainWinDesign)
    MainWinDesign.show()
    sys.exit(app.exec_())
