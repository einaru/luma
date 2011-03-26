# -*- coding: utf-8 -*-
#
# base.gui.AbstractLumaPlugin
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
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

from PyQt4.QtGui import QIcon
from base.util.IconTheme import pixmapFromThemeIcon

lumaPlugin = False
pluginName = "generic"
pluginUserString = "Generic"
version = ""
author = ""


def getIcon(iconPath = None):
    return QIcon(pixmapFromThemeIcon('package-x-generic', ':/icons/plugin-generic'))


def getPluginWidget(parent, mainwin):
    pass


def getPluginSettingsWidget(parent):
    return


def postprocess():
    return