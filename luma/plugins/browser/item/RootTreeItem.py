# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Christian Forfang, <cforfang@gmail.com>
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

import logging
from AbstractLDAPTreeItem import AbstractLDAPTreeItem

class RootTreeItem(AbstractLDAPTreeItem):
    """
    Represent the (invisible) root item of the model.
    """
    
    def __init__(self, title, parent = None):
        AbstractLDAPTreeItem.__init__(self, None, parent)
        
        self.title = title
        self.logger = logging.getLogger(__name__)
        
    def data(self, column):
        return self.title
    
    def columnCount(self):
        return 1
    
    def fetchChildList(self):
        return (None, None, None)
    
    def smartObject(self):
        return None

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
