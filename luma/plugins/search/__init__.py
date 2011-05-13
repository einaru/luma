# -*- coding: utf-8 -*-
#
# plugins.search.__init__
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

from base.util.IconTheme import iconFromTheme
from .Search import (SearchPlugin, SearchPluginSettingsWidget)

lumaPlugin = True
pluginName = u'search'
pluginUserString = u'Search'
version = u'0.3'
author = u'Einar Uvsløkk'
description = u"""Do simple and advanced LDAP search,
create filters to speed up efficiency.
"""

def getIcon(iconPath=None):
    return iconFromTheme('luma-search-plugin', ':/icons/plugins/search')


def getPluginWidget(parent, mainwin):
    return SearchPlugin(parent)


def getPluginSettingsWidget(parent):
    return SearchPluginSettingsWidget()


def postprocess():
    return


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
