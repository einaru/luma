#! /usr/bin/env python

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <wido.depping@tu-clausthal.de>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


import sys
from qt import *

from base.gui.MainWin import MainWin

def run_it():
    app = QApplication(sys.argv)
    gui = MainWin(None)
    QObject.connect(app, SIGNAL('lastWindowClosed()'), gui.quit_application)
    
    
    app.setMainWidget(gui)
    gui.show()
    app.exec_loop()

if __name__ == '__main__':
    run_it()

