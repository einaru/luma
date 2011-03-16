# -*- coding: utf-8 -*-

###########################################################################
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4.QtGui import *
import os.path

lumaPlugin = True
pluginName = "template"
pluginUserString = "Templates"
version = "0.1"
author = "MEG!"

def getIcon(iconPath):
    try:
        iconPixmap = QIcon (os.path.join (iconPath, "plugin.png"))
    except:
        print "Debug: Icon for plugin " + pluginName + " could not be opened."
        return None

    return iconPixmap
    
###############################################################################

def getPluginWidget(parent):
    from .TemplateWidget import TemplateWidget
    pluginWidget = TemplateWidget()
    return pluginWidget
    
###############################################################################

def getPluginSettingsWidget(parent):
    return None
    
###############################################################################

def postprocess():
    return
