# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import re
import base64

def lumaStringEncode(tmpString):
    tmpString = tmpString.replace("\\", "\\\\")
    tmpString = tmpString.replace(",", r"\\\1")
        
    return tmpString
        
###############################################################################

def lumaStringDecode(tmpString):
    tmpString = unicode(tmpString)
    tmpString = tmpString.replace(r"\\\1", ",")
    tmpString = tmpString.replace("\\\\", "\\")
        
    return tmpString

###############################################################################

def isBinaryAttribute(tmpString):
    if tmpString == None:
        return False
        
    BINARY_PATTERN = '(^(\000|\n|\r| |:|<)|[\000\n\r\200-\377]+|[ ]+$)'
    binaryPattern = re.compile(BINARY_PATTERN)
    
    if binaryPattern.search(tmpString) == None:
        return False
    else:
        return True
        
###############################################################################

def encodeBase64(tmpString):
    return base64.encodestring(tmpString)
    
###############################################################################

def stripSpecialChars(tmpString):
    tmpString = tmpString.replace(r'\5C', '\\')
    tmpString = tmpString.replace(r'\2C', ',')
    tmpString = tmpString.replace(r'\3D', '=')
    tmpString = tmpString.replace(r'\2B', '+')
        
    return tmpString
        
###############################################################################
    
def escapeSpecialChars(tmpString):
    tmpList = tmpString.split('=')
    
    if 2 == len(tmpList):
        attribute = tmpList[0]
        value = tmpList[1]
        value = value.replace('\\', r'\5C')
        value = value.replace(',', r'\2C')
        value = value.replace('=', r'\3D')
        value = value.replace('+', r'\2B')
        
        tmpString = attribute + '=' + value
        
    return tmpString
    
###############################################################################

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

###############################################################################

def getSortedDnList(tmpList):
    """ Returns a sorted list for distinguished names.
    
    The higher the object in the tree, the more it will be at the beginning 
    of the sorted list. Leaves should be at the end of the list.
    """
    
    tmpList.sort(__dnCompare)
    
    return tmpList
    
###############################################################################

def __dnCompare(firstDN, secondDN):
    firstList = explodeDN(firstDN)
    secondList = explodeDN(secondDN)
    
    return cmp(len(firstList), len(secondList))
