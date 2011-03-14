# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
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

@DeprecationWarning
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
        
        @return: An existing instance if one exists, a new instance if not.
        """
        if not cls.__instance:
            cls.__instance = super(Paths, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    @property
    def i18nPath(self):
        """
        @return: The path to the translation files.
        """
        return self.__i18nPath

    @i18nPath.setter
    def i18nPath(self, path):
        """
        Sets the path to the translation files. Should be called only from
        the startup script.
        
        @param path: The path to the translation files.
        """
        self.__i18nPath = path

import os
from os import listdir
from PyQt4.QtCore import QDir
import resources

@DeprecationWarning
class LanguageHandler(object):
    """
    NOTE! use i18n.LanguageHandler instead
    
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
        """
        This constructure must be given the full path to where the 
        translation files are located.
        """
        #paths = Paths()
        self.__translationPath = QDir(':/i18n')
        # Must be put in manually because there exists no translation file
        # UPDATE: well it does now, but we'll keep it this way none the less
        self.__availableLanguages['en'] = ['English', 'English']
        #if os.path.isdir(self.__translationPath):
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
        for i18n in self.__translationPath:
            for iso, lang in self.__isolangCodes.iteritems():
                if i18n == iso:
                    self.__availableLanguages[iso] = lang
        #for file in listdir(self.__translationPath):
        #    if (file[:5] == 'luma_') and (file[-3:] == '.qm'):
        #        code = file[5:-3]
        #        for key, value in self.__isolangCodes.iteritems():
        #            if code == key:
        #                self.__availableLanguages[code] = value

    @property
    def availableLanguages(self):
        """
        @return: A dictionary containing all available application 
                 languages. The dictionary will be structured like this:
                 { ... ,
                 <iso code> : [ <native name>, <english name> ],
                 ... }
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
        """
        Returns the associated translation file for the provided iso code
        
        @param isoCode: A legal 2 char language code as spesified by the
                        ISO 638-1 standard. If it is empty the code for
                        the default language will be used (en).
        @return: The full path to the associated .qm translation file
        """
        if isoCode == '' or isoCode == None:
            isoCode = u'en'
        return os.path.join(self.translationPath, u'luma_%s.qm' % isoCode)
import re
import base64

def lumaStringEncode(tmpString):
    tmpString = tmpString.replace("\\", "\\\\")
    tmpString = tmpString.replace(",", r"\\\1")
        
    return tmpString


def lumaStringDecode(tmpString):
    tmpString = unicode(tmpString)
    tmpString = tmpString.replace(r"\\\1", ",")
    tmpString = tmpString.replace("\\\\", "\\")
        
    return tmpString


def isBinaryAttribute(tmpString):
    if tmpString == None:
        return False
        
    BINARY_PATTERN = '(^(\000|\n|\r| |:|<)|[\000\n\r\200-\377]+|[ ]+$)'
    binaryPattern = re.compile(BINARY_PATTERN)
    
    if binaryPattern.search(tmpString) == None:
        return False
    else:
        return True


def encodeBase64(tmpString):
    return base64.encodestring(tmpString)


def stripSpecialChars(tmpString):
    tmpString = tmpString.replace(r'\5C', '\\')
    tmpString = tmpString.replace(r'\2C', ',')
    tmpString = tmpString.replace(r'\3D', '=')
    tmpString = tmpString.replace(r'\2B', '+')
    # tmpString = tmpString.replace(r'\"', '"')
    tmpString = tmpString.replace(r'\22', '"')
    tmpString = tmpString.replace(r'\3C', '<')
    tmpString = tmpString.replace(r'\3E', '>')
    tmpString = tmpString.replace(r'\3B', ';')
        
    return tmpString

  
def escapeSpecialChars(tmpString):
    tmpList = tmpString.split('=')
    
    if 2 == len(tmpList):
        attribute = tmpList[0]
        value = "=".join(tmpList[1:])
        value = value.replace('\\', r'\5C')
        value = value.replace(',', r'\2C')
        value = value.replace('=', r'\3D')
        value = value.replace('+', r'\2B')
        # value = value.replace('"', r'\"')
        value = value.replace('"', r'\22')
        value = value.replace('<', r'\3C')
        value = value.replace('>', r'\3E')
        value = value.replace(';', r'\3B')
        
        tmpString = attribute + '=' + value
        
    return tmpString


def testEscaping():
    assert r"cn=foo" == escapeSpecialChars("cn=foo")
    assert r"cn=foo\2C" == escapeSpecialChars("cn=foo,")
    assert r"cn=foo\5C" == escapeSpecialChars("cn=foo\\")
    assert r"cn=foo\5C\2C" == escapeSpecialChars("cn=foo\\,")
    assert r"cn=\22foo\22" == escapeSpecialChars("cn=\"foo\"")
    
    assert "cn=foo" == stripSpecialChars(r"cn=foo")
    assert "cn=foo," == stripSpecialChars(r"cn=foo\2C")
    assert "cn=foo\\" == stripSpecialChars(r"cn=foo\5C")
    assert "cn=foo\\," == stripSpecialChars(r"cn=foo\5C\2C")
    assert "cn=\"foo\"" == stripSpecialChars(r"cn=\22foo\22")


def explodeDN(tmpString):
    """ Function for spliting the dn into it's parts.
    """
        
    tmpList = tmpString.split(',')
        
    tokenList = []
    for x in xrange(0, len(tmpList)):
        value = tmpList[x]
        if "=" in value:
            tokenList.append(value)
        else:
            if len(tokenList) > 0:
                tokenList[-1] = tokenList[-1] + ',' + value
    
    return tokenList

def getSortedDnList(tmpList):
    """ Returns a sorted list for distinguished names.
    
    The higher the object in the tree, the more it will be at the beginning 
    of the sorted list. Leaves should be at the end of the list.
    """
    
    tmpList.sort(__dnCompare)
    
    return tmpList

def __dnCompare(firstDN, secondDN):
    firstList = explodeDN(firstDN)
    secondList = explodeDN(secondDN)
    
    return cmp(len(firstList), len(secondList))

if __name__ == "__main__":
    testEscaping()