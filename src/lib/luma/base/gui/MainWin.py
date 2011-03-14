# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.no>
#     Christian Forfang, <cforfang@gmail.com>
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
This module contains several Luma GUI classes:

MainWindow:
    The Luma main window.

LoggerWidget:
    A dockable loggerwidget used by MainWindow.

PluginToolBar:
    A toolbar widget for quick plugin access.

SettingsDialog:
    A dialog for accessing and setting variuos application settings.

AboutDialog:
    A simple about dialog, including credits and license.
"""
import sys
import logging
from random import randint

from PyQt4.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt4.QtCore import QEvent, QString
from PyQt4.QtCore import QTranslator

from PyQt4.QtGui import QAction, QActionGroup, QApplication, qApp
from PyQt4.QtGui import QDialog, QDockWidget
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QLabel, QListWidget
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QStandardItem, QStandardItemModel
from PyQt4.QtGui import QToolBar
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QProgressBar

from base.backend.ServerList import ServerList
from base.gui import Settings
from base.gui.AboutDialogDesign import Ui_AboutDialog
from base.gui.AboutLicenseDesign import Ui_AboutLicense
from base.gui.AboutCreditsDesign import Ui_AboutCredits
from base.gui.LoggerWidgetDesign import Ui_LoggerWidget
from base.gui.MainWinDesign import Ui_MainWindow
from base.gui.PluginSettings import PluginSettings
from base.gui.SettingsDialogDesign import Ui_SettingsDialog
from base.gui.ServerDialog import ServerDialog
from base.util import LanguageHandler
from base.util.gui.PluginListWidget import PluginListWidget
from base.model.PluginSettingsModel import PluginSettingsModel




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

    def __init__(self, parent=None):
        QMainWindow.__init__(self)

        self.translator = QTranslator()
        self.languageHandler = LanguageHandler()
        self.languages = self.languageHandler.availableLanguages
        self.setupUi(self)
        
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
#        s = QSettings(qApp.organizationName(), qApp.applicationName())
#        
#        s.beginGroup(u'mainwin')
#        self.resize(s.value(u'size').toSize())
#        self.move(s.value(u'position').toPoint())
#        s.endGroup()
#        
#        s.beginGroup(u'logger')
#        self.actionShowLogger.setChecked(s.value('show_on_start').toBool())
#        self.loggerWidget.errorBox.setChecked(s.value('show_errors').toBool())
#        self.loggerWidget.debugBox.setChecked(s.value('show_debug').toBool())
#        self.loggerWidget.infoBox.setChecked(s.value('show_info').toBool())
#        s.endGroup()
#        
#        s.beginGroup(u'i18n')
#        self.loadLanguage(s.value(u'language').toString())
#        s.endGroup()

        settings = Settings()
        """ General Mainwin"""
        if mainWin:
            self.resize(settings.size)
            self.move(settings.position)

        """ Logger """
        self.actionShowLogger.setChecked(settings.showLoggerOnStart)
        self.loggerWidget.errorBox.setChecked(settings.showErrors)
        self.loggerWidget.debugBox.setChecked(settings.showDebug)
        self.loggerWidget.infoBox.setChecked(settings.showInfo)

        self.showLoggerWindow(self.actionShowLogger.isChecked())

        """ Language """
        self.loadLanguage(settings.language)

        """ Plugins """
        self.TODO(u'load settings[plugins]%s' % str(self.__class__))


    def writeSettings(self):
        """
        Save settings to file.
        """
#        s = QSettings(qApp.organizationName(), qApp.applicationName())
#        
#        s.beginGroup(u'mainwin')
#        s.setValue(u'size', self.size())
#        s.setValue(u'position', self.pos())
#        s.endGroup()
#        
#        s.beginGroup(u'logger')
#        s.setValue(u'show_on_start', self.actionShowLogger.isChecked())
#        s.setValue(u'show_errors', self.loggerWidget.errorBox.isChecked())
#        s.setValue(u'show_debug', self.loggerWidget.debugBox.isChecked())
#        s.setValue(u'show_info', self.loggerWidget.infoBox.isChecked())
#        s.endGroup()
#        
#        s.beginGroup(u'i18n')
#        s.setValue(u'language', self.currentLanguage)
#        s.endGroup()

        settings = Settings()

        """ Mainwin """
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
            self.switchTranslator(self.translator, qmFile)


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


    def switchTranslator(self, translator, qmFile):
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
    def showLoggerWindow(self, show):
        """
        Slot for toggling the logger window.
        
        @param show: If true the logger window will be shown, if false
                     it will be hidden.
        """
        if show:
            self.loggerDockWindow.show()
        else:
            self.loggerDockWindow.hide()


    def showServerEditor(self):
        """
        Slot to display the server editor dialog.
        """
        serverEditor = ServerDialog(ServerList(u'/tmp'))
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
                    except Exception, e:
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
        self.writeSettings()
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
        self.logSignal.connect(self.appendMsg, type = Qt.QueuedConnection)


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

class SettingsDialog(QDialog, Ui_SettingsDialog):
    """
    The application settings dialog
    
    Contains all the application settings.
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, currentLanguage, languages={}, parent=None):
        """
        The constructor must be given the currentLanguage from the
        Main window to keep things synchronized.
        
        currentLanguage
            the currently selected language in the main window
        
        languages [optional]
            a list of available languages. Might want to provide this
            from the main window as it's already loaded.
        """
        QDialog.__init__(self)
        self.setupUi(self)
        self.languages = languages
        self.currentLanguage = currentLanguage
        if self.currentLanguage == {}:
            """ If the list of languages is empty we fetch the list
            with the LanguageHelper. """
            lh = LanguageHandler()
            self.currentLanguage = lh.availableLanguages
        self.loadSettings()


    def loadSettings(self):
        """
        Loads the application settings from file.
        """
        settings = Settings()

        """ Logging """
        self.showLoggerOnStart.setChecked(settings.showLoggerOnStart)
        self.showErrors.setChecked(settings.showErrors)
        self.showDebug.setChecked(settings.showDebug)
        self.showInfo.setChecked(settings.showInfo)
        
        
        """ Language """
        self.languageSelector
        i = 0
        for key, name in self.languages.iteritems():
            self.languageSelector.addItem('%s [%s]' % (name[0], key), key)
            if key == self.currentLanguage:
                self.languageSelector.setCurrentIndex(i)
            i = i + 1


        """ Plugins """
        self.pluginListView.setModel(PluginSettingsModel())

    def pluginSelected(self, index):
        """
        If a plugin has a pluginsettingswidget,
        it will be put into the QStackedWidget.
        """
        
        plugin = self.pluginListView.model().itemFromIndex(index).plugin
        
        widget = plugin.getPluginSettingsWidget(self.pluginSettingsStack)
    
        if not widget:
            return
         
        if self.pluginSettingsStack.indexOf(widget) == -1:
            self.pluginSettingsStack.addWidget(widget)
        
        if self.pluginSettingsStack.currentWidget() != widget:
            self.pluginSettingsStack.setCurrentWidget(widget)
    
    
    def saveSettings(self):
        """
        This slot is called when the ok button is clicked.
        It saves the selected settigns to file.
        """
        settings = Settings()

        """ Logging """
        settings.showLoggerOnStart = self.showLoggerOnStart.isChecked()
        settings.showErrors = self.showErrors.isChecked()
        settings.showDebug = self.showDebug.isChecked()
        settings.showInfo = self.showInfo.isChecked()

        """ Language """
        i = self.languageSelector.currentIndex()
        settings.language = self.languageSelector.itemData(i).toString()

        """ Plugins """
        self.pluginListView.model().saveSettings()

        QDialog.accept(self)

    def cancelSettings(self):
        self.loadSettings()
        QDialog.reject(self)


class AboutDialog(QDialog, Ui_AboutDialog):
    """
    A simple about dialog.
    
    It includes basic application information, a short outline of the 
    application license, and of course credit is given where credit is due
    """

    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)

    def showLicense(self):
        """
        Displays a simple dialog containing the application license
        """
        license = QDialog()
        Ui_AboutLicense().setupUi(license)
        license.exec_()

    def giveCreditWhereCreditIsDue(self):
        """
        Displays a simple dialog containing developer information, and
        credit is given where credit is due
        """
        credits = QDialog()
        Ui_AboutCredits().setupUi(credits)
        credits.exec_ ()
