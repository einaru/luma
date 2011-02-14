#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# Copyright (c) 2003, 2004, 2005 
#      Wido Depping, <widod@users.sourceforge.net>
#
# Luma is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public Licence as published by 
# the Free Software Foundation; either version 2 of the Licence, or 
# (at your option) any later version.
#
# Luma is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence 
# for more details.
#
# You should have received a copy of the GNU General Public Licence along 
# with Luma; if not, write to the Free Software Foundation, Inc., 
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

"""
Luma cross-platform startup script
"""

import os
import platform
import sys
import logging

from PyQt4 import QtGui, QtCore

from base.backend.Config import Config
from base.gui.MainWin import MainWin
from splashscreen import SplashScreen

# TODO Luma spesific import (eventualy) goes here

def startApplication(argv):
    """
    First we must determine what platform we're running on. Making sure we 
    follow the platform convention for configuration files and directories, 
    """
    
    app = QtGui.QApplication(argv)
    
    splash = SplashScreen()
    splash.show()
#    import time
#    time.sleep(1)
    
    # DEVELOPMENT SPECIFICS
    
    configPrefix = getConfigPrefix()

    print "DEBUG::config folder=%s" % configPrefix
    # TODO Write the rest of the startup script.
    
    config = Config(configPrefix, os.path.join(os.getcwd(), 'i18n'))
    print config.languageHandler
    
    #Logging to console
    l = logging.getLogger("base")
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())
    
    mainWin = MainWin(config)
    
    QtCore.QObject.connect(app, QtCore.SIGNAL('lastWindowClosed()'), mainWin.close)

    mainWin.loadPlugins()
    
    screen = QtGui.QDesktopWidget().screenGeometry()
    size =  mainWin.geometry()
    mainWin.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
    
    mainWin.show()
    
 
    splash.finish(mainWin)

    #sys.excepthook = unhandledException
    
    sys.exit(app.exec_())


def getConfigPrefix():
    """
    We must determine what platform we're running on. Making sure we follow
    the platform convention for configuration files and directories,

    The platform validation, can be done through a number of modules: 
    
        os.name           -> posix, nt
        sys.platform      -> linux2, windows, darwin
        platform.system() -> Linux, Windows, Darwin
    
    This method will check for a existing config folder based on the platform.
    If it is not found it will be created. Either way the path will be returned.
    """
    configPrefix = ""
    _platform = platform.system()
    if _platform == "Linux":
        """
        Best practise config storage on Linux:
        ~/.config/luma
        """
        try:
            from xdg import BaseDirectory
            configPrefix = os.path.join(BaseDirectory.xdg_config_home, 'luma')
        except:
            # TODO do some logging :)
            pass
        finally:
            configPrefix = os.path.join(os.environ['HOME'], '.config', 'luma')
    elif _platform == "Darwin":
        """
        Best practise config storage on Mac OS:
        http://developer.apple.com/tools/installerpolicy.html
        ~/Library/Application Support/luma
        """
        configPrefix = os.path.join(os.environ['HOME'], 'Library', 'Application Support', 'luma')
    elif _platform == "Windows":
        """
        Best practise config storage on Windows:
        C:\Users\<USERNAME>\Application Data\luma
        """
        configPrefix = os.path.join(os.environ['APPDATA'], 'luma')
    else:
        """
        Default config storage for undetermined platforms
        """
        configPrefix = os.path.join(os.environ['HOME'], '.luma')

    if not os.path.exists(configPrefix):
        try:
            #os.mkdir(configPrefix)
            print "TODO::os.mkdir(%s)" % (configPrefix)
        except (IOError, OSError):
            # TODO Do some logging. We should load the application, but 
            #      provide information to user that no settings will be 
            #      saved due to (most likely) file permission issues.
            #      Maybe prompt for a user spesific folder?
            pass

    return configPrefix


def unhandledException(eType, eValue, eTraceback):
    """
    UnhandledException handler
    """
    l = logging.getLogger("base")
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())
    # TODO Take a look at the <reporoot>/tags/Luma2.4/src/bin/luma file
    print "unhandled exception"
    print eType, eValue, eTraceback

if __name__ == "__main__":
    startApplication(sys.argv)
