# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.no>
#     Christian Forfang, <cforfang@gmail.com>
#     Johannes Harestad, <johannesharestad@gmail.com>
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
"""
This module contains several Luma Widget classes:

MainWindow:
    The Luma main window.

LoggerWidget:
    A dockable loggerwidget used by MainWindow.

PluginToolBar:
    A toolbar widget for quick plugin access.
"""
import logging
import gc
import platform

from PyQt4.QtCore import (Qt, pyqtSlot, pyqtSignal)
from PyQt4.QtCore import (QObject)
from PyQt4.QtCore import (QEvent, QString, QTimer)
from PyQt4.QtCore import (QTranslator)

from PyQt4.QtGui import (QAction, QActionGroup, QApplication, qApp)
from PyQt4.QtGui import (QDockWidget, QMenu)
from PyQt4.QtGui import (QFont)
from PyQt4.QtGui import (QKeySequence)
from PyQt4.QtGui import (QLabel)
from PyQt4.QtGui import (QMainWindow)
from PyQt4.QtGui import (QPushButton)
from PyQt4.QtGui import (QScrollArea)
from PyQt4.QtGui import (QToolBar)
from PyQt4.QtGui import (QWidget)
from PyQt4.QtGui import (QErrorMessage)
from PyQt4.QtGui import (QInputDialog, QLineEdit)

from base.backend.LumaConnection import LumaConnection
from base.backend.ServerList import ServerList

from ..gui.AboutDialog import AboutDialog
from ..gui.ServerDialog import ServerDialog
from ..gui.Settings import Settings
from ..gui.SettingsDialog import SettingsDialog
from ..gui.design.LoggerWidgetDesign import Ui_LoggerWidget
from ..gui.design.MainWindowDesign import Ui_MainWindow
from ..util.i18n import LanguageHandler
from ..util.IconTheme import iconFromTheme
from ..util.gui.PluginListWidget import PluginListWidget
from ..gui.WelcomeTab import WelcomeTab


class MainWindow(QMainWindow, Ui_MainWindow):
    """The Main window of Luma.
    """

    logger = logging.getLogger(__name__)
    languages = {}
    translator = None
    languageHandler = None
    currentLanguage = ''

    def __init__(self, parent=None):
        """The constructor sets up the MainWindow widget, and connects
        all necessary signals and slots
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # We store the window size to make sure the previous window size
        # is restored when leaving fullscreen mode. This varible is used
        # in the toggleFullscreen slot.
        self.__tmpWinSize = self.size()
        self.eventFilter = LumaEventFilter(self)
        
        self.mainTabs.installEventFilter(self.eventFilter)
        
        self.translator = QTranslator()
        self.languageHandler = LanguageHandler()
        self.languages = self.languageHandler.availableLanguages

        #self.__createPluginToolBar()
        self.__createLoggerWidget()
        self.__loadSettings()
        self.__createLanguageOptions()

        self.setStatusBar(self.statusBar)

        self.mainTabs.setTabsClosable(True)
        self.mainTabs.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mainTabs.customContextMenuRequested.connect(self.__mainTabsContextMenu)

        self.defaultTabStyle = ''
        self.lumaHeadStyle = 'background: url(:/icons/luma-gray);\n' + \
                     'background-position: bottom right;\n' + \
                     'background-attachment: fixed;\n' + \
                     'background-repeat:  no-repeat;'

        #Sets up pluginWidget
        #self in parameter is used to call pluginSelected here...
        self.pluginWidget = PluginListWidget(self)
        self.showPlugins()

        self.welcomeTab = WelcomeTab()
        self.welcomeTab.textBrowser.setStyleSheet(self.lumaHeadStyle)

        #This value comes from __loadSettings()
        #Its a checkbox set in WelcomeTab
        if self.showWelcomeSettings == 2:
            self.showWelcome()
        else:
            # Let's do some styling of the tab widget when no tabs are opened
            if self.mainTabs.currentIndex() == -1:
                self.__setTabWidgetStyle(self.lumaHeadStyle)

            self.actionShowWelcomeTab.setEnabled(True)

        self.serversChangedMessage = QErrorMessage(self)

    def __mainTabsContextMenu(self, pos):
        menu = QMenu()
        if self.mainTabs.count() > 0:
            return
            # The menu is displayed even when the rightclick is not
            # done over the actual tabs so to avoid confusion the 
            # function is disabled entirey
            #menu.addAction(QApplication.translate("MainWindow", "Close all plugin-tabs"), self.tabCloseAll)
        else:
            # If there's no tabs, offer to display the pluginlist
            menu.addAction(self.actionShowPluginList)
        menu.exec_(self.mainTabs.mapToGlobal(pos))

    def __createPluginToolBar(self):
        """Creates the pluign toolbar.
        """
        self.pluginToolBar = PluginToolBar(self)
        self.pluginToolBar.setWindowTitle(QApplication.translate('MainWindow', 'Plugintoolbar', None, QApplication.UnicodeUTF8))
        self.pluginToolBar.setObjectName('pluginToolBar')
        self.addToolBar(self.pluginToolBar)
        self.pluginToolBar.hide()

    def __createLoggerWidget(self):
        """Creates the logger widget.
        """
        self.loggerDockWindow = QDockWidget(self)
        self.loggerDockWindow.setObjectName('loggerDockWindow')
        self.loggerDockWindow.visibilityChanged[bool].connect(self.actionShowLogger.setChecked)
        self.loggerDockWindow.setWindowTitle(QApplication.translate('MainWindow', 'Logger', None, QApplication.UnicodeUTF8))
        self.loggerWidget = LoggerWidget(self.loggerDockWindow)
        self.loggerDockWindow.setWidget(self.loggerWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.loggerDockWindow)
        self.loggerDockWindow.hide()

    def __createLanguageOptions(self):
        """Creates the language selection in the menubar.
        """
        self.langGroup = QActionGroup(self)
        self.langGroup.setExclusive(True)
        self.langGroup.triggered['QAction*'].connect(self.languageChanged)

        for key, name in self.languages.iteritems():
            action = QAction(self)
            action.setCheckable(True)
            action.setData(key)
            action.setText(name[0])
            action.setStatusTip(name[1])
            action.setActionGroup(self.langGroup)
            self.menuLanguage.addAction(action)
            if key == self.currentLanguage:
                action.setChecked(True)

    def __loadSettings(self, mainWin=True):
        """Loads settings from file.
        
        Parameters:
        
        - `mainWin`: If set to ``False``, neither the values for the
          window size or the window position will be loaded. This is
          i.e done when the settings dialog returns 1.
        """
        settings = Settings()
        # We might want to use these methods to restore the
        # application state and geometry.
        if mainWin:
            self.restoreGeometry(settings.geometry)
        #self.restoreState(settings.state)

        # General Mainwin
        #if mainWin:
        #    self.resize(settings.size)
        #    self.move(settings.position)
        #    if settings.maximize:
        #        self.showMaximized()

        # If the geometry saved inticates fullscreen mode, 
        # we need to explicitly set the fullscreen menuaction checkbox
        if self.isFullScreen():
            self.actionFullscreen.setChecked(True)

        # Logger

        # Logger
        # The `allwaysShowLoggerOnStart` a precedence on the
        # `showLogger` value.
        if settings.showLoggerOnStart:
            self.actionShowLogger.setChecked(True)
        else:
            self.actionShowLogger.setChecked(settings.showLogger)

        self.loggerWidget.errorBox.setChecked(settings.showErrors)
        self.loggerWidget.debugBox.setChecked(settings.showDebug)
        self.loggerWidget.infoBox.setChecked(settings.showInfo)

        self.toggleLoggerWindow(self.actionShowLogger.isChecked())

        # Language
        self.loadLanguage(settings.language)

        #Tabs
        self.showWelcomeSettings = settings.value("showWelcome", 2).toInt()[0]

    def __writeSettings(self):
        """Save settings to file.
        """
        settings = Settings()
        # We might want to use these methods to restore the
        # application state and geometry.
        settings.geometry = self.saveGeometry()
        #settings.state = self.saveState()

        # Mainwin
        #max = self.isMaximized()
        #settings.maximize = max
        #if not max:
        #    settings.size = self.size()
        #    settings.position = self.pos()

        # The global logger settings is managed from the settings dialog.
        # Logger
        settings.showLogger = self.actionShowLogger.isChecked()
        settings.showErrors = self.loggerWidget.errorBox.isChecked()
        settings.showDebug = self.loggerWidget.debugBox.isChecked()
        settings.showInfo = self.loggerWidget.infoBox.isChecked()

        # Language
        settings.language = self.currentLanguage

    def __switchTranslator(self, translator, qmFile):
        """Called when a new language is loaded.
        
        Parameters:

        - `translator`: The translator object to install.
        - `qmFile`: The translation file for the loaded language.
        """
        qApp.removeTranslator(translator)
        if translator.load(qmFile):
            qApp.installTranslator(translator)

    def __setTabWidgetStyle(self, stylesheet):
        self.mainTabs.setStyleSheet(stylesheet)

    @pyqtSlot('QAction*')
    @pyqtSlot(int)
    def languageChanged(self, value):
        """This slot is called by actions and signals related to 
        application translations. The slot contains validation for
        those parameters defined by the pyqtSlot meta info in the
        method header.
        
        Parameters:
        - `value`: Can be either a ``QAction`` or an integer value.
          I.e. menu actions provide ``QActions`` but a ``QCombobox`` 
          might send it's index. 
        """
        locale = None
        if isinstance(value, int):
            locale = self.languageSelector.itemData(value).toString()
        elif isinstance(value, QAction):
            locale = value.data().toString()
        #else:
        #    locale = value
        if locale:
            self.loadLanguage(locale)

    def loadLanguage(self, locale):
        """Loads a language by the given language iso code.
        
        Parameters:
        - `locale`: A twoletter lowercase ISO 639 language code and
          possibly a twoletter uppercase ISO 3166 country code
          separeted by a underscore.
        """
        if self.currentLanguage != locale:
            self.currentLanguage = locale
            qmFile = self.languageHandler.getQmFile(locale)
            self.__switchTranslator(self.translator, qmFile)

    def changeEvent(self, event):
        """This event is called when a new translator is loaded or the
        system language (locale) is changed.
        
        Parameters:

        - `event`: The event that generated the `changeEvent`.
        """
        if None != event:
            type = event.type()
            if QEvent.LanguageChange == type or QEvent.LocaleChange == type:
                self.retranslateUi(self)
                self.loggerWidget.retranslateUi(self.loggerWidget)

    def showAboutLuma(self):
        """Slot for displaying the about dialog.
        """
        AboutDialog().exec_()
    
    @pyqtSlot(bool)
    def toggleLoggerWindow(self, show):
        """Slot for toggling the logger window.
        
        Parameters:
        
        - `show`: a boolean value indicating whether the logger window
          should be shown or not.
        """
        if show:
            self.loggerDockWindow.show()
        else:
            self.loggerDockWindow.hide()

    @pyqtSlot(bool)
    def toggleStatusbar(self, show):
        """Slot for toggling the logger window.
        
        Parameters:
        
        - `show`: a boolean value indicating whether the statusbar
          should be shown or not.
        """
        if show:
            self.statusBar.show()
        else:
            self.statusBar.hide()

    @pyqtSlot(bool)
    def toggleFullscreen(self, fullscreen):
        """Slot for toggling the logger window.
        
        Parameters:
        
        - `fullscreen`: a boolean value indicating whether to enter
          fullscreenmode or not.
        """
        if fullscreen:
            self.__tmpWinSize = self.size()
            self.showFullScreen()
        else:
            self.showNormal()
            self.resize(self.__tmpWinSize)

    def showServerEditor(self):
        """Slot to display the server editor dialog.
        """
        serverEditor = ServerDialog()
        r = serverEditor.exec_()
        if r:
            #TODO -- only display if plugins open:
            self.serversChangedMessage.showMessage(QApplication.translate("MainWindow","You may need to restart plugins for changes to take effect."))

    def showTempPasswordDialog(self):
        """ Sets overridePassword for a server.
        Using this one doesn't actually have to enter the password
        in the ServerDialog (and by extension save to disk).
        """
        
        serverList = ServerList()
        
        # Create a stringlist to be used by the qinputdialog
        stringList = []
        for server in serverList.getTable():
            stringList.append(server.name)

        # Display list of servers
        (serverString, ok) =  QInputDialog.getItem(self, "Select server", "Server:", stringList, editable = False)
        if ok:
            server = serverList.getServerObjectByName(serverString)
            if server != None:
                # Ask for password
                (value, ok) = QInputDialog.getText(self, "Temporary password", "Enter password:", QLineEdit.Password)
                if ok:
                    # Use value as the overridePassword for the server.
                    LumaConnection(server).overridePassword(value)

    def showSettingsDialog(self, tab=0):
        """Slot to display the settings dialog. If the settings dialog
        returns 1, i.e. the user has clicked the ok button, the
        loadSettings method is called with mainWin=False, to load the 
        (assumed) newly changed settings.
        
        Parameters:
        
        - `tab`: The index of the tab to display in the settings dialog. 
        """
        #settingsDialog = SettingsDialog(self.currentLanguage, self.languages)
        settingsDialog = SettingsDialog()
        if tab < 0:
            tab = 0
        settingsDialog.tabWidget.setCurrentIndex(tab)
        if settingsDialog.exec_():
            self.reloadPlugins()
#            # We assume that some settings is changed 
#            # if the user clicked the ok button, and
#            # reloads the application settings
#            self.__loadSettings(mainWin=False)
#            # A Hack but it'll do for now
#            for a in self.langGroup.actions():
#                if a.data().toString() == self.currentLanguage:
#                    a.setChecked(True)

    def configurePlugins(self):
        """Slot to display the plugins configuration. This currently
        calls `showSettingsDialog` with tab index set to 2.
        """
        self.showSettingsDialog(1)

    def reloadPlugins(self):
        """Slot to reload plugins.
        """
        self.pluginWidget.updatePlugins()

    def pluginSelected(self, item):
        """This method will be called from the `PluginListWidget`.
        """
        # Clear the stylesheet when a tab is opened
        self.__setTabWidgetStyle(self.defaultTabStyle)

        widget = item.plugin.getPluginWidget(None, self)

        if platform.system() == "Windows":
            scroll = QScrollArea() 
            scroll.setWidget(widget)
            scroll.setWidgetResizable(True)
            index = self.mainTabs.addTab(scroll, item.icon(), item.plugin.pluginUserString)
        else:
            index = self.mainTabs.addTab(widget, item.icon(), item.plugin.pluginUserString)

        self.mainTabs.setCurrentIndex(index)

    def tabClose(self, index):
        """Slot for the signal `tabCloseRequest(int)` for the tabMains.
        """

        widget = self.mainTabs.widget(index)

        # If the tab closed is one of these, enable the toggle-action
        if widget == self.pluginWidget:
            self.actionShowPluginList.setEnabled(True)
        if widget == self.welcomeTab:
            self.actionShowWelcomeTab.setEnabled(True)

        self.mainTabs.removeTab(index)

        # Unparent the widget since it was reparented by the QTabWidget
        # so it's garbage collected
        widget.setParent(None)

        # In case the widget contained circular references
        # -- force GC to take care of the objects since there can be
        #    quite many if it was BrowserWidget that was closed.
        # Can't call it directly since that'll be too soon
        QTimer.singleShot(1000, self.gc)

        # Let's do some styling of the tab widget when no tabs are opened
        if self.mainTabs.currentIndex() == -1:
            self.__setTabWidgetStyle(self.lumaHeadStyle)

    def gc(self):
        """Runs Python's garbage-collection manually.
        Used to make sure circular references are taken care of *now*.
        """
        gc.collect()

    def showWelcome(self):
        """Shows the Welcome-tab
        """
        self.__setTabWidgetStyle(self.defaultTabStyle)
        index = self.mainTabs.addTab(self.welcomeTab,
        QApplication.translate("MainWindow", "Welcome"))

        self.mainTabs.setCurrentIndex(index)
        self.actionShowWelcomeTab.setEnabled(False)

    def showPlugins(self):
        """Will show the pluginlistwidget-tab
        """
        self.__setTabWidgetStyle(self.defaultTabStyle)
        if self.mainTabs.indexOf(self.pluginWidget) == -1:
            index = self.mainTabs.addTab(self.pluginWidget, QApplication.translate("MainWindow", "Plugins"))
            self.mainTabs.setCurrentIndex(index)
            self.actionShowPluginList.setEnabled(False)

    def closeEvent(self, e):
        """Overrides the ``QMainWindow.closeEvent`` slot to save
        settings before we tear down the application.
        """
        self.__writeSettings()

        from PyQt4.QtCore import QThreadPool
        if QThreadPool.globalInstance().activeThreadCount() > 0:
            print QApplication.translate("MainWindow", "There are operations in progress which needs to finish before Luma can close.")
            print "Waiting for: " + str(QThreadPool.globalInstance().activeThreadCount()) + " operations."
        QMainWindow.closeEvent(self, e)


class LumaEventFilter(QObject):
    """An Event handler for the Luma Main application.
    
    To act upon widget events, install an instance of this class with
    the target widget, and add the capture logic in the eventFilter
    method.
    """

    def eventFilter(self, target, event):
        """
        Parameters:
        
        - `target`: a QObject that contains the target widget, i.e the
          widget that got the handler installed.
        - `event`: the QEvent event to act upon.
        """
        if event.type() == QEvent.KeyPress:
            # If we have a match on the QKeySequence we're looking for
            # we keep things safe by explicitly checking if the target
            # is the correct for our purpose.
            # In the case of the Search plugin, only the tab widget for
            # the search results ('right') is expected to act upon the
            # close event.
            if target.objectName() == 'mainTabs':
                index = target.currentIndex()
                if event.matches(QKeySequence.Close):
                    target.tabCloseRequested.emit(index)
                    # When we actually catches and acts upon an event,
                    # we need to inform the eventHandler about this.
                    return True

        # All events we didn't act upon must be forwarded        
        return QObject.eventFilter(self, target, event)


class LoggerWidget(QWidget, Ui_LoggerWidget):
    """The Luma logger window.
    
    This widget contains a text field where the LumaLogHandler is
    writing it's log messages to. The widget also provides options
    to filter the log based on the loglevel on messages.
    """

    logSignal = pyqtSignal(QString)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.clearButton.setIcon(iconFromTheme(
            'edit-clear', ':icons/32/edit-clear'))

        self.logList = []

        # log() can be called by any thread, so to append the message
        # to the loggerwidget, we emit it and have the owner of the textfield
        # (the gui thread) receive it and do the appending.
        self.logSignal.connect(self.appendMsg)

    def clearLogger(self):
        """
        Clears the logwindow. Currently the loglist is deleted when this
        method is called.
        """
        self.logList = []
        self.messageEdit.clear()

    def rebuildLog(self):
        """
        This method is called when on of the checkboxes indicates new
        filter state.
        """
        self.messageEdit.clear()
        # Filter out unwanted log-items
        for l in self.logList:
            self.log(l, rebuild = True)

    @pyqtSlot(QString)
    def appendMsg(self, msg):
        """
        For thread-safety: this is executed in the thread
        which owns the loggerwidget, ie. the gui-thread
        """
        self.messageEdit.append(msg)

    def log(self, log, rebuild = False):
        """
        Appends the log the the logList
        and uses a signal in order to have it 
        be appended to the textfield by the gui-thread
        """
        loglvl, msg, name, threadName = log
        if not rebuild:
            self.logList.append(log)
        if loglvl == "DEBUG" and self.debugBox.isChecked():
            self.logSignal.emit("DEBUG ["+name+"/"+threadName+"]: " + msg)
            return
        if loglvl == "ERROR" and self.errorBox.isChecked():
            self.logSignal.emit("ERROR: " + msg)
            return
        if loglvl == "INFO" and self.infoBox.isChecked():
            self.logSignal.emit("INFO: " + msg)
            return
        if loglvl not in ["INFO", "ERROR", "DEBUG"]:
            # This shouldn't really happen...
            # Please only use the above levels
            self.logSignal.emit("UNKNOWN: " + msg)


class PluginToolBar(QToolBar):
    """The plugin toolbar.
    
    Provides a toolbar for quickly switching between installed plugins
    
    The button will be enabled and disabled directly from main-win,
    and the label for the plugin-name too.
    """

    def __init__(self, parent=None):
        QToolBar.__init__(self, parent)
        self.parent = parent
        self.setupUi()

    def setupUi(self):
        font = QFont()
        font.setBold(True)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label.setFont(font)
        self.label.setMargin(5)
        self.addWidget(self.label)
        self.button = QPushButton(self)
        self.addWidget(self.button)
        self.retranslateUi(self)

        self.button.clicked.connect(self.choosePlugin)

    def retranslateUi(self, pluginToolBar):
        pluginToolBar.label.setText(QApplication.translate('MainWindow', 'Available plugins', None, QApplication.UnicodeUTF8))
        pluginToolBar.button.setText(QApplication.translate('MainWindow', 'Choose plugin', None, QApplication.UnicodeUTF8))

    def choosePlugin(self):
        if hasattr(self.parent, "showPlugins"):
            self.parent.showPlugins()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
