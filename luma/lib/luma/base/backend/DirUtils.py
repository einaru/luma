# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import os.path
import sys


class DirUtils(object):
    """A class for getting the location of some importan directories.
    
    self.SCRIPTNAME: is a string representing the name of the script.
    
    self.PREFIX: is a string of the prefix directory where the programm
    is installed.
    self.USERDIR: is a string of the home directory of the user running the programm 
    
    
    """
    SCRIPTNAME = ""
    PREFIX= ""
    USERDIR= ""
    
###############################################################################

    def __init__(self):
        tmpList = os.path.split(sys.argv[0])
        tmpPrefix = os.path.abspath(tmpList[0])
        self.PREFIX= os.path.split(tmpPrefix)[0]
        
        self.SCRIPTNAME = tmpList[1]
        self.USERDIR = os.path.expanduser("~")
    
