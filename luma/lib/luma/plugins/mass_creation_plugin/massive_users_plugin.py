###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *

from plugins.mass_creation_plugin.MassCreation import MassCreation

class TaskPlugin(object):

    def __init__(self):
        self.pluginName = "Massive user creation"
        self.pluginPath = ""
        self.pluginWidget = None
        print "Trying to initialize plugin \"" + self.pluginName + "\""

    def postprocess (self):
        print "Plugin \"" + self.pluginName + "\" will be shut down"

    def get_icon(self):
        try:
            iconPixmap = QPixmap(self.pluginPath + "/icons/massive_users.png")
        except:
            print "Icon konnte nicht geöffnet werden"

        return iconPixmap


    def set_widget(self, parent):
        self.pluginWidget = MassCreation(parent)
        return self.pluginWidget

