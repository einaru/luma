# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import ldap
import os
import copy
from sets import Set

from base.backend.ServerList import ServerList
from base.backend.LumaConnection import LumaConnection
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.utils.gui.AddAttributeWizard import AddAttributeWizard
from base.utils.gui.LumaErrorDialog import LumaErrorDialog
import environment
from base.utils.gui import EditorFactory

class AdvancedObjectWidget(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)
        
        self.mainLayout = QHBoxLayout(self)
        
        # Standard pixmaps used by the widget
        self.iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        self.binaryPixmap = QPixmap(os.path.join(self.iconPath, "binary_big.png"))
        self.binaryImage = self.binaryPixmap.convertToImage()
        self.deletePixmap = QPixmap(os.path.join(self.iconPath, "deleteEntry.png"))
        self.deleteSmallPixmap = QPixmap(os.path.join(self.iconPath, "editdelete.png"))
        self.editPixmap = QPixmap(os.path.join(self.iconPath, "edit.png"))
        self.exportBinaryPixmap = QPixmap(os.path.join(self.iconPath, "exportBinary.png"))
        self.deletePixmap = QPixmap(os.path.join(self.iconPath, "deleteEntry.png"))
        self.reloadPixmap = QPixmap(os.path.join(self.iconPath, "reload.png"))
        self.savePixmap = QPixmap(os.path.join(self.iconPath, "save.png"))
        self.addPixmap = QPixmap(os.path.join(self.iconPath, "single.png"))
        
        #create a scrollable frame
        self.attributeFrame = QScrollView(self,"attributeFrame")
        self.attributeFrame.setMinimumSize(QSize(300,100))
        self.attributeFrame.setFrameShape(QFrame.NoFrame)
        self.attributeFrame.setResizePolicy(QScrollView.AutoOneFit)
        self.mainLayout.addWidget(self.attributeFrame)
        
        # create the widget containing the object data
        self.objectWidget = QTextBrowser(self.attributeFrame.viewport())
        self.objectWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.objectWidget.setWrapPolicy(QTextEdit.Anywhere)
        self.connect(self.objectWidget, SIGNAL("anchorClicked (const QString&, const QString&)"), self.modifierClicked)
    
        self.attributeFrame.addChild(self.objectWidget)
        
        # Data of the current object
        self.ldapDataObject = None
        
        # boolean to indicate if the current ldap object has been modified
        self.EDITED = False
        
        # is the current object a leaf of the ldap tree?
        self.ISLEAF = False
        
        # do we create a completely new object?
        self.CREATE = False
        
        # Factory object for storing images
        self.mimeFactory = None
        
        # String of the current document for rendering ldap data
        self.currentDocument = None
        
###############################################################################
        
    def initView(self, data, create=False):
        self.ldapDataObject = data
        
        self.mimeFactory = LumaMimeFactory()
        self.objectWidget.setMimeSourceFactory(self.mimeFactory) 
        
        if create:
            self.EDITED = True
            self.ISLEAF = False
            self.CREATE = True
        else:
            self.EDITED = False
        
            # check if current object is a leaf of the ldap tree
            isLeave = False
            
            tmpObject = ServerList()
            tmpObject.readServerList()
            serverMeta = tmpObject.getServerObject(self.ldapDataObject.getServerAlias())
        
            lumaConnection = LumaConnection(serverMeta)
        
            bindSuccess, exceptionObject = lumaConnection.bind()
            
            if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                return 
            
            success, resultList, exceptionObject = lumaConnection.search(self.ldapDataObject.dn, ldap.SCOPE_ONELEVEL, filter="(objectClass=*)", attrList=None, attrsonly=1)
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
        environment.setBusy(True)
        self.objectWidget.setText("")
        
        # Something went wrong. We have no data object.
        # This might happen if we want to refresh an item and 
        # it might be deleted already.
        if None == self.ldapDataObject:
            self.enableToolButtons(False)
            return 
        
        tmpList = []
        tmpList.append("<html>")
        tmpList.append("""<body>""")
        tmpList.append("""<table border="0" cellpadding="1" cellspacing="0" width="100%">""")
        tmpList.append("""<tr>""")
        tmpList.append("""<td bgcolor="#B2CAE7" width="40%"><font size="+1"> <b>Distinguished Name:</b> </font></td>""")
        tmpList.append("""<td bgcolor="#B2CAE7" width="60%"><font size="+1"><b>""" + self.ldapDataObject.getPrettyDN() + """</b></font></td>""")
        
        if self.CREATE:
            self.mimeFactory.setPixmap("editPixmap", self.editPixmap)
            tmpList.append("""<td width=5%><a name=RDN__0__edit><img source="editPixmap"></a></td>""")
        
        tmpList.append("""</tr>""")
        
        tmpList.append("</table>")
        tmpList.append("<br>")
        
        tmpList.append(self.createClassString())
        
        tmpList.append("<br>")
        
        tmpList.append(self.createAttributeString())
        
        tmpList.append("</body>")
        tmpList.append("</html>")
        
        self.currentDocument = ("".join(tmpList))
        
        self.objectWidget.setText(self.currentDocument)
        
        self.enableToolButtons(True)
        environment.setBusy(False)
        
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
            if self.ldapDataObject.isObjectclassStructural(x):
                classString = "<b>" + classString + "</b>"
            tmpList.append("""<tr>""")
            tmpList.append("""<td colspan=2 bgcolor="#E5E5E5" width="100%">""")
            tmpList.append(classString)
            
            allowDelete = True
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
                self.mimeFactory.setPixmap("deletePixmap", self.deletePixmap)
                tmpList.append(""" <a name=\"""" + deleteName + """><img source="deletePixmap"></a>""")
            
            
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
            environment.updateUI()
            attributeIsBinary = self.ldapDataObject.isAttributeBinary(x)
            attributeIsImage = self.ldapDataObject.isAttributeImage(x)
            attributeIsPassword = self.ldapDataObject.isAttributePassword(x)
            attributeIsSingle = self.ldapDataObject.isAttributeSingle(x)
            attributeIsMust = self.ldapDataObject.isAttributeMust(x)
            
            attributeBinaryExport = False
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
            
            if self.ldapDataObject.isAttributeMust(x, self.ldapDataObject.getObjectClasses()):
                attributeString = "<b>" + attributeString + "</b>"
            
            if valueList[0] == None:
                attributeString = """<font color="red">""" + attributeString + """</font>"""
                
            tmpList.append("""<td bgcolor="#E5E5E5" width="35%">""" + attributeString + """</td>""")
            
            attributeIndex = 0
            univAttributeName = x + "__" + unicode(attributeIndex)

            attributeModify = True
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
                environment.updateUI()
                attributeIndex += 1
                univAttributeName = x + "__" + unicode(attributeIndex)
                
                attributeModify = True
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
        
        tmpList.append("""<td width=10%>""")
        
        if attributeModify:
        #if True:
            editName = univAttributeName + "__edit\""
            self.mimeFactory.setPixmap("editPixmap", self.editPixmap)
            tmpList.append("""<a name=\"""" + editName + """><img source="editPixmap"></a>""")
        
            if allowDelete:
            #if True:
                deleteName = univAttributeName + "__delete\""
                self.mimeFactory.setPixmap("deletePixmap", self.deletePixmap)
                tmpList.append(""" <a name=\"""" + deleteName + """><img source="deletePixmap"></a>""")
            
            if attributeBinaryExport:
                exportName = univAttributeName + "__export\""
                self.mimeFactory.setPixmap("exportPixmap", self.exportBinaryPixmap)
                tmpList.append(""" <a name=\"""" + exportName + """><img source="exportPixmap"></a>""")
        
        tmpList.append("""</td>""")
        
            
        return "".join(tmpList)
        
###############################################################################

    def modifierClicked(self, nameString, linkString):
        nameString = unicode(nameString)
        tmpList = nameString.split("__")
        
        if tmpList[0] in self.ldapDataObject.getObjectClasses():
            self.deleteObjectClass(tmpList[0])
        else:
            if not len(tmpList) == 3:
                return

            attributeName = tmpList[0]
            index = int(tmpList[1])
            operation = tmpList[2]
        
            if operation == "edit":
                self.editAttribute(attributeName, index)
            elif operation == "delete":
                self.deleteAttribute(attributeName, index)
            elif operation == "export":
                self.exportAttribute(attributeName, index)

###############################################################################

    def exportAttribute(self, attributeName, index):
        """ Show the dialog for exporting binary attribute data.
        """
        
        value = self.ldapDataObject.getAttributeValue(attributeName, index)

        fileName = unicode(QFileDialog.getSaveFileName(\
                            None,
                            None,
                            self, None,
                            self.trUtf8("Export binary attribute to file"),
                            None, 1))

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
            
        dialog = EditorFactory.getEditorWidget(self, self.ldapDataObject, attributeName, index)
        
        dialog.exec_loop()
        
        if dialog.result() == QDialog.Accepted:
            newValue = dialog.getValue()
            if not (newValue == None):
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

    def aboutToChange(self):
        if not self.EDITED:
            return
            
        result = QMessageBox.warning(None,
            self.trUtf8("Save entry"),
            self.trUtf8("""Do you want to save the entry?"""),
            self.trUtf8("&OK"),
            self.trUtf8("&Cancel"),
            None,
            0, -1)
            
        if result == 0:
            self.saveView()

        
###############################################################################

    def buildToolBar(self, parent):
        toolBar = QToolBar(parent)
        
        
        # Reload button
        self.reloadButton = QToolButton(toolBar, "reloadEntry")
        self.reloadButton.setIconSet(QIconSet(self.reloadPixmap))
        self.reloadButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.reloadButton.setAutoRaise(True)
        self.reloadButton.setBackgroundMode(self.backgroundMode())
        QToolTip.add(self.reloadButton, self.trUtf8("Reload"))
        self.connect(self.reloadButton, SIGNAL("clicked()"), self.refreshView)
        
        # Save button
        self.saveButton = QToolButton(toolBar, "saveValues")
        self.saveButton.setIconSet(QIconSet(self.savePixmap))
        self.saveButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.saveButton.setAutoRaise(True)
        self.saveButton.setBackgroundMode(self.backgroundMode())
        QToolTip.add(self.saveButton, self.trUtf8("Save"))
        self.connect(self.saveButton, SIGNAL("clicked()"), self.saveView)
        
        toolBar.addSeparator()
        
        # Add attribute button
        self.addAttributeButton = QToolButton(toolBar, "addAttribute")
        self.addAttributeButton.setIconSet(QIconSet(self.addPixmap))
        self.addAttributeButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.addAttributeButton.setAutoRaise(True)
        self.addAttributeButton.setBackgroundMode(self.backgroundMode())
        QToolTip.add(self.addAttributeButton, self.trUtf8("Add attribute..."))
        self.connect(self.addAttributeButton, SIGNAL("clicked()"), self.addAttribute)
        
        # Delete button
        self.deleteObjectButton = QToolButton(toolBar)
        self.deleteObjectButton.setIconSet(QIconSet(self.deleteSmallPixmap))
        self.deleteObjectButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.deleteObjectButton.setAutoRaise(True)
        self.deleteObjectButton.setBackgroundMode(self.backgroundMode())
        QToolTip.add(self.deleteObjectButton, self.trUtf8("Delete object"))
        self.connect(self.deleteObjectButton, SIGNAL("clicked()"), self.deleteObject)
        
        self.enableToolButtons(False)
        
###############################################################################

    def refreshView(self):
        """ Refreshes the LDAP data from server and displays values.
        """
        
        lumaConnection = LumaConnection(self.ldapDataObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bind()
        
        if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
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
        
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not refresh entry.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
        
###############################################################################

    def saveView(self):
        """ Save changes to the current object.
        """
        
        lumaConnection = LumaConnection(self.ldapDataObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bind()
        
        if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                return 
        
        if self.CREATE:
            success, exceptionObject = lumaConnection.addDataObject(self.ldapDataObject)
            lumaConnection.unbind()
            
            if success:
                self.CREATE = False
                self.EDITED = False
                self.displayValues()
            else:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not add entry.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
        else:
            success, exceptionObject = lumaConnection.updateDataObject(self.ldapDataObject)
            lumaConnection.unbind()
            if success:
                self.EDITED = False
                self.displayValues()
            else:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not save entry.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()

###############################################################################

    def addAttribute(self):
        """ Add attributes to the current object.
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
        
###############################################################################

    def deleteObject(self):
        
        tmpDialog = QMessageBox(self.trUtf8("Delete object"),
                self.trUtf8("Do your really want to delete the object?"),
                QMessageBox.Critical,
                QMessageBox.Yes,
                QMessageBox.No,
                QMessageBox.NoButton,
                self)
        
        tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
        tmpDialog.exec_loop()
            
        if tmpDialog.result() == 4:
            return
        
        lumaConnection = LumaConnection(self.ldapDataObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bind()
        
        if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                return
        
        success, exceptionObject = lumaConnection.delete(self.ldapDataObject.getDN())
        lumaConnection.unbind()
        
        if success:
            serverName = self.ldapDataObject.getServerAlias()
            dn = self.ldapDataObject.getPrettyParentDN()
            self.emit(PYSIGNAL("REOPEN_PARENT"), (serverName, dn,))
            self.clearView()
            self.enableToolButtons(False)
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not delete entry.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            
###############################################################################

    def clearView(self):
        self.objectWidget.setText("")
        

###############################################################################
###############################################################################
###############################################################################

class LumaMimeFactory(QMimeSourceFactory):
    """ MimeFactory for providing icons to QTextBrowser. 
    
    Only used internaly.
    """
    
    def __init__(self):
        QMimeSourceFactory.__init__(self)
        
