###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <wido.depping@tu-clausthal.de>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from base.gui.PluginLoaderGuiDesign import PluginLoaderGuiDesign
from base.backend.DirUtils import DirUtils
from qt import *
import copy
from os.path import isdir
import os

class PluginLoaderGui(PluginLoaderGuiDesign):
    """Dialog for choosing which plugins should be loaded."""

    def __init__(self, tmpPlugins=None, parent=None):
        PluginLoaderGuiDesign.__init__(self, parent)
        self.checkerList = []
        self.PLUGINS = tmpPlugins
        for x in self.PLUGINS.keys():
            tmpObject = self.PLUGINS[x]
            tmpCheckBox = QCheckListItem(self.chooserView,
                            tmpObject["PLUGIN_NAME"],
                            QCheckListItem.CheckBox )
            self.checkerList.append(tmpCheckBox)

        dirHelper = DirUtils()
        self.userHome = dirHelper.USERDIR
        self.defaultsHome = self.userHome + "/.luma/plugin.defaults"
        try:
            fileHandler = open(self.defaultsHome, 'r')
            tmpStrings = fileHandler.readlines()
            fileHandler.close()
            for x in tmpStrings:
                tmp = str(x[:-1])
                if self.PLUGINS.has_key(tmp):
                    for y in self.checkerList:
                        if str(y.text()) == tmp:
                            y.setOn(1)
        except IOError, errorData:
            print "Could not open file for plugin defaults :("
            print "Reason: ", errorData

###############################################################################

    def saveValues(self):
        try:
            # if luma dir in home does not exist -> create 
            if not (isdir(self.userHome + "/.luma")):
                os.mkdir (self.userHome + "/.luma")
            
            fileHandler = open(self.defaultsHome, 'w')
            for x in self.checkerList:
                if x.isOn():
                    fileHandler.write(str(x.text()) + "\n")
            fileHandler.close()
        except IOError, errorData:
            print "Could not open file for plugin defaults :("
            print "Reason: ", errorData
        self.accept()

