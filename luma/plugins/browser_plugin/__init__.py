# -*- coding: utf-8 -*-

from PyQt4.QtGui import QIcon 
import os.path

lumaPlugin = True
pluginName = "browser"
pluginUserString = "Browser"
version = "0.1"
author = "Christian Forfang, Simen Natvig, Per Ove Ringdal"

def getIcon(iconPath):
    try:
        iconPixmap = QIcon (os.path.join (iconPath, "plugin.png"))
    except:
        print "Debug: Icon for plugin " + pluginName + " could not be opened."
        return None

    return iconPixmap
    
def getPluginWidget(parent, mainwin):
    # parent is not used, but the widget is reparented by the QTabWidget
    from plugins.browser_plugin.BrowserView import BrowserView
    pluginWidget = BrowserView()
    return pluginWidget

def getPluginSettingsWidget(parent):
    return None

def postprocess():
    return
