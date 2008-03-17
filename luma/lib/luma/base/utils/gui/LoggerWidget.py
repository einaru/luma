# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4 import QtCore
from PyQt4.QtGui import *
from ConfigParser import *
import os.path

from base.utils.gui.LoggerWidgetDesign import Ui_LoggerWidgetDesign
from base.utils.backend.LogObject import LogObject
import environment


class LoggerWidget(QWidget, Ui_LoggerWidgetDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent)

        self.setupUi(self)
        
        self.parent = parent
        self.configFile = os.path.join(environment.userHomeDir, ".luma", "luma")
        self.readSettings()
        
        self.logObjectList = []

        self.connect(self.errorBox, QtCore.SIGNAL("stateChanged(int)"), self.displayMessages)
        self.connect(self.debugBox, QtCore.SIGNAL("stateChanged(int)"), self.displayMessages)
        self.connect(self.infoBox, QtCore.SIGNAL("stateChanged(int)"), self.displayMessages)
        

###############################################################################

    def displayMessages(self):
        self.messageEdit.clear()
        
        for x in self.logObjectList:
            self.appendMessage(x)
            
        self.saveSettings()
            
###############################################################################

    def appendMessage(self, messageObject):
        if (messageObject.getLogType() == "Debug") \
                and self.debugBox.checkState() == QtCore.Qt.Checked:
            self.messageEdit.append(messageObject.getLogMessage())
            self.messageEdit.append("\n")
            return
            
        if (messageObject.getLogType() == "Error") \
                and self.errorBox.checkState() == QtCore.Qt.Checked:
            self.messageEdit.append(messageObject.getLogMessage())
            self.messageEdit.append("\n")
            return
            
        if (messageObject.getLogType() == "Info") \
                and self.infoBox.checkState() == QtCore.Qt.Checked:
            self.messageEdit.append(messageObject.getLogMessage())
            self.messageEdit.append("\n")
            return
            
###############################################################################

    def newMessage(self, messageObject):
        self.logObjectList.append(messageObject)
        if len(self.logObjectList) > 100:
                del self.logObjectList[0]
                
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
            
        configParser.set("Logger", "Show_Error", str(self.errorBox.checkState() == QtCore.Qt.Checked))
        configParser.set("Logger", "Show_Debug", str(self.debugBox.checkState() == QtCore.Qt.Checked))
        configParser.set("Logger", "Show_Info", str(self.infoBox.checkState() == QtCore.Qt.Checked))
        
        try:
            configParser.write(open(self.configFile, 'w'))
        except Exception, errorData:
            tmpString = "Could not save logger settings file. Reason:\n"
            tmpString += str(errorData)
            environment.logMessage(LogObject("Error", tmpString))
            
###############################################################################

    def _getConfigCheckstate(self, configParser, section, option):
        if configParser.has_option(section, option):
            if configParser.getboolean(section, option):
                return QtCore.Qt.Checked
            else:
                return QtCore.Qt.Unchecked

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
         
        self.errorBox.setCheckState(
                self._getConfigCheckstate(configParser, 'Logger', 'Show_Error'))
        self.debugBox.setCheckState(
                self._getConfigCheckstate(configParser, 'Logger', 'Show_Debug'))
        self.infoBox.setCheckState(
                self._getConfigCheckstate(configParser, 'Logger', 'Show_Info'))
