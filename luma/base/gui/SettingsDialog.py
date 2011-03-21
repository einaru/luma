# -*- coding: utf-8 -*-
#
# base.gui.SettingsDialog
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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

from PyQt4.QtGui import QDialog

from ..gui.Settings import Settings
from ..gui.design.SettingsDialogDesign import Ui_SettingsDialog
from ..model.PluginSettingsListModel import PluginSettingsListModel
from ..util.i18n import LanguageHandler


class SettingsDialog(QDialog, Ui_SettingsDialog):
    """ The application settings dialog
    
    Contains all the application settings.
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, currentLanguage, languages={}, parent=None):
        """ The constructor must be given the currentLanguage from the
        Main window to keep things synchronized.
        
        @param currentLanguage: string;
            the iso code for the current selected application language
        
        @param languages: dictionary;
            This should be a dictionary with iso codes and language
            names for available languages. NOTE: Might want to provide
            this from the main window as it's already loaded.
        """
        super(SettingsDialog, self).__init__(parent)

        self.setupUi(self)
        self.languages = languages
        self.currentLanguage = currentLanguage
        if self.currentLanguage == {}:
            """ If the list of languages is empty we fetch the list
            with the LanguageHelper. """
            lh = LanguageHandler()
            self.currentLanguage = lh.availableLanguages
        self.loadSettings()

    def loadSettings(self):
        """ Loads the application settings from file.
        """
        settings = Settings()

        # Logging
        self.showLoggerOnStart.setChecked(settings.showLoggerOnStart)
        self.showErrors.setChecked(settings.showErrors)
        self.showDebug.setChecked(settings.showDebug)
        self.showInfo.setChecked(settings.showInfo)

        # Language
        self.languageSelector
        i = 0
        for key, name in self.languages.iteritems():
            self.languageSelector.addItem('%s [%s]' % (name[0], key), key)
            if key == self.currentLanguage:
                self.languageSelector.setCurrentIndex(i)
            i = i + 1

        # Plugins
        self.pluginListView.setModel(PluginSettingsListModel())

    def pluginSelected(self, index):
        """ If a plugin has a pluginsettingswidget, it will be put into
        the QStackedWidget.
        """

        plugin = self.pluginListView.model().itemFromIndex(index).plugin

        widget = plugin.getPluginSettingsWidget(self.pluginSettingsStack)

        if not widget:
            return

        if self.pluginSettingsStack.indexOf(widget) == -1:
            self.pluginSettingsStack.addWidget(widget)

        if self.pluginSettingsStack.currentWidget() != widget:
            self.pluginSettingsStack.setCurrentWidget(widget)

    def saveSettings(self):
        """
        This slot is called when the ok button is clicked. It saves the
        selected settigns to file.
        """
        settings = Settings()

        # Logging
        settings.showLoggerOnStart = self.showLoggerOnStart.isChecked()
        settings.showErrors = self.showErrors.isChecked()
        settings.showDebug = self.showDebug.isChecked()
        settings.showInfo = self.showInfo.isChecked()

        # Language
        i = self.languageSelector.currentIndex()
        settings.language = self.languageSelector.itemData(i).toString()

        # Plugins
        self.pluginListView.model().saveSettings()

        QDialog.accept(self)

    def cancelSettings(self):
        self.loadSettings()
        QDialog.reject(self)
