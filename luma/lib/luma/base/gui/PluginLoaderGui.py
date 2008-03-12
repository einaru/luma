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

from PyQt4.QtGui import *
import copy
import os.path
import os
from ConfigParser import *

class PluginLoaderGui(PluginLoaderGuiDesign):
    """Dialog for choosing which plugins should be loaded.
    """

    def __init__(self, tmpPlugins=None, parent=None):
        PluginLoaderGuiDesign.__init__(self, parent)
        
        self.defaultsHome = os.path.join(environment.userHomeDir, ".luma", "plugins")
        firstStart = not (os.path.exists(self.defaultsHome))
        
        self.fooWidget = QWidget(self.settingsStack)
        self.settingsStack.addWidget(self.fooWidget)
        
        self.checkerList = []
        self.PLUGINS = tmpPlugins
        
        for x in self.PLUGINS.keys():
            tmpObject = self.PLUGINS[x]
            tmpCheckBox = QCheckListItem(self.chooserView,
                            tmpObject["pluginName"],
                            QCheckListItem.CheckBox )
            tmpCheckBox.pluginName = tmpObject["pluginName"]
            self.checkerList.append(tmpCheckBox)
            
            tmpObject = self.PLUGINS[x]
            reference = tmpObject['getPluginSettingsWidget']
            
            widgetTmp = reference(self.settingsStack)
            if widgetTmp == None:
                widgetTmp = QWidget(self.settingsStack)
            id = self.settingsStack.addWidget(widgetTmp, -1)
            tmpObject["SETTINGS_WIDGET_ID"] = id

        
        # This is executed if Luma is started for the first time. It ensures 
        # that all plugins are selected altough no plugins files exists.
        if firstStart:
            for x in self.checkerList:
                x.setOn(1)
        
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
            configParser = ConfigParser()
            if os.path.isfile(self.defaultsHome):
                configParser.readfp(open(self.defaultsHome, 'r'))
            
            for x in self.checkerList:
                pluginName = x.pluginName
                if not(configParser.has_section(pluginName)):
                    configParser.add_section(pluginName)
                
                tmpVal = 0
                if x.isOn():
                    tmpVal = 1
                    
                configParser.set(pluginName, "load", tmpVal)
                configParser.write(open(self.defaultsHome, 'w'))
        except IOError, errorData:
            print "Could not save to file for plugin defaults :("
            print "Reason: ", errorData
            
        self.accept()

###############################################################################

    def pluginSelected(self, item):
        text = str(item.text())
        for x in self.PLUGINS.keys():
            tmpObject = self.PLUGINS[x]
            if tmpObject["pluginName"] == item.pluginName:
                self.settingsStack.raiseWidget(tmpObject["SETTINGS_WIDGET_ID"])
                self.settingsBox.setTitle(text)
                




