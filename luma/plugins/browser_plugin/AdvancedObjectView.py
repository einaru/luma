# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTextBrowser, QTextOption, QPixmap, QSizePolicy, QTextOption, QLineEdit, QToolBar, QImage, QMessageBox, QVBoxLayout, QWidget
from PyQt4.QtCore import QSize, SIGNAL
from base.backend.LumaConnection import LumaConnection
import ldap
import copy
import logging

class AdvancedObjectView(QWidget):

    def __init__(self, smartObject, index, parent=None):
        QWidget.__init__(self, parent)
        
        self.index = index

        self.ldapDataObject = smartObject
        self.setLayout(QVBoxLayout(self))

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.objectWidget = QTextBrowser()
        self.objectWidget.setWordWrapMode(QTextOption.WrapAnywhere)
        self.objectWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.objectWidget.setMinimumSize(QSize(300, 100))
        self.objectWidget.setOpenLinks(False)
        self.layout().addWidget(self.objectWidget)
        
        self.connect(self.objectWidget, SIGNAL("anchorClicked(const QUrl&)"), self.modifierClicked)

        self.setHtml("")
                
        # boolean to indicate if the current ldap object has been modified
        self.EDITED = False
        
        # is the current object a leaf of the ldap tree?
        self.ISLEAF = False
        
        # do we create a completely new object?
        self.CREATE = False

        self.readServerSchema = False
        
        self.buildToolBar(None)

        self.initView(None)
        

###############################################################################

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
        self.enableToolButtons

        self.displayValues()
        self.enableToolButtons(True)

###############################################################################

    # TODO: remove
    def setHtml(self, text):
        self.objectWidget.setHtml(text)

###############################################################################

    def displayValues(self):
        self.setHtml("")

        # Something went wrong. We have no data object.
        # This might happen if we want to refresh an item and
        # it might be deleted already.
        if None == self.ldapDataObject:
            self.enableToolButtons(False)
            return

        self.ldapDataObject.checkIntegrity()

        if not self.ldapDataObject.isValid:
            # TODO: debug
            pass
        self.ldapDataObject.isValid = True
        if self.ldapDataObject.isValid:
            tmpList = []
            tmpList.append("<html>")
            tmpList.append("""<body>""")
            tmpList.append("""<table border="0" cellpadding="1" cellspacing="0" width="100%">""")
            tmpList.append("""<tr>""")
            tmpList.append("""<td bgcolor="#B2CAE7" width="40%"><font size="+1"> <b>Distinguished Name:</b> </font></td>""")
            tmpList.append("""<td bgcolor="#B2CAE7" width="60%"><font size="+1"><b>""" + self.ldapDataObject.getPrettyDN() + """</b></font></td>""")
        
            if self.CREATE:
                tmpList.append("""<td width=5%><a href=RDN__0__edit><img source=":/icons/edit"></a></td>""")

            tmpList.append("""</tr>""")
        
            tmpList.append("</table>")
            tmpList.append("<br>")
        
            tmpList.append(self.createClassString())
        
            tmpList.append("<br>")
        
            tmpList.append(self.createAttributeString())
        
            tmpList.append("</body>")
            tmpList.append("</html>")
        
            #self.currentDocument = ("".join(tmpList))
        
            self.setHtml("".join(tmpList))
        else:
            tmpList = []
            tmpList.append("<html>")
            tmpList.append("""<body>""")
            tmpList.append("""<table border="0" cellpadding="1" cellspacing="0" width="100%">""")
            tmpList.append("""<tr>""")
            tmpList.append("""<td <font size="+1"> """ + unicode(self.trUtf8("<b>Could not display ldap entry. Reason:</b>")) + """</font></td>""")
            tmpList.append("""</tr>""")
            tmpList.append("""<tr>""")
            tmpList.append("""</tr>""")
            for x in self.ldapDataObject.checkErrorMessageList:
                tmpList.append("""<tr>""")
                tmpList.append("""<td>""" + x + """</td>""")
                tmpList.append("""</tr>""")

            tmpList.append("</body>")
            tmpList.append("</html>")

            self.setHtml("".join(tmpList))

###############################################################################

    def createClassString(self):
        tmpList = []
        
        tmpList.append("""<table border="0" cellpadding="1" cellspacing="0" width="100%">""")
        tmpList.append("""<tr>""")
        tmpList.append("""<td bgcolor="#C4DFFF" align="center"><b>ObjectClasses</b></td>""")
        tmpList.append("""</tr>""")
        
        rdn = self.ldapDataObject.getPrettyRDN()
        rdnClass = rdn.split("=")[0]
        
        for x in self.ldapDataObject.getObjectClasses():
            classString = x[:]
            
            if self.readServerSchema:
                if self.ldapDataObject.isObjectclassStructural(x):
                    classString = "<b>" + classString + "</b>"
            tmpList.append("""<tr>""")
            tmpList.append("""<td colspan=2 bgcolor="#E5E5E5" width="100%">""")
            tmpList.append(classString)
            
            allowDelete = True
            if self.readServerSchema:
                if self.ldapDataObject.isObjectclassStructural(x):
                    classList = self.ldapDataObject.getObjectClasses()
                    classList.remove(x)
                    if len(self.ldapDataObject.getObjectClassChain(x, classList)) == 0:
                        allowDelete = False
                       
                if rdnClass in self.ldapDataObject.getAttributeListForObjectClass(x):
                    allowDelete = False
                    
                    # Now we check if another objectclass provides the rdn attribute
                    classList = self.ldapDataObject.getObjectClasses()
                    classList.remove(x)
                    for y in classList:
                        if rdnClass in self.ldapDataObject.getAttributeListForObjectClass(y):
                            allowDelete = True
                            break
            
            if allowDelete and (not (x == 'top')):
                deleteName = x + "__delete\""
                tmpList.append(""" <a href=\"""" + deleteName + """><img source=":/icons/deleteEntry"></a>""")
            
            
            
            tmpList.append("""</td></tr>""")
        
        tmpList.append("""</table>""")
        
        return "".join(tmpList)

###############################################################################

    def createAttributeString(self):
        tmpList = []
        
        tmpList.append("""<table border="0" cellpadding="0" cellspacing="0" width="100%">""")
        tmpList.append("""<tr>""")
        tmpList.append("""<td colspan=2 bgcolor="#C4DFFF" align="center"><b>Attributes</b></td>""")
        tmpList.append("""</tr>""")
        tmpList.append("""</table>""")
        
        attributeList = self.ldapDataObject.getAttributeList()
        attributeList.sort()
        
        tmpList.append("""<table border="0" cellpadding="1" cellspacing="1" width="100%">""")
        
        for x in attributeList:
            #environment.updateUI()
            #attributeIsBinary = self.ldapDataObject.isAttributeBinary(x)
            #attributeIsImage = self.ldapDataObject.isAttributeImage(x)
            #attributeIsPassword = self.ldapDataObject.isAttributePassword(x)
            #attributeIsSingle = self.ldapDataObject.isAttributeSingle(x)
            #attributeIsMust = self.ldapDataObject.isAttributeMust(x)

            attributeIsBinary = False
            attributeIsImage = False
            attributeIsPassword = False
            attributeIsSingle = False
            attributeIsMust = False
            
            attributeBinaryExport = False
            #if attributeIsBinary:
            #    if attributeIsImage:
            #        attributeBinaryExport = True
            #    elif not attributeIsPassword:
            #        attributeBinaryExport = True
                    
            valueList = self.ldapDataObject.getAttributeValueList(x)
            
            if None == valueList:
                continue
            
            if not (len(valueList) > 0):
                continue
                
            
            allowDelete = False
            if attributeIsMust:
                if len(valueList) > 1:
                    allowDelete = True
            else:
                allowDelete = True
            
            tmpList.append("""<tr>""")
            
            attributeString = copy.copy(x)
            
            #if self.ldapDataObject.isAttributeMust(x, self.ldapDataObject.getObjectClasses()):
            #    attributeString = "<b>" + attributeString + "</b>"
            
            if valueList[0] == None:
                attributeString = """<font color="red">""" + attributeString + """</font>"""
                
            tmpList.append("""<td bgcolor="#E5E5E5" width="35%">""" + attributeString + """</td>""")
            
            attributeIndex = 0
            univAttributeName = x + "__" + unicode(attributeIndex)

            attributeModify = True
            #if not (valueList[0] == None):
            #    attributeModify = not self.ldapDataObject.isAttributeValueRDN(x, valueList[0])
            
            if (valueList[0] == None):
                tmpList.append("""<td bgcolor="#E5E5E5" width="60%"><font color="#ff0000">""" + 
                    unicode(self.trUtf8("Value not set.")) + """</font></td>""")
                    
                tmpList.append(self.getAttributeModifierString(univAttributeName, 
                    allowDelete, False, attributeModify))
            else:
                tmpList.append(self.getAttributeValueString(univAttributeName, valueList[0], 
                    attributeIsBinary, attributeIsImage, attributeIsPassword))
            
                tmpList.append(self.getAttributeModifierString(univAttributeName, 
                    allowDelete, attributeBinaryExport, attributeModify))
                
            tmpList.append("""</tr>""")
            
            
            for y in valueList[1:]:
                #environment.updateUI()
                attributeIndex += 1
                univAttributeName = x + "__" + unicode(attributeIndex)
                
                attributeModify = True
                #if not (y == None):
                #    attributeModify = not self.ldapDataObject.isAttributeValueRDN(x, y)
                
                tmpList.append("""<tr><td width="35%"></td>""")
                
                if y == None:
                    tmpList.append("""<td bgcolor="#E5E5E5" width="55%"><font color="#ff0000">""" +
                        unicode(self.trUtf8("Value not set.")) + """</font></td>""")
                        
                    tmpList.append(self.getAttributeModifierString(univAttributeName, 
                        allowDelete, False, attributeModify))
                else:
                    tmpList.append(self.getAttributeValueString(univAttributeName, y, 
                        attributeIsBinary, attributeIsImage, attributeIsPassword))
                    
                    tmpList.append(self.getAttributeModifierString(univAttributeName, 
                        allowDelete, attributeBinaryExport, attributeModify))
                    
                tmpList.append("""</tr>""")
                
                
        tmpList.append("""</table>""")
        
        return "".join(tmpList)
        

###############################################################################

    def getAttributeValueString(self, univAttributeName, value, attributeIsBinary, 
        attributeIsImage, attributeIsPassword):
        tmpList = []
        
        # Create the value part
        if attributeIsBinary:
            if attributeIsImage:
                tmpImage = QImage()
                tmpImage.loadFromData(value)
                self.mimeFactory.setImage(univAttributeName, tmpImage)
                tmpList.append("""<td width="55%"><img source=""" + univAttributeName + """></td>""")
            elif attributeIsPassword:
                tmpList.append("""<td bgcolor="#E5E5E5" width="55%">""" + value + """</td>""")
            else:
                self.mimeFactory.setImage(univAttributeName, self.binaryImage)
                tmpList.append("""<td width="55%"><img source=""" + univAttributeName + """></td>""")
        else:
            tmpList.append("""<td bgcolor="#E5E5E5" width="55%">""" + value + """</td>""")
            
        return "".join(tmpList)
        
###############################################################################

    def getAttributeModifierString(self, univAttributeName, allowDelete, attributeBinaryExport, attributeModify):
        tmpList = []
        
        tmpList.append("""<td width=20%>""")
        
        if attributeModify:
        #if True:
            editName = univAttributeName + "__edit\""
            tmpList.append("""<a href=\"""" + editName + """><img source=":/icons/edit"></a>""")
        
            if allowDelete:
            #if True:
                deleteName = univAttributeName + "__delete\""
                tmpList.append(""" <a href=\"""" + deleteName + """><img source=":/icons/deleteEntry"></a>""")
            
            if attributeBinaryExport:
                exportName = univAttributeName + "__export\""
                tmpList.append(""" <a href=\"""" + exportName + """><img source=":/icons/exportPixmap"></a>""")
        
        tmpList.append("""</td>""")
        
            
        return "".join(tmpList)

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
    # TODO: check
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

    def editAttribute(self, attributeName, index):
        oldDN = self.ldapDataObject.getDN()
        
        if attributeName == 'RDN':
            self.ldapDataObject.setDN(self.baseDN)

        attributeValue = self.ldapDataObject.getAttributeValue(attributeName, index)
        newValue, ok = QtGui.QInputDialog.getText(self, 'Input dialog', 'Attribute value:', QLineEdit.Normal, attributeValue)
        newValue = unicode(newValue)
        if ok:
            if not newValue == None:
                self.ldapDataObject.setAttributeValue(attributeName, index, newValue)
                self.EDITED = True
                self.displayValues()
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

    # TODO: add logging for each error
    def refreshView(self):
        """ Refreshes the LDAP data from server and displays values.
        """
        
        lumaConnection = LumaConnection(self.ldapDataObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bind()
        
        if not bindSuccess:
            #dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            QMessageBox.critical(self, "Bind error", errorMsg)
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
            QMessageBox.critical(self, "Bind error", errorMsg)
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
                QMessageBox.critical(self, "Bind error", errorMsg)
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
                QMessageBox.critical(self, "Bind error", errorMsg)
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
            QMessageBox.critical(self, "Bind error", errorMsg)
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
            QMessageBox.critical(self, "Delete error", errorMsg)
            #dialog.setErrorMessage(errorMsg)
            #dialog.exec_loop()

###############################################################################

    def clearView(self):
        self.objectWidget.setText("")
