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

from base.gui.SettingsDialogDesign import Ui_SettingsDialog

class SettingsDialog(QtGui.QDialog, Ui_SettingsDialog):
    """
    The settings dialog class
    """
    
    __logger = logging.getLogger(__name__)
    
    def __init__(self, configObject):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.configObject = configObject
        
        """
        Initialize general settings
        """
        languageHandler = self.configObject.languageHandler
        i = 0
        for key, value in languageHandler.availableLanguages.iteritems():
            self.languageSelector.addItem('%s [%s]' % (value, key))
            if key == self.configObject.language:
                self.languageSelector.setCurrentIndex(i)
            i = i + 1
        
        """
        Initialize logger settings
        """
        self.showErrors.setChecked(self.configObject.showErrors)
        self.showDebug.setChecked(self.configObject.showDebug)
        self.showInfo.setChecked(self.configObject.showInfo)
        
        """
        Initialize plugin settings
        """
        
        model = QtGui.QStandardItemModel()

        for plugin in self.configObject.plugins:                   
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
        self.configObject.showErrors = self.showErrors.isChecked()
        self.configObject.showDebug = self.showDebug.isChecked()
        self.configObject.showInfo = self.showInfo.isChecked()
        
        text = self.languageSelector.itemText(self.languageSelector.currentIndex())
        
        # TODO Not pretty! 
        #      Find a more elegenta way of stripping the language code
        langCode = text[-4:].replace('[', '').replace(']', '')
        self.configObject.language = langCode
        
        self.configObject.saveSettings()
        self.close()
    
    
    def cancelSettings(self):
        """
        Cancel the settings session. Ensure that no changed settings are
        written to the config file
        """
        todo = "[TODO] Cancel settings dialog routine: %s" % self.__class__
        self.__logger.debug(todo)
        self.close()