# -*- coding: utf-8 -*-
#
# base.gui.SettingsDialog
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
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

import logging

from PyQt4 import QtCore
from PyQt4.QtGui import QDialog

from ..gui.Settings import Settings
from ..gui.design.SettingsDialogDesign import Ui_SettingsDialog
from ..model.PluginSettingsListModel import PluginSettingsListModel
from ..gui.AboutPlugin import AboutPlugin


class SettingsDialog(QDialog, Ui_SettingsDialog):
    """ The application settings dialog

    .. note:: Only settings that are irrelevant to the running main
       application while be available in this settings Dialog. This
       way we need not worry about keeping things synchronized with
       each other.
    """
    # TODO: We might want to add some options to let the user control
    # the level of warnings and messages shown through message boxes.

    #: Signal used for telling the plugin settings widgets that
    #: settings values have (possibly) changed.
    onSettingsChanged = QtCore.pyqtSignal(name='onSettingsChanged')

    __logger = logging.getLogger(__name__)

    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.settings = Settings()
        self.loadSettings()

    def loadSettings(self):
        """ Loads the application settings from file.
        """
        # Logging
        self.showLoggerOnStart.setChecked(self.settings.showLoggerOnStart)

        # Plugins
        self.pluginListView.setModel(PluginSettingsListModel())

    def pluginSelected(self, index):
        """If a plugin has a pluginsettingswidget, it will be put into
        the tabWidget, if not, only a tab with "about" will show.

        :param index: the index of the selected plugin.
        :type index: int
        """
        plugin = self.pluginListView.model().itemFromIndex(index).plugin

        aboutwidget = AboutPlugin(plugin)
        self.pluginTabs.clear()
        self.pluginTabs.addTab(aboutwidget, 'About')

        settingswidget = plugin.getPluginSettingsWidget(None)
        if not settingswidget:
            return

        self.pluginTabs.addTab(settingswidget, "Settings")
        # Try to connect the plugin settingswidget to the
        # onSettingsChanged signal, in order to tell it to save its
        # settings. We will get an AttributeError if this plugin don't
        # have the writeSettings method implemented in its settingswidget.
        try:
            self.onSettingsChanged.connect(settingswidget.writeSettings)
        except AttributeError:
            msg = 'Missing writeSettings method in the SettingsWidget for ' \
                  'plugin: {0}.'.format(plugin.pluginUserString)
            self.__logger.error(msg)

    def saveSettings(self):
        """This slot is called when the ok button is clicked. It saves
        the selected settigns to file.
        """
        # Logging
        self.settings.showLoggerOnStart = self.showLoggerOnStart.isChecked()

        # Plugins
        self.pluginListView.model().saveSettings()

        # Emit the settings changed signal
        self.onSettingsChanged.emit()

        QDialog.accept(self)

    def cancelSettings(self):
        self.loadSettings()
        QDialog.reject(self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
