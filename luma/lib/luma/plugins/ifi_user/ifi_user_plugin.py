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

from plugins.ifi_user.IfiUser import IfiUser

class TaskPlugin(object):

    def __init__(self):
        self.pluginName = "Ifi user creation"
        self.pluginPath = ""
        self.pluginIconPath = ""
        self.pluginWidget = None

###############################################################################

    def postprocess (self):
        pass
        
###############################################################################

    def getIcon(self):
        try:
            iconPixmap = QPixmap (os.path.join(self.pluginIconPath, "ifi_user.png"))
        except:
            print "Debug: Icon konnte nicht geöffnet werden"

        return iconPixmap

###############################################################################

    def getPluginWidget(self, parent):
        self.pluginWidget = IfiUser(parent)
        return self.pluginWidget

###############################################################################

    def getPluginSettingsWidget(self, parent):
        return
        

