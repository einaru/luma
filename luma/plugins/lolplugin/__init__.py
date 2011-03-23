# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2005 by Vegar Westerlund
#    <vegarwe@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4.QtGui import *
import os.path

lumaPlugin = True
pluginName = "lol"
pluginUserString = "Lol"
version = ""
author = ""

def getIcon():
    return None
    try:
        iconPixmap = QIcon (os.path.join (iconPath, "plugin.png"))
    except:
        print "Debug: Icon for plugin " + pluginName + " could not be opened."
        return None

    return iconPixmap
    
###############################################################################

def getPluginWidget(parent, mainwin):
    return QLabel("loool",parent)

    
###############################################################################

def getPluginSettingsWidget(parent):
    return None
    
###############################################################################

def postprocess():
    return
