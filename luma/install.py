#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import sys
import os.path
import os
import string
from popen2 import Popen3
import py_compile

prefixDir = ""
compileOnly = False


def doImportCheck():
    print "Check for preinstalled modules:\n"
    
    try:
        import ldap
        vString = "2.0.0pre13"
        print "python-ldap is installed..."
        print "\tInstalled version: " + ldap.__version__
        print "\tMinimum version: " + vString
        print ""
    except ImportError:
        print """ERROR: python-ldap not installed!!!
You can get the module here: http://python-ldap.sourceforge.net
"""

    try:
        import qt
        vString = "3.10"
        print "PyQt is installed..."
        print "\tInstalled version: " + qt.PYQT_VERSION_STR
        print "\tMinimum version: " + vString
        print ""
    except ImportError:
        print """\nERROR: PyQt not installed!!!
You can get the module here: http://www.riverbankcomputing.co.uk/pyqt
"""

###############################################################################

def doChecks():

    # Check ob Prefix existiert
    if os.path.exists(prefixDir):
        doCompile()
        doInstall()
    else:
        print "Prefix directory does not exist!"
        sys.exit(1)

###############################################################################

def doInstall():
    print "Copy program files...\n"
    
    try:
        a = Popen3("cp -R bin " + prefixDir)
        while a.poll() == -1:
            pass
        if a.poll() > 0:
            raise "CopyError", "Error!!! Could not copy File. Maybe wrong permissions?"

        a = Popen3("cp -R lib " + prefixDir)
        while a.poll() == -1:
            pass
        if a.poll() > 0:
            raise "CopyError", "Error!!! Could not copy File. Maybe wrong permissions?"

        a = Popen3("cp -R share " + prefixDir)
        while a.poll() == -1:
            pass
        if a.poll() > 0:
            raise "CopyError", "Error!!! Could not copy File. Maybe wrong permissions?"

        print "Finished copying program files.\n"
        print "LUMA installed succesfully! :)"
        
    except "CopyError", errorMessage:
        print errorMessage
        sys.exit(1)
    
###############################################################################

def checkPath():
    pathVariable = os.environ['PATH']

    pathValues = string.split(pathVariable, ':')

    good = False
    for x in pathValues:
        if x == (prefixDir+"/bin"):
            good = True
            break

    if good:
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
    helpString = """Install options:
 --prefix=PATH \t\t Install path (e.g. /usr/local)
 --compile-only \t Just compile source files. No installation.
 \n"""
    print helpString
    sys.exit(1)
    
###############################################################################
    
def doCompile():
    print "Compiling python source files ...\n"
    
    input, output = os.popen2("find . -name \"*.py\"")
    tmpArray = output.readlines()
    fileList = []
    for x in tmpArray:
        if x[:11] == "./lib/luma/":
            fileList.append(x[:-1])
    for x in fileList:
        print "compile " + x
        py_compile.compile(x)
        
    print "\nFinished compiling.\n"
         
###############################################################################

def evalArguments():
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
            print "Unknown options. Exiting..."
            sys.exit(1)

###############################################################################


print "LUMA 1.3pre4 (C) 2003,2004 Wido Depping\n"

doImportCheck()
print ""

evalArguments()

# Check if prefixDir exists
if not(os.path.exists(prefixDir)):
    print "Prefix directory does not exist!"
    sys.exit(1)
    
doCompile()

if not compileOnly:
    doInstall()
    checkPath()
