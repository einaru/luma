# -*- coding: utf-8 -*-

from os import listdir 
import imp 
from os import path

class PluginLoader(object):
    
    """
    This is the new version of PluginLoader, with the use of a PluginObject.
    The plugins field is a list of PluginObjects.
    
    lumaInstallationPrefix: the path to where luma is installed
    pluginsToLoad: a list of plugin names, or 'ALL'
    """
    
    def __init__(self, lumaInstallationPrefix, pluginsToLoad = []):
        
        self._pluginsToLoad = pluginsToLoad
        
        self._plugins = [] #PluginObjects
        self._lumaInstallationPrefix = lumaInstallationPrefix
        self._pluginsBaseDir = path.join(lumaInstallationPrefix,
            "lib", "luma", "plugins")

        print self._pluginsBaseDir

        self._changed = True
    
            
###############################################################################

    @property
    def pluginsToLoad(self):
        return self._pluginsToLoad

###############################################################################

    @pluginsToLoad.setter
    def pluginsToLoad(self, value):
        self._changed = True
        self._pluginsToLoad = value

###############################################################################
    
    @property   
    def plugins(self):
    
        """
        It should not be possible to set the plugin field
        from outside, so no @plugins.setter is made.
        """
        if self._changed == True:
            self.__loadPlugins()
            self._changed = False
        
        return self._plugins
    
###############################################################################

    def __loadPlugins(self):
        """
        Will load the plugins, or well, create a list of plugins.
        """
        for x in self.__findPluginDirectories():
            if x == "CVS" or x == ".svn":
                continue
        
            try:
                self._plugins.append(self.__readMetaInfo(x))
                #do logging here z0mg
            except PluginMetaError, x:
                pass

###############################################################################

    def __findPluginDirectories(self):
    
        tmpList = []
    
        try:
            #look for directories
            for x in listdir(self._pluginsBaseDir):
                xPath = path.join(self._pluginsBaseDir, x)
                print xPath
                if path.isdir(xPath):
                    tmpList.append(x)
            
            return tmpList
        
        #do exception and loggin here pl0x!
        except OSError, errorData:
                pass

############################################################################### 
    
    def __readMetaInfo(self, pluginName):
        """
        Reads meta information for a plugin by its directory.
        If the plugin is in pluginsToLoad, the load attribute will be
        set to true.
        All of the meta information about a plugin, if it valid or nothing 
        is missing, will be put into a PluginObject.
        """

        
        from PluginObject import PluginObject
        plugin = PluginObject()
        
        attributes =    ["lumaPlugin", 
                        "pluginName", 
                        "author",
                        "pluginUserString", 
                        "version", 
                        "getIcon", 
                        "getPluginWidget", 
                        "getPluginSettingsWidget"]
                        
        importedModule = None

        
        try:
            searchList = [self._pluginBaseDir]
            foundModule = imp.find_module(pluginName, searchList)
            importedModule = imp.load_module(pluginName, *foundModule)
        except ImportError, errorData:
            errorString = "Plugin meta information could not be loaded. Reason:\n"
            errorString += str(errorData)
            #environment.logMessage(LogObject("Error", errorString))
            raise PluginMetaError, errorData
        
        missingAttributes = []
        for x in attributes:
            if not hasattr(importedModule, x):
                missingAttributes.append(x)
        
        if len(missingAttributes) > 0:
            errorString = "Loaded module " + pluginPath + " is not a Luma plugin."
            errorString = errorString + "The following attributes are missing: \n"
            for x in missingAttributes:
                errorString = errorString + x + " "
            raise PluginMetaError, errorString
            
        plugin.pluginName = importedModule.pluginName
        plugin.pluginUserString = importedModule.pluginUserString
        plugin.author = importedModule.author
        plugin.version = importedModule.version
        plugin.getPluginWidget = importedModule.getPluginWidget
        plugin.getPluginSettingsWidget = importedModule.getPluginSettingsWidget
            
        iconPath = path.join(self._lumaInstallationPrefix, "share", 
                 "luma", "icons", "plugins", pluginPath)
                                
        icon = importedModule.getIcon(iconPath)
        plugin.icon = icon
        
        if pluginsToLoad == 'ALL':
                plugin.load = True
        else:
            for x in self.pluginsToLoad:
                if x == plugin.pluginName:
                    plugin.load = True
                break

        return plugin
            
###############################################################################

class PluginMetaError(Exception):
    """
    When __readMetaInfo sees that a directory is not a plugin-directory,
    this exception is raised..
    """
    pass
