# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from base.gui.PluginLoaderGuiDesign import PluginLoaderGuiDesign
import environment

from qt import *
import copy
import os.path
import os
from ConfigParser import *

class PluginLoaderGui(PluginLoaderGuiDesign):
    """Dialog for choosing which plugins should be loaded.
    """

    def __init__(self, tmpPlugins=None, parent=None):
        PluginLoaderGuiDesign.__init__(self, parent)
        
        self.fooWidget = QWidget(self.settingsStack)
        self.settingsStack.addWidget(self.fooWidget)
        
        self.defaultsHome = os.path.join(environment.userHomeDir, ".luma", "plugins")
        self.checkerList = []
        self.PLUGINS = tmpPlugins
        
        for x in self.PLUGINS.keys():
            tmpObject = self.PLUGINS[x]
            tmpCheckBox = QCheckListItem(self.chooserView,
                            tmpObject["PLUGIN_NAME"],
                            QCheckListItem.CheckBox )
            self.checkerList.append(tmpCheckBox)
            
            tmpObject = self.PLUGINS[x]
            widgetTmp = tmpObject["PLUGIN_CODE"].getPluginSettingsWidget(self.settingsStack)
            if widgetTmp == None:
                widgetTmp = QWidget(self.settingsStack)
            id = self.settingsStack.addWidget(widgetTmp, -1)
            tmpObject["SETTINGS_WIDGET_ID"] = id
            #self.settingsStack.raiseWidget(id)
            
            #tmpObject["WIDGET_REF"] = widgetTmp
            #tmpObject["ICON_REF"] = iconTmp
            #tmpObject["WIDGET_ID"] = self.taskStack.addWidget(widgetTmp, -1)
                
            #self.taskList.insertItem(iconTmp)
                
        
        # Read the plugin config from disk. This does not get the specific plugin settings.
        # It is only determined, which plugins should be loaded.
        try:
            configParser = ConfigParser()
            configParser.readfp(open(self.defaultsHome, 'r'))
            for x in configParser.sections():
                if not configParser.has_option(x, "load"):
                    continue
                if (configParser.getint(x, "load") == 1) and (self.PLUGINS.has_key(x)):
                    for y in self.checkerList:
                        if str(y.text()) == x:
                            y.setOn(1)
        except Exception, errorData:
            print "Could not open file for plugin defaults :("
            print "Reason: ", errorData
          

###############################################################################

    def saveValues(self):
        try:
            # if luma dir in home does not exist -> create 
            configDir = os.path.join(environment.userHomeDir,  ".luma")
            if not (os.path.isdir(configDir)):
                os.mkdir (configDir)
            
            configParser = ConfigParser()
            if os.path.isfile(self.defaultsHome):
                configParser.readfp(open(self.defaultsHome, 'r'))
            
            for x in self.checkerList:
                pluginName = str(x.text())
                if not(configParser.has_section(pluginName)):
                    configParser.add_section(pluginName)
                
                tmpVal = 0
                if x.isOn():
                    tmpVal = 1
                    
                configParser.set(pluginName, "load", tmpVal)
                configParser.write(open(self.defaultsHome, 'w'))
        except IOError, errorData:
            print "Could not open file for plugin defaults :("
            print "Reason: ", errorData
            
        self.accept()

###############################################################################

    def pluginSelected(self, item):
        text = str(item.text())
        for x in self.PLUGINS.keys():
            tmpObject = self.PLUGINS[x]
            if tmpObject["PLUGIN_NAME"] == text:
                self.settingsStack.raiseWidget(tmpObject["SETTINGS_WIDGET_ID"])
                self.settingsBox.setTitle(text)
                




