#! /usr/bin/env python
# -*- coding: <utf-8> -*-

###########################################################################
#    Copyright (C) 2003, 2004 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


import sys
from qt import *

import environment
from base.gui.MainWin import MainWin


def run_it():
    app = QApplication(sys.argv)
    gui = MainWin(None)
    QObject.connect(app, SIGNAL('lastWindowClosed()'), gui.quitApplication)
    
    
    app.setMainWidget(gui)
    gui.loadPlugins()
    gui.show()
    app.exec_loop()

if __name__ == '__main__':
    run_it()

