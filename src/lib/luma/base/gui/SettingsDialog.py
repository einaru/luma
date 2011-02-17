# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
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

import logging
from random import randint

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from base.backend.Settings import Settings
from base.gui.SettingsDialogDesign import Ui_SettingsDialog
from base.utils import LanguageHandler

class SettingsDialog(QtGui.QDialog, Ui_SettingsDialog):
    """
    The settings dialog class
    """

    __logger = logging.getLogger(__name__)

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.__loadSettings()


    def __loadSettings(self):
        """
        Initialize logger settings
        """
        settings = Settings()
        # TODO remove Config dependecies
        #languageHandler = LanguageHandler()
        languageHandler = LanguageHandler()
        i = 0
        for key, value in languageHandler.availableLanguages.iteritems():
            self.languageSelector.addItem('%s [%s]' % (value[0], key))
            if key == settings.language:
                self.languageSelector.setCurrentIndex(i)
            i = i + 1

        self.showLoggerOnStart.setChecked(settings.showLoggerOnStart)
        self.showErrors.setChecked(settings.showErrors)
        self.showDebug.setChecked(settings.showDebug)
        self.showInfo.setChecked(settings.showInfo)

        """ Loads the plugin settings """
        model = QtGui.QStandardItemModel()
        for plugin in settings.plugins:
            item = QtGui.QStandardItem(plugin)
            check = Qt.Checked if randint(0, 1) == 1 else Qt.Unchecked
            item.setCheckState(check)
            item.setCheckable(True)
            model.appendRow(item)

        self.pluginListView.setModel(model)


    def saveSettings(self):
        """
        Save the user settings.
        """
        settings = Settings()
        # Testing with QSettings
        settings.showLoggerOnStart = self.showLoggerOnStart.isChecked()
        settings.showErrors = self.showErrors.isChecked()
        settings.showDebug = self.showDebug.isChecked()
        settings.showInfo = self.showInfo.isChecked()

        # TODO Not pretty! 
        #      Find a more elegenta way of stripping the language code
        text = self.languageSelector.itemText(self.languageSelector.currentIndex())
        langCode = text[-4:].replace('[', '').replace(']', '')

        settings.language = langCode

        #self.close()
        QtGui.QDialog.accept(self)


    def cancelSettings(self):
        """
        Cancel the settings session. Ensure that no changed settings are
        written to the config file
        """
        todo = "[TODO] Cancel settings dialog routine: %s" % self.__class__
        self.__logger.debug(todo)
        self.__loadSettings()
        self.close()
        #QtGui.QDialog.reject(self)
