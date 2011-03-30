# -*- coding: utf-8 -*-
#
# plugins.search.SearchResult
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

from PyQt4 import QtGui
from PyQt4.QtGui import (QSortFilterProxyModel, QTreeView, QWidget)

from base.util.IconTheme import pixmapFromThemeIcon

from .model.SearchResultModel import createTestModel

class ResultView(QWidget):
    """This class respresent a search result view.
    """

    DEVEL = True

    def __init__(self, filter='', attributelist=[], resultlist=[], parent=None):
        """
        @param filter: string;
            The search filter used for the preceeding search.
        @param attributelist: list;
            The attributes used in the search. Extracted from the filter.
        @param resultlist: list;
            The result from the preceeding search operation.
        """
        super(ResultView, self).__init__(parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.retranslate()
        if len(resultlist) == 0:
            self.onNoResult()
            return

        # The proxy model is used for sort and filter support
        self.proxymodel = QSortFilterProxyModel(self)
        self.proxymodel.setDynamicSortFilter(True)

        # TODO: Testing: refactor and clean code -> (* source model *)
        self.headerdata = ['dn']
        self.headerdata.extend(attributelist)

        self.model = createTestModel(self, len(self.headerdata), self.headerdata)
        self.proxymodel.setSourceModel(self.model)

        self.resultview = QTreeView(self)
        self.resultview.setUniformRowHeights(True)
        self.resultview.setRootIsDecorated(False)
        self.resultview.setAlternatingRowColors(True)
        self.resultview.setSortingEnabled(True)
        self.resultview.setModel(self.proxymodel)

        self.layout.addWidget(self.resultview)

        self.setResultData(resultlist)
        self.resultview.resizeColumnToContents(0)

    def setResultData(self, data=[]):
        """Populates the result view model with result data.
        
        @param data: list;
            A list containing the SmartDataObjects representing items
            in the LDAP search result.
        """
        row = 0
        for object in data:
            self.model.insertRow(row)
            col = 0
            for attr in self.headerdata:
                if self.isDistinguishedName(attr):
                    modelData = object.getPrettyDN()
                if self.isObjectClass(attr):
                    modelData = ','.join(object.getObjectClasses())
                if object.hasAttribute(attr):
                    if object.isAttributeBinary(attr):
                        modelData = self.str_BINARY_DATA
                    else:
                        modelData = object.getAttributeValueList(attr)

                self.model.setData(self.model.index(row, col), modelData)
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

    def __getVSpacer(self):
        return QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

    def onNoResult(self):
        """Adds a styled 'no result' message to the main layout.
        """
        font = QtGui.QFont()
        font.setBold(True)
        sadface = QtGui.QLabel(self)
        sadface.setPixmap(pixmapFromThemeIcon('face-sad', ':/icons/face-sad'))
        noresult = QtGui.QLabel(self)
        noresult.setText(self.str_NO_RESULT)
        noresult.setFont(font)
        hlayout = QtGui.QHBoxLayout()
        hlayout.addItem(self.__getVSpacer())
        hlayout.addWidget(sadface)
        hlayout.addWidget(noresult)
        hlayout.addItem(self.__getVSpacer())

        self.layout.addLayout(hlayout)

    def retranslate(self):
        """For dynamic translation support.
        """
        self.str_NO_RESULT = QtGui.QApplication.translate("ResultView", "Sorry, no result to display!")
        self.str_BINARY_DATA = QtGui.QApplication.translate("ResultView", "Binary Data")
