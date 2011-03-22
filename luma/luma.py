# -*- coding: utf-8 -*-
#
# lumaWithOptions
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#     Christian Forfang, <cforfang@gmail.com>
#
# Copyright (c) 2003, 2004, 2005 
#     Wido Depping, <widod@users.sourceforge.net>
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
import optparse
import os
import StringIO
import sys
import traceback

from PyQt4.QtCore import (QEvent, Qt)
from PyQt4.QtGui import QApplication

import __init__ as appinfo
from base.backend.Log import LumaLogHandler
from base.gui.MainWindow import MainWindow
from base.gui.SplashScreen import SplashScreen
from base.gui.Settings import Settings
from base.util.Paths import getConfigPrefix

import resources


class Luma(QApplication):
    """ Possibly to be used later.
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
                
class TempLogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.logList = []

    def emit(self, record):
        self.logList.append(record)


def startApplication(argv, verbose=False, clear=[], dirs={}):
    """ Preparing Luma for take-off
    
    @param verbose: boolean value;
        Whether or not to print more than error messages to console.
    @param clear: a list;
        containing what should be cleared before start.
    @param dirs: a dict;
        containing possible dirs to consider on start-up.
    """
    #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("cleanlooks"))
    #QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
    
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
    
    # Keep all logs from now until the GUI-LoggerWidget is up and can be populated
    tmpLH = TempLogHandler()
    l.addHandler(tmpLH)

    settings = Settings()
    # Because we use QSettings for the application settings we 
    # facilitate QSettings if the user wishes to start Luma fresh
    if 'config' in clear:
        clear.remove('config')
        settings.clear()
        
    if settings.configPrefix == u'':
        # This will be the case on the first run, or if the user
        # have startet the application with the --clear-config option
        # We therefore need to retrive the config prefix in a best
        # practize cross-platform way
        #
        # NOTE: The first return value is a bool that indicates wheter
        #       the configprefix exists or not. As of now the config
        #       prefix is return regardless if it is writable or not.
        (_, settings.configPrefix) = getConfigPrefix()
        
    (_, configPrefix) = getConfigPrefix()
    
    if verbose:
        """ If verbose mode is enabled we start logging to the console
        TODO: Add support for adjusting the level of verbosity ?
        """
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)
        l.addHandler(consoleHandler)
    
    __handleClearOptions(configPrefix, clear)
    
    # Initialize the splash screen
    splash = SplashScreen()
    splash.show()
    
    # Initialize the main window
    mainwin = MainWindow()
    
    llh = LumaLogHandler(mainwin.loggerWidget)
    l.addHandler(llh)
    
    # Populate the loggerWidget
    for x in tmpLH.logList:
        llh.emit(x)
    l.removeHandler(tmpLH)
    
    app.lastWindowClosed.connect(mainwin.close)

    mainwin.show()

    splash.finish(mainwin)
    
    # Add a exception hook to handle all 
    # exceptions missed in the main application
    sys.excepthook = unhandledException

    sys.exit(app.exec_())


def main(argv):
    """ Set up and parse the command line for supported application
    options and arguments.
    """
    usage = u'%prog [options] [args]'
    p = optparse.OptionParser(usage=usage)
    p.add_option(
        '-v', '--verbose',
        dest='verbose',
        action='store_true',
        help='print more error, debug and info messages to console'
    )
    p.add_option(
        '--clear-config',
        dest='clear_config',
        action='store_true',
        help='clear the config file before launching Luma'
    )
    p.add_option(
        '--clear-serverlist',
        dest='clear_serverlist',
        action='store_true',
        help='clear the serverlist before launching Luma'
    )
    p.add_option(
        '--clear-templatefile',
        dest='clear_templatefile',
        action='store_true',
        help='clear the templates file before launching Luma'
    )
    p.add_option(
        '--clear-all',
        dest='clear_all',
        action='store_true',
        help='clear everything before launching Luma. \n ' +
        'This will result in the same as providing all the before ' +
        'mentioned clear options'
    )
    # TODO: These last two options is put here as a reminder. Would have
    #       been a cool feature to be able to launch Luma with different
    #       configuration locations.
    #           The option to specify yet another plugin directory to look
    #       for plugins could also be cool. Especially if you are in the 
    #       midle of developing a new plugin, a want to do some occasionally
    #       testing.
    #
    #p.add_option(
    #    '--config-dir',
    #    dest='config_dir',
    #    action='store',
    #    type='string',
    #    metavar='DIR',
    #    help='run Luma with another configuration directory'
    #)
    #p.add_option(
    #    '--plugin-dir',
    #    dest='plugin_dir',
    #    action='store',
    #    type='string',
    #    metavar='DIR',
    #    help='define another directory to look for plugins. DIR will be ' +
    #    'appended to the list of default plugins directories'
    #)

    (opt, _) = p.parse_args()
    
    dirs = {}
    clear = []
    
    # TODO: If we append the filenames to the clear list, it becomes
    #       trivial to clear the specified files. The way we do it here
    #       works only if we are sure to use the same filenames
    #       through out the application. Also, because we use QSettings
    #       for the config file we need to handle this case differently.
    #if opt.config_dir:
    #    dirs['config'] = opt.config_dir
    #if opt.plugin_dir:
    #    dirs['plugins'] = opt.plugin_dir
    if opt.clear_all:
        clear.append('config')
        clear.append('serverlist.xml')
        clear.append('templates')
    else:
        if opt.clear_config:
            clear.append('config')
        if opt.clear_serverlist:
            clear.append('serverlist.xml')
        if opt.clear_templatefile:
            clear.append('templates')

    startApplication(argv, opt.verbose, clear, dirs)


def __handleClearOptions(configPrefix, clear=[]):
    """ If the application has been started with clear options, we
    handle these before setting up the application main window
    """
    for file in clear:
        path = os.path.join(configPrefix, file)
        if os.path.isfile(path):
            f = open(path, 'w')
            f.close()
        else:
            l = logging.getLogger('luma')
            l.info('%s couldn\'t be located in %s' % (file, configPrefix))
            

def unhandledException(etype, evalue, etraceback):
    """ UnhandledException handler
    """
    tmp = StringIO.StringIO()
    traceback.print_tb(etraceback, None, tmp)
    e = """[Unhandled (handled) Exception]
This is most likely a bug. In order to fix this, please send an email to
    <luma-users@lists.sourceforge.net>
with the following text and a short description of what you were doing:
>>>\n[%s] Reason:\n%s\n%s\n<<<""" % (tmp.getvalue(), str(etype), str(evalue))
    logger = logging.getLogger('luma')
    logger.error(e)
    # Make sure the cursor is normal
    QApplication.restoreOverrideCursor()



if __name__ == '__main__':
    main(sys.argv)
