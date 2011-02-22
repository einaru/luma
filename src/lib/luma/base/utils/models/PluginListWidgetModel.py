# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class PluginListWidgetModel(QStandardItemModel):
    """
    This model will create its own items, from the QSettings where 
    plugins is set to "load".
    """
    def __init__(self, parent = None):
        QStandardItemModel.__init__(self, parent)
        self._settings = QSettings()
        
        self._settings.beginGroup("plugins")
        
        #When beginGroup is set to plugins, the childgroups will be each of the plugins..
        for plugin in self._settings.childGroups():
            valueString = str(plugin) + "/load"
            print valueString
            value = self._settings.value(valueString).toString()
            print value
            if value == "True":
                item = QStandardItem(str.capitalize(str(plugin)))
                #TODO: Change this path!
                item.setIcon(QIcon('/Users/johannes/Programmering/Luma/git/src/share/luma/icons/plugins/addressbook/plugin.png'))
                font = item.font()
                font.setPointSize(font.pointSize() +4 )
                item.setFont(font)
                item.setEditable(False)
                self.appendRow(item)
                
                #self.widget = something smart