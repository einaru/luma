# -*- coding: utf-8 -*-
#
# base.backend.PluginLoader
#
# Copyright (C) 2011
#     Johannes Harestad, <johanhar@stud.ntnu.no>
#
# This is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# oya-invitationals is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from os import listdir
import imp
from os import path
import logging

from ..util.Paths import getLumaRoot


class PluginObject(object):
    """This object is for keeping information about a Plugin.
    """

    def __init__(self):
        self.lumaPlugin = True
        self.pluginName = None
        self.author = None
        self.pluginUserString = None
        self.version = None
        self.getIcon = None
        self.getPluginWidget = None
        self.getPluginSettingsWidget = None
        self.icon = None
        self.load = False


class PluginLoader(object):
    """This is the new version of PluginLoader, with the use of a
    PluginObject.

    The plugins field is a list of PluginObjects.
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, pluginsToLoad=[]):
        self.__pluginsToLoad = pluginsToLoad
        self.__plugins = []
        self.__changed = True
        self.__pluginsBaseDir = path.join(getLumaRoot(), 'plugins')

    @property
    def pluginsToLoad(self):
        return self.__pluginsToLoad

    @pluginsToLoad.setter
    def pluginsToLoad(self, value):
        self.__changed = True
        self.__pluginsToLoad = value

    @property
    def plugins(self):
        """It should not be possible to set the plugin field from
        outside, therefore no ``plugins.setter`` is available.
        """
        if self.__changed == True:
            self.__loadPlugins()
            self.__changed = False

        return self.__plugins

    def __loadPlugins(self):
        """Will load plugins from the directories returned by
        `__findPluginDirectories`.
        """
        self.__plugins = []

        pluginDirs = self.__findPluginDirectories()
        if not pluginDirs:
            return

        for x in pluginDirs:
            if x in ['CVS', '.svn', '.git']:
                continue

            try:
                self.__plugins.append(self.__readMetaInfo(x))

            except PluginMetaError, y:
                msg = 'Plugin {0} gave an exception:\n{1}'
                self.__logger.error(msg.format(str(x), str(y)))

    def __findPluginDirectories(self):
        """Returns a list of directories found inside `pluginBaseDir`.
        """
        tmpList = []

        try:
            #look for directories
            for x in listdir(self.__pluginsBaseDir):
                xPath = path.join(self.__pluginsBaseDir, x)

                if path.isdir(xPath):
                    tmpList.append(x)

            return tmpList

        except OSError, e:
            msg = 'Could not read from directory where plugins are stored.'
            self.__logger.error('{0} Reason:\n{1}'.format(msg, str(e)))

    def __readMetaInfo(self, pluginName):
        """Reads meta information for a plugin by its directory.

        If the plugin is in pluginsToLoad, the load attribute will be
        set to True  All of the meta information about a plugin will be
        put into a PluginObject.
        """
        plugin = PluginObject()

        attributes = [
            'lumaPlugin',
            'pluginName',
            'author',
            'pluginUserString',
            'version',
            'getIcon',
            'getPluginWidget',
            'getPluginSettingsWidget'
        ]

        importedModule = None

        try:
            searchList = [self.__pluginsBaseDir]
            foundModule = imp.find_module(pluginName, searchList)
            importedModule = imp.load_module(pluginName, *foundModule)
        except ImportError, e:
            msg = 'Plugin meta information could not be loaded. Reason:\n{0}'
            self.__logger.error(msg.format(str(e)))
            raise PluginMetaError(e)

        missingAttributes = []
        for x in attributes:
            if not hasattr(importedModule, x):
                missingAttributes.append(x)

        if len(missingAttributes) > 0:
            msg = 'Loaded module {0} is not a Luma plugin.'.format(pluginName)
            raise PluginMetaError('{0} Attributes are missing!'.format(msg))

        plugin.pluginName = importedModule.pluginName
        plugin.pluginUserString = importedModule.pluginUserString
        plugin.author = importedModule.author
        plugin.version = importedModule.version
        plugin.getPluginWidget = importedModule.getPluginWidget
        plugin.getPluginSettingsWidget = importedModule.getPluginSettingsWidget

        try:
            plugin.icon = importedModule.getIcon()
        except Exception, e:
            msg = 'Plugin {0} gave error: {1}'
            self.__logger.error(msg.format(plugin.pluginName, str(e)))

        if self.__pluginsToLoad == 'ALL':
            plugin.load = True
        else:
            for ptl in self.__pluginsToLoad:
                if plugin.pluginName == ptl:
                    plugin.load = True
                    break

        return plugin


class PluginMetaError(Exception):
    """When `__readMetaInfo` discovers a directory in the search path
    with corrupted metainfo, this exception is raised.
    """
    pass


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
