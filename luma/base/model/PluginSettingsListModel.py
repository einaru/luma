# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Johannes Harestad, <johannesharestad@gmail.com>
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

from PyQt4.QtGui import QStandardItemModel, QStandardItem
from PyQt4.QtCore import QSettings, Qt
from ..backend.PluginLoader import PluginLoader 

class PluginSettingsListModel(QStandardItemModel):
    """
    This model will create its own items, out of the list from PluginLoader
    in backend. 
    """
    def __init__(self, parent = None):
        QStandardItemModel.__init__(self, parent)
        self._settings = QSettings()
        for pluginobject in PluginLoader("ALL").plugins:
            # Changed the plugin viewable name to the UserString value
            # as it looks better for the user.
            #item = QStandardItem(pluginobject.pluginName)
            item = QStandardItem(pluginobject.pluginUserString)
            check = Qt.Unchecked
            valueString = "plugins/" + pluginobject.pluginName + "/load"
            if self._settings.value(valueString).toString() == "True":
                check = Qt.Checked
            item.setCheckState(check)
            item.setCheckable(True)
            item.setEditable(False)
            item.plugin = pluginobject
            self.appendRow(item)
            
    def saveSettings(self):
        
        items = self.rowCount()
        for x in range(items):
            item = self.item(x)
            valueString = "plugins/" + item.plugin.pluginName + "/load"
            if item.checkState() == 2:
                self._settings.setValue(valueString, "True")
            else:
                self._settings.setValue(valueString, "False")

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
