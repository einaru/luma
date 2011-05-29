# -*- coding: utf-8 -*-
#
# base.gui.PluginSettings
#
# Copyright (c) 2011
#     Johannes Harestad, <johanhar@stud.ntnu.no>
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

from PyQt4.QtGui import QDialog
from base.gui.PluginSettingsDialog import Ui_PluginsDialog
from base.model.PluginSettingsModel import PluginSettingsModel


class PluginSettings(QDialog, Ui_PluginsDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self._model = PluginSettingsModel()
        self.listView.setModel(self._model)

    def pluginSelected(self, index):
        """Whenever a plugin is selected, the groupbox should be filled
        with a widget from the plugin for its settings. If no such
        widget is made for the plugin, the box will be empty.
        """
        plugin = self._model.itemFromIndex(index).plugin
        widget = plugin.getPluginSettingsWidget(self.stackedWidget)
        if widget is not None:
            self.stackedWidget.addWidget(widget)
            self.stackedWidget.setCurrentWidget(widget)

    def reject(self):
        """
        When the main exit button (the X) is hit
        """
        self.closeButton()

    def closeButton(self):
        self._model.saveSettings()
        self.accept()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
