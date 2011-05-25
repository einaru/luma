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

import ldap
import logging

from base.backend.LumaConnectionWrapper import LumaConnectionWrapper

from PyQt4 import QtCore
from PyQt4.QtGui import QPixmap, QIcon

from .LDAPErrorItem import LDAPErrorItem
from .AbstractLDAPTreeItem import AbstractLDAPTreeItem
from .LDAPTreeItem import LDAPTreeItem

class ServerTreeItem(AbstractLDAPTreeItem):
    """
    Represents the servers in the model.
    """
    
    logger = logging.getLogger(__name__)

    def __init__(self, data, serverMeta, parent):
        AbstractLDAPTreeItem.__init__(self, self, parent)
        
        self.itemData = data
        self.serverMeta = serverMeta

        self.loading = False
        self.ignoreItemErrors = False

    def columnCount(self):
        return len(self.itemData)

    def data(self, column, role):
        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.DecorationRole:
            return None
        
        if role == QtCore.Qt.DecorationRole:
            return QIcon(QPixmap(":/icons/16/network-server"))
        else:
            return self.itemData[column]

    def smartObject(self):
        return None
    
    def fetchChildList(self):
        """
        Gets the list of baseDNs for the server and return them.
        """
                
        connection = LumaConnectionWrapper(self.serverMeta)
        
        # If baseDNs are aleady spesified
        if self.serverMeta.autoBase == False:
            self.logger.debug("autoBase=False")
            tmpList = self.serverMeta.baseDN
            
            #Need to bind in order to fetch the data for the baseDNs
            bindSuccess, exceptionObject = connection.bindSync()
            if not bindSuccess:
                self.logger.debug("Bind failed.")
                tmp = LDAPErrorItem(str("["+exceptionObject[0]["desc"]+"]"), self, self)
                # We're adding the error as LDAPErrorItem-child, so return True
                return (True, [tmp], exceptionObject)
            
        # Else get them from the server
        else:
            self.logger.debug("Using getBaseDNList()")
            #self.isWorking.emit()
            success, tmpList, exceptionObject = connection.getBaseDNListSync()
        
            if not success:
                self.logger.debug("getBaseDNList failed:"+str(exceptionObject))
                tmp = LDAPErrorItem(str("["+exceptionObject[0]["desc"]+"]"), self, self)
                return (True, [tmp], exceptionObject) #See above
            
            #getBaseDNList calles unbind(), so let's rebind
            connection.bindSync()
        
        self.logger.debug("Entering for-loop")

        # Get the info for the baseDNs
        newChildList = []
        for base in tmpList:
            success, resultList, exceptionObject = connection.searchSync(base, \
                    scope=ldap.SCOPE_BASE,filter='(objectclass=*)', sizelimit=1)
            if not success:
                self.logger.debug("Couldn't search item:"+str(exceptionObject))
                tmp = LDAPErrorItem(str(base+" ["+exceptionObject[0]["desc"]+"]"), self, self)
                newChildList.append(tmp)
                continue
            
            if resultList:
                self.logger.debug("Found item")
                tmp = LDAPTreeItem(resultList[0], self, self)    
                newChildList.append(tmp)
            
        self.logger.debug("End populatItem")
        
        return (True, newChildList, exceptionObject)
        
    def getSupportedOperations(self):
        return AbstractLDAPTreeItem.SUPPORT_CLEAR|AbstractLDAPTreeItem.SUPPORT_RELOAD
        

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
