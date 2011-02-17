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
from os import listdir

from base.utils import Paths

@DeprecationWarning
class LanguageHandler(object):
    """
    Helper class providing useful functionality for handling available
    application translations
    """
    
    """
    We use the ISO 638-1 standard for 2 char language codes:
    http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    """
    __isoCodeMappings = {
        "de" : u"Deutch", # German
        "en" : u"English", # English
        "no" : u"Norsk", # Norwegian
        "pt" : u"Português", # Portugese
        "cs" : u"České", # Czech
        "se" : u"Svensk", # Swedish
        "ru" : u"Россию", # Russian
        "fr" : u"Français", # French
        "se" : u"Español", # Spanish
        "jp" : u"日本", # Japanse
    }
    
    __availableLanguages = {}
    
    
    def __init__(self, path=None):
        """
        This constructure must be given the full path to where the 
        translation files are located.
        """
#        global isoCodeMappings
#        global __availableLanguages
        paths = Paths()
        self.__translationPath = paths.i18nPath
        # Must be put in manually because there exists no translation file
        self.__availableLanguages['en'] = 'English'
        if os.path.isdir(self.__translationPath):
            self.__buildLanguageDictionary()
    
    def __buildLanguageDictionary(self):
        """
        Scannes @path for available translation files, and builds a 
        dictionary with the language code as key and language name as 
        value. This works as long as we are consitent in filname 
        conventions for these files.
        
            luma_<iso-code>.qm
        
        It's a hack but it works (provided we got < 10 translation files:)
        """
        for file in listdir(self.__translationPath):
            if (file[:5] == 'luma_') and (file[-3:] == '.qm'):
                code = file[5:-3]
                for key, value in self.__isoCodeMappings.iteritems():
                    if code == key:
                        self.__availableLanguages[code] = value
    
    @property
    def availableLanguages(self):
        """
        Returns a dictionary containing all available language translations
        """
        return self.__availableLanguages

