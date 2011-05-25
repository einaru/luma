# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Johannes Harestad, <johannesharestad@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/
from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QStandardItemModel, QStandardItem
from ..backend.PluginLoader import PluginLoader


class PluginListWidgetModel(QStandardItemModel):
    """This model will create its own items, from the ``QSettings``
    where plugins is set to *load*.
    """
    def __init__(self, parent = None):
        QStandardItemModel.__init__(self, parent)
        self._settings = QSettings()
        self._settings.beginGroup("plugins")
        self.pluginloader = PluginLoader()
        self.pluginloader.pluginsToLoad = self.__checkToLoad()

        for plugin in self.pluginloader.plugins:
            if plugin.load == True:
                item = QStandardItem(plugin.pluginUserString)
                if plugin.icon:
                    item.setIcon(plugin.icon)
                font = item.font()
                font.setPointSize(font.pointSize() + 4)
                item.setFont(font)
                item.setEditable(False)
                item.plugin = plugin
                self.appendRow(item)

    def __checkToLoad(self):
        pluginlist = []

        # When beginGroup is set to plugins, the childgroups will be
        # each of the plugins.
        for plugin in self._settings.childGroups():
            valueString = str(plugin) + "/load"
            value = self._settings.value(valueString, "True").toString()
            if value == "True":
                pluginlist.append(str(plugin))

        return pluginlist


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
