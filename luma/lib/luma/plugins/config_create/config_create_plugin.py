###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *

from plugins.config_create.ConfigPanel import ConfigPanel

class TaskPlugin(object):

	def __init__(self):
		self.pluginName = "Create Config File"
		self.pluginPath = ""
		self.pluginWidget = None
		print "Trying to initialize plugin \"" + self.pluginName + "\""

	def postprocess (self):
		print "Plugin \"" + self.pluginName + "\" will be shut down"

	def get_icon(self):
		try:
			iconPixmap = QPixmap(self.pluginPath + "/icons/config.png")
		except:
			print "Icon konnte nicht geöffnet werden"

		return iconPixmap


	def set_widget(self, parent):
		self.pluginWidget = ConfigPanel(parent)
		return self.pluginWidget

