# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget
from ..gui.design.AboutPluginDesign import Ui_AboutPlugin

class AboutPlugin(QWidget, Ui_AboutPlugin):
    def __init__(self, plugin, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        if not plugin:
            return

        self.label_name.setText(plugin.pluginUserString)
        self.label_version.setText(plugin.version)
        self.label_author.setText(plugin.author)

