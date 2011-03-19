# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTextBrowser, QTextOption, QPixmap, QSizePolicy, QTextOption, QLineEdit, QToolBar, QImage, QMessageBox, QVBoxLayout, QWidget, QToolButton, QIcon, QComboBox
from PyQt4.QtCore import QSize, SIGNAL
from base.backend.LumaConnection import LumaConnection
from base.backend.ServerList import ServerList
from plugins.browser_plugin.view.ClassicView import ClassicView
import ldap
import copy
import logging

# TODO Extract to model, rename to AdvancedObjectWidget
class AdvancedObjectWidget(QWidget):

    def __init__(self, smartObject, index, parent=None):
        QWidget.__init__(self, parent)
        

        # Standard pixmaps used by the widget
        self.deleteSmallPixmap = QPixmap(":/icons/edit-delete")
        self.reloadPixmap = QPixmap(":/icons/reload")
        self.savePixmap = QPixmap(":/icons/save")
        self.addPixmap = QPixmap(":/icons/single")

        self.index = index

        self.ldapDataObject = smartObject
        self.setLayout(QVBoxLayout(self))
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # create the widget containing the data
        self.objectWidget = QTextBrowser()
        self.objectWidget.setWordWrapMode(QTextOption.WrapAnywhere)
        self.objectWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.objectWidget.setMinimumSize(QSize(300, 100))
        self.objectWidget.setOpenLinks(False)
        self.layout().addWidget(self.objectWidget)
        self.connect(self.objectWidget, SIGNAL("anchorClicked(const QUrl&)"), self.modifierClicked)

        self.objectWidget.setHtml("")
                
        # boolean to indicate if the current ldap object has been modified
        self.EDITED = False
        
        # is the current object a leaf of the ldap tree?
        self.ISLEAF = False
        
        # do we create a completely new object?
        self.CREATE = False
        
        # ignore ServerMeta
        self.ignoreServerMetaError = True

        # views that will be displayed
        self.views = [ClassicView(False), ClassicView(True)]
        self.usedViews = []
        self.currentViewIndex = 0
        self.addViews()

        self.buildToolBar()

        self.initView(None)


###############################################################################


    def getSmartObject(self):
        return self.ldapDataObject
    
###############################################################################

    # TODO: fix
    def initView(self, data, create=False):
        #self.ldapDataObject = data

        if create:
            self.EDITED = True
            self.ISLEAF = False
            self.CREATE = True
        else:
            self.EDITED = False
            isLeave = False

            tmpObject = ServerList("/tmp")
            tmpObject.readServerList()
            serverMeta = tmpObject.getServerObject(self.ldapDataObject.getServerAlias())
        
            lumaConnection = LumaConnection(serverMeta)
        
            bindSuccess, exceptionObject = lumaConnection.bind()
            
            if not bindSuccess:
                if self.ignoreServerMetaError:
                    self.EDITED = False
                    self.ISLEAF = True
                    self.CREATE = False
                    self.displayValues()
                    self.enableToolButtons(True)
                else:
                    errorMsg = QString(self.trUtf8("Could not bind to server.<br><br>Reason: "))
                    errorMsg.append(str(exceptionObject))
                    QMessageBox.critical(self,
                                        self.trUtf8("Connection error"),
                                        errorMsg)
                return 
            
            success, resultList, exceptionObject = lumaConnection.search(self.ldapDataObject.dn, ldap.SCOPE_ONELEVEL, filter="(objectClass=*)", attrList=None, attrsonly=1, sizelimit=1)
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
                self. ISLEAF = False
                errorMsg = self.trUtf8("Could not check if object is a leaf in the ldap tree.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                QMessageBox.critical(self,
                                        self.trUtf8("Connection error"),
                                        errorMsg)
                
            self.CREATE = False
            
        self.displayValues()

        self.enableToolButtons(True)

###############################################################################

    def displayValues(self):
        self.objectWidget.setHtml("")

        # Something went wrong. We have no data object.
        # This might happen if we want to refresh an item and
        # it might be deleted already.
        if None == self.ldapDataObject:
            self.enableToolButtons(False)
            return
        
        self.usedViews[self.currentViewIndex].displayValues(self.objectWidget, self.ldapDataObject, self)

        self.enableToolButtons(True)

###############################################################################

    def modifierClicked(self, url):
        nameString = unicode(url.toString())
        tmpList = nameString.split("__")
        
        if tmpList[0] in self.ldapDataObject.getObjectClasses():
            self.deleteObjectClass(tmpList[0])
            self.EDITED = True
            self.displayValues()
        else:
            if not len(tmpList) == 3:
                return
            attributeName, index, operation = tmpList[0], int(tmpList[1]), tmpList[2]
            if operation == "edit":
                self.editAttribute(attributeName, index)
            elif operation == "delete":
                self.deleteAttribute(attributeName, index)
            elif operation == "export":
                self.exportAttribute(attributeName, index)

###############################################################################

    # TODO: not used yet
    def exportAttribute(self, attributeName, index):
        return
        """ Show the dialog for exporting binary attribute data.
        """
        
        value = self.ldapDataObject.getAttributeValue(attributeName, index)


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

###############################################################################

    # TODO: enable toolbuttons
    def editAttribute(self, attributeName, index):
        oldDN = self.ldapDataObject.getDN()
        
        if attributeName == 'RDN':
            self.ldapDataObject.setDN(self.baseDN)

        attributeValue = self.ldapDataObject.getAttributeValue(attributeName, index)
        newValue, ok = QtGui.QInputDialog.getText(self, 
                            self.trUtf8('Input dialog'), 
                            self.trUtf8('Attribute value:'), 
                            QLineEdit.Normal, 
                            attributeValue)
        newValue = unicode(newValue)
        if ok:
            if not newValue == None:
                self.ldapDataObject.setAttributeValue(attributeName, index, newValue)
                self.EDITED = True
                self.displayValues()
                self.enableToolButtons(True)
        else:
            if attributeName == 'RDN':
                self.ldapDataObject.setDN(oldDN)

###############################################################################

    def deleteAttribute(self, attributeName, index):
        self.ldapDataObject.deleteAttributeValue(attributeName, index)
        self.EDITED = True
        self.displayValues()

###############################################################################

    def deleteObjectClass(self, className):
        self.ldapDataObject.deleteObjectClass(className)
        self.EDITED = True
        self.displayValues()

###############################################################################

    def enableToolButtons(self, enable):
        if self.EDITED:
            self.saveButton.setEnabled(enable)
        else:
            self.saveButton.setEnabled(False)
            
        if self.ISLEAF:
            self.deleteObjectButton.setEnabled(enable)
        else:
            self.deleteObjectButton.setEnabled(False)
           
        if self.CREATE:
            self.reloadButton.setEnabled(False)
        else:
            self.reloadButton.setEnabled(enable)
            
        self.addAttributeButton.setEnabled(enable)


###############################################################################

    def aboutToChange(self):
        if not self.EDITED:
            return
            
        result = QMessageBox.warning(None,
            self.trUtf8("Save entry"),
            self.trUtf8("""Do you want to save the entry before continuing?"""),
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Cancel)
        
            
        if result == QMessageBox.Save:
            self.saveView()
            if self.EDITED:
                # Saving failed
                result = QMessageBox.critical(None,
                            self.trUtf8(""),
                            self.trUtf8("Saving failed, continue anyway?"),
                            QMessageBox.Ok | QMessageBox.Cancel,
                            QMessageBox.Cancel)
        return result

        
###############################################################################
    """
    def buildToolBar(self, parent):
        self.bar = QToolBar()
        reloadAction = self.bar.addAction("Reload",self.refreshView)
        saveAction = self.bar.addAction("Save",self.saveView)
        addAttributeAction = self.bar.addAction("Add attribute",self.addAttribute)
        deleteObjectAction = self.bar.addAction("Delete",self.deleteObject)

        self.reloadButton = self.bar.widgetForAction(reloadAction)
        self.saveButton = self.bar.widgetForAction(saveAction)
        self.addAttributeButton = self.bar.widgetForAction(reloadAction)
        self.deleteObjectButton = self.bar.widgetForAction(reloadAction)

        self.layout().insertWidget(0, self.bar)
        """

    def buildToolBar(self):
        self.toolBar = QToolBar()
        
        
        # Reload button
        self.reloadButton = QToolButton()
        self.reloadButton.setIcon(QIcon(self.reloadPixmap))
        self.reloadButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.reloadButton.setAutoRaise(True)
        #self.reloadButton.setBackgroundMode(self.backgroundMode())
        #QToolTip.add(self.reloadButton, self.trUtf8("Reload"))
        self.connect(self.reloadButton, SIGNAL("clicked()"), self.refreshView)
        self.toolBar.addWidget(self.reloadButton)
        
        
        # Save button
        self.saveButton = QToolButton()
        self.saveButton.setIcon(QIcon(self.savePixmap))
        self.saveButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.saveButton.setAutoRaise(True)
        #self.saveButton.setBackgroundMode(self.backgroundMode())
        #QToolTip.add(self.saveButton, self.trUtf8("Save"))
        self.connect(self.saveButton, SIGNAL("clicked()"), self.saveView)
        self.toolBar.addWidget(self.saveButton)
        
        self.toolBar.addSeparator()
        
        # Add attribute button
        self.addAttributeButton = QToolButton()
        self.addAttributeButton.setIcon(QIcon(self.addPixmap))
        self.addAttributeButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.addAttributeButton.setAutoRaise(True)
        #self.addAttributeButton.setBackgroundMode(self.backgroundMode())
        #QToolTip.add(self.addAttributeButton, self.trUtf8("Add attribute..."))
        self.connect(self.addAttributeButton, SIGNAL("clicked()"), self.addAttribute)
        self.toolBar.addWidget(self.addAttributeButton)
        
        # Delete button
        self.deleteObjectButton = QToolButton()
        self.deleteObjectButton.setIcon(QIcon(self.deleteSmallPixmap))
        self.deleteObjectButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.deleteObjectButton.setAutoRaise(True)
        #self.deleteObjectButton.setBackgroundMode(self.backgroundMode())
        #QToolTip.add(self.deleteObjectButton, self.trUtf8("Delete object"))
        self.connect(self.deleteObjectButton, SIGNAL("clicked()"), self.deleteObject)
        self.toolBar.addWidget(self.deleteObjectButton)

        self.comboBox = QComboBox()
        for view in self.usedViews:
            self.comboBox.addItem(view.getName())
        self.connect(self.comboBox, SIGNAL("currentIndexChanged(int)"), self.changeView)
        self.toolBar.addWidget(self.comboBox)
        
        self.enableToolButtons(False)
        self.layout().insertWidget(0, self.toolBar)

###############################################################################

    def addViews(self):
        for view in self.views:
            if view.supportsSmartObject(self.ldapDataObject):
                self.usedViews.append(view)

###############################################################################

    def changeView(self, index):
        if not index == self.currentViewIndex:
            self.currentViewIndex = index
            self.usedViews[self.currentViewIndex].displayValues(self.objectWidget, self.ldapDataObject, self)

###############################################################################

    # TODO: add logging for each error
    def refreshView(self):
        """ Refreshes the LDAP data from server and displays values.
        """
        if self.aboutToChange() == QMessageBox.Cancel:
            return
        
        lumaConnection = LumaConnection(self.ldapDataObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bind()
        
        if not bindSuccess:
            #dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            QMessageBox.critical(self, self.trUtf8("Bind error"), errorMsg)
            #dialog.setErrorMessage(errorMsg)
            #dialog.exec_loop()
            return 
        
        success, resultList, exceptionObject = lumaConnection.search(self.ldapDataObject.getDN(), ldap.SCOPE_BASE)
        lumaConnection.unbind()
        
        if success and (len(resultList) > 0):
            self.ldapDataObject = resultList[0]
            self.EDITED = False
            self.displayValues()
        else:
            self.ldapDataObject = None
            self.EDITED = False
            self.displayValues()
        
            #dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not refresh entry.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            QMessageBox.critical(self, "Bind error", errorMsg)
            #dialog.setErrorMessage(errorMsg)
            #dialog.exec_loop()

###############################################################################

    # TODO: add logging for each error
    def saveView(self):
        """ Save changes to the current object.
        """
        
        lumaConnection = LumaConnection(self.ldapDataObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bind()
        
        if not bindSuccess:
            #dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            QMessageBox.critical(self, self.trUtf8("Bind error"), errorMsg)
            #dialog.setErrorMessage(errorMsg)
            #dialog.exec_loop()
            return 
        
        if self.CREATE:
            success, exceptionObject = lumaConnection.addDataObject(self.ldapDataObject)
            lumaConnection.unbind()
            
            if success:
                self.CREATE = False
                self.EDITED = False
                self.displayValues()
            else:
                #dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not add entry.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                QMessageBox.critical(self, self.trUtf8("Bind error"), errorMsg)
                #dialog.setErrorMessage(errorMsg)
                #dialog.exec_loop()
        else:
            success, exceptionObject = lumaConnection.updateDataObject(self.ldapDataObject)
            lumaConnection.unbind()
            if success:
                self.EDITED = False
                self.displayValues()
            else:
                #dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not save entry.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                QMessageBox.critical(self, self.trUtf8("Bind error"), errorMsg)
                #dialog.setErrorMessage(errorMsg)
                #dialog.exec_loop()

###############################################################################

    def addAttribute(self):
        """ Add attributes to the current object.
        """
        
        QMessageBox.critical(self, "?", "I dont exist, yet")
        """
        dialog = AddAttributeWizard(self)
        dialog.setData(copy.deepcopy(self.ldapDataObject))
        
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
            self.ldapDataObject.addObjectClass(objectClass)
            
            serverSchema = ObjectClassAttributeInfo(self.ldapDataObject.getServerMeta())
            mustAttributes = serverSchema.getAllMusts([objectClass])
            mustAttributes = mustAttributes.difference(Set(self.ldapDataObject.getAttributeList()))
            attributeList = mustAttributes.union(Set([attribute]))
            
        for x in attributeList:
            self.ldapDataObject.addAttributeValue(x, None)
        
        self.displayValues()
        """

###############################################################################

    # TODO: add logging for each error, remove tab and node from parent
    def deleteObject(self):
        
        buttonClicked = QMessageBox.critical(self, 
                self.trUtf8("Delete object"),
                self.trUtf8("Do your really want to delete the object?"),
                QMessageBox.Yes,
                QMessageBox.No)
        
        #tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
        #tmpDialog.exec_loop()
            
        if not (buttonClicked == QMessageBox.Yes):
            return
        
        lumaConnection = LumaConnection(self.ldapDataObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bind()
        
        if not bindSuccess:
            #dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            QMessageBox.critical(self, self.trUtf8("Bind error"), errorMsg)
            #dialog.setErrorMessage(errorMsg)
            #dialog.exec_loop()
            return
        
        success, exceptionObject = lumaConnection.delete(self.ldapDataObject.getDN())
        lumaConnection.unbind()
        
        if success:
            serverName = self.ldapDataObject.getServerAlias()
            dn = self.ldapDataObject.getPrettyParentDN()
            #self.emit(PYSIGNAL("REOPEN_PARENT"), (serverName, dn,))
            self.clearView()
            self.enableToolButtons(False)
            self.index.model().reloadItem(self.index.parent())
            self.deleteLater()
        else:
            #dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not delete entry.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            QMessageBox.critical(self, self.trUtf8("Delete error"), errorMsg)
            #dialog.setErrorMessage(errorMsg)
            #dialog.exec_loop()

###############################################################################

    def clearView(self):
        self.objectWidget.setText("")
