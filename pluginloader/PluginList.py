# -*- coding: utf-8 -*-

from os import listdir #to "walk" around in the filesystem
import imp #to import modules (i.e .py files)
from os import path

class PluginLoader(object):
	
	"""
	This is the new version of PluginLoader.
	
	pluginsPath: the path to plugindirectory
	pluginsToLoad: a list of plugin names, or 'ALL'
	"""
	
	def __init__(self, lumaInstallationPrefix, pluginsToLoad = []):
		
		self.pluginsToLoad = pluginsToLoad
		
		self._plugins = [] #PluginObjects
		
		self._pluginsBaseDir = path.join(lumaInstallationPrefix,
			"lib", "luma", "plugins")
			
			
###############################################################################
	
	@property	
	def plugins(self):
		
		"""
		It should not be possible to set the plugin field
		from outside, so no @plugins.setter is set.
		"""
		
		return self._plugins
		
###############################################################################

	def __findPluginDirectories(self):
		
		tempList = []
		
		try:
			#look for directories
			for x in listdir(self._pluginsBaseDir):
				xPath = path.join(self._pluginsBaseDir, x)
				if path.isdir(xPath):
					tmpList.append(x)
			
			return tempList
		
		#do exception and loggin here pl0x!
		except OSError, errorData:
			pass

###############################################################################		
		
	def __readMetaInfo(self, pluginPath):
		"""
		Reads meta information for a plugin by its directory.
		If the plugin is in pluginsToLoad, the load attribute will be
		set to true.
		All of the information about a plugin, if it valid, will be put into
		a PluginObject.
		"""
		
###############################################################################

class PluginMetaError(Exception):
	"""
	When __readMetaInfo sees that a directory is not a plugin-directory,
	this exception is raised..
	"""
	pass
		

	