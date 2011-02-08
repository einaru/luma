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

from base.gui.MainWin import MainWin

# TODO Luma spesific import (eventualy) goes here

def start_application():
    """
    First we must determine what platform we're running on. Making sure we 
    follow the platform convention for configuration files and directories, 
    """
    config_prefix = get_config_prefix()
    print "DEBUG::config folder=%s" % config_prefix
    # TODO Write the rest of the startup script.
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWin()
    
    QtCore.QObject.connect(app, QtCore.SIGNAL('lastWindowClosed()'), mainWin.close)

    mainWin.loadPlugins()
    mainWin.show()

    sys.excepthook = unhandledException
    
    sys.exit(app.exec_())


def get_config_prefix():
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
    l = logging.getLogger("base")
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())
    # TODO Take a look at the <reporoot>/tags/Luma2.4/src/bin/luma file
    print "unhandled exception"

if __name__ == "__main__":
    start_application()

