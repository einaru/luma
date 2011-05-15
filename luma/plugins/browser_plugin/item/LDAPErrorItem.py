# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Christian Forfang, <cforfang@gmail.com>
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

from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from PyQt4.QtGui import QIcon, QPixmap
from PyQt4 import QtCore

from base.util.IconTheme import iconFromTheme

class LDAPErrorItem(AbstractLDAPTreeItem):
    """
    Used to indicate an error.
    """
    
    def __init__(self, data, serverParent, parent):
        AbstractLDAPTreeItem.__init__(self, serverParent, parent)
                
        if data != None:
            self.error = data
        else:
            self.error = "Error!"
        
        self.populated = 1
        
    def data(self, column, role):
        if role == QtCore.Qt.StatusTipRole:
            return QtCore.QCoreApplication.translate("LDAPErrorItem","There was an error receiving this item or it's parent. See the attached error-message and/or the log for details.")
        if role == QtCore.Qt.DecorationRole:
            #return QIcon(QPixmap(":/icons/no"))
            return iconFromTheme('dialog-error', ':/icons/48/dialog-error')
        if not role == QtCore.Qt.DisplayRole:
            return None
        return self.error
    
    def columnCount(self):
        return 1
    
    def smartObject(self):
        return None
    
    def fetchChildList(self):
        return (None, None, None)
    
    def getSupportedOperations(self):
        return AbstractLDAPTreeItem.SUPPORT_NONE
        

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
