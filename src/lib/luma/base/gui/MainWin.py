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

from PyQt4.QtCore import QTranslator, QObject, Qt, SIGNAL
from PyQt4.QtGui import QApplication, QMainWindow, QToolBar, QListWidget
from PyQt4.QtGui import QDockWidget, QPushButton, QLabel, QFont
from PyQt4.QtGui import qApp, QActionGroup, QAction


from base.gui.MainWinDesign import Ui_MainWindow
from base.utils.gui.LoggerWidget import LoggerWidget
from base.gui.AboutDialog import AboutDialog
from base.gui.ServerDialog import ServerDialog
from base.backend.ServerList import ServerList
from base.gui.SettingsDialog import SettingsDialog
from base.backend.Settings import Settings
from base.utils import LanguageHandler


class MainWin(QMainWindow, Ui_MainWindow):
    """
    The Luma Main Window
    """

    DEVEL = True

    __logger = logging.getLogger(__name__)

    def __init__(self, parent=None):
        """
        The constructor loads the generated ui code and setup the rest
        of the widgets. It assures that the configuration values concerning
        the GUI are loaded and set correctly; language settings, etc.
        """
        QMainWindow.__init__(self)

        self.serverDialog = None
        self.settingsDialog = None
        self.aboutDialog = None
        self.languageHandler = LanguageHandler()

        self.setupUi(self)
        self.__generateLanguageMenu()

        """  Setup the plugin toolbar """
        self.pluginToolBar = QToolBar(self)
        self.pluginToolBar.setObjectName("toolBar")
        self.addToolBar(self.pluginToolBar)

        self.pluginLabel = QLabel(self.pluginToolBar)
        self.pluginLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.pluginLabel.setText(self.trUtf8("Plugin Name"))
        font = QFont()
        font.setBold(True)
        self.pluginLabel.setFont(font)
        self.pluginLabel.setMargin(5)
        self.pluginToolBar.addWidget(self.pluginLabel)

        self.pluginButton = QPushButton(self.pluginToolBar)
        self.pluginButton.setText(self.trUtf8("Choose plugin"))
        self.pluginToolBar.addWidget(self.pluginButton)
        self.connect(self.pluginButton, SIGNAL("clicked()"),
                     self.showPluginSelection)

        self.pluginBox = QListWidget(None)
        font = self.pluginBox.font()
        font.setPointSize(font.pointSize() + 4)
        self.pluginBox.setFont(font)
        self.connect(self.pluginBox, SIGNAL("itemClicked(QListWidgetItem*)"),
                     self.pluginSelected)
        self.pluginBoxId = self.mainStack.addWidget(self.pluginBox)

        """  Setup the Logger Window """
        self.loggerDockWindow = QDockWidget(self)
        self.loggerDockWindow.setWindowTitle(
            QApplication.translate(
                "MainWindow", "Logger", None, QApplication.UnicodeUTF8))
        self.loggerWidget = LoggerWidget(self.loggerDockWindow)
        self.loggerDockWindow.setWidget(self.loggerWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.loggerDockWindow)

        # TODO Setup the rest of the defaults in the Main Window:
        #      fix translation stuff, 
        #      load configured language
        #      load the plugin list
        self.__loadSettings()
        self.__installLanguageTranslator()
        if self.DEVEL:
            self.actionEditServerList.setStatusTip(
                u'Final GUI polishing by Granbusk\u2122 Polishing')



    def __installLanguageTranslator(self):
        """
        Load the preferred application language. Defaults to english.
        """
        qApp.installTranslator(QTranslator())
        self.languageChange()


    def __generateLanguageMenu(self):
        """
        Helper method for generating available language translations in
        the menu
        """
        settings = Settings()
        lang = settings.language
        self.menuLangGroup = QActionGroup(self)
        languages = self.languageHandler.availableLanguages

        for key, value in languages.iteritems():
            action = QAction(self)
            action.setObjectName('language_%s' % key)
            action.setCheckable(True)
            if key == lang:
                action.setChecked(True)
            action.setActionGroup(self.menuLangGroup)
            action.setText(value[0])
            action.setStatusTip(value[1])
            QObject.connect(action, SIGNAL("triggered()"), self.languageChanged)
            self.menuLanguage.addAction(action)


    def __writeSettings(self):
        """
        Writes the MainWindow spesific settings to disk
        """
        settings = Settings()
        settings.size = self.size()
        settings.posistion = self.pos()


    def __loadSettings(self):
        """
        Load the application settings from disk
        """
        settings = Settings()
        """ Main window """
        self.resize(settings.size)
        self.move(settings.posistion)

        """ Logger widget """
        self.loggerWidget.errorBox.setChecked(settings.showErrors)
        self.loggerWidget.debugBox.setChecked(settings.showDebug)
        self.loggerWidget.infoBox.setChecked(settings.showInfo)

        if self.DEVEL or settings.showLoggerOnStart:
            self.loggerWidget.show()
            text = "Hide"
        else:
            self.loggerWidget.hide()
            text = "Show"

        self.__translate(self.actionShowLogger, "%s logger" % text)


    def __translate(self, widget, text):
        """
        Helper method for setting ut translation support for widgets
        not created by .ui files 
        """
        widget.setText(QApplication.translate(
            "MainWindow", text, None, QApplication.UnicodeUTF8))


    def close(self):
        """
        Quit the application.
        Leaving the main Qt execution loop. We must unload plugins and do
        necessary Qt cleanup, before tearing the application down.
        """
        self.saveOnClose = True
        if self.saveOnClose:
            self.__writeSettings()
        qApp.quit()


    def languageChanged(self, *isoCode):
        """
        Slot for the changing the application language
        """
        action = self.sender()
        if not isoCode:
            isoCode = action.objectName()[-2:]
        qmFile = self.languageHandler.getQmFile(isoCode)
        self.__logger.info('Loading translation file: %s' % qmFile)
        qApp.translator = QTranslator()
        qApp.translator.load(qmFile)
        qApp.installTranslator(qApp.translator)
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
        self.TODO("Show plugin selection")


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

        self.actionShowLogger.setText(QApplication.translate(
                "MainWindow", menuText, None, QApplication.UnicodeUTF8))

    def loggerVisibilityChanged(self):
        pass


    def showSettingsDialog(self, settingsTab=0):
        """
        Displays the settings dialog, enabling the user to configure
        some application settings.
        
        We do some post-work depending on the dialog return value.
        """
        if self.settingsDialog == None:
            self.settingsDialog = SettingsDialog()

        self.settingsDialog.tabWidget.setCurrentIndex(settingsTab)

        if self.settingsDialog.exec_():
            """ If the settingsDialog returns 1, the Ok button is clicked
            and we try to load the new translation if it is changed.
            """
            settings = Settings()
            currentLang = self.menuLangGroup.checkedAction().objectName()[-2:]
            # TODO We might want to move this piece of code somewhere else,
            #      or even better write some code code to replace it :)
            if settings.language != currentLang:
                currentLang = settings.language
                self.languageChanged(currentLang)
                for a in self.menuLangGroup.actions():
                    lang = a.objectName()[-2:]
                    if lang == currentLang:
                        a.setChecked(True)
            # We load all settings anew
            self.__loadSettings()


    def TODO(self, msg):
        """
        Helper method for logging TODO messages to the Logger widget
        """
        self.__logger.debug("TODO: %s: %s" % (msg, self.__class__))
