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

def set_paths():
    global lumaInstallationPrefix 
    global lumaScriptName 
    global userHomeDir 
    
    tmpList = os.path.split(sys.argv[0])
    
    # This ensure that you can start luma in two ways:
    # 1. using the symlink in luma/bin
    # 2. using luma.py from /luma/lib/luma
    if (tmpList[1] == 'luma.py') and (os.path.split(os.path.abspath(tmpList[0]))[1] == 'luma'):
        tmpPrefix = os.path.abspath(tmpList[0])
        lumaInstallationPrefix = os.path.split(os.path.split(tmpPrefix)[0])[0]
    else:
        tmpPrefix = os.path.abspath(tmpList[0])
        lumaInstallationPrefix = os.path.split(tmpPrefix)[0]
        
    lumaScriptName = tmpList[1]
    userHomeDir = os.path.expanduser("~")
    
###############################################################################

def update_ui():
    """ This is only a function dummy. The MainWin sets its update_ui function to this one.
    
    This way these functions can be accessed globally. No need to import qt and use qApp
    """
    pass

###############################################################################

def set_busy(self, busy):
    """ This is only a function dummy. The MainWin sets its update_ui function to this one.
    
    This way these functions can be accessed globally. No need to import qt and use qApp
    """
    pass
    
###############################################################################
  
lumaInstallationPrefix = None
lumaScriptName = None
userHomeDir = None
  
set_paths()

