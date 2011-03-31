# -*- coding: utf-8 -*-
#
# base.util.icontheme
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

from PyQt4.QtCore import QSize
from PyQt4.QtGui import QIcon

def iconFromTheme(themeIcon, fallbackIcon):
    """ Utility method for getting icons from default X11 icon theme.
    
    @param themeIcon: a string;
        the name of the icontheme icon
    @param fallbackIcon: a string;
        the name of the fallback icon
    
    @return:
        a QIcon from the current icon theme if a match is found, 
        the fallback QIcon if not.
    """
    return QIcon.fromTheme(themeIcon, QIcon(fallbackIcon))

def pixmapFromThemeIcon(themeIconName, fallbackIconName, width=48, height=48,
                           mode=QIcon.Normal, state=QIcon.Off):
    """
    Utility method for converting a QIcon to a QPixmap. Useful when
    trying to use icons from a X11 iconTheme but need a pixmap.
    
    @param themeIcon: string;
        the name of the icontheme icon
    @param fallbackIcon: string;
        the name of the fallback icon
    @param widht: integer;
        the width of the icon, defaults to 48
    @param height: integer;
        the height of the icon, defaults to 48
    @param mode:
        defaults to QIcon.Normal
    @param state:
        defaults to QIcon.Off
        
    @return:
        a QPixmap from a icon in the current icon theme if a match is
        found. A QPixmap from the fallback icon if not. 
    """
    icon = iconFromTheme(themeIconName, fallbackIconName)
    return icon.pixmap(QSize(width, height), QIcon.Normal, QIcon.Off)

