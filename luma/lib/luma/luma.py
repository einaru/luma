#! /usr/bin/env python
# -*- coding: <utf-8> -*-

###########################################################################
#    Copyright (C) 2003, 2004, 2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


import sys
import traceback
import threading
import time
import StringIO
from qt import *

import environment
from base.gui.MainWin import MainWin
from base.utils.backend.LogObject import LogObject
import environment
import os

def startApplication():
    #Check if configuration directory exists. If not, create it.
    configPrefix = os.path.join(environment.userHomeDir, ".luma")
    if not os.path.exists(configPrefix):
        os.mkdir(configPrefix)
    
    app = QApplication(sys.argv)
    gui = MainWin(None)
    QObject.connect(app, SIGNAL('lastWindowClosed()'), gui.quitApplication)
    
    
    app.setMainWidget(gui)
    gui.loadPlugins()
    gui.show()
    app.exec_loop()

###############################################################################

def unhandledException(exceptionType, exceptionValue, exceptionTraceback):
    tmpString = StringIO.StringIO()
    traceback.print_tb(exceptionTraceback, None, tmpString)
    errorString = """An unhandled exception occured. This is most likely a bug 
in the programming of Luma. In order to fix this, send an email with the 
following text and a detailed description of what you were doing to
luma-users@lists.sourceforge.net.\n"""
    errorString = errorString + tmpString.getvalue()
    errorString = errorString + "Reason: " + str(exceptionValue)
    environment.logMessage(LogObject("Error", errorString))

###############################################################################
    
sys.excepthook = unhandledException

if __name__ == '__main__':
    startApplication()


