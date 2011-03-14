# -*- coding: utf-8 -*-

<<<<<<< HEAD
from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QStandardItemModel, QStandardItem
=======
from PyQt4.QtCore import *
from PyQt4.QtGui import *
>>>>>>> S3-installation-v2
from base.backend.PluginLoader import PluginLoader

class PluginListWidgetModel(QStandardItemModel):
    """
    This model will create its own items, from the QSettings where 
    plugins is set to "load".
    """
<<<<<<< HEAD
    def __init__(self, widgetParent, parent = None):
        QStandardItemModel.__init__(self, parent)
        self._settings = QSettings()
        self._settings.beginGroup("plugins")
        self.widgetParent = widgetParent    
        self.pluginloader = PluginLoader()
        
        self.pluginloader.pluginsToLoad = self.__checkToLoad()
        
        for plugin in self.pluginloader.plugins:
            if plugin.load == True:
                
=======
    def __init__(self, parent = None):
        QStandardItemModel.__init__(self, parent)
        self._settings = QSettings()
            
        pluginloader = PluginLoader(".", self.__checkToLoad())
        for plugin in pluginloader.plugins:
            
            if plugin.load == True:
>>>>>>> S3-installation-v2
                item = QStandardItem(str.capitalize(plugin.pluginName))
                #item.setIcon(QIcon('/Users/johannes/Programmering/Luma/git/src/share/luma/icons/plugins/addressbook/plugin.png'))
                font = item.font()
                font.setPointSize(font.pointSize() +4 )
                item.setFont(font)
                item.setEditable(False)
                item.plugin = plugin
<<<<<<< HEAD
                item.widget = plugin.getPluginWidget(self.widgetParent)
                self.appendRow(item)
    
    def __checkToLoad(self):
=======
                self.appendRow(item)
    
    def __checkToLoad(self):
        self._settings.beginGroup("plugins")
        
>>>>>>> S3-installation-v2
        pluginlist = []
        
        #When beginGroup is set to plugins, the childgroups will be each of the plugins..
        for plugin in self._settings.childGroups():
            valueString = str(plugin) + "/load"
<<<<<<< HEAD
            value = self._settings.value(valueString, "True").toString()
            print plugin
            print value
            if value == "True":
                pluginlist.append(str(plugin))
       
        return pluginlist


        
        
=======
            value = self._settings.value(valueString).toString()
            if value == "True":
                pluginlist.append(str(plugin))
        return pluginlist
>>>>>>> S3-installation-v2
