# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import environment
from base.utils.backend.LogObject import LogObject
from base.gui.PluginLoaderGuiDesign import Ui_PluginLoaderGuiDesign

from PyQt4 import QtCore
from PyQt4.QtGui import *
import copy
import os.path
import os
from ConfigParser import *

class PluginLoaderGui(QDialog, Ui_PluginLoaderGuiDesign):
    """Dialog for choosing which plugins should be loaded.
    """

    def __init__(self, tmpPlugins=None, parent=None):
        QDialog.__init__(self, parent)

        self.setupUi(self)
        
        self.defaultsHome = os.path.join(environment.userHomeDir, ".luma", "plugins")
        firstStart = not (os.path.exists(self.defaultsHome))
        
        self.fooWidget = QWidget(self.settingsStack)
        self.settingsStack.addWidget(self.fooWidget)
        
        self.checkerList = []
        self.PLUGINS = tmpPlugins

        self.wasUpdated = False
        
        for x in self.PLUGINS.keys():
            tmpObject = self.PLUGINS[x]
            tmpCheckBox = QListWidgetItem(tmpObject["pluginName"])
            tmpCheckBox.setFlags(QtCore.Qt.ItemIsUserCheckable | tmpCheckBox.flags())
            tmpCheckBox.setCheckState(QtCore.Qt.Unchecked)
            tmpCheckBox.pluginName = tmpObject["pluginName"]
            self.checkerList.append(tmpCheckBox)
            self.chooserView.addItem(tmpCheckBox)
            
            reference = tmpObject['getPluginSettingsWidget']
            
            widgetTmp = reference(self.settingsStack)
            if widgetTmp == None:
                widgetTmp = QWidget(self.settingsStack)
            id = self.settingsStack.addWidget(widgetTmp)
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
        except Exception, errorData:
            errorMsg = self.trUtf8("Could not open file for plugin defaults<br><br>Reason: ")
            errorMsg.append(str(errorData))
            environment.logMessage(LogObject("Error", errorMsg))
            return

        for x in configParser.sections():
            if not configParser.has_option(x, "load"):
                continue
            if (configParser.getint(x, "load") == 1) and (self.PLUGINS.has_key(x)):
                for y in self.checkerList:
                    if str(y.text()) == x:
                        y.setCheckState(QtCore.Qt.Checked)
          

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
                if x.checkState() == QtCore.Qt.Checked:
                    tmpVal = 1

                if configParser.has_option(pluginName, "load"):
                    oldVal = configParser.getint(pluginName, "load")
                    if tmpVal == oldVal:
                        continue
                    
                configParser.set(pluginName, "load", tmpVal)
                configParser.write(open(self.defaultsHome, 'w'))
                self.wasUpdated = True
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
                




