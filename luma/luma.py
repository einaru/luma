#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# Copyright (c) 2003, 2004, 2005 
#     Wido Depping, <widod@users.sourceforge.net>
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

import logging
import os
import platform
import traceback
import StringIO
import sys

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QEvent

import __init__ as appinfo
from base.gui import SplashScreen
from base.gui.MainWin import MainWindow
from base.backend import LumaLogHandler

#Resource file
import resources

class LumaApp(QtGui.QApplication):
    """
    Possibly to be used later.
    """
    def __init__(self, argv):
        QtGui.QApplication.__init__(self, argv)
        self.progressBar = None
        
    def setProgressBar(self, bar):
        self.progressBar = bar
        
    def event(self, event):
        if event.type() == QEvent.User:
            event.accept()
            self.setBusy(True)
            return True
        else:
            return QtGui.QApplication.event(self, event)
    
    def setBusy(self, status):
        print "setBusy()"
        if status:
            self.setOverrideCursor(Qt.WaitCursor)
            if self.progressBar != None:
                self.progressBar.setRange(0,0)
        else:
            self.restoreOverrideCursor()
            if self.progressBar != None:
                self.progressBar.setRange(0,100)

def startApplication(argv):
    """
    First we must determine what platform we're running on. Making sure we 
    follow the platform convention for configuration files and directories, 
    """
    #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("cleanlooks"))
    #QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())

    app = LumaApp(argv)
        
    app.setOrganizationName(appinfo.ORGNAME)
    app.setApplicationName(appinfo.APPNAME)
    app.setApplicationVersion(appinfo.VERSION)
    
    """ Setup the logging mechanism """
    l = logging.getLogger()
    l.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(threadName)s] - %(name)s - %(levelname)s - %(message)s")

    """ Log to console until LoggerWidget is up """
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)

    l.addHandler(consoleHandler)
        
    splash = SplashScreen()
    splash.show()

    """ Find and set some resource paths """
    #paths = Paths()
    #paths.i18nPath = os.path.join(os.getcwd(), 'i18n')
    
    mainWin = MainWindow()
    
    """ Remove logging to console and instead log to the LoggerWidget """
    #l.removeHandler(consoleHandler)
    llh = LumaLogHandler(mainWin.loggerWidget)
    l.addHandler(llh)
    
    app.lastWindowClosed.connect(mainWin.close)

    #mainWin.loadPlugins()
    mainWin.show()

    splash.finish(mainWin)

    """ Add a exception hook to handle all exceptions missed in the main
    application """
    sys.excepthook = unhandledException

    sys.exit(app.exec_())

@DeprecationWarning
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
    __platform = platform.system()
    if __platform == "Linux":
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
    elif __platform == "Darwin":
        """
        Best practise config storage on Mac OS:
        http://developer.apple.com/tools/installerpolicy.html
        ~/Library/Application Support/luma
        """
        configPrefix = os.path.join(os.environ['HOME'], 'Library', 'Application Support', 'luma')
    elif __platform == "Windows":
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
            logger = logging.getLogger(__name__)
            logger.debug("TODO: os.mkdir(%s)" % (configPrefix))
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
    tmp = StringIO.StringIO()
    traceback.print_tb(eTraceback, None, tmp)
    e = """[Unhandled (handled) Exception]
This is most likely a bug. In order to fix this, please send an email to
    <luma-users@lists.sourceforge.net>
with the following text and a short description of what you were doing:
>>>\n[%s] Reason:\n%s\n%s\n<<<""" % (tmp.getvalue(), str(eType), str(eValue))
    logger = logging.getLogger("base")
    logger.error(e)

if __name__ == "__main__":
    startApplication(sys.argv)
