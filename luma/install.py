#!/usr/bin/env python

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
    myError = 0
    try:
        import ldap
        vString = "2.0.0pre13"
        if ldap.__version__ >= vString:
            print "\tGood: python-ldap (>= " + vString + ") installed."
        else:
            print "\tBad: Installed version of python-ldap is out of date."
            print "\t     At least version " + vString + " is needed"
            print "\t     Currently version " + ldap.__version__ + " is available.\n"
            myError = 1
    except ImportError:
        print """\tERROR: python-ldap not installed!!!
\tYou can get the module here: http://python-ldap.sourceforge.net
"""
        myError = 1

    try:
        import qt
        print "\tGood: PyQt installed."
    except ImportError:
        print """\n\tERROR: PyQt not installed!!!
\tYou can get the module here: http://www.riverbankcomputing.co.uk/pyqt
"""
        myError = 1
        
    try:
        import mx.DateTime
        print "\tGood: Egenix mx package installed."
    except ImportError:
        print """\n\tERROR: Egenix mx package not installed!!!
\tYou can get the module here: http://www.egenix.com/
\tNOTE: This package is only needed for the "Massive User Creation"- and the
\t"Admin Utilities"-Plugin.
"""

    if myError:
        sys.exit(1)

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
        a = Popen3("cp -pR bin " + prefixDir)
        while a.poll() == -1:
            pass
        if a.poll() > 0:
            raise "CopyError", "Error!!! Could not copy File. Maybe wrong permissions?"

        a = Popen3("cp -pR lib " + prefixDir)
        while a.poll() == -1:
            pass
        if a.poll() > 0:
            raise "CopyError", "Error!!! Could not copy File. Maybe wrong permissions?"

        a = Popen3("cp -pR share " + prefixDir)
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
 --prefix=PATH \t install path (e.g. /usr/local)"""
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
         


print "LUMA 1.0beta1 (C) 2003 Wido Depping\n"
print "Check for preinstalled modules:"
doImportCheck()
print ""

doChecks()
