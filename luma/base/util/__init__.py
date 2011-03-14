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