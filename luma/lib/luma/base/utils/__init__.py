from qt import *
import re
import base64

def lumaStringEncode(tmpString):
    #tmpString = unicode(tmpString).encode('utf-8')
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
        return 0
    else:
        return 1
        
###############################################################################

def encodeBase64(tmpString):
    return base64.encodestring(tmpString)
    
