# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from base.backend.PluginLoader import PluginLoader

class PluginListWidgetModel(QStandardItemModel):
    """
    This model will create its own items, from the QSettings where 
    plugins is set to "load".
    """
    def __init__(self, widgetParent, parent = None):
        QStandardItemModel.__init__(self, parent)
        self._settings = QSettings()
        self._settings.beginGroup("plugins")
        self.widgetParent = widgetParent    
        self.pluginloader = PluginLoader()
        
        self.pluginloader.pluginsToLoad = self.__checkToLoad()
        
        for plugin in self.pluginloader.plugins:
            if plugin.load == True:
                
                item = QStandardItem(str.capitalize(plugin.pluginName))
                #item.setIcon(QIcon('/Users/johannes/Programmering/Luma/git/src/share/luma/icons/plugins/addressbook/plugin.png'))
                font = item.font()
                font.setPointSize(font.pointSize() +4 )
                item.setFont(font)
                item.setEditable(False)
                item.plugin = plugin
                item.widget = plugin.getPluginWidget(self.widgetParent)
                self.appendRow(item)
    
    def __checkToLoad(self):
        pluginlist = []
        
        #When beginGroup is set to plugins, the childgroups will be each of the plugins..
        for plugin in self._settings.childGroups():
            valueString = str(plugin) + "/load"
            value = self._settings.value(valueString).toString()
            if value == "True":
                pluginlist.append(str(plugin))
       
        return pluginlist


        
        