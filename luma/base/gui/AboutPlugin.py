# -*- coding: utf-8 -*-
#
# base.gui.AboutPlugin
#
# Copyright (c) 2011
#     Johannes Harestad, <johanhar@stud.ntnu.no>
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

from PyQt4.QtGui import QWidget
from ..gui.design.AboutPluginDesign import Ui_AboutPlugin


class AboutPlugin(QWidget, Ui_AboutPlugin):

    def __init__(self, plugin, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        if not plugin:
            return

        self.label_name.setText(plugin.pluginUserString)
        self.label_version.setText(plugin.version)
        self.label_author.setText(plugin.author)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
