# -*- coding: utf-8 -*-
#
# plugins.search.__init__
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

from base.util.IconTheme import iconFromTheme

lumaPlugin = True
pluginName = u"browser"
pluginUserString = u"Browser"
version = u"0.3"
author = u"Christian Forfang, Simen Natvig, Per Ove Ringdal, Vegar Westerlund"
description = u""

def getIcon():
    return iconFromTheme('luma-browser-plugin', ':/icons/plugins/browser')

def getPluginWidget(parent, mainwin):
    from plugins.browser.BrowserView import BrowserView
    # parent is not used, but the widget is reparented by the QTabWidget
    pluginWidget = BrowserView()
    return pluginWidget

def getPluginSettingsWidget(parent):
    return None

def postprocess():
    return

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
