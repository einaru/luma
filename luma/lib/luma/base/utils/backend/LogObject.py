# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import time

class LogObject(object):
    
    logTypesDict = {"Error": None, "Debug": None, "Info": None}
        
    def __init__(self, logType, logMessage):
        self.logType = "Error"
        self.message = u""
        
        self.setLogType(logType)
        self.setLogMessage(logMessage)
        
###############################################################################
        
    def setLogType(self, logType):
        if self.logTypesDict.has_key(logType):
            self.logType = logType
        else:
            self.logType = "Error"
            
###############################################################################

    def getLogType(self):
        return self.logType
        
###############################################################################

    def setLogMessage(self, logMessage):
        try:
            unicode(logMessage)
            tmpTime = time.localtime()
            timeString = time.strftime("%H:%M:%S   ", tmpTime)
            self.message = timeString + logMessage
        except Exception, e:
            self.message = u""
            
###############################################################################

    def getLogMessage(self):
        return self.message
