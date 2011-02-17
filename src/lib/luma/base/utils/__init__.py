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

class Paths(object):
    """
    The Paths class is a worshipper of the evil Singleton pattern.
    It thinks it provides a clever solution to the resource path
    problem, but will it fail EPIC when the debugging starts ?
    
    It uses the python property mechanism to provide setters and getters.
    """
    __instance = None
    __i18nPath = None

    def __new__(cls, *args, **kwargs):
        """
        Overrides the __new__ method and checks if there exists an
        instance of this class.
        
        Returns the instance if one exists, creates a new one if not.
        """
        if not cls.__instance:
            cls.__instance = super(Paths, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    @property
    def i18nPath(self):
        return self.__i18nPath

    @i18nPath.setter
    def i18nPath(self, path):
        self.__i18nPath = path

import os
from os import listdir

class LanguageHandler(object):
    """
    Helper class providing useful functionality for handling available
    application translations
    """

    """
    We use the ISO 638-1 standard for 2 char language codes:
    http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    """
    __isolangCodes = {
        u'af' : [u'Afrikaans', u'Afrikaans'],
        u'ar' : [u'العربية', u'Arabic'],
        u'be' : [u'Беларуская', u'Belarusian'],
        u'bg' : [u'Български', u'Bulgarian'],
        u'ca' : [u'Català', u'Catalan'],
        u'cs' : [u'České', u'Czech'],
        u'cy' : [u'Cymraeg', u'Welsh'],
        u'da' : [u'Dansk', u'Danish'],
        u'de' : [u'Deutsch', u'German'],
        u'el' : [u'Ελληνικά', u'Greek'],
        u'en' : [u'English', u'English'],
        u'es' : [u'Español', u'Spanish'],
        u'et' : [u'Eesti', u'Estonian'],
        u'fa' : [u'فارسی', u'Persian'],
        u'fi' : [u'Suomalainen', u'Finnish'],
        u'fr' : [u'Française', u'French'],
        u'ga' : [u'Na hÉireann', u'Irish'],
        u'gl' : [u'Galego', u'Galician'],
        u'he' : [u'עברית', u'Hebrew'],
        u'hi' : [u'हिन्दी', u'Hindi'],
        u'hr' : [u'Hrvatski', u'Croatian'],
        u'hu' : [u'Magyar', u'Hungarian'],
        u'id' : [u'Bahasa Indonesia', u'Indonesian'],
        u'is' : [u'Íslenska', u'Icelandic'],
        u'it' : [u'Italiano', u'Italian'],
        u'ja' : [u'日本', u'Japanese'],
        u'ko' : [u'한국어', u'Korean'],
        u'lt' : [u'Lietuvos', u'Lithuanian'],
        u'lv' : [u'Latvijā', u'Latvian'],
        u'mk' : [u'Македонски', u'Macedonian'],
        u'ms' : [u'Melayu', u'Malay'],
        u'mt' : [u'Malti', u'Maltese'],
        u'nl' : [u'Nederlandse', u'Dutch'],
        u'no' : [u'Norsk', u'Norwegian'],
        u'pl' : [u'Polska', u'Polish'],
        u'pt' : [u'Português', u'Portuguese'],
        u'ro' : [u'Română', u'Romanian'],
        u'ru' : [u'Россию', u'Russian'],
        u'sk' : [u'Slovenskému', u'Slovak'],
        u'sl' : [u'Slovenščina', u'Slovenian'],
        u'sq' : [u'Shqiptar', u'Albanian'],
        u'sr' : [u'Српска', u'Serbian'],
        u'sv' : [u'Svenska', u'Swedish'],
        u'sw' : [u'Swahili', u'Swahili'],
        u'th' : [u'ไทย', u'Thai'],
        u'tl' : [u'Filipino', u'Filipino'],
        u'tr' : [u'Türk', u'Turkish'],
        u'uk' : [u'Українське', u'Ukrainian'],
        u'vi' : [u'Việt', u'Vietnamese'],
        u'yi' : [u'ייִדיש', u'Yiddish'],
        u'zh' : [u'中文', u'Chinese'],
    }

    __availableLanguages = {}

    def __init__(self):
        """
        This constructure must be given the full path to where the 
        translation files are located.
        """
        paths = Paths()
        self.__translationPath = paths.i18nPath
        # Must be put in manually because there exists no translation file
        self.__availableLanguages['en'] = ['English', 'English']
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
                for key, value in self.__isolangCodes.iteritems():
                    if code == key:
                        self.__availableLanguages[code] = value

    @property
    def availableLanguages(self):
        """
        Returns a dictionary containing all available language translations
        The dictionary is structured like this:
            { ... ,
            <iso_code> : [ <native name>, <english name> ] ,
            ... }
        """
        return self.__availableLanguages

    @property
    def translationPath(self):
        return self.__translationPath

    def getQmFile(self, isoCode):
        if isoCode == 'en':
            return 'NATIVE'
        return os.path.join(self.translationPath, 'luma_%s.qm' % isoCode)
