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

        self.__PLUGINS = {}
        self.__ICONPREFIX = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        environment.updateUI = self.updateUI
        environment.setBusy = self.setBusy
        self.load_plugins()

###############################################################################

    def showAboutLuma(self):
        """Shows the about dialog of Luma."""
        
        a = AboutDialog(self)
        a.show()

###############################################################################

    def quit_application(self):
        """Quits Luma.
        
        Before that, all plugins are unloaded. This way all plugins have the 
        possibility for a cleanup.
        """
        
        self.unload_plugins()
        qApp.quit()

###############################################################################

    def showServerEditor(self):
        """Show the dialog for editing the accessible servers."""
        
        dialog = ServerDialog()
        dialog.exec_loop()
        self.reload_plugins()

###############################################################################

    def load_plugins(self):
        """ Load all wanted plugins."""
        
        pluginObject = PluginLoader(self.__check_to_load())
        self.__PLUGINS = pluginObject.PLUGINS
        iconTmp = None
        
        for x in self.__PLUGINS.keys():
            tmpObject = self.__PLUGINS[x]
            if tmpObject['PLUGIN_LOAD']:
                iconTmp =QIconViewItem(self.taskList, tmpObject["PLUGIN_NAME"],
                        tmpObject["PLUGIN_CODE"].get_icon())
                        
                widgetTmp = tmpObject["PLUGIN_CODE"].getPluginWidget(self.taskStack)
                
                tmpObject["WIDGET_REF"] = widgetTmp
                tmpObject["ICON_REF"] = iconTmp
                tmpObject["WIDGET_ID"] = self.taskStack.addWidget(widgetTmp, -1)
                
                self.taskList.insertItem(iconTmp)
                
        self.taskList.emit(SIGNAL("clicked()"), (iconTmp,))
        if not(iconTmp == None):
            iconTmp.setSelected(1, 0)
            
        self.PLUGINS_LOADED = 1

###############################################################################

    def unload_plugins(self):
        """ Tries to unload all plugins.
        
        All children of the widget stack and icon view are deleted, 
        also alle references to them.
        """
        
        for x in self.__PLUGINS.keys():
            tmpObject = self.__PLUGINS[x]
            
            if tmpObject['PLUGIN_LOAD']:
                widgetRef = tmpObject["WIDGET_REF"]
                tmpObject["PLUGIN_CODE"].postprocess()
                
                # We use deleteLater() because of a bug in QT. 
                widgetRef.deleteLater()
                
        self.__PLUGINS = {}
        self.taskList.clear()

###############################################################################

    def task_selection_changed(self, taskSender=None):
        """If a plugin icon is clicked, the corresponding plugin widget is
        raised.
        """ 
        
        # Make sure an icon was selected.
        if not(taskSender == None):
            fooString = str(taskSender.text())
            
            if self.__PLUGINS.has_key(fooString):
                self.taskStack.raiseWidget(self.__PLUGINS[fooString]["WIDGET_ID"])
                self.taskBox.setTitle(fooString)

###############################################################################

    def configure_plugins(self):
        """Show the dialog for configuring the plugins.
        """
        
        dialog = PluginLoaderGui(PluginLoader('ALL').PLUGINS, self)
        dialog.exec_loop()

###############################################################################

    def __check_to_load(self):
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

    def reload_plugins(self):
        """Unload plugins and reload them afterwards.
        """
        
        self.unload_plugins()
        self.load_plugins()

###############################################################################

    def updateUI(self):
        """ Updates the progress bar of the GUI and keeps it responsive.
        """
        
        qApp.processEvents()
        progress = self.progressBar.progress()
        self.progressBar.setProgress(progress + 1)
            

###############################################################################

    def setBusy(self, busy=1):
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

    def show_language_dialog(self):
        """ Show the language dialog and install the chosen language.
        
        Afterwards all plugins are reloaded, otherwise the language changes 
        would have no effect.
        """
        
        dialog = LanguageDialog()
        dialog.setCaption(self.trUtf8("Choose Language"))
        dialog.exec_loop()
        if dialog.result() == dialog.Accepted:
            trFile = dialog.get_language_file()
            if trFile == 'NATIVE':
                qApp.removeTranslator(self.translator)
            else:
                self.translator.load(trFile)
                qApp.installTranslator(self.translator)
               
            self.languageChange()

            configParser = ConfigParser()
            
            try:
                configParser.readfp(open(self.configFile, 'r'))
            except Exception, errorData:
                print "Error: Could not open luma config file for storing language settings. Reason:"
                print errorData
                
            if not(configParser.has_section("Defaults")):
                configParser.add_section("Defaults")
                    
            configParser.set("Defaults", "language", trFile)
            
            try:
                configParser.write(open(self.configFile, 'w'))
            except Exception, errorData:
                print "Error: could not save language settings file. Reason:"
                print errorData
                
            self.reload_plugins()
    
