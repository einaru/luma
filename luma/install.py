#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
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


def doImportCheck():
    try:
        import ldap
        vString = "2.0.0pre13"
        print "python-ldap is installed..."
        print "\tInstalled Version: " + ldap.__version__
        print "\tNeeded Version: " + vString
        print ""
    except ImportError:
        print """ERROR: python-ldap not installed!!!
You can get the module here: http://python-ldap.sourceforge.net
"""

    try:
        import qt
        vString = "3.7"
        print "PyQt is installed..."
        print "\tInstalled Version: " + qt.PYQT_VERSION_STR
        print "\tNeeded Version: " + vString
        print ""
    except ImportError:
        print """\nERROR: PyQt not installed!!!
You can get the module here: http://www.riverbankcomputing.co.uk/pyqt
"""

def doChecks():
    global prefixDir
    if len(sys.argv) == 1:
        printHelp()
    else:
        prefix = sys.argv[1]
        if prefix[:9] == "--prefix=":
            prefixDir = prefix[9:]
            if (prefixDir[-1:] == "/") and (len(prefixDir) > 1):
                prefixDir = prefixDir[:-1]
        else:
            print "Bad argument!"
            sys.exit(1)

    # Check ob Prefix existiert
    if os.path.exists(prefixDir):
        doCompile()
        doInstall()
    else:
        print "Prefix directory does not exist!"
        sys.exit(1)

def doInstall():
    print "Copy programm files ..."
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

        print "LUMA installed succesfully! :)"
        
    except "CopyError", errorMessage:
        print errorMessage
        sys.exit(1)

    pathVariable = os.environ['PATH']

    pathValues = string.split(pathVariable, ':')

    good = 0
    for x in pathValues:
        if x == (prefixDir+"/bin"):
            good = 1
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


def printHelp():
    helpString = """Install options:
 --prefix=PATH \t install path (e.g. /usr/local)\n"""
    print helpString
    sys.exit(1)
    
def doCompile():
    input, output = os.popen2("find . -name \"*.py\"")
    tmpArray = output.readlines()
    fileList = []
    for x in tmpArray:
        if x[:11] == "./lib/luma/":
            fileList.append(x[:-1])
    for x in fileList:
        print "compile " + x
        py_compile.compile(x)
         


print "LUMA 1.2 (C) 2003 Wido Depping\n"
print "Check for preinstalled modules:\n"
doImportCheck()
print ""

doChecks()
