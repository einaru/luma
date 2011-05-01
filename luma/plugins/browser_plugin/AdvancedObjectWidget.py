# -*- coding: utf-8 -*-

import ldap
import copy
import logging
import os

from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtCore import QSize, SIGNAL, QString
from PyQt4.QtGui import (QTextBrowser, QTextOption, QPixmap, QSizePolicy,
                         QTextOption, QLineEdit, QToolBar, QImage, 
                         QMessageBox, QVBoxLayout, QWidget, QToolButton, 
                         QIcon, QComboBox, QInputDialog, QDialog, QFileDialog)

from base.backend.LumaConnection import LumaConnection
from base.backend.ServerList import ServerList
from base.backend.SmartDataObject import SmartDataObject
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.util.IconTheme import pixmapFromThemeIcon
from base.util.Paths import getLumaRoot

from .model.EntryModel import EntryModel
from .HtmlParser import HtmlParser
from .TemplateFactory import TemplateFactory
from .editors.EditorFactory import getEditorWidget
from .AddAttributeWizard import AddAttributeWizard

class AdvancedObjectWidget(QWidget):

    def __init__(self, smartObject, index, currentTemplate="classic.html", create=False, parent=None):
        QWidget.__init__(self, parent)
        
        w = 24
        h = 24
        self.initModel(smartObject, create)

        # Standard pixmaps used by the widget
        self.reloadPixmap = pixmapFromThemeIcon("view-refresh", ":/icons/reload", w, h)
        self.savePixmap = pixmapFromThemeIcon("document-save", ":/icons/save",w, h)
        self.addPixmap = pixmapFromThemeIcon("list-add", ":/icons/single", w, h)
        self.deleteSmallPixmap = pixmapFromThemeIcon("list-remove", ":/icons/edit-delete", w, h)

        self.index = index

        self.setLayout(QVBoxLayout(self))
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # create the widget containing the data
        self.objectWidget = QTextBrowser()
        self.objectWidget.setOpenLinks(False)
        self.objectWidget.setWordWrapMode(QTextOption.WrapAnywhere)
        self.layout().addWidget(self.objectWidget)
        self.connect(self.objectWidget, SIGNAL("anchorClicked(const QUrl&)"), self.anchorClicked)

        self.currentDocument = ''
        self.addingToComboBox = False
        
        # create the combobox containing the different views
        self.comboBox = QComboBox()
        self.currentTemplate = currentTemplate
        self.usedTemplates = []
        # FIXME: Need a more robust way for locating the path used in
        #        the TemplateFactory for locating the template view
        #        files
        # FIXED: with base.util.Paths.getLumaRoot this should work.
        #        Probably needs some validation testing on platforms
        #        other than Linux
        #self.templateFactory = TemplateFactory(os.path.join("plugins", "browser_plugin", "templates"))
        self.templateFactory = TemplateFactory(unicode(os.path.join(getLumaRoot(), 'plugins', 'browser_plugin', 'templates')))

        self.htmlParser = HtmlParser(self.entryModel, self.objectWidget)
        
        self.buildToolBar()
        self.displayValues()

###############################################################################
    @staticmethod
    def smartObjectCopy(smartObject):
        return SmartDataObject(copy.deepcopy([smartObject.dn, smartObject.data]), copy.deepcopy(smartObject.serverMeta))

###############################################################################

    def getSmartObject(self):
        return self.entryModel.getSmartObject()

###############################################################################
    
    def initModel(self, smartObject, create=False):
        if not create:
            # use a copy of the smartObject
            smartObject = AdvancedObjectWidget.smartObjectCopy(smartObject)
        self.entryModel = EntryModel(smartObject, self)
        self.entryModel.modelChangedSignal.connect(self.displayValues)
        success, exceptionMsg, exceptionObject = self.entryModel.initModel(create)
        if not success:
            errorMsg = self.trUtf8("%s <br><br>Reason: %s" % (exceptionMsg, str(exceptionObject)))
            QMessageBox.critical(self,
                                self.trUtf8(""),
                                errorMsg)

###############################################################################
    
    def loadTemplates(self):
        self.usedTemplates = []
        objectClasses = self.getSmartObject().getObjectClasses()
        newIndex = -1
        i = 0
        #TODO add sorting and default template?
        for objectClass, fileName in self.templateFactory.getTemplateList():
            if objectClass == '' or objectClass in objectClasses:
                if fileName == self.currentTemplate:
                    newIndex = i
                self.usedTemplates.append(fileName)
                i += 1
        if newIndex == -1:
            newIndex = 0
        self.currentTemplate = self.usedTemplates[newIndex]
        #TODO do this properly, signals ignored
        self.addingToComboBox = True
        self.comboBox.clear()
        self.comboBox.addItems(self.usedTemplates)
        self.comboBox.setCurrentIndex(newIndex)
        self.addingToComboBox = False
        
    
###############################################################################

    def displayValues(self):
        # Something went wrong. We have no data object.
        # This might happen if we want to refresh an item and
        # it might be deleted already.
        if None == self.entryModel.getSmartObject():
            self.enableToolButtons(False)
            return
        
        self.loadTemplates()
        if self.currentTemplate == None:
            selt.objectWidget.setHtml("No templates available")
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
        if index == -1 or self.addingToComboBox:
            return
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
            else:
                self.displayValues()

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
            # update the smartObject in the tree
            if self.entryModel.CREATE:
                pass
            elif self.index.isValid():
                row = self.index.row()
                column = self.index.column()
                # QPersistenIndex doesn't have internalPointer()
                # so we aquire a QModelIndex which does
                index = self.index.sibling(row,column)
                index.internalPointer().itemData = self.getSmartObject()
            return True

###############################################################################

    def addAttribute(self):
        """ Add attributes to the current object.
        """
        
        dialog = AddAttributeWizard(self)
        #TODO model
        dialog.setData(self.smartObjectCopy(self.entryModel.smartObject))
        
        dialog.exec_()
        
        if dialog.result() == QDialog.Rejected:
            return
        
        attribute = str(dialog.attributeBox.currentText())
        showAll = dialog.enableAllBox.isChecked()
        if dialog.binaryBox.isChecked():
            attributeList = set([attribute + ";binary"])
        else:
            attributeList = set([attribute])
        
        if showAll and not(attribute.lower() in dialog.possibleAttributes):
            objectClass = str(dialog.classBox.currentItem().text())
            #TODO model
            self.entryModel.smartObject.addObjectClass(objectClass)
            
            serverSchema = ObjectClassAttributeInfo(self.entryModel.smartObject.getServerMeta())
            mustAttributes = serverSchema.getAllMusts([objectClass])
            mustAttributes = mustAttributes.difference(set(self.entryModel.smartObject.getAttributeList()))
            attributeList = mustAttributes.union(set([attribute]))
            
        for x in attributeList:
            #TODO model
            self.entryModel.smartObject.addAttributeValue(x, None)
        
        self.displayValues()
        

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
            index = self.index.sibling(row,column)
            success, message = index.model().deleteItem(index)
            if success:
                self.enableToolButtons(False)
                self.deleteLater()
            else:
                errorMsg = self.trUtf8("%s<br><br>Reason: %s" % (message))#, str(exceptionObject))) # We ain't got no exceptionObject here ?
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
        
        addAttribute = False
        if attributeName == 'RDN':
            # TODO correct this, used on creation?
            oldValue = oldDN
            #smartObject.setDN(self.baseDN)
        else:
            if smartObject.hasAttribute(attributeName):
                addValue = False
                oldValue = smartObject.getAttributeValue(attributeName, index)
                if oldValue == None:
                    oldValue = ''
            else:
                addValue = True
                oldValue = ''
        dialog = getEditorWidget(self, smartObject, attributeName, index)
        dialog.exec_()

        if dialog.result() == QDialog.Accepted:
            # TODO check attribute types
            newValue = dialog.getValue()
            if not (newValue == None):
                if attributeName == 'RDN':
                    self.entryModel.editRDN(newValue)
                else:
                    if addValue:
                        self.entryModel.addAttributeValue(attributeName, [newValue])
                    else:
                        self.entryModel.editAttribute(attributeName, index, newValue)
        #else:
        #    if attributeName == 'RDN':
        #        # TODO correct this
        #        smartObject.setDN(oldDN)

###############################################################################

    def deleteAttribute(self, attributeName, index):
        self.entryModel.deleteAttribute(attributeName, index)

###############################################################################

    def exportAttribute(self, attributeName, index):
        """ Show the dialog for exporting binary attribute data.
        """
        value = self.getSmartObject().getAttributeValue(attributeName, index)


        fileName = unicode(QFileDialog.getSaveFileName(\
                            self,
                            self.trUtf8("Export binary attribute to file"),
                            QString(""),
                            "All files (*)",
                            None))

        if unicode(fileName) == "":
            return
            
        try:
            fileHandler = open(fileName, "w")
            fileHandler.write(value)
            fileHandler.close()
            SAVED = True
        except IOError, e:
            result = QMessageBox.warning(\
                    self,
                    self.trUtf8("Export binary attribute"),
                    self.trUtf8("""Could not export binary data to file. Reason:\n"""
                        + str(e) + """\n\nPlease select another filename."""),
                    QMessageBox.Cancel | QMessageBox.Ok,
                    QMessageBox.Cancel)

