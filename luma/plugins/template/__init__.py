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
pluginName = u"template"
pluginUserString = u"Templates"
version = u"0.2"
author = u"Simen Natvig"
description = u"Used to define the templates used by the browser-plugin."

def getIcon():
    return iconFromTheme('luma-template-plugin', ':/icons/plugins/template')

def getPluginWidget(parent, mainwin):
    from .gui.TemplateWidget import TemplateWidget
    pluginWidget = TemplateWidget()
    return pluginWidget
    
def getPluginSettingsWidget(parent):
    return None
    
def postprocess():
    return

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
