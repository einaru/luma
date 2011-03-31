# -*- coding: utf-8 -*-
#
# base.util.paths
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einaru@stud.ntnu.no>
#     Johannes Harestad, <johannesharestad@gmail.com>
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

import os
import platform
import tempfile

def getLumaRoot():
    """Utility method for locating the Luma root location.
    
    This is done by using pythons magical __file__ attribute, to get
    the location of this module, and joining it with the required
    number of levels up to the root.
    
    NOTE: The use of __file__ most  likely will cause some issues if 
          Luma is packaged with 
    
    @return:
        The absolute file path to the luma root directory, without the
        trailing separator -> /full/path/to/luma
    """
    levelsUp = '..' + os.path.sep + '..'
    return os.path.abspath(os.path.join(os.path.split(__file__)[0], levelsUp))
 

def getConfigPrefix():
    """We must determine what platform we're running on. Making sure
    we follow the platform convention for configuration files and
    directories,

    The platform validation, can be done through a number of modules: 
    
        os.name           -> posix, nt
        sys.platform      -> linux2, windows, darwin
        platform.system() -> Linux, Windows, Darwin
    
    This method will check for a existing config folder based on the
    platform. If it is not found it will be created. Either way the
    path will be returned.
    
    @return: a tuple (success, prefix);
        the boolean value, success, indicates wheter the config prefix
        path exists. It will be true if the path existed or was
        successfully created. If it doesn't exists, and we don't have
        write permissions, it will be False. In this case we will
        return the system temp directory.
    """
    prefix = ''
    success = True

    __platform = platform.system()
    if __platform == "Linux":
        # Best practise config storage on Linux:
        # ~/.config/luma
        # On Linux we try to load the xdg module, to check if the
        # xdg_config_home variable is set to other than default.
        try:
            from xdg import BaseDirectory
            prefix = os.path.join(BaseDirectory.xdg_config_home, 'luma')
        except ImportError:
            prefix = os.path.join(os.environ['HOME'], '.config', 'luma')

    elif __platform == "Darwin":
        # Best practise config storage on Mac OS:
        # http://developer.apple.com/tools/installerpolicy.html
        # ~/Library/Application Support/luma
        prefix = os.path.join(os.environ['HOME'], 'Library', 'Application Support', 'luma')

    elif __platform == "Windows":
        # Best practise config storage on Windows:
        # C:\Users\<USERNAME>\Application Data\luma
        prefix = os.path.join(os.environ['APPDATA'], 'luma')

    else:
        # Default config storage for undetermined platforms
        prefix = os.path.join(os.environ['HOME'], '.luma')

    if not os.path.exists(prefix):
        try:
            os.mkdir(prefix)
        except (IOError, OSError):
            # TODO Do some logging. We should load the application, but 
            #      provide information to user that no settings will be 
            #      saved due to (most likely) file permission issues.
            #      Maybe prompt for a user spesific folder?
            prefix = tempfile.gettempdir()
            success = False

    return (success, prefix)

def getUserHomeDir():
    """Helper method for finding the user home directory.
    
    On UNIX systems this is achieved by using the python os.getenv
    module. On Windows NT systems users is able to have roaming or
    local profiles. For example:
    CSIDL_APPDATA gets for the roaming 'Application Data' directory,
    and CSIDL_LOCAL_APPDATA gets the local one.
    
    @return:
        The path to the user home directory.
    """
    #homedir = os.path.expanduser('~')
    homedir = os.getenv('HOME')
    try:
        from win32com.shell import shellcon, shell         
        homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
    except ImportError:
        homedir = os.path.expanduser("~")
    return homedir