###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *

from plugins.admin_utils.AdminPanel import AdminPanel

class TaskPlugin(object):

    def __init__(self):
        self.pluginName = "Admin Utilities"
        self.pluginPath = ""
        self.pluginWidget = None
        print "Trying to initialize plugin \"" + self.pluginName + "\""

    def postprocess (self):
        print "Plugin \"" + self.pluginName + "\" will be shut down"

    def get_icon(self):
        try:
            iconPixmap = QPixmap(self.pluginPath + "/icons/admin_utils.png")
        except:
            print "Icon could not be opened."

        return iconPixmap


    def set_widget(self, parent):
        self.pluginWidget = AdminPanel(parent)
        return self.pluginWidget

