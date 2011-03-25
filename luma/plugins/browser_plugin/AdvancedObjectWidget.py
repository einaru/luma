# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTextBrowser, QTextOption, QPixmap, QSizePolicy, QTextOption, QLineEdit, QToolBar, QImage, QMessageBox, QVBoxLayout, QWidget, QToolButton, QIcon, QComboBox, QInputDialog
from PyQt4.QtCore import QSize, SIGNAL
from base.backend.LumaConnection import LumaConnection
from base.backend.ServerList import ServerList
from plugins.browser_plugin.model.EntryModel import EntryModel
from plugins.browser_plugin.HtmlParser import HtmlParser
from plugins.browser_plugin.TemplateFactory import TemplateFactory
import ldap
import copy
import logging
import os

class AdvancedObjectWidget(QWidget):

    def __init__(self, smartObject, index, currentTemplate=None, parent=None):
        QWidget.__init__(self, parent)
        
        self.entryModel = EntryModel(smartObject, self)
        self.entryModel.modelChangedSignal.connect(self.displayValues)
        self.initModel()

        # Standard pixmaps used by the widget
        self.deleteSmallPixmap = QPixmap(":/icons/edit-delete")
        self.reloadPixmap = QPixmap(":/icons/reload")
        self.savePixmap = QPixmap(":/icons/save")
        self.addPixmap = QPixmap(":/icons/single")

        self.index = index

        self.setLayout(QVBoxLayout(self))
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # create the widget containing the data
        self.objectWidget = QTextBrowser()
        self.objectWidget.setOpenLinks(False)
        self.layout().addWidget(self.objectWidget)
        self.connect(self.objectWidget, SIGNAL("anchorClicked(const QUrl&)"), self.anchorClicked)

        self.currentDocument = ''

        
        self.currentTemplate = currentTemplate
        self.usedTemplates = []
        #TODO move to BrowserView
        self.templateFactory = TemplateFactory(os.path.join("plugins", "browser_plugin", "templates"))

        self.htmlParser = HtmlParser(smartObject)
        
        self.loadTemplates()
        self.buildToolBar()
        self.displayValues()
    

###############################################################################

    def getSmartObject(self):
        return self.entryModel.getSmartObject()

###############################################################################
    
    def initModel(self):
        success, exceptionMsg, exceptionObject = self.entryModel.initModel()
        if not success:
            errorMsg = self.trUtf8("%s <br><br>Reason: %s" % (exceptionMsg, str(exceptionObject)))
            QMessageBox.critical(self,
                                self.trUtf8(""),
                                errorMsg)

###############################################################################
    
    def loadTemplates(self):
        objectClasses = self.getSmartObject().getObjectClasses()
        for objectClass, fileName in self.templateFactory.getTemplateList():
            if objectClass == '' or objectClass in objectClasses:
                self.usedTemplates.append(fileName)
        if self.currentTemplate not in self.usedTemplates:
            self.currentTemplate = self.usedTemplates[0]
        
    
###############################################################################

    def displayValues(self):
        # Something went wrong. We have no data object.
        # This might happen if we want to refresh an item and
        # it might be deleted already.
        if None == self.entryModel.getSmartObject():
            self.enableToolButtons(False)
            return
        
        if self.currentTemplate == None:
            return
        htmlTemplate = self.templateFactory.getTemplateFile(self.currentTemplate)
        self.currentDocument = self.htmlParser.parseHtml(htmlTemplate)
        self.objectWidget.setHtml(self.currentDocument)
        

        self.enableToolButtons(True)

###############################################################################

    def enableToolButtons(self, enable):
        if self.entryModel.EDITED:
            self.saveButton.setEnabled(enable)
        else:
            self.saveButton.setEnabled(False)
            
        if self.entryModel.ISLEAF:
            self.deleteObjectButton.setEnabled(enable)
        else:
            self.deleteObjectButton.setEnabled(False)
           
        if self.entryModel.CREATE:
            self.reloadButton.setEnabled(False)
        else:
            self.reloadButton.setEnabled(enable)
            
        self.addAttributeButton.setEnabled(enable)


        
###############################################################################

    def buildToolBar(self):
        self.toolBar = QToolBar()
        self.toolBar.layout().setContentsMargins(0, 0, 0, 0)
        
        # Reload button
        self.reloadButton = QToolButton(self.toolBar)
        self.reloadButton.setIcon(QIcon(self.reloadPixmap))
        self.reloadButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.reloadButton.setAutoRaise(True)
        self.reloadButton.setBackgroundRole(self.backgroundRole())
        self.reloadButton.setToolTip(self.trUtf8("Reload"))
        self.connect(self.reloadButton, SIGNAL("clicked()"), self.refreshView)
        self.toolBar.addWidget(self.reloadButton)
        
        
        # Save button
        self.saveButton = QToolButton(self.toolBar)
        self.saveButton.setIcon(QIcon(self.savePixmap))
        self.saveButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.saveButton.setAutoRaise(True)
        self.saveButton.setBackgroundRole(self.backgroundRole())
        self.saveButton.setToolTip(self.trUtf8("Save"))
        self.connect(self.saveButton, SIGNAL("clicked()"), self.saveObject)
        self.toolBar.addWidget(self.saveButton)
        
        self.toolBar.addSeparator()
        
        # Add attribute button
        self.addAttributeButton = QToolButton(self.toolBar)
        self.addAttributeButton.setIcon(QIcon(self.addPixmap))
        self.addAttributeButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.addAttributeButton.setAutoRaise(True)
        self.addAttributeButton.setBackgroundRole(self.backgroundRole())
        self.addAttributeButton.setToolTip(self.trUtf8("Add attribute"))
        self.connect(self.addAttributeButton, SIGNAL("clicked()"), self.addAttribute)
        self.toolBar.addWidget(self.addAttributeButton)
        
        # Delete button
        self.deleteObjectButton = QToolButton(self.toolBar)
        self.deleteObjectButton.setIcon(QIcon(self.deleteSmallPixmap))
        self.deleteObjectButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.deleteObjectButton.setAutoRaise(True)
        self.deleteObjectButton.setBackgroundRole(self.backgroundRole())
        self.deleteObjectButton.setToolTip(self.trUtf8("Delete object"))
        self.connect(self.deleteObjectButton, SIGNAL("clicked()"), self.deleteObject)
        self.toolBar.addWidget(self.deleteObjectButton)

        self.comboBox = QComboBox()
        for template in self.usedTemplates:
            self.comboBox.addItem(template)
        self.comboBox.setToolTip(self.trUtf8("Switch between views"))
        self.connect(self.comboBox, SIGNAL("currentIndexChanged(int)"), self.changeView)
        self.toolBar.addWidget(self.comboBox)
        
        self.enableToolButtons(False)
        self.layout().insertWidget(0, self.toolBar)

###############################################################################

    def changeView(self, index):
        """
        change between different views
        """
        self.currentTemplate = self.usedTemplates[index]
        self.displayValues()

###############################################################################

    def aboutToChange(self):
        """
        Asks the user whether changes should be saved
        returns True if changes were saved, or discarded
        """
        if not self.entryModel.EDITED:
            return True
            
        result = QMessageBox.warning(self,
            self.trUtf8("Save entry"),
            self.trUtf8("""Do you want to save the entry before continuing?"""),
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Cancel)
        
            
        # TODO add exception message
        if result == QMessageBox.Save:
            if not self.saveObject():
                # Saving failed
                result = QMessageBox.question(None,
                            self.trUtf8(""),
                            self.trUtf8("Saving failed, continue anyway?"),
                            QMessageBox.Ok | QMessageBox.Cancel,
                            QMessageBox.Cancel)
        return not(result == QMessageBox.Cancel)

###############################################################################

    # TODO: add logging for each error
    def refreshView(self):
        """ Refreshes the LDAP data from server and displays values.
        """
        if self.aboutToChange():
            success, exceptionMsg, exceptionObject = self.entryModel.reloadModel()
            if not success:
                errorMsg = self.trUtf8("%s<br><br>Reason: %s" % (exceptionMsg, str(exceptionObject)))
                QMessageBox.critical(self, self.trUtf8(""), errorMsg)
            #else:
            #    self.displayValues()

###############################################################################

    # TODO: add logging for each error
    def saveObject(self):
        success, exceptionMsg, exceptionObject = self.entryModel.saveModel()
        if not success:
            # Saving failed
            errorMsg = self.trUtf8("%s<br><br>Reason: %s" % (exceptionMsg, str(exceptionObject)))
            QMessageBox.critical(self, self.trUtf8(""), errorMsg)
            return False
        else:
            return True

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
                            self.trUtf8("Do you really want to delete the object?"),
                            QMessageBox.Yes,
                            QMessageBox.No)
        if not (buttonClicked == QMessageBox.Yes):
            return
        # If we have an index, use it tell the item to delete itself
        # so that the view is updated
        if self.index.isValid():
            row = self.index.row()
            column = self.index.column()
            # QPersistenIndex doesn't have internalPointer()
            # so we aquire a QModelIndex which does
            item = self.index.parent().child(row,column).internalPointer()
            success, message, exceptionObject = item.delete()
            if success:
                self.index.model().layoutChanged.emit()
                self.enableToolButtons(False)
                self.deleteLater()
            else:
                errorMsg = self.trUtf8("%s<br><br>Reason: %s" % (message, str(exceptionObject)))
                QMessageBox.critical(self, self.trUtf8(""), errorMsg)
        # if not, we just delete it ourselves since there's not view on the object
        else:
            success, message, exceptionObject = self.entryModel.deleteObject()
            if success:
                self.enableToolButtons(False)
                self.deleteLater()
            else:
                errorMsg = self.trUtf8("%s<br><br>Reason: %s" % (message, str(exceptionObject)))
                QMessageBox.critical(self, self.trUtf8(""), errorMsg)

###############################################################################

    def anchorClicked(self, url):
        nameString = unicode(url.toString())
        tmpList = nameString.split("__")
        
        if tmpList[0] in self.entryModel.getSmartObject().getObjectClasses():
            self.entryModel.deleteObjectClass(tmpList[0])
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

    def editAttribute(self, attributeName, index):
        smartObject = self.entryModel.getSmartObject()
        oldDN = smartObject.getDN()
        
        if attributeName == 'RDN':
            # TODO correct this, used on creation?
            smartObject.setDN(self.baseDN)

        attributeValue = smartObject.getAttributeValue(attributeName, index)
        newValue, ok = QInputDialog.getText(self.objectWidget, 
                            self.trUtf8('Input dialog'), 
                            self.trUtf8('Attribute value:'), 
                            QLineEdit.Normal, 
                            attributeValue)
        if ok:
            newValue = unicode(newValue)
            if not newValue == None:
                self.entryModel.editAttribute(attributeName, index, newValue)
        else:
            if attributeName == 'RDN':
                # TODO correct this
                smartObject.setDN(oldDN)

###############################################################################

    def deleteAttribute(self, attributeName, index):
        self.entryModel.deleteAttribute(attributeName, index)

###############################################################################

    # TODO: not used yet
    def exportAttribute(self, attributeName, index):
        return
        """ Show the dialog for exporting binary attribute data.
        """
        '''
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
        '''
