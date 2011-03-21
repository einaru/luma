# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTextBrowser, QTextOption, QPixmap, QSizePolicy, QTextOption, QLineEdit, QToolBar, QImage, QMessageBox, QVBoxLayout, QWidget, QToolButton, QIcon, QComboBox, QStackedWidget
from PyQt4.QtCore import QSize, SIGNAL
from base.backend.LumaConnection import LumaConnection
from base.backend.ServerList import ServerList
from plugins.browser_plugin.model.EntryModel import EntryModel
from plugins.browser_plugin.view.ClassicView import ClassicView
from plugins.browser_plugin.view.HtmlView import HtmlView
import ldap
import copy
import logging

class AdvancedObjectWidget(QWidget):

    def __init__(self, smartObject, index, parent=None):
        QWidget.__init__(self, parent)
        
        self.entryModel = EntryModel(smartObject, self)
        self.entryModel.modelChangedSignal.connect(self.modelChanged)
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
        #self.layout().addWidget(self.objectWidget)
        #self.connect(self.objectWidget, SIGNAL("anchorClicked(const QUrl&)"), self.anchorClicked)

        
        # ignore ServerMeta
        self.ignoreServerMetaError = True


        # views that will be displayed
        self.usedViews = []
        self.usedViews.extend(ClassicView.supportedViews(self.entryModel))
        self.usedViews.extend(HtmlView.supportedViews(self.entryModel))
        HtmlView.supportedViews(self.entryModel)

        self.currentViewIndex = 0
        self.buildToolBar()
        self.stackedWidget = QStackedWidget(self)
        self.layout().addWidget(self.stackedWidget)
        # TODO always create all widgets?
        for view in self.usedViews:
            view.initWidget(self.stackedWidget)
            self.stackedWidget.addWidget(view.getWidget())


        self.displayValues()

###############################################################################

    def getSmartObject(self):
        return self.entryModel.getSmartObject()

###############################################################################

    def modelChanged(self):
        """
        called when the model is changed
        """
        self.displayValues()

###############################################################################
    
    def initModel(self):
        success, exceptionMsg, exceptionObject = self.entryModel.initModel()
        if not success:
            errorMsg = self.trUtf8("%s <br><br>Reason: %s" % (exceptionMsg, str(exceptionObject)))
            QMessageBox.critical(self,
                                self.trUtf8(""),
                                errorMsg)

    
###############################################################################

    def getCurrentView(self):
        return self.usedViews[self.currentViewIndex]

###############################################################################

    def displayValues(self):
        # Something went wrong. We have no data object.
        # This might happen if we want to refresh an item and
        # it might be deleted already.
        if None == self.entryModel.getSmartObject():
            self.enableToolButtons(False)
            return
        
        currentView = self.getCurrentView()
        currentView.refreshView()

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
        for view in self.usedViews:
            self.comboBox.addItem(view.getName())
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
        self.currentViewIndex = index
        self.stackedWidget.setCurrentIndex(index)
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

        success, exceptionMsg, exceptionObject = self.entryModel.deleteObject()
        if not success:
            errorMsg = self.trUtf8("%s<br><br>Reason: %s" % (exceptionMsg, str(exceptionObject)))
            QMessageBox.critical(self, self.trUtf8(""), errorMsg)
        else:
            #self.emit(PYSIGNAR("REOPEN_PARENT"), (serverName, dn,))
            #self.clearView()
            self.enableToolButtons(False)
            self.index.model().reloadItem(self.index.parent())
            self.deleteLater()

