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

from plugins.mass_creation_plugin.MassCreation import MassCreation
import environment

class TaskPlugin(object):

    def __init__(self):
        self.pluginName = "Massive user creation"
        self.pluginPath = ""
        self.pluginIconPath = ""
        self.pluginWidget = None

###############################################################################

    def postprocess (self):
        pass

###############################################################################

    def getIcon(self):
        iconPixmap = None
        try:
            iconPixmap = QPixmap (os.path.join (self.pluginIconPath, "massive_users.png"))
        except:
            print "Debug: Icon konnte nicht geöffnet werden"

        return iconPixmap

###############################################################################

    def getPluginWidget(self, parent):
        self.pluginWidget = MassCreation(parent)
        return self.pluginWidget

###############################################################################

    def getPluginSettingsWidget(self, parent):
        return
        

