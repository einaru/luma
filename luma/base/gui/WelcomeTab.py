# -*- coding: utf-8 -*-
#
# base.gui.WelcomeTab
#
# Copyright (c) 2011:
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

from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import Qt
from ..gui.design.WelcomeTabDesign import Ui_WelcomeTab

class WelcomeTab(QWidget, Ui_WelcomeTab):
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.settings = QSettings()
        show = self.settings.value('showWelcome', 2).toInt()[0]
        self.checkBox.setCheckState(Qt.CheckState(show))

    def dontShow(self, state):
        self.settings.setValue('showWelcome', state)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
