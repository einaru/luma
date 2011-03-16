# -*- coding: utf-8 -*-
#
# base.gui.Dialog
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
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
    def __init__(self):
        QSplashScreen.__init__(self)
        self.setupUi()

    def setupUi(self):
        self.setObjectName(u'splash_screen')
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        splash_image = QPixmap(u':/icons/luma-128')
        self.setPixmap(splash_image)
        self.setMask(splash_image.mask())
        self.resize(128, 123)
        QMetaObject.connectSlotsByName(self)


#class Ui_SplashScreen(object):
#    
#    def setupUi(self, SplashScreen):
#        SplashScreen.setObjectName(u'SplashScreen')
#        SplashScreen.setWindowModality(Qt.NonModal)
#        SplashScreen.setEnabled(True)
#        SplashScreen.resize(400, 300)
#        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
#        sizePolicy.setHorizontalStretch(0)
#        sizePolicy.setVerticalStretch(0)
#        sizePolicy.setHeightForWidth(SplashScreen.sizePolicy().hasHeightForWidth())
#        SplashScreen.setSizePolicy(sizePolicy)
#        SplashScreen.setContextMenuPolicy(Qt.PreventContextMenu)
#        self.verticalLayout = QVBoxLayout(SplashScreen)
#        self.verticalLayout.setSpacing(0)
#        self.verticalLayout.setMargin(0)
#        self.verticalLayout.setObjectName(u'verticalLayout')
#        self.SplashImage = QLabel(SplashScreen)
#        self.SplashImage.setPixmap(QPixmap(u'/images/splash.png'))
#        self.SplashImage.setObjectName(u'SplashImage')
#        self.verticalLayout.addWidget(self.SplashImage)
#
#        self.retranslateUi(SplashScreen)
#        QMetaObject.connectSlotsByName(SplashScreen)
#
#    def retranslateUi(self, SplashScreen):
#        SplashScreen.setWindowTitle(QApplication.translate("SplashScreen", "Splash Screen", None, QApplication.UnicodeUTF8))
