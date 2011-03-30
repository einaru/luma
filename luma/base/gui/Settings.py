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

from ..util import encodeUTF8

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
    def state(self):
        return self.value('application/state').toByteArray()

    @state.setter
    def state(self, state):
        self.setValue('application/state', state)

    @property
    def geometry(self):
        return self.value('application/geometry').toByteArray()

    @geometry.setter
    def geometry(self, geometry):
        self.setValue('application/geometry', geometry)
        
    @property
    def configPrefix(self):
        return self.value('application/config_prefix', self.__configPrefix).toString()
    
    @configPrefix.setter
    def configPrefix(self, path):
        self.setValue('application/config_prefix', path)

    @property
    def maximize(self):
        return self.value('mainwin/maximize', self.__maximize).toBool()

    @maximize.setter
    def maximize(self, maximize):
        self.setValue('mainwin/maximize', maximize)

    @property
    def size(self):
        return self.value('mainwin/size', self.__size).toSize()

    @size.setter
    def size(self, size):
        self.setValue('mainwin/size', size)

    @property
    def position(self):
        return self.value('mainwin/position', self.__position).toPoint()

    @position.setter
    def position(self, position):
        self.setValue('mainwin/position', position)

    @property
    def language(self):
        return self.value('i18n/language', self.__language).toString()

    @language.setter
    def language(self, language):
        self.setValue('i18n/language', language)

    @property
    def showLoggerOnStart(self):
        return self.value('logger/show_on_start', self.__showOnStart).toBool()

    @showLoggerOnStart.setter
    def showLoggerOnStart(self, show):
        self.setValue('logger/show_on_start', show)

    @property
    def showErrors(self):
        return self.value('logger/show_errors', self.__showErrors).toBool()

    @showErrors.setter
    def showErrors(self, show):
        self.setValue('logger/show_errors', show)

    @property
    def showDebug(self):
        return self.value('logger/show_debug', self.__showDebug).toBool()

    @showDebug.setter
    def showDebug(self, show):
        self.setValue('logger/show_debug', show)

    @property
    def showInfo(self):
        return self.value('logger/show_info', self.__showInfo).toBool()

    @showInfo.setter
    def showInfo(self, show):
        self.setValue('logger/show_info', show)

    def genericValue(self, key, default):
        """Utility method for getting an arbitrary setting value.
        
        @param key: string;
            The key to get the value of
        @default:
            The default fallback value, if no value is found for the
            key.
        """
        return self.value(key, default)

    def setGenericValue(self, key, value):
        """Utility method for setting an arbitrary setting value.
        
        @param key: string;
            The key to store the value in.
        @param value:
            The value to store.
        """
        self.setValue(key, value)


class PluginSettings(object):
    """Wrapper Settings class for plugins.
    
    This is a generic settings class, which provide consistent loading
    and saving of settings for plugins.
    It works by providing the plugin name to the constructor, and using
    this value to retrive and save settings in the main luma settings
    file.
    """
    
    def __init__(self, pluginName):
        """
        @param pluginName: string;
            The name of the plugin, usually the plugin.name value found
            in the plugins __init__.py file.
            NOTE: The plugin name must be distinct from other plugins,
                  as it will be the main key to retrive values from the
                  settings file.
        """
        self.s = QSettings()
        self.name = pluginName
    
    def pluginValue(self, key, default):
        return self.s.value('plugins/{0}/{1}'.format(self.name, key), default)
    
    def setPluginValue(self, key, value):
        self.s.setValue('plugins/{0}/{1}'.format(self.name, key), value)
    
    @property
    def configPrefix(self):
        return encodeUTF8(self.s.value('application/config_prefix').toString())
