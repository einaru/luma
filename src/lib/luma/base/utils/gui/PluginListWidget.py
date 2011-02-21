# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from base.utils.gui.PluginListWidgetDesign import Ui_pluginListWidget
from base.models.PluginLoaderModel import PluginLoaderModel

import sys
from random import randint

class PluginSettings(QWidget, Ui_pluginListWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        