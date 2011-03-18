# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTextBrowser, QTextOption, QPixmap, QSizePolicy, QTextOption, QLineEdit, QToolBar, QImage, QMessageBox, QVBoxLayout, QWidget, QToolButton, QIcon
from PyQt4.QtCore import QSize, SIGNAL
from base.backend.LumaConnection import LumaConnection
from base.backend.ServerList import ServerList
import ldap
import copy
import logging

class AdvancedObjectView(QWidget):

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

        # ignore ldapObjectInvalid
        self.ignoreLdapDataObjectInvalid = True
        
        # ignore ServerMeta
        self.ignoreServerMetaError = True

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
                                        QString("Connection error"),
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
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not check if object is a leaf in the ldap tree.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                
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

        self.ldapDataObject.checkIntegrity()

        # TODO: serverschema errors ignored
        if self.ignoreLdapDataObjectInvalid or self.ldapDataObject.isValid:
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
        
            self.objectWidget.setHtml("".join(tmpList))
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

            self.objectWidget.setHtml("".join(tmpList))

        self.enableToolButtons(True)

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
            if self.ldapDataObject.isValid and self.ldapDataObject.isObjectclassStructural(x):
                classString = "<b>" + classString + "</b>"
            tmpList.append("""<tr>""")
            tmpList.append("""<td colspan=2 bgcolor="#E5E5E5" width="100%">""")
            tmpList.append(classString)
            
            allowDelete = True
            if self.ldapDataObject.isValid:
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
            if self.ldapDataObject.isValid:
                attributeIsBinary = self.ldapDataObject.isAttributeBinary(x)
                attributeIsImage = self.ldapDataObject.isAttributeImage(x)
                attributeIsPassword = self.ldapDataObject.isAttributePassword(x)
                attributeIsSingle = self.ldapDataObject.isAttributeSingle(x)
                attributeIsMust = self.ldapDataObject.isAttributeMust(x)
            else:
                attributeIsBinary = False
                attributeIsImage = False
                attributeIsPassword = False
                attributeIsSingle = False
                attributeIsMust = False
            
            attributeBinaryExport = False
            if self.ldapDataObject.isValid:
                if attributeIsBinary:
                    if attributeIsImage:
                        attributeBinaryExport = True
                    elif not attributeIsPassword:
                        attributeBinaryExport = True
                    
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
            
            if self.ldapDataObject.isValid:
                if self.ldapDataObject.isAttributeMust(x, self.ldapDataObject.getObjectClasses()):
                    attributeString = "<b>" + attributeString + "</b>"
            
            if valueList[0] == None:
                attributeString = """<font color="red">""" + attributeString + """</font>"""
                
            tmpList.append("""<td bgcolor="#E5E5E5" width="35%">""" + attributeString + """</td>""")
            
            attributeIndex = 0
            univAttributeName = x + "__" + unicode(attributeIndex)

            attributeModify = True

            if self.ldapDataObject.isValid:
                if not (valueList[0] == None):
                    attributeModify = not self.ldapDataObject.isAttributeValueRDN(x, valueList[0])
            
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
                if self.ldapDataObject.isValid:
                    if not (y == None):
                        attributeModify = not self.ldapDataObject.isAttributeValueRDN(x, y)
                
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
        newValue, ok = QtGui.QInputDialog.getText(self, 'Input dialog', 'Attribute value:', QLineEdit.Normal, attributeValue)
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
            self.trUtf8("""Do you want to save the entry?"""),
            QMessageBox.Ok,
            QMessageBox.Cancel)
            
        if result == QMessageBox.Ok:
            self.saveView()

        
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
        
        self.enableToolButtons(False)
        self.layout().insertWidget(0, self.toolBar)

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
