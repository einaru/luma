# -*- coding: utf-8 -*-

###########################################################################
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4.QtGui import *
from base.util.IconTheme import iconFromTheme
import os.path

lumaPlugin = True
pluginName = "template"
pluginUserString = "Templates"
version = "0.1"
author = "MEG!"

def getIcon():
    return iconFromTheme('luma-template-plugin', ':/icons/plugins/template')
    
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

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
