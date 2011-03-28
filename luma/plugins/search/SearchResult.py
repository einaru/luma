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
from PyQt4.QtGui import QWidget

from base.util.IconTheme import pixmapFromThemeIcon

from .model.SearchResultModel import ResultListModel

class ResultView(QWidget):
    """This class respresent a search result view.
    """

    def __init__(self, filter='', criteria=[], result=[], parent=None):
        super(ResultView, self).__init__(parent)
        self.layout = QtGui.QVBoxLayout(self)
        if len(result) == 0:
            self.onNoResult()
            return
        
        self.model = ResultListModel(self)
        # TODO: display the search result:
        #       * Implement the result list model
        #       * setup the result widget gui
        #       * implement result item browsing 
        

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
