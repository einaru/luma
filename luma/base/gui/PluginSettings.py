# -*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from base.gui.PluginSettingsDialog import Ui_PluginsDialog
from base.model.PluginSettingsModel import PluginSettingsModel

class PluginSettings(QDialog, Ui_PluginsDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self._model = PluginSettingsModel()
        self.listView.setModel(self._model)

###############################################################################

    def pluginSelected(self, index):
        """
        Whenever a plugin is selected, the groupbox should be filled
        with a widget from the plugin for its settings.
        If no such widget is made for the plugin, the box will be empty.
        """
        plugin = self._model.itemFromIndex(index).plugin
        widget = plugin.getPluginSettingsWidget(self.stackedWidget)
        if widget is not None:
            self.stackedWidget.addWidget(widget)
            self.stackedWidget.setCurrentWidget(widget)
    
###############################################################################
        
    def reject(self):
        """
        When the main exit button (the X) is hit
        """
        self.closeButton()

###############################################################################
    
    def closeButton(self):
        self._model.saveSettings()
        self.accept()
