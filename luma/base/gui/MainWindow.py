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

from PyQt4.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt4.QtCore import QEvent, QString, QTimer
from PyQt4.QtCore import QTranslator

from PyQt4.QtGui import QAction, QActionGroup, QApplication, qApp
from PyQt4.QtGui import QDockWidget, QMenu
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QToolBar
from PyQt4.QtGui import QWidget

from ..backend.ServerList import ServerList
from ..gui.AboutDialog import AboutDialog
from ..gui.ServerDialog import ServerDialog
from ..gui.Settings import Settings
from ..gui.SettingsDialog import SettingsDialog
from ..gui.design.LoggerWidgetDesign import Ui_LoggerWidget
from ..gui.design.MainWindowDesign import Ui_MainWindow
from ..util.i18n import LanguageHandler
from ..util.gui.PluginListWidget import PluginListWidget
from ..gui.WelcomeTab import WelcomeTab


class MainWindow(QMainWindow, Ui_MainWindow):
    """ The Main window of Luma.
    """

    DEVEL = True

    logger = logging.getLogger(__name__)
    languages = {}
    translator = None
    languageHandler = None
    currentLanguage = ''

    def __init__(self, parent=None):
        """ The constructor sets up the MainWindow widget, 
        and connects all necessary signals and slots
        """
        super(MainWindow, self).__init__(parent)

        self.translator = QTranslator()
        self.languageHandler = LanguageHandler()
        self.languages = self.languageHandler.availableLanguages
        self.setupUi(self)

        self.setWindowIcon(QIcon(':/icons/luma-16'))

        self.__createPluginToolBar()
        self.__createLoggerWidget()
        self.__loadSettings()
        self.__createLanguageOptions()

        self.setStatusBar(self.statusBar)
        
        self.mainTabs.setTabsClosable(True)
        self.mainTabs.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mainTabs.customContextMenuRequested.connect(self.__mainTabsContextMenu)
    
        #Sets up pluginWidget
        #self in parameter is used to call pluginSelected here...
        self.pluginWidget = PluginListWidget(self)
        self.showPlugins()
        self.welcomeTab = WelcomeTab()

        stylesheet = 'background: url(:/icons/luma-gray);\n' + \
                     'background-position: bottom right;\n' + \
                     'background-attachment: fixed;\n' + \
                     'background-repeat:  no-repeat;'

        self.welcomeTab.textBrowser.setStyleSheet(stylesheet)
        

        #This value comes from __loadSettings()
        #Its a checkbox set in WelcomeTab
        if self.showWelcomeSettings == 2:
            self.showWelcome()
        else:
            # Let's do some styling of the tab widget when no tabs are opened
            if self.mainTabs.currentIndex() == -1:
                stylesheet = 'background: url(:/icons/luma-gray);\n' + \
                             'background-position: bottom right;\n' + \
                             'background-attachment: fixed;\n' + \
                             'background-repeat:  no-repeat;'
                self.__setTabWidgetStyle(stylesheet)

            self.actionShowWelcomeTab.setEnabled(True)
            
    def __mainTabsContextMenu(self, pos):
        menu = QMenu()
        if self.mainTabs.count() > 0:
            return # The menu is displayed even when the rightclick is not done over the actual tabs
            # so to avoid confusion the function is disabled entirey
            #menu.addAction(QApplication.translate("MainWindow", "Close all plugin-tabs"), self.tabCloseAll)
        else:
            # If there's no tabs, offer to display the pluginlist
            menu.addAction(self.actionShowPluginList)
        menu.exec_(self.mainTabs.mapToGlobal(pos))
        
    def __createPluginToolBar(self):
        """ Creates the pluign toolbar.
        """
        self.pluginToolBar = PluginToolBar(self)
        self.pluginToolBar.setWindowTitle(QApplication.translate('MainWindow', 'Plugintoolbar', None, QApplication.UnicodeUTF8))
        self.pluginToolBar.setObjectName('pluginToolBar')
        self.addToolBar(self.pluginToolBar)
        self.pluginToolBar.hide()

    def __createLoggerWidget(self):
        """ Creates the logger widget.
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
        """ Creates the language selection in the menubar.
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
        """ Loads settings from file.
        
        @param mainWin: boolean values;
            If set to false, neither the values for the window size or
            the window position will be loaded. This is i.e done when
            the settings dialog returns 1.
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
        self.actionShowLogger.setChecked(settings.showLoggerOnStart)
        self.loggerWidget.errorBox.setChecked(settings.showErrors)
        self.loggerWidget.debugBox.setChecked(settings.showDebug)
        self.loggerWidget.infoBox.setChecked(settings.showInfo)

        self.toggleLoggerWindow(self.actionShowLogger.isChecked())

        # Language
        self.loadLanguage(settings.language)

        #Tabs
        self.showWelcomeSettings = settings.value("showWelcome", 2).toInt()[0]

    def __writeSettings(self):
        """ Save settings to file.
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

        # Logger
        settings.showLoggerOnStart = self.actionShowLogger.isChecked()
        settings.showErrors = self.loggerWidget.errorBox.isChecked()
        settings.showDebug = self.loggerWidget.debugBox.isChecked()
        settings.showInfo = self.loggerWidget.infoBox.isChecked()

        # Language
        settings.language = self.currentLanguage

        # Plugins """
        self.TODO(u'write settings%s' % self.__class__)

    def __switchTranslator(self, translator, qmFile):
        """ Called when a new language is loaded.
        
        @param translator:
            The translator object to install.
        @param qmFile:
            The translation file for the loaded language.
        """
        qApp.removeTranslator(translator)
        if translator.load(qmFile):
            qApp.installTranslator(translator)

    def __setTabWidgetStyle(self, stylesheet):
        self.mainTabs.setStyleSheet(stylesheet)

    @pyqtSlot('QAction*')
    @pyqtSlot(int)
    def languageChanged(self, value):
        """ This slot is called by actions and signals related to 
        application translations. The slot contains validation for
        those parameters defined by the pyqtSlot meta info in the
        method header.
        
        @param value:
            Can be either a QAction or a integer value. I.e. menu
            actions provide QActions and a QCombobox might send it's
            index. 
        """
        isoCode = None
        if isinstance(value, int):
            isoCode = self.languageSelector.itemData(value).toString()
        elif isinstance(value, QAction):
            isoCode = value.data().toString()
        #else:
        #    isoCode = value
        if isoCode:
            self.loadLanguage(isoCode)

    def loadLanguage(self, isoCode):
        """ Loads a language by the given language iso code.
        
        @param isoCode: 
            A 2 char language code as defined by the ISO 638-1 standard.
        """
        if self.currentLanguage != isoCode:
            self.currentLanguage = isoCode
            qmFile = self.languageHandler.getQmFile(isoCode)
            self.__switchTranslator(self.translator, qmFile)

    def changeEvent(self, event):
        """ This event is called when a new translator is loaded or the
        system language (locale) is changed.
        
        @param event:
            The event that generated the method call.
        """
        if None != event:
            type = event.type()
            if QEvent.LanguageChange == type:
                self.retranslateUi(self)
                self.pluginToolBar.retranslateUi(self.pluginToolBar)
                self.loggerWidget.retranslateUi(self.loggerWidget)
            elif QEvent.LocaleChange == type:
                print u'System Locale changed'

    def showAboutLuma(self):
        """ Slot for displaying the about dialog.
        """
        AboutDialog().exec_()

    @pyqtSlot(bool)
    def toggleLoggerWindow(self, show):
        """ Slot for toggling the logger window.
        
        @param show: boolean value;
            If True the logger window will be shown,
            If False it will be hidden.
        """
        if show:
            self.loggerDockWindow.show()
        else:
            self.loggerDockWindow.hide()

    @pyqtSlot(bool)
    def toggleToolbar(self, show):
        """ Slot for toggling the plugin toolbar.
        
        @param show: boolean value;
            If True the plugin toolbar will be shown,
            If False it will be hidden.
        """
        if show:
            self.pluginToolBar.show()
        else:
            self.pluginToolBar.hide()

    @pyqtSlot(bool)
    def toggleStatusbar(self, show):
        """ Slot for toggling the logger window.
        
        @param show: boolean value;
            If True the statusbar will be shown,
            if False it will be hidden.
        """
        if show:
            self.statusBar.show()
        else:
            self.statusBar.hide()

    @pyqtSlot(bool)
    def toggleFullscreen(self, fullscreen):
        """
        Slot for toggling the logger window.
        
        @param fullscreen: boolean value;
            If True the application will enter fullscreen mode,
            if False it will enter normal mode.
        """
        if fullscreen:
            self.showFullScreen()
        else:
            self.showNormal()

    def showServerEditor(self):
        """
        Slot to display the server editor dialog.
        """
        serverEditor = ServerDialog(ServerList())
        serverEditor.exec_()

    def showSettingsDialog(self, tab=0):
        """ Slot to display the settings dialog. If the settings dialog
        returns 1, i.e. the user has clicked the ok button, the
        loadSettings method is called with mainWin=False, to load the 
        (assumed) newly changed settings.
        
        @param tab:
            The index of the tab to display in the settings dialog. 
        """
        settingsDialog = SettingsDialog(self.currentLanguage, self.languages)
        settingsDialog.tabWidget.setCurrentIndex(tab)
        if settingsDialog.exec_():
            # We assume that some settings is changed 
            # if the user clicked the ok button, and
            # reloads the application settings
            self.__loadSettings(mainWin=False)
            self.reloadPlugins()
            # A Hack but it'll do for now
            for a in self.langGroup.actions():
                if a.data().toString() == self.currentLanguage:
                    a.setChecked(True)

    def configurePlugins(self):
        """ Slot to display the plugins configuration. This currently
        calls showSettingsDialog with tab index set to 2.
        """
        self.showSettingsDialog(2)

    def reloadPlugins(self):
        """ Slot to reload plugins.
        """
        self.pluginWidget.updatePlugins()

    def loadPlugins(self):
        """ Hmmm...
        """
        self.showPlugins()

    def pluginSelected(self, item):
        """ 
        This method will be called from the PluginListWidget.
        """
        # Clear the stylesheet when a tab is opened
        self.__setTabWidgetStyle('')

        widget = item.plugin.getPluginWidget(None, self)
        
        index = self.mainTabs.addTab(widget, item.icon(), item.plugin.pluginUserString)
        self.mainTabs.setCurrentIndex(index)

    def tabClose(self, index):
        """ 
        Slot for the signal tabCloseRequest(int) for the tabMains
        """

        widget = self.mainTabs.widget(index)
        if widget == self.pluginWidget:
            self.actionShowPluginList.setEnabled(True)

        if widget == self.welcomeTab:
            self.actionShowWelcomeTab.setEnabled(True)

        self.mainTabs.removeTab(index)

        #Unparent the widget since it was reparented by the QTabWidget so it's gargabe collected
        widget.setParent(None)

        #Done automatically by PyQt since there's no refs to the widget
        #widget.deleteLater()

        # In case the widget contained circular references -- force GC to take care of the objects
        # since there can be quite many if it was BrowserWidget that was closed
        # Can't call it directly since that'll be too soon
        QTimer.singleShot(0, self.gc)

        # Let's do some styling of the tab widget when no tabs are opened
        if self.mainTabs.currentIndex() == -1:
            stylesheet = 'background: url(:/icons/luma-gray);\n' + \
                         'background-position: bottom right;\n' + \
                         'background-repeat:  no-repeat;'
            self.__setTabWidgetStyle(stylesheet)

    def gc(self):
        gc.collect()

    def showWelcome(self):
        self.__setTabWidgetStyle('')
        index = self.mainTabs.addTab(self.welcomeTab,
        QApplication.translate("MainWindow", "Welcome"))

        self.mainTabs.setCurrentIndex(index)
        self.actionShowWelcomeTab.setEnabled(False)
        
    def showPlugins(self):
        """ Will set the pluginlistwidget on top of the mainstack.
        """
        
        self.__setTabWidgetStyle('')
        if self.mainTabs.indexOf(self.pluginWidget) == -1:
            index = self.mainTabs.addTab(self.pluginWidget, QApplication.translate("MainWindow", "Plugins"))
            self.mainTabs.setCurrentIndex(index)
            self.actionShowPluginList.setEnabled(False)

        else:
            """TODO: REMOVE THIS """
            self.logger.debug("Johannes fix: linje 438")

    def closeEvent(self, e):
        """ Overrides the QMainWindow closeEvent slot to save settings
        before we tear down the application.
        """
        self.__writeSettings()
        QMainWindow.closeEvent(self, e)

    def TODO(self, todo):
        """ Helper method for displaying special TODO debug messages.
        The TODO message is prefixed with <[TODO]> and suffixed with
        <self.__class__>
        
        @param todo:
            The todo message to display in the logger window.
        """
        self.logger.debug(u'[TODO] %s%s' % (todo, str(self.__class__)))


class LoggerWidget(QWidget, Ui_LoggerWidget):
    """ The Luma logger window.
    
    This widget contains a text field where the LumaLogHandler is
    writing it's log messages to. The widget also provides options
    to filter the log based on the loglevel on messages.
    """

    logSignal = pyqtSignal(QString)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.logList = []

        # log() can be called by any thread, so to append the message
        # to the loggerwidget, we emit it and have the owner of the textfield
        # (the gui thread) receive it and do the appending.
        self.logSignal.connect(self.appendMsg, type=Qt.QueuedConnection)

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
        for l in self.logList:
            loglvl, msg = l
            if loglvl == "DEBUG" and self.debugBox.isChecked():
                self.messageEdit.append("DEBUG: " + msg)
                continue
            if loglvl == "ERROR" and self.errorBox.isChecked():
                self.messageEdit.append("ERROR: " + msg)
                continue
            if loglvl == "INFO" and self.infoBox.isChecked():
                self.messageEdit.append("INFO: " + msg)
                continue

    @pyqtSlot(QString)
    def appendMsg(self, msg):
        """
        For thread-safety: this is executed in the thread
        which owns the loggerwidget, ie. the gui-thread
        """
        self.messageEdit.append(msg)

    def log(self, log):
        """
        Appends the log the the logList
        and uses a signal in order to have it 
        be appended to the textfield by the gui-thread
        """
        loglvl, msg = log
        self.logList.append(log)
        if loglvl == "DEBUG" and self.debugBox.isChecked():
            #self.logList.append(log)
            self.logSignal.emit("DEBUG: " + msg)
            #self.messageEdit.append("DEBUG: " + msg)
            return
        if loglvl == "ERROR" and self.errorBox.isChecked():
            #self.logList.append(log)
            #self.messageEdit.append("ERROR: " + msg)
            self.logSignal.emit("ERROR: " + msg)
            return
        if loglvl == "INFO" and self.infoBox.isChecked():
            #self.logList.append(log)
            #self.messageEdit.append("INFO: " + msg)
            self.logSignal.emit("INFO: " + msg)
            return
        if loglvl not in ["INFO", "ERROR", "DEBUG"]:
            # This shouldn't really happen...
            # Please only use the above levels
            #self.logList.append(log)
            #self.messageEdit.append("UNKNOWN: " + msg)
            self.logSignal.emit("UNKNOWN: " + msg)


class PluginToolBar(QToolBar):
    """ The plugin toolbar.
    
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

