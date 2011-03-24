# -*- coding: utf-8 -*-

###########################################################################
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4.QtGui import *
from base.util.IconTheme import pixmapFromThemeIcon
import os.path

lumaPlugin = True
pluginName = "template"
pluginUserString = "Templates"
version = "0.1"
author = "MEG!"

def getIcon():
    return QIcon(pixmapFromThemeIcon("document-new", ":/icons/template_plugin-plugin"))
    
###############################################################################

def getPluginWidget(parent, mainwin):
    from .gui.TemplateWidget import TemplateWidget
    pluginWidget = TemplateWidget()
    return pluginWidget
    
###############################################################################

def getPluginSettingsWidget(parent):
    return None
    
###############################################################################

def postprocess():
    return
