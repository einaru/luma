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

from plugins.admin_utils.AdminPanel import AdminPanel

class TaskPlugin(object):

    def __init__(self):
        self.pluginName = "Admin Utilities"
        self.pluginPath = ""
        self.pluginIconPath = ""
        self.pluginWidget = None

    def postprocess (self):
        pass

    def get_icon(self):
        try:
            iconPixmap = QPixmap (os.path.join(self.pluginIconPath, "admin_utils.png"))
        except:
            print "Debug: Icon could not be opened."

        return iconPixmap


    def getPluginWidget(self, parent):
        self.pluginWidget = AdminPanel(parent)
        return self.pluginWidget

###############################################################################

    def getPluginSettingsWidget(self, parent):
        return
        
###############################################################################

    def getHelpText(self):
        return
