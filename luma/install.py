#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003-2005 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import sys
import os.path
import os
from popen2 import Popen3
import py_compile
import errno

# This is the prefix directory where luma will be installed.
prefixDir = os.path.join("usr", "local")

# Determines if python source files are only compiled and not installed
compileOnly = False


def doImportCheck():
    """ Checks for installed packages which are needed in order to run Luma.
    Gives only a warning for missing packages.
    """
    
    print "Check for preinstalled modules:\n"
    
    # Check for python-ldap
    try:
        import ldap
        vString = "2.0.1"
        print "python-ldap is installed..."
        print "\tInstalled version: " + ldap.__version__
        print "\tMinimum version: " + vString
        print ""
    except ImportError:
        print """ERROR: python-ldap not installed!!!
You can get the module here: http://python-ldap.sourceforge.net
"""

    # Check for PyQt. If successful, check for Qt, too.
    try:
        import qt
        pyqtVersionString = "3.10"
        qtVersionString = "3.2"
        print "PyQt is installed..."
        print "\tInstalled version: " + qt.PYQT_VERSION_STR
        print "\tMinimum version: " + pyqtVersionString
        print ""
        print "Qt version..."
        print "\tInstalled version: " + qt.QT_VERSION_STR
        print "\tMinimum version: " + qtVersionString
        print ""
    except ImportError:
        print """\nERROR: PyQt not installed!!!
You can get the module here: http://www.riverbankcomputing.co.uk/pyqt
"""

    # Check for the smbpasswd module. Needed for lmhash and nthash password
    # creation. No version checking needed.
    try:
        import smbpasswd
        print "smbpasswd module is installed."
    except ImportError:
        print """\nWARNING: smbpasswd module is not installed.
You will be able to tun Luma, but no nthash and lmhash passwords are available.
You can get the module here: http://barryp.org/software/py-smbpasswd
"""

    print ""

###############################################################################

def logAndStop(message):
    """Small method to print out trapped errormessages and stopping the program."""
    print message
    sys.exit(1)

###############################################################################

def doChecks():
    """Checks if prefix diretory exists. After that Luma will be compiled and installed. 
    If prefix-directory isn't found, doChecks will try to make the whole path.
    """


    if os.path.exists(prefixDir):
        doCompile()
        doInstall()
    else:
        try:
            os.makedirs(prefixDir)
        except OSError,oe:
            logAndStop("Unable to make install-prefix %s. Reason: %s" % (prefixDir,str(oe)))
        doChecks() # Nice, we call ourself if we were able to make directories

###############################################################################

def doInstall():
    """Installs compiled sourcefiles to the installation directory.
    """
    
    print "Copy program files...\n"
    
    try:
        for tmpDir in ["bin", "lib", "share"]:
            if not (os.path.exists(tmpDir)):
                try: 
                    os.makedirs(tmpDir)
                except OSError,oe:
                    logAndStop("Unable to create local directory %s. Reason: %s" % (tmpDir,str(oe)))

            a = Popen3("cp -R " + tmpDir + " " + prefixDir)
            while a.poll() == -1:
                pass
            if a.poll() > 0:
                raise "CopyError", "Error!!! Could not copy File. Maybe wrong permissions?"

            if tmpDir == "bin":
                src,dst = prefixDir + '/lib/luma/luma.py', prefixDir + '/bin/luma'
                pwd = os.getcwd()
                if not (os.path.exists(pwd + "/" + dst)):
                    try:
                        os.symlink(src,dst)
                    except OSError,oerr:
                        if oerr.errno == errno.EEXIST:
                            # Not to wory - seems we're trying to install a newer version
                            pass
                        elif oerr.errno == errno.EACCES:
                            raise "AccessError","Unable to make symbolic link due to access restrictions."
                
        print "Finished copying program files.\n"
        print "LUMA installed succesfully! :)"
        
    except "CopyError", errorMessage:
        logAndStop(errorMessage)
    except "AccessError", errorMessage:
        logAndStop(errorMessage)

    
###############################################################################

def checkPath():
    """ Checks if the install directory for luma is in the local PATH of the user and give him/her feedback.
    """
    
    pathVariable = os.environ['PATH']
    pathValues = pathVariable.split(':')
    tmpPath = os.path.join(prefixDir, "bin")
    
    
    if tmpPath in pathValues:
        print """
Good: The specified prefix is present in your PATH variable.
Start LUMA by typing 'luma' from anywhere in the console.
"""
    else:
        print """
WARNING: The specified prefix is NOT present in your PATH variable.
Add PREFIX to your PATH and then Start LUMA by typing 'luma' from
anywhere in the console.
"""

###############################################################################

def printHelp():
    """Prints a help text for the Luma installation program.
    """
    
    helpString = """Install options:
 --prefix=PATH \t\t Install path (default is /usr/local)
 --compile-only \t Just compile source files. No installation.
 \n"""
 
    logAndStop(helpString)
    
###############################################################################
    
def doCompile():
    """Compiles all source files to python bytecode.
    """
    global compiled

    
    if not compiled:
        print "Compiling python source files ...\n"
    
        input, output = os.popen2("find . -name \"*.py\"")
        tmpArray = output.readlines()
        fileList = []
        for x in tmpArray:
            if x[:11] == "./lib/luma/":
                fileList.append(x[:-1])
        for x in fileList:
            print "compiling " + x
            py_compile.compile(x)
        
        print "\nFinished compiling.\n"
        compiled = True

         
###############################################################################

def evalArguments():
    """ Evaluate options given to the install script by the user.
    """
    
    if len(sys.argv) == 1:
        printHelp()
        return
        
    for x in sys.argv[1:]:
        if x == "--compile-only":
            global compileOnly
            compileOnly = True
        elif x[:9] == "--prefix=":
            global prefixDir
            prefixDir = x[9:]
            if (prefixDir[-1] == "/") and (len(prefixDir) > 1):
                prefixDir = prefixDir[:-1]
        else:
            logAndStop("Unknown options. Exiting...")

###############################################################################


print "Luma 2.4 (C) 2003-2006 Wido Depping\n"

doImportCheck()
print ""

evalArguments()
    
compiled = False
doCompile()

if not compileOnly:
    doChecks()
    doInstall()
    checkPath()
