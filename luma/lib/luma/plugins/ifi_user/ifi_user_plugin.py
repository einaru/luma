###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *

from plugins.ifi_user.IfiUser import IfiUser

class TaskPlugin(object):

    def __init__(self):
        self.pluginName = "Ifi user creation"
        self.pluginPath = ""
        self.pluginWidget = None

    def postprocess (self):
        pass

    def get_icon(self):
        try:
            iconPixmap = QPixmap(self.pluginPath + "/icons/ifi_user.png")
        except:
            print "Debug: Icon konnte nicht geöffnet werden"

        return iconPixmap


    def set_widget(self, parent):
        self.pluginWidget = IfiUser(parent)
        return self.pluginWidget

