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

from plugins.addressbook.AddressbookView import AddressbookView
from plugins.addressbook.AddressbookSettings import AddressbookSettings

class TaskPlugin(object):

    def __init__(self):
        self.pluginName = "Addressbook"
        self.pluginPath = ""
        self.pluginWidget = None

###############################################################################
        
    def postprocess (self):
        pass

###############################################################################
        
    def get_icon(self):
        try:
            iconPixmap = QPixmap (os.path.join(self.pluginPath, "icons", "addressbook.png"))
        except:
            print "Debug: Icon konnte nicht geöffnet werden"

        return iconPixmap

###############################################################################

    def getPluginWidget(self, parent):
        self.pluginWidget = AddressbookView(parent)
        return self.pluginWidget

###############################################################################

    def getPluginSettingsWidget(self, parent):
        self.pluginSettingsWidget = AddressbookSettings(parent)
        return self.pluginSettingsWidget
        
###############################################################################

    def getHelpText(self):
        return
