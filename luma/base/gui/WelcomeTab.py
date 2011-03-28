# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import Qt
from ..gui.design.WelcomeTabDesign import Ui_WelcomeTab

class WelcomeTab(QWidget, Ui_WelcomeTab):
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.settings = QSettings()
        self.checkBox.setCheckState(Qt.CheckState(self.settings.value("showWelcome",
        2).toInt()[0]))

    def dontShow(self, state):
        self.settings.setValue("showWelcome", state)
