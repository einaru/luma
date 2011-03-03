# -*- coding: utf-8 -*-

#from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget
from base.util.gui.PluginListWidgetDesign import Ui_pluginListWidget
from base.util.model.PluginListWidgetModel import PluginListWidgetModel

import sys
from random import randint

class PluginListWidget(QWidget, Ui_pluginListWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        
        self._model = PluginListWidgetModel(self)
        self.listView.setModel(self._model)
        
    def pluginDoubleClicked(self, index):
        self.parent.pluginSelected(self._model.itemFromIndex(index).plugin)