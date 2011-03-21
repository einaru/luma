# -*- coding: utf-8 -*-
#
# base.model.SettingsModel
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

from PyQt4.QtCore import QAbstractListModel

class SettingsModel(QAbstractListModel):
    """ A class for modelling the application settings.
    Provided to keep things centralized and automated, since both the 
    application mainwindow and various dialogs need access to the same
    settings.
    """
    
    def __init__(self, Settings, parent=None):
        """
        @param Settings: 
            the Settings object.
        """
        super(QAbstractListModel, self).__init__(parent)
        self.__Settings = Settings
        
    def removeRows(self, row, count):
        pass
    
    def setData(self, index, value, role):
        pass
    
    def data(self, index, role):
        pass
    
    def rowCount(self, parent):
        pass
    
    def columnCount(self, parent):
        pass
    
    def flags(self, index):
        pass