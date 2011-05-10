# -*- coding: utf-8 -*-

import ldap
import PyQt4
import copy
from PyQt4 import QtCore
from PyQt4.QtCore import QObject


from base.backend.ServerList import ServerList
from base.backend.LumaConnectionWrapper import LumaConnectionWrapper
from base.backend.SmartDataObject import SmartDataObject, LdapDataException

# TODO add translation support
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
        
    modelChangedSignal = QtCore.pyqtSignal("bool")


    def getSmartObject(self):
        return self.smartObject

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
                message = "Could not bind to server."
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
                message = "Could not check if object is a leaf in the ldap tree."
                return (False, message, exceptionObject)
                
            self.CREATE = False
            
        self.modelChangedSignal.emit(True)
        return (True, None, None)

###############################################################################

    # TODO: not used yet
    def exportAttribute(self, attributeName, index):
        return
        """ Show the dialog for exporting binary attribute data.
        """
        '''
        value = self.smartObject.getAttributeValue(attributeName, index)


        #filename = unicode(QFileDialog.getSaveFileName(
        #                    self,
        #fileName = unicode(QFileDialog.getSaveFileName(\
        #                    QString.null,
        #                    "All files (*)",
        #                    self, None,
        #                    self.trUtf8("Export binary attribute to file"),
        #                    None, 1))

        if unicode(fileName) == "":
            return
            
        try:
            fileHandler = open(fileName, "w")
            fileHandler.write(value)
            fileHandler.close()
            SAVED = True
        except IOError, e:
            result = QMessageBox.warning(None,
                self.trUtf8("Export binary attribute"),
                self.trUtf8("""Could not export binary data to file. Reason:
""" + str(e) + """\n\nPlease select another filename."""),
                self.trUtf8("&Cancel"),
                self.trUtf8("&OK"),
                None,
                1, -1)
        '''

###############################################################################

    # TODO: add logging for each error
    def reloadModel(self):
        """ 
        Refreshes the LDAP data from server, 
        """
        lumaConnection = LumaConnectionWrapper(self.smartObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bindSync()
        
        if not bindSuccess:
            message = "Could not bind to server. "
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
            message = "Could not refresh entry.<br><br>Reason: "
            return (False, message, exceptionObject)

###############################################################################

    # TODO: add logging for each error
    def saveModel(self):
        """ 
        Save changes to the current object.
        """
        
        lumaConnection = LumaConnectionWrapper(self.smartObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bindSync()
        
        if not bindSuccess:
            message = "Could not bind to server."
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
                message = "Could not add entry."
                return (False, message, exceptionObject)
        else:
            success, exceptionObject = lumaConnection.updateDataObject(self.smartObject)
            lumaConnection.unbind()
            if success:
                self.EDITED = False
                self.modelChangedSignal.emit(False)
                return (True, None, None)
            else:
                message = "Could not save entry."
                return (False, message, exceptionObject)

###############################################################################

    def addAttribute(self):
        """ 
        Add attributes to the current object.
        """
        
        pass
        '''
        dialog = AddAttributeWizard(self)
        dialog.setData(copy.deepcopy(self.smartObject))
        
        dialog.exec_loop()
        
        if dialog.result() == QDialog.Rejected:
            return
        
        attribute = str(dialog.attributeBox.currentText())
        showAll = dialog.enableAllBox.isChecked()
        if dialog.binaryBox.isOn():
            attributeList = Set([attribute + ";binary"])
        else:
            attributeList = Set([attribute])
        
        if showAll and not(attribute in dialog.possibleAttributes):
            objectClass = str(dialog.classBox.currentText())
            self.smartObject.addObjectClass(objectClass)
            
            serverSchema = ObjectClassAttributeInfo(self.smartObject.getServerMeta())
            mustAttributes = serverSchema.getAllMusts([objectClass])
            mustAttributes = mustAttributes.difference(Set(self.smartObject.getAttributeList()))
            attributeList = mustAttributes.union(Set([attribute]))
            
        for x in attributeList:
            self.smartObject.addAttributeValue(x, None)
        
        self.displayValues()
        '''

###############################################################################

    # TODO: add logging for each error, remove tab and node from parent
    def deleteObject(self):
        """
        Deletes the remote object that this model represents
        """
        
        lumaConnection = LumaConnectionWrapper(self.smartObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bindSync()
        
        if not bindSuccess:
            message = "Could not bind to server."
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
            message = "Could not delete entry."
            return (False, message, exceptionObject)

###############################################################################

    def editAttribute(self, attributeName, index, newValue):
        self.smartObject.setAttributeValue(attributeName, index, newValue)
        self.EDITED = True
        self.modelChangedSignal.emit(False)

###############################################################################

    def deleteAttribute(self, attributeName, index):
        #try:
        self.smartObject.deleteAttributeValue(attributeName, index)
        self.EDITED = True
        self.modelChangedSignal.emit(False)
        #except LdapDataException as e:
        #    print "*" * 30
        #    print e
        #    print "*" * 30

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
