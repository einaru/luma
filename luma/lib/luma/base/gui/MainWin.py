# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003-2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from PyQt4.QtGui import *

import os
import os.path
from ConfigParser import *
import time

from base.gui.MainWinDesign import MainWinDesign
from base.gui.AboutDialog import AboutDialog
import environment
from base.gui.ServerDialog import ServerDialog
from base.backend.PluginLoader import PluginLoader
from base.gui.PluginLoaderGui import PluginLoaderGui
from base.gui.LanguageDialog import LanguageDialog
from base.utils.backend.LogObject import LogObject
from base.utils.gui.LoggerWidget import LoggerWidget
from base.gui.ImprovedServerDialog import ImprovedServerDialog

class MainWin(MainWinDesign):
    """The main window for Luma."""

    configFile = None

    def __init__(self, parent=None):
        MainWinDesign.__init__(self, parent)
        
        environment.updateUI = self.updateUI
        environment.setBusy = self.setBusy
        environment.reloadPlugins = self.reloadPlugins
        environment.displaySizeLimitWarning = self.displaySizeLimitWarning
        environment.logMessage = self.logMessage
        
        self.pluginItemList = []

        # create the progress bar for the status bar
        statusBar = self.statusBar()
        self.progressBar = QProgressBar(statusBar)
        self.progressBar.setMaximumWidth(150)
        self.progressBar.setTotalSteps(0)
        statusBar.addWidget(self.progressBar, 0, 1)
        
        # create button for logged errors
        self.logButton = QToolButton(None)
        iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        self.logButton.setPixmap(QPixmap(os.path.join(iconPath, "bomb.png")))
        self.connect(self.logButton, SIGNAL("clicked()"), self.showLoggerWindow)
        self.logButtonActivated = False
        
        # Build the plugin toolbar
        #self.pluginToolBar = QToolBar(self, "PLUGINTOOLBAR")
        #self.toolBarLabel = QLabel("Plugin:", self.pluginToolBar)
        #self.pluginBox = QComboBox(self.pluginToolBar)
        #self.connect(self.pluginBox, SIGNAL("activated(const QString &)"), self.pluginSelectionChanged)
        self.pluginToolBar = QToolBar(self, "PLUGINTOOLBAR")
        self.pluginLabel = QLabel(self.pluginToolBar)
        self.pluginLabel.setAlignment(Qt.AlignLeft | Qt.SingleLine | Qt.AlignVCenter)
        self.pluginLabel.setText(self.trUtf8("Pluginname   "))
        font = QFont()
        font.setBold(True)
        self.pluginLabel.setFont(font)
        self.pluginLabel.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred))
        self.pluginButton = QPushButton(self.pluginToolBar)
        self.pluginButton.setText(self.trUtf8("Choose plugin"))
        self.pluginButton.installEventFilter(self)
        self.pluginButtonClicked = False
        self.connect(self.pluginButton, SIGNAL("clicked()"), self.showPluginSelection)
        self.timerRunning = False
        
        self.pluginBox = QListBox(None)
        font = self.pluginBox.font()
        font.setPointSize(font.pointSize() + 4)
        self.pluginBox.setFont(font)
        self.connect(self.pluginBox, SIGNAL("clicked(QListBoxItem*)"), self.pluginClicked)
        
        self.pluginBoxId = self.taskStack.addWidget(self.pluginBox, -1)

        self.loggerDockWindow = QDockWindow(QDockWindow.InDock, self)
        self.loggerDockWindow.setResizeEnabled(True)
        self.loggerDockWindow.setOrientation(Qt.Horizontal)
        self.loggerDockWindow.setCloseMode(3)
        self.moveDockWindow(self.loggerDockWindow, Qt.DockMinimized)
        self.connect(self.loggerDockWindow,SIGNAL("visibilityChanged(bool)"),self.loggerVisibilitChanged)
        
        self.loggerWidget = LoggerWidget(self.loggerDockWindow)
        self.loggerDockWindow.setWidget(self.loggerWidget)
        
        self.configFile = os.path.join(environment.userHomeDir,  ".luma", "luma")
        
        # Try to read the chosen language. If this fails, fallback to native,
        # which is english.
        # Additionally restore window size.
        trFile = 'NATIVE'
        try:
            configParser = ConfigParser()
            configParser.readfp(open(self.configFile, 'r'))
            
            if configParser.has_section("Defaults"):
                width = None
                height = None
                
                if configParser.has_option("Defaults", "width"):
                    width = configParser.getint("Defaults", "width")
                    
                if configParser.has_option("Defaults", "height"):
                    height = configParser.getint("Defaults", "height")
                    
                if (not (width == None)) and (not (height == None)):
                    self.resize(width, height)
                
                if configParser.has_option("Defaults", "language"):
                    trFile = configParser.get("Defaults", "language")
        except IOError, e:
            tmpString = "Could not read config file. Reason:\n"
            tmpString += str(e)
            environment.logMessage(LogObject("Debug", tmpString))
        
        # Install translator.
        qApp.translator = QTranslator(None)
        if not (trFile == 'NATIVE'):
            qApp.translator.load(trFile)
            qApp.installTranslator(qApp.translator)
            self.languageChanges()
        

        self.PLUGINS = {}
        self.ICONPREFIX = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        self.applicationIcon = QPixmap(os.path.join(self.ICONPREFIX, "luma-32.png"))
        self.setIcon(self.applicationIcon)
        
        self.showPluginSelection()
        

###############################################################################

    def showAboutLuma(self):
        """Shows the about dialog of Luma."""
        
        a = AboutDialog(self)
        a.show()

###############################################################################

    def quitApplication(self):
        """Quits Luma.
        
        Before that, all plugins are unloaded. This way all plugins have the 
        possibility for a cleanup.
        """
        self.unloadPlugins()
        self.savePosition()
        qApp.quit()

###############################################################################

    def showServerEditor(self):
        """Show the dialog for editing the accessible servers."""
        
        #dialog = ServerDialog()
        dialog = ImprovedServerDialog()
        dialog.exec_loop()
        if (dialog.result() == QDialog.Accepted) or dialog.SAVED:
            currentPlugin = self.pluginBox.currentText()
            self.reloadPlugins()
            #self.pluginBox.setCurrentText(currentPlugin)
            #self.pluginSelectionChanged(currentPlugin)

###############################################################################

    def loadPlugins(self, splash=None):
        """ Load all wanted plugins."""
        
        if not (None == splash):
            splash.message("Loading plugins...", Qt.AlignLeft + Qt.AlignBottom, Qt.white)
        
        pluginObject = PluginLoader(self.checkToLoad())
        self.PLUGINS = pluginObject.PLUGINS
        
        self.pluginBox.clear()
        
        pluginNameList = []
        for x in self.PLUGINS.keys():
            tmpObject = self.PLUGINS[x]
            if tmpObject['load'] == True:
                if not (None == splash):
                    tmpMessage = "Loading plugin " + unicode(self.trUtf8(self.PLUGINS[x]['pluginUserString']))
                    splash.message(tmpMessage, Qt.AlignLeft + Qt.AlignBottom, Qt.white)

                pluginNameList.append(self.PLUGINS[x]['pluginName'])
                reference = tmpObject["getPluginWidget"]
                widgetTmp = reference(self.taskStack)
                tmpObject["WIDGET_REF"] = widgetTmp
                tmpObject["WIDGET_ID"] = self.taskStack.addWidget(widgetTmp, -1)
                
        pluginNameList.sort()
        #map(self.pluginBox.insertItem, pluginNameList)
                
        #pluginName = str(self.pluginBox.currentText())
        #if self.PLUGINS.has_key(pluginName):
        #    self.taskStack.raiseWidget(self.PLUGINS[pluginName]["WIDGET_ID"])
        #    try:
        #        self.PLUGINS[pluginName]["WIDGET_REF"].buildToolBar(self)
        #    except AttributeError, e:
        #        pass
        #    
        
        for x in pluginNameList:
            name = self.trUtf8(self.PLUGINS[x]["pluginUserString"])
            icon = self.PLUGINS[x]["icon"]
            item = QListBoxPixmap(icon, QString(name))
            self.pluginBox.insertItem(item)
            
            item.widgetID = self.PLUGINS[x]["WIDGET_ID"]
            item.widgetRef = self.PLUGINS[x]["WIDGET_REF"]
            item.name = name
            self.pluginItemList.append(item)
            
            
        if not (None == splash):
            splash.message("Finished.", Qt.AlignLeft + Qt.AlignBottom, Qt.white)
            
        #self.taskStack.raiseWidget()
            

###############################################################################

    def unloadPlugins(self):
        """ Tries to unload all plugins.
        
        All children of the widget stack and icon view are deleted, 
        also alle references to them.
        """
        
        for x in self.PLUGINS.keys():
            tmpObject = self.PLUGINS[x]
            
            if tmpObject['load']:
                widgetRef = tmpObject["WIDGET_REF"]
                #tmpObject["PLUGIN_CODE"].postprocess()
                
                # We use deleteLater() because of a bug in QT. 
                widgetRef.deleteLater()
                
        self.PLUGINS = {}

###############################################################################

    def configurePlugins(self):
        """Show the dialog for configuring the plugins.
        """
        
        dialog = PluginLoaderGui(PluginLoader('ALL').PLUGINS, self)
        dialog.exec_loop()

###############################################################################

    def checkToLoad(self):
        """Return a list of plugin names to load.
        
        The plugins configuration file is opened and the list of plugins to 
        load is read.
        """
        
        defaultsHome = os.path.join(environment.userHomeDir, ".luma", "plugins")
        pluginList = []
        try:
            configParser = ConfigParser()
            configParser.readfp(open(defaultsHome, 'r'))
            for x in configParser.sections():
                if not configParser.has_option(x, "load"):
                    continue
                if configParser.getint(x, "load") == 1:
                    pluginList.append(x)
        except Exception, errorData:
            errorString = "Could not open file for plugin defaults.\n"
            errorString += "Reason: " + str(errorData)
            environment.logMessage(LogObject("Debug", errorString))
            pluginList = "ALL"

        return pluginList

###############################################################################

    def reloadPlugins(self):
        """Unload plugins and reload them afterwards.
        """
        
        self.unloadPlugins()
        
        self.pluginItemList = []
        
        toolBars = self.toolBars(Qt.DockTop)
        
        for x in toolBars:
            if not (str(x.name()) == "PLUGINTOOLBAR"):
                x.deleteLater()
        
        self.loadPlugins()
        
        self.showPluginSelection()
        translatedNamed = unicode(self.trUtf8("Pluginname")) + "   "
        self.pluginLabel.setText(translatedNamed)

###############################################################################

    def updateUI(self):
        """ Updates the progress bar of the GUI and keeps it responsive.
        """
        
        qApp.processEvents()
        progress = self.progressBar.progress()
        self.progressBar.setProgress(progress + 1)
            

###############################################################################

    def setBusy(self, busy=True):
        """ Set the X mouse cursor busy. 
        
        Better for user feedback.
        """
        
        if busy:
            # set cursor busy
            cursor = QCursor()
            cursor.setShape(Qt.WaitCursor)
            qApp.setOverrideCursor(cursor)
        else:
            qApp.restoreOverrideCursor()
            self.progressBar.setProgress(0)

###############################################################################

    def showLanguageDialog(self):
        """ Show the language dialog and install the chosen language.
        
        Afterwards all plugins are reloaded, otherwise the language changes 
        would have no effect.
        """
        
        configParser = ConfigParser()
            
        try:
            configParser.readfp(open(self.configFile, 'r'))
        except Exception, errorData:
            tmpString = "Could not read language settings file. Reason:\n"
            tmpString += str(errorData)
            environment.logMessage(LogObject("Debug", tmpString))
            
        if not(configParser.has_section("Defaults")):
            configParser.add_section("Defaults")
            
        language = "NATIVE"
        
        if configParser.has_option("Defaults", "language"):
            language = configParser.get("Defaults", "language")
            
        language = os.path.split(language)[-1]
        
        dialog = LanguageDialog()
        dialog.setCurrentLanguage(language)
        dialog.exec_loop()
        
        if dialog.result() == QDialog.Accepted:
            trFile = dialog.getLanguageFile()
            if trFile == 'NATIVE':
                qApp.removeTranslator(qApp.translator)
            else:
                qApp.translator.load(trFile)
                qApp.installTranslator(qApp.translator)
               
            self.languageChanges()
                
            configParser.set("Defaults", "language", trFile)
            
            try:
                configParser.write(open(self.configFile, 'w'))
            except Exception, errorData:
                tmpString = "Could not save language settings file. Reason:\n"
                tmpString += str(errorData)
                environment.logMessage(LogObject("Error", tmpString))
                
            self.reloadPlugins()

###############################################################################

    def displaySizeLimitWarning(self):
        statusBar = self.statusBar()
        statusBar.message("Search request reached server side size limit!", 10000)
        
        
###############################################################################

    def savePosition(self):
        width = self.width()
        height = self.height()
        
        configParser = ConfigParser()
            
        try:
            configParser.readfp(open(self.configFile, 'r'))
        except Exception, errorData:
            tmpString = "Could not read settings file. Reason:\n"
            tmpString += str(errorData)
            environment.logMessage(LogObject("Debug", tmpString))
            
        if not(configParser.has_section("Defaults")):
            configParser.add_section("Defaults")
            
        configParser.set("Defaults", "width", width)
        configParser.set("Defaults", "height", height)
        
        try:
            configParser.write(open(self.configFile, 'w'))
        except Exception, errorData:
            tmpString = "Could not save window settings. Reason:\n"
            tmpString += str(errorData)
            environment.logMessage(LogObject("Error", tmpString))

###############################################################################


    def showLoggerWindow(self):
        statusBar = self.statusBar()
        statusBar.removeWidget(self.logButton)
        self.logButton = None
        self.logButtonActivated = False
        
        self.moveDockWindow(self.loggerDockWindow, Qt.DockBottom)
        self.loggerWidget.displayMessages()
        
###############################################################################

    def loggerVisibilitChanged(self, visible):
        if not visible:
            self.moveDockWindow(self.loggerDockWindow, Qt.DockMinimized)
            
###############################################################################

    def logMessage(self, messageObject):
        if isinstance(messageObject, LogObject):
            self.loggerWidget.newMessage(messageObject)
               
            if "Error" == messageObject.getLogType():
                if not self.logButtonActivated:
                    self.logButton = QToolButton(None)
                    self.logButton.setAutoRaise(True)
                    iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
                    self.logButton.setPixmap(QPixmap(os.path.join(iconPath, "bomb.png")))
                    self.connect(self.logButton, SIGNAL("clicked()"), self.showLoggerWindow)
                    statusBar = self.statusBar()
                    statusBar.addWidget(self.logButton, 0, 1)
                    self.logButtonActivated = True
        else:
            pass

###############################################################################

    def eventFilter(self, object, event):
        if (event.type() == QEvent.Enter):
            if object == self.pluginButton:
                if not self.timerRunning:
                    self.pluginButtonClicked = False
                    QTimer.singleShot( 500, self.checkCursorPosition)
                
        return 0
                
###############################################################################

    def checkCursorPosition(self):
        self.timerRunning = False
        if self.pluginButtonClicked:
            return
            
	# Annoying behavior.. disabled # bgrotan
        #if self.pluginButton.hasMouse():
        #    self.showPluginSelection()
            
###############################################################################

    def showPluginSelection(self):
        self.pluginButtonClicked = True
        self.taskStack.raiseWidget(self.pluginBoxId)
        
###############################################################################
    
    def pluginClicked(self, item):
        if item == None:
            return
            
        self.taskStack.raiseWidget(item.widgetID)
        self.pluginLabel.setText(unicode(item.text()) + "   ")
        
        toolBars = self.toolBars(Qt.DockTop)
        
        for x in toolBars:
            if not (str(x.name()) == "PLUGINTOOLBAR"):
                x.deleteLater()
        
        #build the toolbar for the selected plugin
        try:
            item.widgetRef.buildToolBar(self)
        except AttributeError, e:
            pass
            
            
###############################################################################

    def __tr(self,s,c = None):
        return qApp.translate("MainWin",s,c)
        
###############################################################################

    def languageChanges(self):
        self.languageChange()
        self.pluginButton.setText(self.trUtf8("Choose plugin"))
        
        #for x in self.pluginItemList:
        #    x.setText(qApp.translate(str(x.name))
        #    print "foo"
        
        
        
        
        
        
        
