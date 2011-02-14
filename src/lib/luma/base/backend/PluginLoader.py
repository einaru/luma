# -*- coding: utf-8 -*-
#
# Copyright (C) 2003
#    Wido Depping, <widod@users.sourceforge.net>                                                             
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

from os import listdir
import os.path
import sys
import imp
import logging

class PluginLoader:
    """
    A class for finding and loading Luma plugins.
    
    self.PLUGINS:
        A dictionary of the plugins. Keys are the plugin names. 
        The values contain metainformation for each plugin. 
        This information is stored in a dictionary with the following keys:
    
        PLUGIN_NAME:
            Name of the plugin (string).
    
        PLUGIN_VERSION:
            The version of the plugin (string).
    
        PLUGIN_AUTHOR:
            Plugin author (string).
    
        PLUGIN_FILE:
            The base python script for the plugin (string).
    
        PLUGIN_LOAD:
            Indicates if the plugin should be loaded (integer).
    
        PLUGIN_PATH:
            Base path of the plugin (string).
    
        PLUGIN_CODE:
            The python code object (callable code).
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, pluginsToLoad=[]):
        self.PLUGINS = {}

#        # get the base diretory of the plugins as a string
#        self.pluginBaseDir = os.path.join(environment.lumaInstallationPrefix,  "lib", "luma", "plugins")
        # XXX temporary hardcoded plugin base dir
        self.pluginBaseDir = os.path.join(os.getcwd(), 'plugins')
        print self.pluginBaseDir
        self.pluginDirList = []
        self.pluginDirList = self.getPluginList()

        self.importPluginMetas(pluginsToLoad)


    def getPluginList(self):
        """
        Returns a list of diretories, where possible plugins a stored.
        """

        tmpList = []
        try:
            # test for every file listed, if it is a directory
            for x in listdir(self.pluginBaseDir):
                tmpPath = os.path.join(self.pluginBaseDir, x)
                if os.path.isdir(tmpPath):
                    tmpList.append(x)
                    print x

            return tmpList
        except OSError, e:
            msg = "Could not read from directory where plugins are stored. Reason:\n%s" % str(e)
            self.__logger.debug(msg)


    def importPluginMetas(self, pluginsToLoad=[]):
        """ 
        Read the meta information for every plugin directory which is found.
        
        pluginsToLoad is a list of plugins which should be loaded.
        """

        for x in self.pluginDirList:
            if x == "CVS":
                continue

            pluginMetaObject = {}

            try:
                pluginMetaObject = self.readMetaInfo(x, pluginsToLoad)
                self.PLUGINS[pluginMetaObject["pluginName"]] = pluginMetaObject
            except PluginMetaError, e:
                msg = "Plugin from the following directory could not be loaded:\n%s" % str(e)
                self.__logger.error(msg)


    def readMetaInfo(self, pluginPath, pluginsToLoad):
        """ 
        Read the meta information for a plugin given by its directory.
        
        If the plugin is in pluginsToLoad, the flag for using this plugin
        will be set.
        """

        attributeList = ["lumaPlugin", "pluginName", "author",
                         "pluginUserString", "version", "getIcon",
                         "getPluginWidget", "getPluginSettingsWidget"]
        metaInformation = {}

        importedModule = None
        try:
            modulePath = os.path.join("plugins", pluginPath)
            foundModule = imp.find_module(modulePath)
            importedModule = imp.load_module(pluginPath, *foundModule)
        except ImportError, e:
            msg = "Plugin meta information could not be loaded. Reason:\n%s" % str(e)
            self.__logger.error(msg)
            raise PluginMetaError, e

        missingAttributes = []
        for x in attributeList:
            if not hasattr(importedModule, x):
                missingAttributes.append(x)

        if len(missingAttributes) > 0:
            errorString = "Loaded module " + pluginPath + " is not a Luma plugin."
            errorString = errorString + "The following attributes are missing: \n"
            for x in missingAttributes:
                errorString = errorString + x + " "
            raise PluginMetaError, errorString

        metaInformation["pluginName"] = importedModule.pluginName
        metaInformation["pluginUserString"] = importedModule.pluginUserString
        metaInformation["author"] = importedModule.author
        metaInformation["version"] = importedModule.version
        metaInformation["getPluginWidget"] = importedModule.getPluginWidget
        metaInformation["getPluginSettingsWidget"] = importedModule.getPluginSettingsWidget

#        iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons", "plugins", pluginPath)
#        icon = importedModule.getIcon(iconPath)
#        metaInformation["icon"] = icon

        metaInformation["load"] = False
        if pluginsToLoad == 'ALL':
            metaInformation["load"] = True
        else:
            for x in pluginsToLoad:
                if x == metaInformation["pluginName"]:
                    metaInformation["load"] = True
                    break

        return metaInformation


class PluginMetaError(Exception):
    """
    Custom exception class.
    """
    
    pass
