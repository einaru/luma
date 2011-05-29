# -*- coding: utf-8 -*-
#
# base.gui.Settings
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
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
    """The Settings class extends the QSettings class, to provide an
    easy and persistent way to set and retrive settings from different
    parts of the application.

    The main benefit for doing it this way is that the config sections
    and keys is defined in one location, should we in the future decide
    to change some of these.

    The class provides setters and getters for all settings values
    through the python property mechanism.

    The following settings is available::

        [General]
        showWelcome=0

        [application]
        config_prefix=<string>
        geometry=<ByteArray>

        [logger]
        show_logger_on_start=<bool>
        show_logger<bool>
        show_errors<bool>
        show_debug<bool>
        show_info<bool>
        show_on_start=<bool>

        [i18n]
        language=<string>

    """

    def __init__(self):
        """ The Settings constructor initializes the default settings
        values, which is provided as a fallback, should the config file
        somehow go missing. We use the ``qApp`` instance of The running
        ``QApplication`` to register organization and application name,
        as well as the application version.
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
        self.__showLoggerOnStart = False
        self.__showLogger = False
        self.__showErrors = True
        self.__showDebug = True
        self.__showInfo = True

    @property
    def state(self):
        key = 'application/state'
        return self.value(key).toByteArray()

    @state.setter
    def state(self, value):
        key = 'application/state'
        self.setValue(key, value)

    @property
    def geometry(self):
        key = 'application/geometry'
        return self.value(key).toByteArray()

    @geometry.setter
    def geometry(self, value):
        key = 'application/geometry'
        self.setValue(key, value)

    @property
    def configPrefix(self):
        key = 'application/config_prefix'
        return self.value(key, self.__configPrefix).toString()

    @configPrefix.setter
    def configPrefix(self, value):
        key = 'application/config_prefix'
        self.setValue(key, value)

    @property
    def maximize(self):
        key = 'mainwin/maximize'
        return self.value(key, self.__maximize).toBool()

    @maximize.setter
    def maximize(self, value):
        key = 'mainwin/maximize'
        self.setValue(key, value)

    @property
    def size(self):
        key = 'mainwin/size'
        return self.value(key, self.__size).toSize()

    @size.setter
    def size(self, value):
        key = 'mainwin/size'
        self.setValue(key, value)

    @property
    def position(self):
        key = 'mainwin/position'
        return self.value(key, self.__position).toPoint()

    @position.setter
    def position(self, value):
        key = 'mainwin/position'
        self.setValue(key, value)

    @property
    def language(self):
        key = 'i18n/language'
        return self.value(key, self.__language).toString()

    @language.setter
    def language(self, value):
        key = 'i18n/language'
        self.setValue(key, value)

    @property
    def showLoggerOnStart(self):
        key = 'logger/show_logger_on_start'
        return self.value(key, self.__showLoggerOnStart).toBool()

    @showLoggerOnStart.setter
    def showLoggerOnStart(self, value):
        key = 'logger/show_logger_on_start'
        self.setValue(key, value)

    @property
    def showLogger(self):
        key = 'logger/show_logger'
        return self.value(key, self.__showLogger).toBool()

    @showLogger.setter
    def showLogger(self, value):
        key = 'logger/show_logger'
        self.setValue(key, value)

    @property
    def showErrors(self):
        key = 'logger/show_errors'
        return self.value(key, self.__showErrors).toBool()

    @showErrors.setter
    def showErrors(self, value):
        key = 'logger/show_errors'
        self.setValue(key, value)

    @property
    def showDebug(self):
        key = 'logger/show_debug'
        return self.value(key, self.__showDebug).toBool()

    @showDebug.setter
    def showDebug(self, value):
        key = 'logger/show_debug'
        self.setValue(key, value)

    @property
    def showInfo(self):
        key = 'logger/show_info'
        return self.value(key, self.__showInfo).toBool()

    @showInfo.setter
    def showInfo(self, value):
        key = 'logger/show_info'
        self.setValue(key, value)

    def genericValue(self, key, default):
        """Returns an arbitrary settings value, corrosponding to `key`.
        The `default` value is used should the `key` contain no value.

        :param key: the name of the key to get the value from.
        :type key: string
        :param default: the value to be used as fallback if `key`
         contains no value.
        """
        return self.value(key, default)

    def setGenericValue(self, key, value):
        """Utility method for setting an arbitrary setting value.

        :param key: the key for the value.
        :type key: string
        :param value: the value to be saved.
        """
        self.setValue(key, value)


class PluginSettings(object):
    """Wrapper Settings class for plugins.

    This is a generic settings class, which provide consistent loading
    and saving of settings for plugins. It works by providing the
    plugin name to the constructor, and using this value to retrive and
    save settings in the main luma settings file.
    """

    def __init__(self, pluginName):
        """The `PluginSettings` contructor.

        :param pluginName: the name of the plugin. In most cases this
         will be the same as the ``plugin.name`` value in the top level
         plugin``__init__.py`` file. The plugin name must be distinct
         from other plugins (and keys in the settings file), as it will
         be the main key to retrive values from the settings file.
        :type pluginName: string
        """
        self.s = QSettings()
        self.name = pluginName

    def pluginValue(self, key, default):
        """Returns the plugin settings value for the `key`, if such a
        value exists. If not the `default` value is returned.

        :param key: the name of the key to get the value from.
        :type key: string
        :param default: the value to be used as fallback if `key`
         contains no value.
        """
        return self.s.value('plugins/{0}/{1}'.format(self.name, key), default)

    def setPluginValue(self, key, value):
        """Saves a `value` associated with a `key` to the settings file.

        :param key: the key for the value.
        :type key: string
        :param value: the value to be saved.
        """
        self.s.setValue('plugins/{0}/{1}'.format(self.name, key), value)

    @property
    def configPrefix(self):
        prefix = self.s.value('application/config_prefix').toString()
        return unicode(prefix).encode('utf-8')


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
