# -*- coding: utf-8 -*-
#
# base.gui.SplashScreen
#
# Copyright (c) 2011
#     Christian Forfang, <cforfang@gmail.com>
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
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

from PyQt4.QtCore import Qt, QMetaObject
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QSplashScreen

class SplashScreen(QSplashScreen):
    """ Defines the splash-screen used by Luma
    """
    
    def __init__(self):
        QSplashScreen.__init__(self)
        self.setupUi()

    def setupUi(self):
        self.setObjectName(u'splash_screen')
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        splash_image = QPixmap(u':/icons/128/luma')
        self.setPixmap(splash_image)
        self.setMask(splash_image.mask())
        self.resize(128, 128)
        QMetaObject.connectSlotsByName(self)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
