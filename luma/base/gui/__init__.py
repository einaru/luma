# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# Luma is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public Licence as published by 
# the Free Software Foundation; either version 2 of the Licence, or 
# (at your option) any later version.
#
# Luma is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence 
# for more details.
#
# You should have received a copy of the GNU General Public Licence along 
# with Luma; if not, write to the Free Software Foundation, Inc., 
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

from PyQt4.QtCore import QSettings, QPoint, QSize, QVariant, Qt, QMetaObject
from PyQt4.QtGui import QApplication, qApp
from PyQt4.QtGui import QDesktopWidget
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QSizePolicy, QSplashScreen
from PyQt4.QtGui import QVBoxLayout

class Settings(QSettings):
    """ The Settings class extends the QSettings class, to provide an
    easy and persistent way to set and retrive settings from different
    parts of the application.
    
    The main benefit for doing it this way is that the config sections
    and keys is defined in one location, should we in the future decide
    to change some of these.
    
    The class provides setters and getters for all settings values
    through the python property mechanism.
    
    The following settings is available:
    
        [general]
        save_window_size=<bool>
        save_window_position=<bool>
        
        [mainwin]
        size=<QSize>
        position=<QPoint>
        
        [i18n]
        language=<ISO 638-1 code>
        
        [logger]
        show_on_start=<bool>
        show_errors=<bool>
        show_debug=<bool>
        show_info=<bool>
    """

    def __init__(self):
        """ The Settings constructor initializes the default settings
        values, which is provided as a fallback, should the config file
        somehow go missing. We use the qApp instance of The running
        QApplication to register organization and application name, as
        well as the application version.
        """
        QSettings.__init__(self)
        
        # This is the path prefix where we store all luma related
        # files (serverlist, templates, filter bookmarks etc.)
        self.__configPrefix = ''
        
        # Defaults for section: mainwindow
        self.__maximize = False
        self.__size = QSize(750, 500)
        screen = QDesktopWidget().screenGeometry()
        self.__position = QPoint((screen.width() - self.__size.width()) / 2,
                                 (screen.height() - self.__size.height()) / 2)
        # Defaults for section: i18n
        self.__language = u'en'
        # Defaults for section: logger
        self.__showOnStart = False
        self.__showErrors = True
        self.__showDebug = True
        self.__showInfo = True

    @property
    def configPrefix(self):
        return self.value(u'application/config_prefix', self.__configPrefix).toString()
    
    @configPrefix.setter
    def configPrefix(self, path):
        self.setValue(u'application/config_prefix', path)

    @property
    def maximize(self):
        return self.value(u'mainwin/maximize', self.__maximize).toBool()

    @maximize.setter
    def maximize(self, maximize):
        self.setValue(u'mainwin/maximize', maximize)

    @property
    def size(self):
        return self.value(u'mainwin/size', self.__size).toSize()

    @size.setter
    def size(self, size):
        self.setValue(u'mainwin/size', size)

    @property
    def position(self):
        return self.value(u'mainwin/position', self.__position).toPoint()

    @position.setter
    def position(self, position):
        self.setValue(u'mainwin/position', position)

    @property
    def language(self):
        return self.value(u'i18n/language', self.__language).toString()

    @language.setter
    def language(self, language):
        self.setValue(u'i18n/language', language)

    @property
    def showLoggerOnStart(self):
        return self.value(u'logger/show_on_start', self.__showOnStart).toBool()

    @showLoggerOnStart.setter
    def showLoggerOnStart(self, show):
        self.setValue(u'logger/show_on_start', show)

    @property
    def showErrors(self):
        return self.value(u'logger/show_errors', self.__showErrors).toBool()

    @showErrors.setter
    def showErrors(self, show):
        self.setValue(u'logger/show_errors', show)

    @property
    def showDebug(self):
        return self.value(u'logger/show_debug', self.__showDebug).toBool()

    @showDebug.setter
    def showDebug(self, show):
        self.setValue(u'logger/show_debug', show)

    @property
    def showInfo(self):
        return self.value(u'logger/show_info', self.__showInfo).toBool()

    @showInfo.setter
    def showInfo(self, show):
        self.setValue(u'logger/show_info', show)

    @property
    def plugins(self):
        # TODO This is just temoporary, until we implement the actual 
        #      plugin loading code
        return [ u'Adress book',
                 u'Admin utils',
                 u'Browser',
                 u'Massive user creation',
                 u'Schema browser',
                 u'Search',
                 u'Templates',
                 u'User management' ]

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
