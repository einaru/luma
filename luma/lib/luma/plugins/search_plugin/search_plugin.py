###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *

from plugins.search_plugin.SearchView import SearchView

class TaskPlugin(object):

    def __init__(self):
        self.pluginName = "Search Plugin"
        self.pluginPath = ""
        self.pluginWidget = None

###############################################################################

    def postprocess (self):
        pass

###############################################################################

    def get_icon(self):
        try:
            iconPixmap = QPixmap(self.pluginPath + "/icons/plugin.png")
        except:
            print "Debug: Icon konnte nicht geöffnet werden"

        return iconPixmap

###############################################################################


    def set_widget(self, parent):
        self.pluginWidget = SearchView()
        return self.pluginWidget
