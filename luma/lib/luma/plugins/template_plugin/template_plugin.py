###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *

from plugins.template_plugin.TemplateForm import TemplateForm

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
            print "Debug: Icon konnte nicht geöffnet werden"

        return iconPixmap


    def set_widget(self, parent):
        self.pluginWidget = TemplateForm()
        return self.pluginWidget
