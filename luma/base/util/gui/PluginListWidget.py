# -*- coding: utf-8 -*-

<<<<<<< HEAD
#from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget
=======
from PyQt4.QtCore import *
from PyQt4.QtGui import *
>>>>>>> S3-installation-v2
from base.util.gui.PluginListWidgetDesign import Ui_pluginListWidget
from base.util.model.PluginListWidgetModel import PluginListWidgetModel

import sys
<<<<<<< HEAD
import logging

class PluginListWidget(QWidget, Ui_pluginListWidget):
    """
    Used by mainwin to show the list of plugins that can be loaded
    
    Parent is given to the model, because it is going to contain not only
    the QStandardItems but the widget for each item, that requires a parent.
    """
    _logger = logging.getLogger(__name__)
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        
        self.parent = parent
        self.setupUi(self)

        self.listView.setModel(PluginListWidgetModel(self.parent))

        
        self._model = PluginListWidgetModel(self)
        self.listView.setModel(self._model)

        
    def pluginDoubleClicked(self, index):
        if self.parent and hasattr(self.parent, "pluginSelected"):
            self.parent.pluginSelected(self.listView.model().itemFromIndex(index))
        else:
            self._logger.error("Cannot enter a plugin when no parent is given to PluginListWidget")       
    
    def updatePlugins(self):
        """
        Updates the listview with new plugins
        """
        self.listView.reset()
        self.listView.setModel(PluginListWidgetModel(self.parent))
=======
from random import randint

class PluginListWidget(QWidget, Ui_pluginListWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        
        self._model = PluginListWidgetModel()
        self.listView.setModel(self._model)
        
    def pluginDoubleClicked(self, index):
        self.parent.pluginSelected(self._model.itemFromIndex(index).plugin)
>>>>>>> S3-installation-v2
