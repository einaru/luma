# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import base64

from base.utils import isBinaryAttribute
import environment
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo

class LdifHelper(object):

    def __init__(self, serverName):
        self.SERVERNAME = serverName
        
        self.SCHEMAMETA = ObjectClassAttributeInfo(self.SERVERNAME)
        
###############################################################################

    def convertToLdif(self, data):
        if data == None:
            return ""
            
        tmpList = []
            
        for a in data:
            tmpDN = a[0]
            if isBinaryAttribute(a[0]):
                tmpDN = base64.encodestring(tmpDN)
                tmpList.append("dn:: " + tmpDN)
            else:
                tmpList.append("dn: " + tmpDN + "\n")
            for x in a[1].keys():
                for y in a[1][x]:
                    if isBinaryAttribute(y) or self.SCHEMAMETA.isBinary(x) :
                        tmpList.append(x + ":: " + base64.encodestring(y))
                    else:
                        tmpList.append(x + ": " + y + "\n")

            tmpList.append("\n")
        return "".join(tmpList)
