# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *

import os
import os.path
from ConfigParser import *

from base.gui.MainWinDesign import MainWinDesign
from base.gui.AboutDialog import AboutDialog
import environment
from base.gui.ServerDialog import ServerDialog
from base.backend.PluginLoader import PluginLoader
from base.gui.PluginLoaderGui import PluginLoaderGui
from base.gui.LanguageDialog import LanguageDialog

class MainWin(MainWinDesign):
    """The main window for Luma."""

    configFile = None

    def __init__(self, parent=None):
        MainWinDesign.__init__(self, parent)
        
        self.configFile = os.path.join(environment.userHomeDir,  ".luma", "luma")
        
        # Try to read the chosen language. If this fails, fallback to native,
        # which is english.
        trFile = 'NATIVE'
        try:
            configParser = ConfigParser()
            configParser.readfp(open(self.configFile, 'r'))
            
            if configParser.has_section("Defaults"):
                trFile = configParser.get("Defaults", "language")
        except NoOptionError:
            pass
        except IOError, e:
            print "Could not read config file. Reason:"
            print e
        
        # Install translator.
        self.translator = QTranslator(None)
        if not (trFile == 'NATIVE'):
            self.translator.load(trFile)
            qApp.installTranslator(self.translator)
            self.languageChange()

        # create the progress bar for the status bar
        statusBar = self.statusBar()
        self.progressBar = QProgressBar(statusBar)
        self.progressBar.setMaximumWidth(150)
        self.progressBar.setTotalSteps(0)
        statusBar.addWidget(self.progressBar, 0, 1)
        
        # Build the plugin toolbar
        self.pluginToolBar = QToolBar(self, "PLUGINTOOLBAR")
        self.toolBarLabel = QLabel("Plugin:", self.pluginToolBar)
        self.pluginBox = QComboBox(self.pluginToolBar)
        self.connect(self.pluginBox, SIGNAL("activated(const QString &)"), self.pluginSelectionChanged)

        self.PLUGINS = {}
        self.ICONPREFIX = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        environment.updateUI = self.updateUI
        environment.setBusy = self.setBusy

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
        qApp.quit()

###############################################################################

    def showServerEditor(self):
        """Show the dialog for editing the accessible servers."""
        
        dialog = ServerDialog()
        dialog.exec_loop()
        if (dialog.result() == QDialog.Accepted) or dialog.SAVED:
            self.reloadPlugins()

###############################################################################

    def loadPlugins(self):
        """ Load all wanted plugins."""
        
        pluginObject = PluginLoader(self.checkToLoad())
        self.PLUGINS = pluginObject.PLUGINS
        iconTmp = None
        
        self.pluginBox.clear()
        
        for x in self.PLUGINS.keys():
            tmpObject = self.PLUGINS[x]
            if tmpObject['PLUGIN_LOAD'] == 1:
                self.pluginBox.insertItem(self.PLUGINS[x]['PLUGIN_NAME'])
                widgetTmp = tmpObject["PLUGIN_CODE"].getPluginWidget(self.taskStack)
                tmpObject["WIDGET_REF"] = widgetTmp
                tmpObject["WIDGET_ID"] = self.taskStack.addWidget(widgetTmp, -1)
                
        pluginName = str(self.pluginBox.currentText())
        if self.PLUGINS.has_key(pluginName):
            self.taskStack.raiseWidget(self.PLUGINS[pluginName]["WIDGET_ID"])
            try:
                self.PLUGINS[pluginName]["WIDGET_REF"].buildToolBar(self)
            except AttributeError, e:
                pass
            

###############################################################################

    def unloadPlugins(self):
        """ Tries to unload all plugins.
        
        All children of the widget stack and icon view are deleted, 
        also alle references to them.
        """
        
        for x in self.PLUGINS.keys():
            tmpObject = self.PLUGINS[x]
            
            if tmpObject['PLUGIN_LOAD']:
                widgetRef = tmpObject["WIDGET_REF"]
                tmpObject["PLUGIN_CODE"].postprocess()
                
                # We use deleteLater() because of a bug in QT. 
                widgetRef.deleteLater()
                
        self.PLUGINS = {}

###############################################################################

    def pluginSelectionChanged(self, pluginName):
        """If a plugin icon is clicked, the corresponding plugin widget is
        raised.
        """ 
        
        pluginName = str(pluginName)

        if self.PLUGINS.has_key(pluginName):
            self.taskStack.raiseWidget(self.PLUGINS[pluginName]["WIDGET_ID"])

        toolBars = self.toolBars(Qt.DockTop)
        
        for x in toolBars:
            if not (str(x.name()) == "PLUGINTOOLBAR"):
                x.deleteLater()

        #build the toolbar for the selected plugin
        try:
            self.PLUGINS[pluginName]["WIDGET_REF"].buildToolBar(self)
        except AttributeError, e:
            print "Could not build toolbar for plugin ", pluginName

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
            print "Debug: Could not open file for plugin defaults."
            print "Reason: ", errorData
            pluginList = "ALL"

        return pluginList

###############################################################################

    def reloadPlugins(self):
        """Unload plugins and reload them afterwards.
        """
        
        self.unloadPlugins()
        
        toolBars = self.toolBars(Qt.DockTop)
        
        for x in toolBars:
            if not (str(x.name()) == "PLUGINTOOLBAR"):
                x.deleteLater()
        
        self.loadPlugins()

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
        
        dialog = LanguageDialog()
        dialog.exec_loop()
        
        if dialog.result() == QDialog.Accepted:
            trFile = dialog.getLanguageFile()
            if trFile == 'NATIVE':
                qApp.removeTranslator(self.translator)
            else:
                self.translator.load(trFile)
                qApp.installTranslator(self.translator)
               
            self.languageChange()

            configParser = ConfigParser()
            
            try:
                configParser.readfp(open(self.configFile, 'r'))
                
                if not(configParser.has_section("Defaults")):
                    configParser.add_section("Defaults")
                
                configParser.set("Defaults", "language", trFile)
                configParser.write(open(self.configFile, 'w'))
            except Exception, errorData:
                print "Error: could not save language settings file. Reason:"
                print errorData
                
            self.reloadPlugins()

