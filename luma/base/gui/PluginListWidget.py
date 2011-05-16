# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Johannes Harestad, <johannesharestad@gmail.com>
#
# Luma is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public Licence as published by
# the Free Software Foundation; either version 2 of the Licence, or
# (at your option) any later version.
#
# Luma is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence
# for more details.
#
# You should have received a copy of the GNU General Public Licence along
# with Luma; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

from PyQt4.QtCore import QSize
from PyQt4.QtGui import QWidget, QListView
from ..gui.design.PluginListWidgetDesign import Ui_pluginListWidget
from ..model.PluginListWidgetModel import PluginListWidgetModel

import sys
import logging


class PluginListWidget(QWidget, Ui_pluginListWidget):
    """Used by mainwin to show the list of plugins that can be loaded.

    Parent is given to the model, because it is going to contain not
    only the ``QStandardItem`` but the widget for each item, that
    requires a parent.
    """
    __logger = logging.getLogger(__name__)

    def __init__(self, parent):
        QWidget.__init__(self, None)
        #dont change None to self in parent

        self.parent = parent
        self.setupUi(self)

        self.listView.setResizeMode(QListView.Adjust)
        self.listView.setViewMode(QListView.IconMode)
        self.listView.setModel(PluginListWidgetModel(self.parent))

    def pluginDoubleClicked(self, index):
        if self.parent and hasattr(self.parent, "pluginSelected"):
            self.parent.pluginSelected(self.listView.model().itemFromIndex(index))
        else:
            msg = 'Cannot open plugin. No parent given to the PluginListWidget'
            self.__logger.error(msg)

    def updatePlugins(self):
        """Updates the listview with new plugins
        """
        self.listView.reset()
        self.listView.setModel(PluginListWidgetModel(self.parent))


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
