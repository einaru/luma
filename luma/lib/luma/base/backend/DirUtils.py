# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <wido.depping@tu-clausthal.de>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import os
import sys
import string

class DirUtils(object):
    """A class for getting the location of some importan directories.
    
    self.SCRIPTNAME: is a string representing the name of the script.
    
    self.PREFIX: is a string of the prefix directory where the programm
    is installed.
    self.USERDIR: is a string of the home directory of the user running the programm 
    
    
    """
    
###############################################################################

    def __init__(self):
        self.SCRIPTNAME, self.argumentStrip = self.__split_argument()
        self.PREFIX = self.__get_prefix()
        self.USERDIR = os.environ['HOME']
        
###############################################################################

    def __split_argument(self):
        tmpList = sys.argv[0].split("/")
        scriptname = tmpList[:-1]
        argumentStrip = "/".join(tmpList[:-1])
        
        return scriptname, argumentStrip
        
###############################################################################

    def __get_prefix(self):
        tmp = os.path.abspath(self.argumentStrip)
        foo = tmp.split("/")
        lastDir = foo[-1:]
        prefix = tmp[:-(len(lastDir[0])+1)]
        
        return prefix

    
