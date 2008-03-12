# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4.QtGui import *
from ConfigParser import *
import os.path

from base.utils.gui.LoggerWidgetDesign import LoggerWidgetDesign
from base.utils.backend.LogObject import LogObject
import environment


class LoggerWidget(LoggerWidgetDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        LoggerWidgetDesign.__init__(self,parent,name,fl)
        
        self.parent = parent
        self.configFile = os.path.join(environment.userHomeDir, ".luma", "luma")
        self.readSettings()
        
        self.logObjectList = []
        
        self.connect(self.errorBox, SIGNAL("stateChanged(int)"), self.displayMessages)
        self.connect(self.debugBox, SIGNAL("stateChanged(int)"), self.displayMessages)
        self.connect(self.infoBox, SIGNAL("stateChanged(int)"), self.displayMessages)
        

###############################################################################

    def displayMessages(self):
        self.messageEdit.clear()
        
        for x in self.logObjectList:
            self.appendMessage(x)
            
        self.saveSettings()
            
###############################################################################

    def appendMessage(self, messageObject):
        if (messageObject.getLogType() == "Debug") and self.debugBox.isOn():
            self.messageEdit.append(messageObject.getLogMessage())
            self.messageEdit.append("\n")
            return
            
        if (messageObject.getLogType() == "Error") and self.errorBox.isOn():
            self.messageEdit.append(messageObject.getLogMessage())
            self.messageEdit.append("\n")
            return
            
        if (messageObject.getLogType() == "Info") and self.infoBox.isOn():
            self.messageEdit.append(messageObject.getLogMessage())
            self.messageEdit.append("\n")
            return
            
###############################################################################

    def newMessage(self, messageObject):
        self.logObjectList.append(messageObject)
        if len(self.logObjectList) > 100:
                del self.logObjectList[0]
                
        if not (self.parent.orientation() == Qt.DockMinimized):
                self.appendMessage(messageObject)
                
###############################################################################

    def clearLogger(self):
        self.logObjectList = []
        self.messageEdit.clear()
        
###############################################################################

    def saveSettings(self):
        configParser = ConfigParser()
            
        try:
            configParser.readfp(open(self.configFile, 'r'))
        except Exception, errorData:
            tmpString = "Could not read logger settings file. Reason:\n"
            tmpString += str(errorData)
            environment.logMessage(LogObject("Debug", tmpString))
            
        if not configParser.has_section("Logger"):
            configParser.add_section("Logger")
            
        configParser.set("Logger", "Show_Error", str(self.errorBox.isOn()))
        configParser.set("Logger", "Show_Debug", str(self.debugBox.isOn()))
        configParser.set("Logger", "Show_Info", str(self.infoBox.isOn()))
        
        try:
            configParser.write(open(self.configFile, 'w'))
        except Exception, errorData:
            tmpString = "Could not save logger settings file. Reason:\n"
            tmpString += str(errorData)
            environment.logMessage(LogObject("Error", tmpString))
            
###############################################################################

    def readSettings(self):
        configParser = ConfigParser()
            
        try:
            configParser.readfp(open(self.configFile, 'r'))
        except Exception, errorData:
            tmpString = "Could not read logger settings file. Reason:\n"
            tmpString += str(errorData)
            print tmpString
            #environment.logMessage(LogObject("Debug", tmpString))
            
        if not configParser.has_section("Logger"):
            return
         
        if configParser.has_option("Logger", "Show_Error"):
            tmpBool = configParser.getboolean("Logger", "Show_Error")
            self.errorBox.setChecked(tmpBool)
            
        if configParser.has_option("Logger", "Show_Debug"):
            tmpBool = configParser.getboolean("Logger", "Show_Debug")
            self.debugBox.setChecked(tmpBool)
            
        if configParser.has_option("Logger", "Show_Info"):
            tmpBool = configParser.getboolean("Logger", "Show_Info")
            self.infoBox.setChecked(tmpBool)
            
            
