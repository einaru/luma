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

from plugins.search_plugin.SearchView import SearchView

class TaskPlugin(object):

    def __init__(self):
        self.pluginName = "Search Plugin"
        self.pluginPath = ""
        self.pluginIconPath = ""
        self.pluginWidget = None

###############################################################################

    def postprocess (self):
        pass

###############################################################################

    def get_icon(self):
        try:
            iconPixmap = QPixmap(os.path.join (self.pluginIconPath, "plugin.png"))
        except:
            print "Debug: Icon konnte nicht geöffnet werden"

        return iconPixmap

###############################################################################


    def getPluginWidget(self, parent):
        self.pluginWidget = SearchView()
        return self.pluginWidget

###############################################################################

    def getPluginSettingsWidget(self, parent):
        return
        
###############################################################################

    def getHelpText(self):
        return
