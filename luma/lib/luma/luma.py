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
from qt import *

import environment
from base.gui.MainWin import MainWin
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

if __name__ == '__main__':
    startApplication()

