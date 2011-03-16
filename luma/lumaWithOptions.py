# -*- coding: utf-8 -*-
#
# lumaWithOptions
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

import logging
import traceback
import StringIO
import sys

import optparse

from PyQt4.QtCore import QEvent, Qt
from PyQt4.QtGui import QApplication

import __init__ as appinfo
from base.gui import SplashScreen
from base.gui.MainWin import MainWindow
from base.backend import LumaLogHandler

class Luma(QApplication):
    """
    Possibly to be used later.
    """
    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self.progressBar = None
        
    def setProgressBar(self, bar):
        self.progressBar = bar
        
    def event(self, event):
        if event.type() == QEvent.User:
            event.accept()
            self.setBusy(True)
            return True
        else:
            return QApplication.event(self, event)
    
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


def startApplication(argv, verbose=False, clear=[], dirs={}):
    """
    Preparing Luma for take-off
    
    @param verbose: boolean value; Whether or not to print more than 
                    error messages to console.
    @param clear: a list; containing what should be cleared before start.
    @param dirs: a dict; containing possible dirs to consider on start-up.
    
    """
    app = Luma(argv)
        
    app.setOrganizationName(appinfo.ORGNAME)
    app.setApplicationName(appinfo.APPNAME)
    app.setApplicationVersion(appinfo.VERSION)
    
    # Setup the logging mechanism
    l = logging.getLogger()
    l.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(threadName)s] - %(name)s - %(levelname)s - %(message)s"
    )
    
    if verbose:
        """
        If verbose mode is enabled we start logging to the console
        TODO: Add support for adjusting the level of verbosity ?
        """
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)
        l.addHandler(consoleHandler)
    
    splash = SplashScreen()
    splash.show()
    
    # Initialize the Main Window
    mainwin = MainWindow()
    app.setProgressBar(mainwin.getProgressBar())
    
    #Remove logging to console and instead log to the LoggerWidget
    #l.removeHandler(consoleHandler)
    llh = LumaLogHandler(mainwin.loggerWidget)
    l.addHandler(llh)
    
    app.lastWindowClosed.connect(mainwin.close)

    mainwin.loadPlugins()
    mainwin.show()

    splash.finish(mainwin)
    
    # Add a exception hook to handle all 
    # wexceptions missed in the main application
    sys.excepthook = unhandledException

    sys.exit(app.exec_())
    print 'items to be cleared:'
    for item in clear:
        print item
    print 'Startup directories:'
    for k, v in dirs.iteritems():
        print k, v

def main(argv):
    """
    The startup main method.
    We setup the config parser and parse the commandline options and 
    arguments.
    """
    usage = u'%prog [options] [args]'
    p = optparse.OptionParser(usage=usage)
    p.add_option(
        '-v', '--verbose',
        dest='verbose',
        action='store_true',
        help='Print more than error messages to console'
    )
    p.add_option(
        '--clear-config',
        dest='clear_config',
        action='store_true',
        help='Clear the config file before launching Luma'
    )
    p.add_option(
        '--clear-serverlist',
        dest='clear_serverlist',
        action='store_true',
        help='Clear the serverlist before launching Luma'
    )
    p.add_option(
        '--clear-templatefile',
        dest='clear_templatefile',
        action='store_true',
        help='Clear the templates file before launching Luma'
    )
    p.add_option(
        '--clear-all',
        dest='clear_all',
        action='store_true',
        help='Clear everything before launching Luma. \n ' +
        'This will result in the same as providing all the before ' +
        'mentioned clear options'
    )
    p.add_option(
        '--config-dir',
        dest='config_dir',
        action='store',
        type='string',
        metavar='DIR',
        help='Run luma with another configuration directory.'
    )
    p.add_option(
        '--plugin-dir',
        dest='plugin_dir',
        action='store',
        type='string',
        metavar='DIR',
        help='Define another directory to look for plugins.'
    )

    (opt, _) = p.parse_args()
    
    clear = []
    dirs = {}
    
    if opt.config_dir:
        dirs['config'] = opt.config_dir
    if opt.plugin_dir:
        dirs['plugin'] = opt.plugin_dir
    if opt.clear_all:
        clear.append('all')
    else:
        if opt.clear_config:
            clear.append('config')
        if opt.clear_serverlist:
            clear.append('serverlist')
        if opt.clear_templatefile:
            clear.append('templatefile')

    startApplication(argv, opt.verbose, clear, dirs)


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


if __name__ == '__main__':
    main(sys.argv)
