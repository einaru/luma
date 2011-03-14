# -*- coding: utf-8 -*-

from os import listdir 
import imp 
from os import path
import logging
import sys

from PyQt4 import QtGui

class PluginLoader(object):
    
    """
    This is the new version of PluginLoader, with the use of a PluginObject.
    The plugins field is a list of PluginObjects.
    
    lumaInstallationPrefix: the path to where luma is installed
    pluginsToLoad: a list of plugin names, or 'ALL'
    """
    
    _logger = logging.getLogger(__name__)
    
<<<<<<< HEAD
    def __init__(self, lumaInstallationPrefix = ".", pluginsToLoad = []):
=======
    def __init__(self, lumaInstallationPrefix, pluginsToLoad = []):
>>>>>>> S3-installation-v2
        
        self._pluginsToLoad = pluginsToLoad
        self._plugins = [] #PluginObjects
        self._lumaInstallationPrefix = lumaInstallationPrefix
        self._pluginsBaseDir = path.join(lumaInstallationPrefix, "plugins")
        """self._pluginsBaseDir = path.join(lumaInstallationPrefix,
            "lib", "luma", "plugins")"""
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
        
<<<<<<< HEAD
       
=======
>>>>>>> S3-installation-v2
        return self._plugins
    
###############################################################################

    def __loadPlugins(self):
        """
        Will load all plugins that was found from the "__findPluginDirectories()".
        """
<<<<<<< HEAD
        
        self._plugins = []
        
        for x in self.__findPluginDirectories():
            if x == "CVS" or x == ".svn" or x == ".git":
=======
        return
        for x in self.__findPluginDirectories():
            if x == "CVS" or x == ".svn":
>>>>>>> S3-installation-v2
                continue
        
            try:
                self._plugins.append(self.__readMetaInfo(x))
        
<<<<<<< HEAD
            except PluginMetaError, y:
                errorString = "Plugin \"" + str(x) + "\" gave an exception: \n"
                errorString += str(y)
=======
            except PluginMetaError, x:
                errorString = "Plugin from the following directory could not be loaded:\n"
                errorString += str(x)
>>>>>>> S3-installation-v2
                self._logger.error(errorString)
                
###############################################################################

    def __findPluginDirectories(self):
        """
        Will find all directories inside the "_pluginBaseDir"
        and put them in a list
        """
        tmpList = []
    
        try:
            #look for directories
            for x in listdir(self._pluginsBaseDir):
                xPath = path.join(self._pluginsBaseDir, x)
                
                if path.isdir(xPath):
                    tmpList.append(x)
            
            return tmpList
        
        except OSError, errorData:
            errorString = "Could not read from directory where plugins are stored. Reason:\n"
            errorString += str(errorData)
            self._logger.error(errorString)

############################################################################### 
    
    def __readMetaInfo(self, pluginName):
        """
        Reads meta information for a plugin by its directory.
        If the plugin is in pluginsToLoad, the load attribute will be
        set to true.
        All of the meta information about a plugin will be put into a PluginObject.
        """
<<<<<<< HEAD
        
=======

>>>>>>> S3-installation-v2
        from base.backend.PluginObject import PluginObject
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
            searchList = [self._pluginsBaseDir]
            foundModule = imp.find_module(pluginName, searchList)
            importedModule = imp.load_module(pluginName, *foundModule)
            
        except ImportError, errorData:
            errorString = "Plugin meta information could not be loaded. Reason:\n"
            errorString += str(errorData)
            self._logger.error(errorString)
            raise PluginMetaError, errorData
        

        missingAttributes = []
        for x in attributes:
            if not hasattr(importedModule, x):
                missingAttributes.append(x)
        
        if len(missingAttributes) > 0:
<<<<<<< HEAD
            errorString = "Loaded module \"" + pluginName + "\" is not a Luma plugin. \n"
            errorString += "The following attributes are missing: \n"
            for x in missingAttributes:
                errorString += "\t" + x + "\n"
                errorString = errorString + x + " "
            errorString = errorString + "\n"
=======
            errorString = "Loaded module " + pluginName + " is not a Luma plugin."
            errorString = errorString + "The following attributes are missing: \n"
            for x in missingAttributes:
                errorString = errorString + x + " "
>>>>>>> S3-installation-v2
            raise PluginMetaError, errorString
            
        plugin.pluginName = importedModule.pluginName
        plugin.pluginUserString = importedModule.pluginUserString
        plugin.author = importedModule.author
        plugin.version = importedModule.version
        plugin.getPluginWidget = importedModule.getPluginWidget
        plugin.getPluginSettingsWidget = importedModule.getPluginSettingsWidget
            
        iconPath = path.join(self._lumaInstallationPrefix, "share", 
                 "luma", "icons", "plugins", pluginName)
                                
        icon = importedModule.getIcon(iconPath)
        plugin.icon = icon
        
        if self._pluginsToLoad == 'ALL':
<<<<<<< HEAD
            plugin.load = True
        else:
            for ptl in self._pluginsToLoad:
                if plugin.pluginName == ptl:
                    plugin.load = True
                    break
           
=======
                plugin.load = True
        else:
            for x in self.pluginsToLoad:
                if x == plugin.pluginName:
                    plugin.load = True
                break

>>>>>>> S3-installation-v2
        return plugin
            
###############################################################################

class PluginMetaError(Exception):
    """
    When __readMetaInfo sees that a directory is not a plugin-directory,
    this exception is raised..
    """
    pass
<<<<<<< HEAD
=======

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    p = PluginLoader("/Users/johannes/Programmering/Luma/git/pluginloader", ["testplugin"])
    widget = p.plugins[0].getPluginWidget(None)
    widget.show()
    sys.exit(app.exec_())
>>>>>>> S3-installation-v2
