# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Simen Natvig, <simen.natvig@gmail.com>
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
from PyQt4.QtCore import QAbstractTableModel, QModelIndex
from PyQt4.QtCore import Qt, SIGNAL, QVariant

from ..TemplateObject import TemplateObject

class TemplateTableModel(QAbstractTableModel):

    def __init__(self, templateList, parent = None):
        QAbstractTableModel.__init__(self, parent)
        self._templateList = templateList

    def insertRow(self, tO):
        if tO:
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            self._templateList.addTemplate(tO)
            self.endInsertRows()
            return True
        return False

    def removeRow(self, index):
        self.beginRemoveRows(QModelIndex(), index.row(), index.row())
        self._templateList.deleteTemplateByIndex(index.row())
        self.endRemoveRows()
        return True

    def setData(self, index, value, role = Qt.EditRole):
        """
        Handles updating data in the TemplateObjects
        """

        if not index.isValid():
            return False

        value = value.toPyObject()
        #value = index.internalPointer()

        row = index.row()
        column = index.column()

        # Find the templateobject from the list of them
        templateObject = self._templateList.getTable()[row]

        # Update the correct field in it (given by the column) with the given data
        templateObject.setIndexToValue(column, value)

        # Let other views know the underlying data is (possibly) changed
        self.emit(SIGNAL("dataChanged( const QModelIndex&, const QModelIndex& )"), index, index)
        return True

    def rowCount(self, parent = QModelIndex()):
        #Number of templates
        return len(self._templateList.getTable())

    def columnCount(self, parent = QModelIndex()):
        #Number of different settings for the templates
        return 5

    def flags(self, index):
        if not index.isValid():
            return QVariant()
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

    def data(self,index,role = Qt.DisplayRole):
        """
        Handles getting the correct data from the TemplateObjects and returning it
        Only used on  the name and description
        """

        if not index.isValid():
            return QVariant()

        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole or role ==Qt.EditRole:
            # getTable() return a list of all the TemplateObjects
            templateObject = self._templateList.getTable()[row]

            # return the property set in the given column
            return templateObject.getList()[column]

    def index(self, row, column, parent = None):
        if row < 0 or column < 0:
            return QModelIndex()
        if row >= self.rowCount() or column >= self.columnCount():
            return QModelIndex()
        internalPointer = self._templateList.getTable()[row]
        return self.createIndex(row, column, internalPointer)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

