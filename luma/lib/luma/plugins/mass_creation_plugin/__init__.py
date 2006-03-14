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

lumaPlugin = True
pluginName = "massiveusercreation"
pluginUserString = qApp.trUtf8("Massive user creation")
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
    from plugins.mass_creation_plugin.MassCreation import MassCreation
    pluginWidget = MassCreation(parent)
    
    return pluginWidget
    
###############################################################################

def getPluginSettingsWidget(parent):
    return None
    
###############################################################################

def postprocess():
    return

###############################################################################    

def preProcess(serverMeta, objectValues):
    pass
    
###############################################################################

def postProcess(serverMeta, objectValues):
    pass
  
