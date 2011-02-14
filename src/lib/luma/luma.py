#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# Copyright (c) 2003, 2004, 2005 
#      Wido Depping, <widod@users.sourceforge.net>
#
# Luma is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public Licence as published by the Free Software
# Foundation; either version 2 of the Licence, or (at your option) any later
# version.
#
# Luma is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence for more 
# details.
#
# You should have received a copy of the GNU General Public Licence along with
# Luma; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA  02110-1301, USA

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
from base.utils.gui.LoggerWidget import LoggerWidget
from base.utils.backend.LumaLogHandler import LumaLogHandler
from splashscreen import SplashScreen

# TODO Luma spesific import (eventualy) goes here

def startApplication():
    """
    First we must determine what platform we're running on. Making sure we 
    follow the platform convention for configuration files and directories, 
    """
    
    app = QtGui.QApplication(sys.argv)
    
    splash = SplashScreen()
    splash.show()
    import time
    #time.sleep(1)
    
    # DEVELOPMENT SPECIFICS
    
    configPrefix = getConfigPrefix()

    print "DEBUG::config folder=%s" % configPrefix
    # TODO Write the rest of the startup script.
    
    config = Config(configPrefix, os.path.join(os.getcwd(), 'i18n'))
    print config.languageHandler
    
    
    mainWin = MainWin(config)
    
    l = logging.getLogger("base")
    #l.setLevel(logging.DEBUG)  
    
    # Log to the loggerwidget
    l.addHandler(LumaLogHandler(mainWin.loggerWidget))
    
    
    #app.setOrganizationName("Luma")
    #app.setApplicationName("Luma")
    #s = QtCore.QSettings()
    #s.setValue("rofl","rofl-settings :O")
    #print s.value("rofl",":(").toString()    
    
    QtCore.QObject.connect(app, QtCore.SIGNAL('lastWindowClosed()'), mainWin.close)

    mainWin.loadPlugins()
    
    screen = QtGui.QDesktopWidget().screenGeometry()
    size =  mainWin.geometry()
    mainWin.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
    
    mainWin.show()
 
    splash.finish(mainWin)

    sys.excepthook = unhandledException
    
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
    config_prefix = ""
    _platform = platform.system()
    if _platform == "Linux":
        """
        Best practise config storage on Linux:
        ~/.config/luma
        """
        try:
            from xdg import BaseDirectory
            config_prefix = BaseDirectory.xdg_config_home
        except:
            # TODO do some logging :)
            pass
        finally:
            config_prefix = os.path.join(os.environ['HOME'], '.config', 'luma')
    elif _platform == "Darwin":
        """
        Best practise config storage on Mac OS:
        http://developer.apple.com/tools/installerpolicy.html
        ~/Library/Application Support/luma
        """
        config_prefix = os.path.join(os.environ['HOME'], 'Library', 'Application Support', 'luma')
    elif _platform == "Windows":
        """
        Best practise config storage on Windows:
        C:\Users\<USERNAME>\Application Data\luma
        """
        config_prefix = os.path.join(os.environ['APPDATA'], 'luma')
    else:
        """
        Default config storage for undetermined platforms
        """
        config_prefix = os.path.join(os.environ['HOME'], '.luma')

    if not os.path.exists(config_prefix):
        pass #os.mkdir(config_prefix)

    return config_prefix


def unhandledException(eType, eValue, eTraceback):
    """
    UnhandledException handler
    """
    # TODO Take a look at the <reporoot>/tags/Luma2.4/src/bin/luma file
    print "unhandled exception"
    print eType, eValue, eTraceback

if __name__ == "__main__":
    startApplication()
