# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTextBrowser, QTextOption, QPixmap, QSizePolicy, QTextOption, QLineEdit, QToolBar, QImage
from PyQt4.QtCore import QSize, SIGNAL
import copy
import logging

class AdvancedObjectView(QTextBrowser):

    def __init__(self, smartObject, parent=None):
        QTextBrowser.__init__(self, parent)
        
        self.ldapDataObject = smartObject

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setWordWrapMode(QTextOption.WrapAnywhere)

        self.connect(self, SIGNAL("anchorClicked(const QUrl&)"), self.modifierClicked)

        self.setOpenLinks(False)
        self.setHtml("")
                
        # boolean to indicate if the current ldap object has been modified
        self.EDITED = False
        
        # is the current object a leaf of the ldap tree?
        self.ISLEAF = False
        
        # do we create a completely new object?
        self.CREATE = False

        self.readServerSchema = False
        
        self.displayValues()
        
        self.bar = QToolBar()
        self.bar.addAction("Save",self.ldapDataObject.updateOnServer)
        self.bar.show()



    def getSmartObject(self):
        return self.ldapDataObject
    
    # TODO: not used
    def initView(self, data, create=False):
        #self.ldapDataObject = data

        if create:
            self.EDITED = True
            self.ISLEAF = False
            self.CREATE = True
        else:
            self.EDITED = False


    def displayValues(self):
        self.setHtml("")

        # Something went wrong. We have no data object.
        # This might happen if we want to refresh an item and
        # it might be deleted already.
        if None == self.ldapDataObject:
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

    def exportAttribute(self, attributeName, index):
        pass

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

    def deleteAttribute(self, attributeName, index):
        self.ldapDataObject.deleteAttributeValue(attributeName, index)
        self.EDITED = True
        self.displayValues()

    def deleteObjectClass(self, className):
        self.ldapDataObject.deleteObjectClass(className)
        self.EDITED = True
        self.displayValues()
