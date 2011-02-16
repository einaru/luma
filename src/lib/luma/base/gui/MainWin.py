# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# Copyright (c) 2003, 2004, 2005 
#      Wido Depping, <widod@users.sourceforge.net>
#
# Luma is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public Licence as published by 
# the Free Software Foundation; either version 2 of the Licence, or 
# (at your option) any later version.
#
# Luma is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence 
# for more details.
#
# You should have received a copy of the GNU General Public Licence along 
# with Luma; if not, write to the Free Software Foundation, Inc., 
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import logging

from PyQt4 import QtCore, QtGui

from base.gui.MainWinDesign import Ui_MainWindow
from base.utils.gui.LoggerWidget import LoggerWidget
from base.gui.AboutDialog import AboutDialog
from base.gui.ServerDialog import ServerDialog
from base.backend.ServerList import ServerList
from base.gui.SettingsDialog import SettingsDialog
from base.gui.PluginSettings import PluginSettings

class MainWin(QtGui.QMainWindow, Ui_MainWindow):
    """
    The Luma Main Window
    """

    DEVEL = True

    __logger = logging.getLogger(__name__)

    def __init__(self, configObject, parent=None):
        """
        The constructor loads the generated ui code and setup the rest
        of the widgets. It assures that the configuration values concerning
        the GUI are loaded and set correctly; language settings, etc.
        """
        QtGui.QMainWindow.__init__(self)

        # TODO We use 
#        self.debug_lang_path = "/mnt/debris/devel/git/src/lib/luma/i18n"
#        self.languageHandler = LanguageHandler(self.debug_lang_path)
        self.config = configObject

        self.serverDialog = None
        self.languageHandler = self.config.languageHandler

        self.setupUi(self)
        self.__generateLanguageMenu()

        """
        Setup the plugin toolbar:
        """
        self.pluginToolBar = QtGui.QToolBar(self)
        self.pluginToolBar.setObjectName("toolBar")
        self.addToolBar(self.pluginToolBar)

        self.pluginLabel = QtGui.QLabel(self.pluginToolBar)
        self.pluginLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.pluginLabel.setText(self.trUtf8("Plugin Name"))
        font = QtGui.QFont()
        font.setBold(True)
        self.pluginLabel.setFont(font)
        self.pluginLabel.setMargin(5)
        self.pluginToolBar.addWidget(self.pluginLabel)

        self.pluginButton = QtGui.QPushButton(self.pluginToolBar)
        self.pluginButton.setText(self.trUtf8("Choose plugin"))
        self.pluginToolBar.addWidget(self.pluginButton)
        self.connect(self.pluginButton, QtCore.SIGNAL("clicked()"), self.showPluginSelection)

        self.pluginBox = QtGui.QListWidget(None)
        font = self.pluginBox.font()
        font.setPointSize(font.pointSize() + 4)
        self.pluginBox.setFont(font)
        self.connect(self.pluginBox, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.pluginSelected)
        self.pluginBoxId = self.mainStack.addWidget(self.pluginBox)

        """
        Setup the Logger Window
        """
        self.loggerDockWindow = QtGui.QDockWidget("Logger", self)
        self.loggerWidget = LoggerWidget(self.loggerDockWindow)
        self.connect(self.loggerDockWindow, QtCore.SIGNAL("visibilityChanged(bool)"), self.loggerVisibilityChanged)

        self.loggerDockWindow.setWidget(self.loggerWidget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.loggerDockWindow)

        logMenuText = "Hide Logger"

        if not self.DEVEL:
            self.loggerDockWindow.hide()
            logMenuText = "Show Logger"

        self.actionShowLogger.setText(
            QtGui.QApplication.translate(
                "MainWindow", logMenuText, None, QtGui.QApplication.UnicodeUTF8))

        # TODO Setup the rest of the defaults in the Main Window:
        #      fix translation stuff, 
        #      load configured language
        #      load the plugin list
        self.__installLanguageTranslator()


        self.settingsDialog = SettingsDialog(self.config)


    def __installLanguageTranslator(self):
        """
        Load the preferred application language. Defaults to english.
        """
        QtGui.qApp.installTranslator(QtCore.QTranslator())
        self.languageChange()


    def __generateLanguageMenu(self):
        """
        Helper method for generating available language translations in
        the menu
        """
        langGroup = QtGui.QActionGroup(self)

        for key, value in self.languageHandler.availableLanguages.iteritems():
            action = QtGui.QAction(self)
            action.setObjectName("language_%s" % key)
            action.setCheckable(True)
            if key == "en":
                action.setChecked(True)
            action.setActionGroup(langGroup)
            action.setText(QtGui.QApplication.translate("MainWindow", value, None, QtGui.QApplication.UnicodeUTF8))
            QtCore.QObject.connect(action, QtCore.SIGNAL("triggered()"), self.languageChanged)
            self.menuLanguage.addAction(action)


    def languageChanged(self):
        """
        Slot for the changing the application language
        """
        action = self.sender()
        langFile = "luma_%s.qm" % action.objectName()[-2:]
        QtGui.qApp.translator = QtCore.QTranslator()
        QtGui.qApp.translator.load("%s/%s" % (self.config.i18nPath, langFile))
        QtGui.qApp.installTranslator(QtGui.qApp.translator)
        self.languageChange()


    def showAboutLuma(self):
        """
        Display the About dialog 
        """
        # TODO we must fix the issue regarding closeing all dialogs and
        #      children of dialogs when the parent is closed. Currently 
        #      we've provided a hackish solution in the MainWin close 
        #      method
        self.about = AboutDialog()
        self.about.exec_()


    def close(self):
        """
        Quit the application.
        Leaving the main Qt execution loop. We must unload plugins and do
        necessary Qt cleanup, before tearing the application down.
        """
        QtGui.qApp.quit()


    def showServerEditor(self):
        """
        Display the server dialog editor
        """
        if self.serverDialog == None:
            self.serverDialog = ServerDialog(ServerList("/tmp"))
        r = self.serverDialog.exec_()

        self.__logger.debug("ServerDialog return code=%s" % r)
        #if r == OK:
        #    self.serverList = self.serverDialog.getList()
        #else:
            #Ingen endring
        #    pass

    def loadPlugins(self):
        """
        Load the all available plugins
        """
        self.TODO("Load plugins")


    def reloadPlugins(self):
        """
        Reaload all available plugins. 
        This is done by first calling unloadPlugins followed by a call 
        to loadPlugins
        """
        self.TODO("Reload plugins")


    def unloadPlugins(self):
        """
        Unload all loaded plugins. 
        We must garbage collect the Qt objects.
        """
        self.TODO("Unload plugins")

    def configurePlugins(self):
        """
        Load the plugin configuration dialog.
        """
        self.showSettingsDialog(2)


    def pluginSelected(self):
        """
        Slot for handling plugin selection.
        """
        self.TODO("Plugin selected")


    def showPluginSelection(self):
        """
        Display the plugin selection.
        """
        s = PluginSettings()
        s.exec_()


    def showLoggerWindow(self):
        """
        Show or hide the logger window, depending on the state.
        """
        if self.loggerDockWindow.isHidden():
            self.loggerDockWindow.show()
            menuText = "Hide Logger"
        else:
            self.loggerDockWindow.hide()
            menuText = "Show Logger"

        self.actionShowLogger.setText(
            QtGui.QApplication.translate(
                "MainWindow", menuText, None, QtGui.QApplication.UnicodeUTF8))

    def loggerVisibilityChanged(self):
        pass


    def showSettingsDialog(self, settingsTab=0):
        self.settingsDialog.tabWidget.setCurrentIndex(settingsTab)
        self.settingsDialog.exec_()

    def TODO(self, msg):
        """
        Helper method for logging TODO messages to the Logger widget
        """
        self.__logger.debug("TODO: %s: %s" % (msg, self.__class__))
