# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *

from plugins.browser_plugin.BrowserView import BrowserView

class TaskPlugin(object):

    def __init__(self):
        self.pluginName = "Browse LDAP Tree"
        self.pluginPath = ""
        self.pluginWidget = None

    def postprocess (self):
        pass

    def get_icon(self):
        try:
            iconPixmap = QPixmap(self.pluginPath + "/icons/plugin.png")
        except:
            print "Debug: Icon could not be opened."

        return iconPixmap


    def set_widget(self, parent):
        self.pluginWidget = BrowserView()
        return self.pluginWidget
