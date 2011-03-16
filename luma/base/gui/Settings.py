# -*- coding: utf-8 -*-
#
# base.gui.Settings
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

from PyQt4.QtCore import QSettings, QPoint, QSize
from PyQt4.QtGui import QDesktopWidget

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
        """
        The Settings constructor initializes the default settings values,
        which is provided as a fallback, should the config file somehow
        go missing. We use the qApp instance of The running QApplication
        to register organization and application name, as well as the 
        application version.
        """
        QSettings.__init__(self)
        """ Register application info throught the qApp instance """
        
        """ Defaults for section: mainwindow """
        self.__size = QSize(750, 500)
        screen = QDesktopWidget().screenGeometry()
        self.__position = QPoint((screen.width() - self.__size.width()) / 2,
                                 (screen.height() - self.__size.height()) / 2)
        """ Defaults for section: i18n """
        self.__language = u'en'
        """ Defaults for section: logger """
        self.__showOnStart = False
        self.__showErrors = True
        self.__showDebug = True
        self.__showInfo = True

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