# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
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

from PyQt4.QtCore import QSettings, QPoint, QSize, QVariant
from PyQt4.QtGui import QDesktopWidget, qApp

class Settings(QSettings):
    """
    The Settings class extends the QSettings class, to provide an easy and
    persistent way to set and retrive settings from different parts of the
    application.
    
    The main benefit for doing it this way is that the config sections and 
    keys is defined in one location, should we in the future decide to 
    change some of these.
    
    The class provides setters and getters for all settings values
    through the python property mechanism.
    """

    APPNAME = ORGNAME = 'luma'
    VERSION = '3.0.2-devel'

    def __init__(self):
        """
        The Settings constructor initializes the default settings values,
        which is provided as a fallback, should the config file somehow
        go missing. We use the qApp instance of The running QApplication
        to register organization and application name, as well as the 
        application version.
        """
        QSettings.__init__(self)
        """ Register application info throught the qApp instance """
        qApp.setOrganizationName(self.ORGNAME)
        qApp.setApplicationName(self.APPNAME)
        qApp.setApplicationVersion(self.VERSION)
        
        """ Defaults for section: mainwindow """
        self.__size = QSize(750, 500)
        screen = QDesktopWidget().screenGeometry()
        self.__position = QPoint((screen.width() - self.__size.width()) / 2, 
                                 (screen.height() - self.__size.height()) / 2)
        """ Defaults for section: i18n """
        self.__language = 'en'
        """ Defaults for section: logger """
        self.__showLoggerOnStart = QVariant(False)
        self.__showErrors = QVariant(True)
        self.__showDebug = QVariant(True)
        self.__showInfo = QVariant(True)

    def log(self, msg):
        self.__logger.info(msg)

    def set(self, key, value):
        self.setValue(key, self.__size)

    @property
    def size(self):
        return self.value('mainwin/size', self.__size).toSize()

    @size.setter
    def size(self, size):
        self.setValue('mainwin/size', size)

    @property
    def posistion(self):
        return self.value('mainwin/position', self.__position).toPoint()
    
    @posistion.setter
    def posistion(self, posistion):
        self.setValue('mainwin/position', posistion)
    
    @property
    def language(self):
        return self.value('i18n/language', self.__language).toString()
        
    
    @language.setter
    def language(self, language):
        self.setValue('i18n/language', language)
    
    @property
    def showLoggerOnStart(self):
        return self.value('logger/show_on_start', self.__showLoggerOnStart).toBool()
    
    @showLoggerOnStart.setter
    def showLoggerOnStart(self, showLoggerOnStart):
        self.setValue('logger/show_on_start', showLoggerOnStart)

    @property
    def showErrors(self):
        return self.value('logger/show_errors', self.__showErrors).toBool()

    @showErrors.setter
    def showErrors(self, showErrors):
        self.setValue('logger/show_errors', showErrors)
    
    @property
    def showDebug(self):
        return self.value('logger/show_debug', self.__showDebug).toBool()
    
    @showDebug.setter
    def showDebug(self, showDebug):
        self.setValue('logger/show_debug', showDebug)
    
    @property
    def showInfo(self):
        return self.value('logger/show_info', self.__showInfo).toBool()
    
    @showInfo.setter
    def showInfo(self, showInfo):
        self.setValue('logger/show_info', showInfo)
    
    @property
    def plugins(self):
        # TODO This is just temoporary, until we implement the actual 
        #      plugin loading code
        return [ "Adress book",
                 "Admin utils",
                 "Browser",
                 "Massive user creation",
                 "Schema browser",
                 "Search",
                 "Templates",
                 "User management" ]

