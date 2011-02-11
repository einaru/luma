# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# Luma is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public Licence as published by the Free Software
# Foundation; either version 2 of the Licence, or (at your option) any later
# version.
#
# Luma is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence for more 
# details.
#
# You should have received a copy of the GNU General Public Licence along with
# Luma; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA  02110-1301, USA

from PyQt4.QtGui import QStandardItemModel
from PyQt4.QtCore import Qt

class PluginListModel(QStandardItemModel):
    """
    Model class for the plugin list
    """

    def __init__(self, dataList, header, parent=None, *args):
        QStandardItemModel.__init__(self, len(dataList), 1)
        self.pluginList = dataList
        self.header = header

    def rowCount(self, parent):
        return len(self.pluginList)

    def columnCount(self, parent):
        return 1
    
    def data(self, index, role):
        if not index.IsValid():
            return Qt.QVariant()
        elif role != Qt.DisplayRole:
            return Qt.QVariant()
        return Qt.QVariant(self.dataList[index.row()])

    def headerData(self, column, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return Qt.QVariant(self.header[column])
        return Qt.QVariant

