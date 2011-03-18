# -*- coding: utf-8 -*-
#
# base.gui.Window
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/
import logging

from PyQt4.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt4.QtCore import QEvent, QString
from PyQt4.QtCore import QTranslator

from PyQt4.QtGui import QAction, QActionGroup, QApplication, qApp
from PyQt4.QtGui import QDockWidget
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QToolBar
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QProgressBar

from ..backend.ServerList import ServerList
from ..gui.Settings import Settings
from ..gui.Dialog import AboutDialog, ServerDialog, SettingsDialog
from ..gui.LoggerWidgetDesign import Ui_LoggerWidget
from ..gui.MainWindowDesign import Ui_MainWindow
from ..util.i18n import LanguageHandler
from ..util.gui.PluginListWidget import PluginListWidget

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    The Main window of Luma.
    """

    DEVEL = True

    logger = logging.getLogger(__name__)
    languages = {}
    translator = None
    languageHandler = None
    currentLanguage = ''

    def __init__(self, configPrefix, parent=None):
        """
        The constructor sets up the MainWindow widget, 
        and connects all necessary signals and slots
        """
        super(MainWindow, self).__init__(parent)

        self.translator = QTranslator()
        self.languageHandler = LanguageHandler()
        self.languages = self.languageHandler.availableLanguages
        self.configPrefix = configPrefix
        self.setupUi(self)

        self.setWindowIcon(QIcon(':/icons/luma-16'))

        self.__createPluginToolBar()
        self.__createLoggerWidget()
        self.__loadSettings()
        self.__setupPluginList()
        self.__createLanguageOptions()

        self.progressBar = QProgressBar()
        #self.progressBar.setRange(0,0)
        self.progressBar.setTextVisible(False)
        self.statusBar.addPermanentWidget(self.progressBar)

        #TODO REMOVE
        #qApp.postEvent(qApp, QEvent(QEvent.User))

        if self.DEVEL:
            self.actionEditServerList.setStatusTip(
                u'Final GUI polishing by Granbusk\u2122 Polishing')
    def getProgressBar(self):
        return self.progressBar

    def __setupPluginList(self):
        """
        self.pluginDockWindow = QDockWidget(self)
        self.pluginDockWindow.setWindowTitle(
             QApplication.translate(
                "MainWindow", "Plugin list", None, QApplication.UnicodeUTF8))
        self.pluginWidget = PluginListWidget()
        self.pluginDockWindow.setWidget(self.pluginWidget) 
        self.addDockWidget(Qt.TopDockWidgetArea, self.pluginDockWindow)
        """

        self.pluginWidget = PluginListWidget(self)
        self.mainStack.addWidget(self.pluginWidget)
        self.showPlugins()

    def __createPluginToolBar(self):
        """
        Creates the pluign toolbar.
        """
        self.pluginToolBar = PluginToolBar(self)
        self.addToolBar(self.pluginToolBar)
        self.pluginToolBar.hide()

    def __createLoggerWidget(self):
        """
        Creates the logger widget.
        """
        self.loggerDockWindow = QDockWidget(self)
        self.loggerDockWindow.visibilityChanged[bool].connect(self.actionShowLogger.setChecked)
        self.loggerDockWindow.setWindowTitle(QApplication.translate('MainWindow', 'Logger', None, QApplication.UnicodeUTF8))
        self.loggerWidget = LoggerWidget(self.loggerDockWindow)
        self.loggerDockWindow.setWidget(self.loggerWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.loggerDockWindow)
        self.loggerDockWindow.hide()

    def __createLanguageOptions(self):
        """
        Creates the language selection in the menubar.
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
        """
        Loads settings from file.
        
        @param mainWin: If set to false, neither the values for the window
                        size or the window position will be loaded. This 
                        is i.e done when the settings dialog returns 1.
        """
        settings = Settings()
        """ General Mainwin"""
        if mainWin:
            self.resize(settings.size)
            self.move(settings.position)
            if settings.maximize:
                self.showMaximized()
                
        """ Logger """
        self.actionShowLogger.setChecked(settings.showLoggerOnStart)
        self.loggerWidget.errorBox.setChecked(settings.showErrors)
        self.loggerWidget.debugBox.setChecked(settings.showDebug)
        self.loggerWidget.infoBox.setChecked(settings.showInfo)

        self.toggleLoggerWindow(self.actionShowLogger.isChecked())

        """ Language """
        self.loadLanguage(settings.language)

        """ Plugins """
        self.TODO(u'load settings[plugins]%s' % str(self.__class__))

    def __writeSettings(self):
        """
        Save settings to file.
        """
        settings = Settings()

        """ Mainwin """
        max = self.isMaximized()
        settings.maximize = max
        if not max:
            settings.size = self.size()
            settings.position = self.pos()

        """ Logger """
        settings.showLoggerOnStart = self.loggerDockWindow.isVisibleTo(self)
        settings.showErrors = self.loggerWidget.errorBox.isChecked()
        settings.showDebug = self.loggerWidget.debugBox.isChecked()
        settings.showInfo = self.loggerWidget.infoBox.isChecked()

        """ Language """
        settings.language = self.currentLanguage

        """ Plugins """
        self.TODO(u'write settings%s' % self.__class__)

    @pyqtSlot('QAction*')
    @pyqtSlot(int)
    def languageChanged(self, value):
        """
        This slot is called by actions and signals related to application
        translations. The slot contains validation for those parameters 
        defined by the pyqtSlot meta info in the method header.
        
        @param value: Can be either a QAction or a integer value.
                      I.e. menu actions provide QActions and a QCombobox
                      might send it's index. 
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
        """
        Loads a language by the given language iso code.
        
        @param isoCode: A legal 2 char language code defined by the 
                        ISO 638-1 standard.
        """
        if self.currentLanguage != isoCode:
            self.currentLanguage = isoCode
            qmFile = self.languageHandler.getQmFile(isoCode)
            self.__switchTranslator(self.translator, qmFile)

    def changeEvent(self, event):
        """
        This event is called when a new translator is loaded or the system
        language (locale) is changed.
        
        @param event: The event that generated the method call.
        """
        if None != event:
            type = event.type()
            if QEvent.LanguageChange == type:
                self.retranslateUi(self)
                self.pluginToolBar.retranslateUi(self.pluginToolBar)
                self.loggerWidget.retranslateUi(self.loggerWidget)
            elif QEvent.LocaleChange == type:
                print u'System Locale changed'

    def __switchTranslator(self, translator, qmFile):
        """
        Called when a new language is loaded.
        
        @param translator: The translator object to install.
        @param qmFile:     The translation file for the loaded language.
        """
        qApp.removeTranslator(translator)
        if translator.load(qmFile):
            qApp.installTranslator(translator)

    def showAboutLuma(self):
        """
        Slot for displaying the about dialog.
        """
        AboutDialog().exec_()

    @pyqtSlot(bool)
    def toggleLoggerWindow(self, show):
        """
        Slot for toggling the logger window.
        
        @param show: boolean value;
            If true the logger window will be shown, if false it will be
            hidden.
        """
        if show:
            self.loggerDockWindow.show()
        else:
            self.loggerDockWindow.hide()

    @pyqtSlot(bool)
    def toggleToolbar(self, show):
        """
        Slot for toggling the plugin toolbar.
        
        @param show: boolean value;
            If true the plugin toolbar will be shown, if false it will be
            hidden.
        """
        if show:
            self.pluginToolBar.show()
        else:
            self.pluginToolBar.hide()
    
    @pyqtSlot(bool)
    def toggleStatusbar(self, show):
        """
        Slot for toggling the logger window.
        
        @param show: boolean value;
            If true the statusbar will be shown, if false it will be hidden.
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
            If true the application will enter fullscreen mode, if false
            it wil enter normal mode.
        """
        if fullscreen:
            self.showFullScreen()
        else:
            self.showNormal()

    def showServerEditor(self):
        """
        Slot to display the server editor dialog.
        """
        self.logger.debug(self.configPrefix)
        serverEditor = ServerDialog(ServerList(configPrefix=self.configPrefix))
        serverEditor.exec_()

    def showSettingsDialog(self, tab=0):
        """
        Slot to display the settings dialog. If the settings dialog returns
        1, i.e. the user has clicked the ok button, the loadSettings method
        is called with mainWin=False, to load the (assumed) newly changed 
        settings.
        
        @param tab: The index of the tab to display in the settings dialog. 
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
        """
        Slot to display the plugins configuration. This currently calls
        showSettingsDialog with tab index set to 2.
        """
        self.showSettingsDialog(2)

    def reloadPlugins(self):
        """
        Slot to reload plugins.
        """
        self.pluginWidget.updatePlugins()

    def loadPlugins(self):
        """
        Hmmm...
        """
        self.showPlugins()

    def pluginSelected(self, item):
        """
        This method will be called from the PluginListWidget.
        """
        widget = item.widget
        if self.mainStack.indexOf(widget) == -1:
            self.mainStack.addWidget(widget)

        if self.mainStack.currentWidget() != widget:
            self.mainStack.setCurrentWidget(widget)

            if self.pluginToolBar:
                self.pluginToolBar.button.setEnabled(True)
                self.pluginToolBar.label.setText(QApplication.translate('MainWindow', item.plugin.pluginUserString, None, QApplication.UnicodeUTF8))

                #The plugin-toolbar should be inside the getPluginWidget
                #This should maybe be required by the PluginLoader, to have this in the __init__.py for a plugin

                self.logger.debug("Trying to build toolbar for plugin")

                if hasattr(widget, "toolbarActions"):
                    try:
                        for action in widget.toolbarActions():
                            self.pluginToolbar.addAction(action)
                    except Exception:
                        self.logger.error("Could not append actions to toolbar from plugin")
                        pass
                else:
                    self.logger.debug("No actions to add to toolbar from plugin")

    def showPlugins(self):
        """
        Will set the pluginlistwidget on top of the mainstack.
        """

        if self.pluginWidget and self.mainStack.currentWidget() != self.pluginWidget:
            self.mainStack.setCurrentWidget(self.pluginWidget)

            if self.pluginToolBar:
                self.pluginToolBar.button.setEnabled(False)
                self.pluginToolBar.label.setText(QApplication.translate('MainWindow', "Available plugins", None, QApplication.UnicodeUTF8))

    def close(self):
        """
        Overrides the QApplication close slot to save settings before
        we tear down the application.
        """
        self.__writeSettings()
        qApp.quit()

    def TODO(self, todo):
        """
        Helper method for displaying special TODO debug messages.
        
        @param todo: The todo message to display in the logger window.
                     The message is prefixed with <[TODO]> and suffixed
                     with the <self.__class__>
        """
        self.logger.debug(u'[TODO] %s%s' % (todo, str(self.__class__)))


class LoggerWidget(QWidget, Ui_LoggerWidget):
    """
    The Luma logger window.
    
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
        For thread-safety: this is executed in the threadq
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
        if loglvl == "DEBUG" and self.debugBox.isChecked():
            self.logList.append(log)
            self.logSignal.emit("DEBUG: " + msg)
            #self.messageEdit.append("DEBUG: " + msg)
            return
        if loglvl == "ERROR" and self.errorBox.isChecked():
            self.logList.append(log)
            #self.messageEdit.append("ERROR: " + msg)
            self.logSignal.emit("ERROR: " + msg)
            return
        if loglvl == "INFO" and self.infoBox.isChecked():
            self.logList.append(log)
            #self.messageEdit.append("INFO: " + msg)
            self.logSignal.emit("INFO: " + msg)
            return
        if loglvl not in ["INFO", "ERROR", "DEBUG"]:
            # This shouldn't really happen...
            # Please only use the above levels
            self.logList.append(log)
            #self.messageEdit.append("UNKNOWN: " + msg)
            self.logSignal.emit("UNKNOWN: " + msg)


class PluginToolBar(QToolBar):
    """
    The plugin toolbar.
    
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