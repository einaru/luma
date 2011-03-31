# -*- coding: utf-8 -*-

"""
This object is for keeping information about a Plugin.
"""

class PluginObject(object):
	
	def __init__(self):

		self.lumaPlugin = True
		self.pluginName = None
		self.author = None
		self.pluginUserString = None
		self.version = None
		self.getIcon = None
		self.getPluginWidget = None
		self.getPluginSettingsWidget = None
		self.icon = None
		self.load = False