#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# Copyright (c) 2003, 2004, 2005 
#      Wido Depping, <widod@users.sourceforge.net>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public Licence as published by the Free Software
# Foundation; either version 2 of the Licence, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence for more 
# details.
#
# You should have received a copy of the GNU General Public Licence along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA  02110-1301, USA
      
"""
Luma cross-platform startup script
"""

import os, platform, sys
import traceback
import threading
import time
import StringIO
from PyQt4 import QtGui, QtCore

# TODO Luma spesific import (eventualy) goes here

def start_application():
    """
    First we must determine what platform we're running on. Making sure we 
    follow the platform convention for configuration files and directories, 
    """
    config_prefix = get_config_prefix()
    print config_prefix
    # TODO Write the rest of the startup script.
    
    
    # And now for something completly different...
    import logging
    from base.backend.ServerList import ServerList
    from base.gui.ServerDialog import ServerDialog
    l = logging.getLogger("base")
    l.setLevel(logging.INFO)
    l.addHandler(logging.StreamHandler())
    app = QtGui.QApplication(sys.argv)
    
    tra = QtCore.QTranslator(app)
    tra.load("luma_no")
    app.installTranslator(tra)
    QtGui.QMessageBox.information(None,QtCore.QCoreApplication.translate("luma","Eh..."), QtCore.QCoreApplication.translate("luma","Luma isn't ready yet.\nBut here's the ServerDialog :D"))
    
    #For bilder
    import luma_rc
    
    s = ServerDialog(ServerList(".","serverlist.xml"))
    s.show()
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
        config_prefix = os.path.join(os.environ['HOME'], '.config', 'luma')
    elif _platform == "Darwin":
        """
        Best practise config storage on Mac OS:
        ~/Library/Preferences/luma
        """
        config_prefix = os.path.join(os.environ['HOME'], 'Library', 'Preferences', 'luma')
    elif _platform == "Windows":
        """
        Best practise config storage on Windows:
        C:\Users\<USERNAME>\Application Data\luma
        """
        config_prefix = os.path.join(os.environ['APPDATA'], 'luma')
    else:
        # TODO Must we decide on a default config storage for undetermined platforms ?
        pass
    
    if not os.path.exists(config_prefix):
        pass #os.mkdir(config_prefix)

    # XXX Remove test printout
    return config_prefix

    
def unhandled_exception(e_type, e_value, e_traceback):
    """
    
    """
    # TODO Take a look at the <reporoot>/tags/Luma2.4/src/bin/luma file
    pass

if __name__ == "__main__":
    start_application()
