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

from .model.SearchResultModel import ResultItemModel, createTestModel

class ResultView(QWidget):
    """This class respresent a search result view.
    """

    DEVEL = True

    def __init__(self, filter='', criterialist=[], resultlist=[], parent=None):
        """
        @param filter: string;
            The search filter used for the preceeding search.
        @param criterialist: list;
            The criterias used in the search. Extracted from the filter.
        @param resultlist: list;
            The result from the preceeding search operation.
        """
        super(ResultView, self).__init__(parent)
        self.layout = QtGui.QVBoxLayout(self)
        if len(resultlist) == 0:
            self.onNoResult()
            return
        
        # TODO: display the search result:
        #       * Implement the result list model
        #       * setup the result widget gui
        #       * implement result item browsing
        if self.DEVEL:
            for item in resultlist:
                print item
            
            for criteria in criterialist:
                print criteria
        
        self.proxymodel = QSortFilterProxyModel(self)
        self.proxymodel.setDynamicSortFilter(True)
        
        # Testing
        self.headerdata = ['dn']
        self.headerdata.extend(criterialist)
        self.model = createTestModel(self, len(self.headerdata), self.headerdata)
        self.proxymodel.setSourceModel(self.model)
        
        self.setResultData(resultlist)
        
        self.resultview = QTreeView(self)
        self.resultview.setRootIsDecorated(False)
        self.resultview.setAlternatingRowColors(True)
        self.resultview.setSortingEnabled(True)
        self.resultview.setModel(self.proxymodel)
        
        self.layout.addWidget(self.resultview)
    
    def setResultData(self, data=[]):
        """
        """
        row = 0
        for d in data:
            self.model.insertRow(row)
            for col in xrange(self.model.columnCount()):
                
                for attr in self.headerdata:
                    if d.hasAttribute(attr):
                        data = d.getAttributeValueList(attr)
                        # TODO: comlete this implementation
                self.model.setData(self.model.index(row, col), d.getPrettyDN())
            row += 1
        

    def onNoResult(self):
        """If the given result list is empty, we display a 'no result'
        message.
        """
        font = QtGui.QFont()
        font.setBold(True)
        sadface = QtGui.QLabel(self)
        sadface.setPixmap(pixmapFromThemeIcon('face-sad', ':/icons/face-sad'))
        noresult = QtGui.QLabel(self)
        noresult.setText('Sorry, no result to display!')
        noresult.setFont(font)
        hlayout = QtGui.QHBoxLayout()
        hlayout.addItem(self.__getVSpacer())
        hlayout.addWidget(sadface)
        hlayout.addWidget(noresult)
        hlayout.addItem(self.__getVSpacer())
        
        self.layout.addLayout(hlayout)
    
    def __getVSpacer(self):
        return QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
