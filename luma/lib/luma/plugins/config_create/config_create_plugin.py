# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path

from plugins.config_create.ConfigPanel import ConfigPanel

class TaskPlugin(object):

    def __init__(self):
        self.pluginName = "Create Config File"
        self.pluginPath = ""
        self.pluginIconPath = ""
        self.pluginWidget = None

    def postprocess (self):
        pass

    def get_icon(self):
        try:
            iconPixmap = QPixmap (os.path.join (self.pluginIconPath, "config.png"))
        except:
            print "Debug: Icon konnte nicht geöffnet werden"

        return iconPixmap


    def getPluginWidget(self, parent):
        self.pluginWidget = ConfigPanel(parent)
        return self.pluginWidget

###############################################################################

    def getPluginSettingsWidget(self, parent):
        return
        
###############################################################################

    def getHelpText(self):
        return

        
