# -*- coding: utf-8 -*-

"""
This object is for keeping information about a Plugin.
"""

class PluginObject(object):
	
	def __init__(self):

		self.lumaPlugin = True #what is this used for!? :P
		self.pluginName = None
		self.author = None
		self.pluginUserString = None
		self.version = None
		self.getIcon = None
		self.getPluginWidget = None
		self.getPluginSettingsWidget = None
		self.icon = None
		self.load = False
		
###############################################################################

	#if no useful stuff to do here, maybe go back to using dictionary..
	#this cant be used as a model (figured this out now..), or can it..?