# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public Licence as published by the Free Software
# Foundation; either version 2 of the Licence, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence for more 
# details.
#
# You should have received a copy of the GNU General Public Licence along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA  02110-1301, USA

#from ConfigParser import ConfigParser

from base.backend.LanguageHandler import LanguageHandler

class Config(object):
    """
    Config object providing acess to the Luma application settings.
    """ 
    __configPrefix      = ""
    __i18nPath          = ""
    __settings_skeleton = {
        "ui" : {
            "width"  : 0,
            "height" : 0,
        }, 
        "logger" : {
            "show_errors" : True,
            "show_debug"  : True,
            "show_info"   : True,
        },
        "i18n" : {
            "language" : "en"
        }
    }
    
    def __init__(self, configPrefix, i18nPath):
        self.__configPrefix  = configPrefix
        self.__i18nPath = i18nPath
        self.__lh = LanguageHandler(self.__i18nPath)
        
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