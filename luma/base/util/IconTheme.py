# -*- coding: utf-8 -*-
#
# base.util.icontheme
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
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


def iconFromTheme(icon, fallback):
    """ Utility method for getting icons from default X11 icon theme.

    Returns a ``QIcon`` from the X11 system-icon theme if a match is
    found, else the `fallback` is used.

    :param icon: the name of the icon in the X11 icon-theme.
    :type icon: string
    :param fallback: the name of the fallback icon.
    :type icon: string
    """
    return QIcon.fromTheme(icon, QIcon(fallback))


def pixmapFromTheme(icon, fallback, width=48, height=48, mode=QIcon.Normal,
                    state=QIcon.Off):
    """Utility method for converting a ``QIcon`` to a ``QPixmap``.
    Useful when trying to use icons from a X11 iconTheme but need a
    pixmap.

    Returns a ``QPixmap`` from the X11 system icon-theme if a match is
    found, else the `fallback` is used.

    :param icon: the name of the icon in the icon theme.
    :type icon: string
    :param fallback: the name of the fallback icon.
    :type fallback: string
    :param widht: the width of the icon, default is 48.
    :type width: int
    :param height: the height of the icon, default is 48.
    :type height: int
    :param mode: the icon mode, default is ``QIcon.Normal``,
    :type mode: see http://doc.trolltech.com/4.7/qicon.html#Mode-enum
    :param state: the icon state, default is ``QIcon.Off``,
    :type state: see http://doc.trolltech.com/4.7/qicon.html#State-enum
    """
    ret = iconFromTheme(icon, fallback)
    return ret.pixmap(QSize(width, height), QIcon.Normal, QIcon.Off)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
