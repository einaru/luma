# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2005 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path
from base.utils.backend.LogObject import LogObject
import environment

lumaPlugin = True
pluginName = "usermanagement"
pluginUserString = "Usermanagement"
version = ""
author = "Wido Depping <wido.depping@gmail.com>"

def getIcon(iconPath):
    try:
        iconPixmap = QPixmap (os.path.join (iconPath, "plugin.png"))
    except:
        print "Debug: Icon for plugin " + pluginName + " could not be opened."
        return None

    return iconPixmap
    
###############################################################################

def getPluginWidget(parent):
    from plugins.usermanagement.Usermanagement import Usermanagement
    pluginWidget = Usermanagement(parent)
    
    return pluginWidget
    
###############################################################################

def getPluginSettingsWidget(parent):
    return None
    
###############################################################################

def postprocess():
    return
    
###############################################################################

def addPreProcess(serverMeta, dn, objectValues, groupName):
    try:
        import UsermanagementExtra
        UsermanagementExtra.addPreProcess(serverMeta, dn, objectValues, groupName)
    except ImportError, e:
        tmpString = "Could not execute addPreProcess. Reason:\n"
        tmpString += str(e)
        environment.logMessage(LogObject("Debug", tmpString))
    
###############################################################################

def addPostProcess(serverMeta, dn, objectValues, groupName):
    try:
        import UsermanagementExtra
        UsermanagementExtra.addPostProcess(serverMeta, dn, objectValues, groupName)
    except ImportError, e:
        tmpString = "Could not execute addPostProcess. Reason:\n"
        tmpString += str(e)
        environment.logMessage(LogObject("Debug", tmpString))
        
###############################################################################

def deletePreProcess(serverMeta, dn):
    try:
        import UsermanagementExtra
        UsermanagementExtra.deletePreProcess(serverMeta, dn)
    except ImportError, e:
        tmpString = "Could not execute deletePreProcess. Reason:\n"
        tmpString += str(e)
        environment.logMessage(LogObject("Debug", tmpString))
    
###############################################################################

def deletePostProcess(serverMeta, dn):
    try:
        import UsermanagementExtra
        UsermanagementExtra.deletePostProcess(serverMeta, dn)
    except ImportError, e:
        tmpString = "Could not execute deletePostProcess. Reason:\n"
        tmpString += str(e)
        environment.logMessage(LogObject("Debug", tmpString))

###############################################################################

def modifyPreProcess(serverMeta, dn, objectValues):
    try:
        import UsermanagementExtra
        UsermanagementExtra.modifyPreProcess(serverMeta, dn, objectValues)
    except ImportError, e:
        tmpString = "Could not execute modifyPreProcess. Reason:\n"
        tmpString += str(e)
        environment.logMessage(LogObject("Debug", tmpString))
    
###############################################################################

def modifyPostProcess(serverMeta, dn, objectValues):
    try:
        import UsermanagementExtra
        UsermanagementExtra.modifyPostProcess(serverMeta, dn, objectValues)
    except ImportError, e:
        tmpString = "Could not execute modifyPostProcess. Reason:\n"
        tmpString += str(e)
        environment.logMessage(LogObject("Debug", tmpString))
