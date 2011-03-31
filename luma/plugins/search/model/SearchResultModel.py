# -*- coding: utf-8 -*-
#
# plugins.search.model.SearchModel
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
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! NOT CURRENTLY IN USE!                                                    !!
!!                                                                          !!
!! This custom model should be implemented in order to support viewing,     !! 
!! deleting and exportingsearch result items.                               !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
from PyQt4 import QtCore
from PyQt4.QtCore import (QAbstractTableModel)
from PyQt4.QtGui import (QStandardItemModel)

class ResultViewModel(QAbstractTableModel):
    """
    """
    
    def __init__(self, parent=None):
        """
        """
        super(ResultViewModel, self).__init__(parent)
        self.resultdata = {}

    def removeRow(self):
        """
        """
        pass
    
    def rowCount(self, parent=QtCore.QModelIndex()):
        pass
    
    def columnCount(self, parent=QtCore.QModelIndex()):
        pass
    
    def headerData(self, section, orientation, role):
        """
        """
        pass

    def flags(self, index):
        if not index.isValid():
            return QtCore.QVariant()
        else:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        """
        pass
    
    def index(self, row, column, parnet):
        """
        """
        pass


class ResultItemModel(QStandardItemModel):
    """The model for the Search plugin Result View
    """

    def __init__(self, row, column, headerdata=[], parent=None):
        super(ResultItemModel, self).__init__(row, column, parent)
        self.headerdata = headerdata
        self.data = []
    
    def index(self, row, column, parent=None):
        """
        """
        if row < 0 or column < 0:
            return QtCore.QModelIndex()
        
    
    def columnCount(self, parent=None):
        """
        @return:
            the length of the headerdata list.
        """
        return len(self.headerdata)

    def rowCount(self, parent):
        """
        @returns:
            the length of the resultdata list
        """
        return len(self.data)
        

    def populateHeader(self, headerdata=[]):
        """Populates the model header with data.
        
        @param headerdata: list;
            A list containing the attributes used in the search.
        """
        i = 0
        for data in headerdata:
            self.setHeaderData(i. Qt.Horizontal, data)
            i += 1

    def populateModel(self, data=[]):
        """Populates the result view model with result data.
        
        @param data: list;
            A list containing the SmartDataObjects representing items
            in the LDAP search result.
        """
        row = 0
        for object in data:
            self.insertRow(row)
            col = 0
            for attr in self.headerdata:
                if self.isDistinguishedName(attr):
                    modelData = object.getPrettyDN()
                elif self.isObjectClass(attr):
                    modelData = ','.join(object.getObjectClasses())
                elif object.hasAttribute(attr):
                    if object.isAttributeBinary(attr):
                        modelData = self.str_BINARY_DATA
                    else:
                        modelData = ','.join(object.getAttributeValueList(attr))

                self.setData(self.model.index(row, col), modelData)
                col += 1

            row += 1

    def isDistinguishedName(self, attr):
        """
        @return: boolean value;
            True if attr is dn, False otherwise.
        """
        return attr.lower() == 'dn'

    def isObjectClass(self, attr):
        """
        @return: boolean value;
            True if attr is objectClass, False otherwise.
        """
        return attr.lower() == 'objectclass'
    
    def deleteItem(self, index):
        """Slot for deleting an item.
        """
        pass
