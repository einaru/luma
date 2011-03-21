# -*- coding: utf-8 -*-
import PyQt4
from PyQt4.QtCore import QString, QSize, SIGNAL
from PyQt4.QtGui import QInputDialog, QLineEdit, QImage, QTextBrowser, QTextOption, QSizePolicy
from plugins.browser_plugin.view.AbstractEntryView import AbstractEntryView
import copy

class ClassicView(AbstractEntryView):

    def __init__(self, entryModel, ignoreInvalid):
        AbstractEntryView.__init__(self)
        self.entryModel = entryModel
        self.ignoreInvalid = ignoreInvalid
        self.name = "classic"
        if self.ignoreInvalid:
            self.name += ("(ignore)")
        self.currentDocument = ""
        self.objectWidget = None

    @staticmethod
    def supportedViews(entryModel):
        """
        returns True if it supports view for the smartObject
        """
        return [ClassicView(entryModel, False), ClassicView(entryModel, True)]
    def getName(self):
        """
        returns the name that will be displayed in the QComboBox
        """
        return self.name


    def initWidget(self, parent=None):
        # create the widget containing the data
        self.objectWidget = QTextBrowser(parent)
        self.objectWidget.setWordWrapMode(QTextOption.WrapAnywhere)
        self.objectWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.objectWidget.setMinimumSize(QSize(300, 100))
        self.objectWidget.setOpenLinks(False)
        self.objectWidget.setHtml("")
        self.objectWidget.connect(self.objectWidget, SIGNAL("anchorClicked(const QUrl&)"), self.anchorClicked)

    def refreshView(self):
        self.currentDocument = self.createDocument()
        self.objectWidget.setHtml(self.currentDocument)

    def getWidget(self):
        return self.objectWidget

    # TODO remove this, implement correctly
    def trUtf8(self, string):
        return self.objectWidget.trUtf8(string)

    def createDocument(self):

        smartObject = self.entryModel.getSmartObject()
        smartObject.checkIntegrity()

        if self.ignoreInvalid or smartObject.isValid:
            tmpList = []
            tmpList.append("<html>")
            tmpList.append("""<body>""")
            tmpList.append("""<table border="0" cellpadding="1" cellspacing="0" width="100%">""")
            tmpList.append("""<tr>""")
            tmpList.append("""<td bgcolor="#B2CAE7" width="40%"><font size="+1"> <b>Distinguished Name:</b> </font></td>""")
            tmpList.append("""<td bgcolor="#B2CAE7" width="60%"><font size="+1"><b>""" + smartObject.getPrettyDN() + """</b></font></td>""")
        
            if self.entryModel.CREATE:
                tmpList.append("""<td width=5%><a href=RDN__0__edit><img source=":/icons/edit"></a></td>""")

            tmpList.append("""</tr>""")
        
            tmpList.append("</table>")
            tmpList.append("<br>")
        
            tmpList.append(self.createClassString())
        
            tmpList.append("<br>")
        
            tmpList.append(self.createAttributeString())
        
            tmpList.append("</body>")
            tmpList.append("</html>")
        
            return "".join(tmpList)
        
        else:
            tmpList = []
            tmpList.append("<html>")
            tmpList.append("""<body>""")
            tmpList.append("""<table border="0" cellpadding="1" cellspacing="0" width="100%">""")
            tmpList.append("""<tr>""")
            tmpList.append("""<td <font size="+1"> """ + unicode(("<b>Could not display ldap entry. Reason:</b>")) + """</font></td>""")
            tmpList.append("""</tr>""")
            tmpList.append("""<tr>""")
            tmpList.append("""</tr>""")
            for x in smartObject.checkErrorMessageList:
                tmpList.append("""<tr>""")
                tmpList.append("""<td>""" + x + """</td>""")
                tmpList.append("""</tr>""")

            tmpList.append("</body>")
            tmpList.append("</html>")

            return "".join(tmpList)

###############################################################################

    def createClassString(self):
        smartObject = self.entryModel.getSmartObject()
        tmpList = []
        
        tmpList.append("""<table border="0" cellpadding="1" cellspacing="0" width="100%">""")
        tmpList.append("""<tr>""")
        tmpList.append("""<td bgcolor="#C4DFFF" align="center"><b>ObjectClasses</b></td>""")
        tmpList.append("""</tr>""")
        
        rdn = smartObject.getPrettyRDN()
        rdnClass = rdn.split("=")[0]
        
        for x in smartObject.getObjectClasses():
            classString = x[:]
            if smartObject.isValid and smartObject.isObjectclassStructural(x):
                classString = "<b>" + classString + "</b>"
            tmpList.append("""<tr>""")
            tmpList.append("""<td colspan=2 bgcolor="#E5E5E5" width="100%">""")
            tmpList.append(classString)
            
            allowDelete = True
            if smartObject.isValid:
                if smartObject.isObjectclassStructural(x):
                    classList = smartObject.getObjectClasses()
                    classList.remove(x)
                    if len(smartObject.getObjectClassChain(x, classList)) == 0:
                        allowDelete = False
                       
                if rdnClass in smartObject.getAttributeListForObjectClass(x):
                    allowDelete = False
                    
                    # Now we check if another objectclass provides the rdn attribute
                    classList = smartObject.getObjectClasses()
                    classList.remove(x)
                    for y in classList:
                        if rdnClass in smartObject.getAttributeListForObjectClass(y):
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
        smartObject = self.entryModel.getSmartObject()
        tmpList = []
        
        tmpList.append("""<table border="0" cellpadding="0" cellspacing="0" width="100%">""")
        tmpList.append("""<tr>""")
        tmpList.append("""<td colspan=2 bgcolor="#C4DFFF" align="center"><b>Attributes</b></td>""")
        tmpList.append("""</tr>""")
        tmpList.append("""</table>""")
        
        attributeList = smartObject.getAttributeList()
        attributeList.sort()
        
        tmpList.append("""<table border="0" cellpadding="1" cellspacing="1" width="100%">""")
        
        for x in attributeList:
            if smartObject.isValid:
                attributeIsBinary = smartObject.isAttributeBinary(x)
                attributeIsImage = smartObject.isAttributeImage(x)
                attributeIsPassword = smartObject.isAttributePassword(x)
                attributeIsSingle = smartObject.isAttributeSingle(x)
                attributeIsMust = smartObject.isAttributeMust(x)
            else:
                attributeIsBinary = False
                attributeIsImage = False
                attributeIsPassword = False
                attributeIsSingle = False
                attributeIsMust = False
            
            attributeBinaryExport = False
            if smartObject.isValid:
                if attributeIsBinary:
                    if attributeIsImage:
                        attributeBinaryExport = True
                    elif not attributeIsPassword:
                        attributeBinaryExport = True
                    
            valueList = smartObject.getAttributeValueList(x)
            
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
            
            if smartObject.isValid:
                if smartObject.isAttributeMust(x, smartObject.getObjectClasses()):
                    attributeString = "<b>" + attributeString + "</b>"
            
            if valueList[0] == None:
                attributeString = """<font color="red">""" + attributeString + """</font>"""
                
            tmpList.append("""<td bgcolor="#E5E5E5" width="35%">""" + attributeString + """</td>""")
            
            attributeIndex = 0
            univAttributeName = x + "__" + unicode(attributeIndex)

            attributeModify = True

            if smartObject.isValid:
                if not (valueList[0] == None):
                    attributeModify = not smartObject.isAttributeValueRDN(x, valueList[0])
            
            if (valueList[0] == None):
                tmpList.append("""<td bgcolor="#E5E5E5" width="60%"><font color="#ff0000">""" + 
                    unicode("Value not set.") + """</font></td>""")
                    
                tmpList.append(self.getAttributeModifierString(univAttributeName, 
                    allowDelete, False, attributeModify))
            else:
                tmpList.append(self.getAttributeValueString(univAttributeName, valueList[0], 
                    attributeIsBinary, attributeIsImage, attributeIsPassword))
            
                tmpList.append(self.getAttributeModifierString(univAttributeName, 
                    allowDelete, attributeBinaryExport, attributeModify))
                
            tmpList.append("""</tr>""")
            
            
            for y in valueList[1:]:
                attributeIndex += 1
                univAttributeName = x + "__" + unicode(attributeIndex)
                
                attributeModify = True
                if smartObject.isValid:
                    if not (y == None):
                        attributeModify = not smartObject.isAttributeValueRDN(x, y)
                
                tmpList.append("""<tr><td width="35%"></td>""")
                
                if y == None:
                    tmpList.append("""<td bgcolor="#E5E5E5" width="55%"><font color="#ff0000">""" +
                        unicode("Value not set.") + """</font></td>""")
                        
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

    #TODO image and password will crash
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

    def anchorClicked(self, url):
        nameString = unicode(url.toString())
        tmpList = nameString.split("__")
        
        if tmpList[0] in self.entryModel.getSmartObject().getObjectClasses():
            self.entryModel.deleteObjectClass(tmpList[0])
            #self.refreshView()
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
        newValue = unicode(newValue)
        if ok:
            if not newValue == None:
                self.entryModel.editAttribute(attributeName, index, newValue)
                #self.refreshView()
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
