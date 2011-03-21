# -*- coding: utf-8 -*-
#
# base.util.i18n
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
from PyQt4.QtCore import (QDir, QString)

class LanguageHandler(object):
    """ Helper class providing useful functionality for handling
    available application translations.

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
        u'hx' : [u'h4x0r', u'01101000 00110100 01111000 00110000 01110010'],
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
        self.__translationPath = QDir(':/i18n')
        
        # Must be put in manually because there exists no translation file
        # UPDATE: well it does now, but we'll keep it this way none the less
        self.__availableLanguages['en'] = ['English', 'English']
        self.__buildLanguageDictionary()

    def __buildLanguageDictionary(self):
        """ Scannes the resources for  available translation files, and
        builds a dictionary with the language code as key and language
        name as value. This works as long as we are consitent in filname
        conventions for these files.
        
            luma_<iso-code>.qm
        
        It's a hack but it works (provided we got < 10 translation files:)
        """
        for i18n in self.__translationPath:
            for iso, lang in self.__isolangCodes.iteritems():
                if i18n == iso:
                    self.__availableLanguages[iso] = lang

    @property
    def availableLanguages(self):
        """ The available application language translations are
        returned in a dictionary on the form:
            { ... ,
            <iso code> : [ <native name>, <english name> ],
            ... }
        
        @return: A dictionary containing all available application 
                 languages.
        """
        return self.__availableLanguages

    @property
    def translationPath(self):
        """
        @return: The full path to the directory containing the 
                 translation files.
        """
        return self.__translationPath

    def getQmFile(self, isoCode=''):
        """ Get the translation file for the provided iso code.
        
        @param isoCode:
            A legal 2 char language code as spesified by the
            ISO 638-1 standard. If it is empty the code for the default
            language will be used (normally 'en').
        
        @return:
            The full path to the associated .qm translation file.
        """
        if isoCode == '' or isoCode == None:
            isoCode = u'en'

        return QString(':/i18n/%s' % isoCode)
