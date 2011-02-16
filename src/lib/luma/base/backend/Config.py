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

import os
import ConfigParser

from base.backend.LanguageHandler import LanguageHandler
import logging

class Config(object):
    """
    Config object providing acess to the Luma application settings.
    """
    __settings_skeleton = {
        "ui" : {
            "__width"  : 0,
            "__height" : 0,
        },
        "logger" : {
            "show_errors" : True,
            "show_debug"  : True,
            "show_info"   : True,
        },
        "i18n" : {
            "__language" : "en"
        }
    }

    __logger = logging.getLogger(__name__)

    def __init__(self, configPrefix, i18nPath):
        """
        Initialize default settings values
        """
        self.__i18nPath = i18nPath
        self.__lh = LanguageHandler(self.__i18nPath)

        self.__configPrefix = configPrefix
        self.__configFile = 'luma.cfg'
        """
        config file sections and values
        """
        self.__sectionUi = 'ui'
        self.__width = 540
        self.__height = 550
        self.__sectionLogger = 'logger'
        self.__showErrors = True
        self.__showDebug = True
        self.__showInfo = True
        self.__sectionI18n = 'i18n'
        self.__language = "en"


    def saveSettings(self):
        """
        Save the current settings to disk
        """
        cp = ConfigParser.ConfigParser()
        cp.add_section(self.__sectionUi)
        cp.set(self.__sectionUi, 'width', self.__width)
        cp.set(self.__sectionUi, 'height', self.__height)
        cp.add_section(self.__sectionLogger)
        cp.set(self.__sectionLogger, 'show_errors', self.__showErrors)
        cp.set(self.__sectionLogger, 'show_debug', self.__showDebug)
        cp.set(self.__sectionLogger, 'show_info', self.__showInfo)
        cp.add_section(self.__sectionI18n)
        cp.set(self.__sectionI18n, 'language', self.__language)

        try:
            configFile = os.path.join(self.__configPrefix, self.__configFile)
#            with open(os.path.join(configFile), 'w') as cfg:
#                cp.write(cfg)
            todo = "TODO: Save Settings: %s" % self.__class__
            self.__logger.debug(todo)

        except IOError, ioe:
            # TODO Do some logging. 
            #      Most Likely it's a file permission issue.
            error = 'Unable to save config file:%s\n%s' % (configFile, ioe)
            self.__logger.error(error)


    def loadSettings(self):
        """
        Read and load settings from disk
        """
        cp = ConfigParser.ConfigParser()
        cfgFullPath = os.path.join(self.__configPrefix, self.__configFile)
        if os.path.isfile(os.path.join(cfgFullPath)):
            cp.read(cfgFullPath)
        else:
            msg = "No Read access on %s\n%s" % (cfgFullPath, self.__class__)
            self.__logger.debug(msg)
            return

        self.__width = cp.getint(self.__width, 'width')
        self.__height = cp.getint(self.__height, 'height')

        self.__showErrors = cp.getboolean(self.__sectionLogger, 'showErrors')
        self.__showDebug = cp.getboolean(self.__sectionLogger, 'showDebug')
        self.__showInfo = cp.getboolean(self.__sectionLogger, 'showInfo')

        self.__language = cp.get(self.__sectionI18n, 'language')


    """
    Python @property: setters and getters
    """

    @property
    def configPrefix(self):
        return self.__configPrefix

    @configPrefix.setter
    def configPrefix(self, configPrefix):
        self.__configPrefix = configPrefix

    @property
    def languageHandler(self):
        return self.__lh

    @property
    def i18nPath(self):
        return self.__i18nPath

    @i18nPath.setter
    def i18nPath(self, path):
        self.__i18nPath = path

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        self.__height = height

    @property
    def showErrors(self):
        return self.__showErrors

    @showErrors.setter
    def showErrors(self, showErrors):
        self.__showErrors = showErrors

    @property
    def showDebug(self):
        return self.__showDebug

    @showDebug.setter
    def showDebug(self, showDebug):
        self.__showDebug = showDebug

    @property
    def showInfo(self):
        return self.__showInfo

    @showInfo.setter
    def showInfo(self, showInfo):
        self.__showInfo = showInfo

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, language):
        self.__language = language

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
