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

from PyQt4.QtCore import (QAbstractItemModel, Qt)
from PyQt4.QtGui import QStandardItemModel


def createTestModel(parent, column=3, headerdata=[]):
    model = QStandardItemModel(0, column, parent)
    
    i = 0
    for header in headerdata:
        model.setHeaderData(i, Qt.Horizontal, header)
        i += 1
    
    return model

class ResultItemModel(QAbstractItemModel):
    """
    """
    
    def __init__(self, parent=None):
        super(ResultItemModel, self).__init__(parent)
        # TODO: implement


class ResultListModel():
    """
    """
    
    def __init__(self, parent=None):
        pass