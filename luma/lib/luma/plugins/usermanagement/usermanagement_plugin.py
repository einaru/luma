# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path

from plugins.usermanagement.Usermanagement import Usermanagement

class TaskPlugin(object):

    def __init__(self):
        self.pluginName = "Usermanagement"
        self.pluginIconPath = ""
        self.pluginPath = ""
        self.pluginWidget = None

###############################################################################
        
    def postprocess (self):
        pass

###############################################################################
        
    def getIcon(self):
        try:
            iconPixmap = QPixmap (os.path.join(self.pluginIconPath, "usermanagement.png"))
        except:
            print "Debug: Icon konnte nicht geöffnet werden"

        return iconPixmap

###############################################################################

    def getPluginWidget(self, parent):
        self.pluginWidget = Usermanagement(parent)
        return self.pluginWidget

###############################################################################

    def getPluginSettingsWidget(self, parent):
        return
        
