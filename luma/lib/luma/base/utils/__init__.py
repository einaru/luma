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
    BINARY_PATTERN = '(^(\000|\n|\r| |:|<)|[\000\n\r\200-\377]+|[ ]+$)'
    binaryPattern = re.compile(BINARY_PATTERN)
    
    if binaryPattern.search(tmpString) == None:
        return False
    else:
        return True
        
###############################################################################

def encodeBase64(tmpString):
    return base64.encodestring(tmpString)
    
