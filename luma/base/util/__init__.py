# -*- coding: utf-8 -*-
#
# Copyright (C) 2004
#     Wido Depping, <widod@users.sourceforge.net>
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