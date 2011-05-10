# -*- coding: utf-8 -*-

import ldap
import PyQt4
import copy
from PyQt4 import QtCore
from PyQt4.QtCore import QObject


from base.backend.ServerList import ServerList
from base.backend.LumaConnectionWrapper import LumaConnectionWrapper
from base.backend.SmartDataObject import SmartDataObject, LdapDataException

class EntryModel(QObject):

    def __init__(self, smartObject, parent=None, entryTemplate = None):
        QObject.__init__(self, parent)
        self.smartObject = smartObject
        self.entryTemplate = entryTemplate
        
        # does the smartobject have a schema?
        self.VALID = False

        # boolean to indicate if the current ldap object has been modified
        self.EDITED = False
        
        # is the current object a leaf of the ldap tree?
        self.ISLEAF = False
        
        # do we create a completely new object?
        self.CREATE = False

        self.str_BIND = QtCore.QCoreApplication.translate("EntryModel", "Could not bind to server.")
        self.str_DELETE = QtCore.QCoreApplication.translate("EntryModel", "Could not delete entry.")
        self.str_ADD = QtCore.QCoreApplication.translate("EntryModel", "Could not add entry.")
        self.str_REFRESH = QtCore.QCoreApplication.translate("EntryModel", "Could not refresh entry.")
        self.str_CHECK_LEAF = QtCore.QCoreApplication.translate("EntryModel", "Could not check if object is a leaf in the ldap tree.")
        self.str_SAVE = QtCore.QCoreApplication.translate("EntryModel", "Could not save entry.")
    
    """ The signal that viewers should connect on, called when the model changes
        The parameter is true when the smartobject is reloaded, and on init, which
        means that the smartobject might have gone invalid
    """
    modelChangedSignal = QtCore.pyqtSignal("bool")

###############################################################################

    def getSmartObject(self):
        return self.smartObject

###############################################################################

    def initModel(self, create=False):
        if create:
            self.EDITED = True
            self.ISLEAF = False
            self.CREATE = True
            self.VALID = True
        else:
            self.EDITED = False
            isLeave = False
            self.smartObject.checkIntegrity()
            self.VALID = self.smartObject.isValid

            serverMeta = self.smartObject.getServerMeta()
        
            lumaConnection = LumaConnectionWrapper(serverMeta, self)
        
            bindSuccess, exceptionObject = lumaConnection.bindSync()
            
            if not bindSuccess:
                message = self.str_BIND
                return (False, message, exceptionObject)
            
            success, resultList, exceptionObject = lumaConnection.searchSync(self.smartObject.dn, ldap.SCOPE_ONELEVEL, filter="(objectClass=*)", attrList=None, attrsonly=1, sizelimit=1)
            lumaConnection.unbind()
            
            # Our search succeeded. No errors
            if success:
                
                # There are no leaves below
                if len(resultList) == 0:
                    self.ISLEAF = True
                
                # Leaves are below
                else:
                    self.ISLEAF = False
                    
            # Error during search request
            else:
                self.ISLEAF = False
                message = self.str_CHECK_LEAF
                return (False, message, exceptionObject)
                
            self.CREATE = False
            
        self.modelChangedSignal.emit(True)
        return (True, None, None)

###############################################################################

    def reloadModel(self):
        """ 
        Refreshes the LDAP data from server, 
        """
        lumaConnection = LumaConnectionWrapper(self.smartObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bindSync()
        
        if not bindSuccess:
            message = self.str_BIND
            return (False, message, exceptionObject)
        
        success, resultList, exceptionObject = lumaConnection.searchSync(self.smartObject.getDN(), ldap.SCOPE_BASE)
        lumaConnection.unbind()
        
        if success and (len(resultList) > 0):
            self.smartObject = resultList[0]
            self.smartObject.checkIntegrity()
            self.VALID = self.smartObject.isValid
            self.EDITED = False
            self.modelChangedSignal.emit(True)
            return (True, None, None)
        else:
            message = self.str_REFRESH
            return (False, message, exceptionObject)

###############################################################################

    def saveModel(self):
        """ 
        Save changes to the current object.
        """
        
        lumaConnection = LumaConnectionWrapper(self.smartObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bindSync()
        
        if not bindSuccess:
            message = self.str_BIND
            return (False, message, exceptionObject)
        
        if self.CREATE:
            success, exceptionObject = lumaConnection.addDataObject(self.smartObject)
            lumaConnection.unbind()
            
            if success:
                #self.CREATE = False
                self.EDITED = False
                self.modelChangedSignal.emit(False)
                return (True, None, None)
            else:
                message = self.str_ADD
                return (False, message, exceptionObject)
        else:
            success, exceptionObject = lumaConnection.updateDataObject(self.smartObject)
            lumaConnection.unbind()
            if success:
                self.EDITED = False
                self.modelChangedSignal.emit(False)
                return (True, None, None)
            else:
                message = self.str_SAVE
                return (False, message, exceptionObject)

###############################################################################

    # TODO: add logging for each error, remove tab and node from parent
    def deleteObject(self):
        """
        Deletes the remote object that this model represents
        """
        
        lumaConnection = LumaConnectionWrapper(self.smartObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bindSync()
        
        if not bindSuccess:
            message = self.str_BIND
            return (False, message, exceptionObject)
        
        success, exceptionObject = lumaConnection.delete(self.smartObject.getDN())
        lumaConnection.unbind()
        
        if success:
            #serverName = self.smartObject.getServerAlias()
            #dn = self.smartObject.getPrettyParentDN()
            #self.model().reloadItem(self.smartObject.parent())
            #self.modelChangedSignal.emit()
            return (True, None, None)
        else:
            message = self.str_DELETE
            return (False, message, exceptionObject)

###############################################################################

    def editAttribute(self, attributeName, index, newValue):
        self.smartObject.setAttributeValue(attributeName, index, newValue)
        self.EDITED = True
        self.modelChangedSignal.emit(False)

###############################################################################

    def deleteAttribute(self, attributeName, index):
        self.smartObject.deleteAttributeValue(attributeName, index)
        self.EDITED = True
        self.modelChangedSignal.emit(False)

###############################################################################

    def deleteObjectClass(self, className):
        self.smartObject.deleteObjectClass(className)
        self.EDITED = True
        self.modelChangedSignal.emit(False)

###############################################################################

    def setDN(self, rdn):
        self.smartObject.setDN(rdn)
        self.EDITED = True
        self.modelChangedSignal.emit(False)
        
###############################################################################

    def addAttributeValue(self, attributeName, attributeValueList):
        self.smartObject.addAttributeValue(attributeName, attributeValueList)
        self.EDITED = True
        self.modelChangedSignal.emit(False)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
