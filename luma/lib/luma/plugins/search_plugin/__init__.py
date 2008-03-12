# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2005 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4.QtGui import *
import os.path

lumaPlugin = True
pluginName = "search"
pluginUserString = "Search"
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
    from plugins.search_plugin.SearchView import SearchView
    pluginWidget = SearchView(parent)
    
    return pluginWidget
    
###############################################################################

def getPluginSettingsWidget(parent):
    return None
    
###############################################################################

def postprocess():
    return
 
