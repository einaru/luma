# -*- coding: utf-8 -*-

from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QStandardItemModel, QStandardItem
from base.backend.PluginLoader import PluginLoader

class PluginListWidgetModel(QStandardItemModel):
    """
    This model will create its own items, from the QSettings where 
    plugins is set to "load".

    FIX BUG: This object is being called twice on startup... ?
    """
    def __init__(self, parent = None):
        QStandardItemModel.__init__(self, parent)
        self._settings = QSettings()
        self._settings.beginGroup("plugins")
        self.pluginloader = PluginLoader()
        self.pluginloader.pluginsToLoad = self.__checkToLoad()
        
        for plugin in self.pluginloader.plugins:
            if plugin.load == True:
                # Why do we need to capitalize the plugin name ?
                # When trying to use unicode strings in the plugin meta
                # information, the str.capitalize complains about
                # receiving a unicode and not a str. -Einar
                #item = QStandardItem(str.capitalize(plugin.pluginName))
                item = QStandardItem(plugin.pluginName)
                if plugin.icon:
                    item.setIcon(plugin.icon)
                font = item.font()
                font.setPointSize(font.pointSize() +4 )
                item.setFont(font)
                item.setEditable(False)
                item.plugin = plugin
                self.appendRow(item)
    
    def __checkToLoad(self):
        pluginlist = []
        
        #When beginGroup is set to plugins, the childgroups will be each of the plugins..
        for plugin in self._settings.childGroups():
            valueString = str(plugin) + "/load"
            value = self._settings.value(valueString, "True").toString()
            if value == "True":
                pluginlist.append(str(plugin))
       
        return pluginlist


        
        

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
