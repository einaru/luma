# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from base.utils.gui.PluginListWidgetDesign import Ui_pluginListWidget
from base.utils.models.PluginListWidgetModel import PluginListWidgetModel

import sys
from random import randint

class PluginListWidget(QWidget, Ui_pluginListWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        
        self._model = PluginListWidgetModel()
        self.listView.setModel(self._model)
        
    def pluginDoubleClicked(self):
        print "TRYKKE TRYKKE!"

            