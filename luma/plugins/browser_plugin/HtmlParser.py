# -*- coding: utf-8 -*-
import os
import copy
import PyQt4
from PyQt4.QtCore import QXmlStreamReader, QString, QResource, QUrl
from PyQt4.QtGui import QImage, QTextDocument

class HtmlParser:
    ''' This class parses a html-template and inserts values from the entry model
    '''
    def __init__(self, objectWidget):
        self.entryModel = None
        self.smartObject = None
        self.objectWidget = objectWidget

    def setModel(self, entryModel):
        self.entryModel = entryModel

    ''' Utility function, checks both smart data object and template object
    '''
    def _isAttributeMust(self, x):
        if self.entryModel.entryTemplate:
            template = self.entryModel.entryTemplate
            if x in template.attributes:
                if template.attributes[x].customMust:
                    return True
        return self.smartObject.isAttributeMust(x)

    def parseHtml(self, htmlTemplate):
        # reload smartObject each time
        self.smartObject = self.entryModel.getSmartObject()
        #TODO remove QString
        reader = QXmlStreamReader(htmlTemplate)
        tmpList = []
        while not reader.atEnd():
            reader.readNext()
            name = unicode(reader.name().toString())
            if reader.isStartElement():
                attributes = reader.attributes()
                if name == "ldapobject":
                    tmpList.append(self.createStringFromTemplate(attributes))
                else:
                    if not attributes.isEmpty():
                        size = attributes.size()
                        list = []
                        for i in range(0, size):
                            attribute = attributes.at(i)
                            attributeName = unicode(attribute.name().toString())
                            attributeValue = unicode(attribute.value().toString())
                            attributeString = '%s="%s"' % (attributeName, attributeValue)
                            list.append(attributeString)
                        attributesString = ' '.join(list)
                        tag = "<%s %s>" % (name, attributesString)
                        tmpList.append(tag)
                    else: 
                        tag = "<%s>" % name
                        tmpList.append(tag)
            elif reader.isEndElement():
                if not (name == "ldapobject"):
                    tag = "</%s>" % name
                    tmpList.append(tag)
            elif reader.isCharacters():
                if not (unicode(reader.name()) == "ldapobject"):
                    tmpList.append(unicode(reader.text().toString()))
            
        if reader.hasError():
            return reader.errorString()
        return ''.join(tmpList)

    def createStringFromTemplate(self, attributes):
        functioncall = unicode(attributes.value(QString("function")).toString())
        id = unicode(attributes.value(QString("id")).toString())
        style = unicode(attributes.value(QString("style")).toString())

        if not functioncall == "":
            if functioncall == "getPrettyDN":
                return self.getPrettyDN()
            elif functioncall == "createClassString":
                if style == "rows":
                    return self.createClassString()
            elif functioncall == "createAttributeString":
                if style == "rows":
                    return self.createAttributeString()
            elif functioncall == "attribute":
                return self.createAttributeValueString(id)
            elif functioncall == "createErrorMessageList":
                return self.createErrorMessageList()

    def getPrettyDN(self):
        tmpList = []

        dn = self.smartObject.getPrettyDN()
        tmpList.append('''<td bgcolor="#B2CAE7" width="40%"><font size="+1"><b>Distinguished Name:</b></font></td>''')
        tmpList.append('''<td bgcolor="#B2CAE7" width="60%"><font size="+1"><b>''' + dn + '''</b></font></td>''')
        if self.entryModel.CREATE:
                tmpList.append('''<td width=5%><a href="RDN__0__edit"><img source=":/icons/16/document-edit"></a></td>''')

        return ''.join(tmpList)

    def createClassString(self):
        tmpList = []
        
        rdn = self.smartObject.getPrettyRDN()
        rdnClass = rdn.split("=")[0]
        
        for x in self.smartObject.getObjectClasses():
            classString = x[:]
            if self.smartObject.isValid and self.smartObject.isObjectclassStructural(x):
                    classString = "<b>" + classString + "</b>"
            tmpList.append('''<tr>''')
            tmpList.append('''<td colspan=2 bgcolor="#E5E5E5" width="100%">''')
            tmpList.append(classString)
            
            allowDelete = True
            if self.smartObject.isValid and self.smartObject.isObjectclassStructural(x):
                classList = self.smartObject.getObjectClasses()
                classList.remove(x)
                if len(self.smartObject.getObjectClassChain(x, classList)) == 0:
                    allowDelete = False
                       
                if rdnClass in self.smartObject.getAttributeListForObjectClass(x):
                    allowDelete = False
                    
                    # Now we check if another objectclass provides the rdn attribute
                    classList = self.smartObject.getObjectClasses()
                    classList.remove(x)
                    for y in classList:
                        if rdnClass in self.smartObject.getAttributeListForObjectClass(y):
                            allowDelete = True
                            break
            if allowDelete and (not (x == 'top')):
                deleteName = x + '__delete"'
                tmpList.append(''' <a href="''' + deleteName + '''><img source=":/icons/16/edit-delete"></a>''')
            
            tmpList.append('''</td></tr>''')
        
        return "".join(tmpList)


    def createAttributeString(self):
        tmpList = []
        attributeList = self.smartObject.getAttributeList()
        attributeList.sort()
        for x in attributeList:
            tmpList.append(self.createAttributeValueString(x))
        return "".join(tmpList)
        
    def createAttributeValueString(self, x, returnEmpty=True):
        tmpList = []
        if self.smartObject.isValid:
            attributeIsBinary = self.smartObject.isAttributeBinary(x)
            attributeIsImage = self.smartObject.isAttributeImage(x)
            attributeIsPassword = self.smartObject.isAttributePassword(x)
            attributeIsSingle = self.smartObject.isAttributeSingle(x)
            #attributeIsMust = self.smartObject.isAttributeMust(x)
            attributeIsMust = self._isAttributeMust(x)
        else:
            attributeIsBinary = False
            attributeIsImage = False
            attributeIsPassword = False
            attributeIsSingle = False
            attributeIsMust = False
        
        attributeBinaryExport = False
        if self.smartObject.isValid:
            if attributeIsBinary:
                if attributeIsImage:
                    attributeBinaryExport = True
                elif not attributeIsPassword:
                    attributeBinaryExport = True
                
        valueList = self.smartObject.getAttributeValueList(x)
        
        if None == valueList or not (len(valueList) > 0):
            if returnEmpty:
                valueList = [None]
            else:
                return ''

            
        
        allowDelete = False
        if attributeIsMust:
            if len(valueList) > 1:
                allowDelete = True
        else:
            allowDelete = True
        
        tmpList.append('''<tr>''')
        
        attributeString = copy.copy(x)
        
        if self.smartObject.isValid:
            if self.smartObject.isAttributeMust(x, self.smartObject.getObjectClasses()):
                attributeString = "<b>" + attributeString + "</b>"
            elif self.entryModel.entryTemplate:
                template = self.entryModel.entryTemplate
                if x in template.attributes:
                    if template.attributes[x].customMust:
                        attributeString = "<b>" + attributeString + "</b>"
                
        
        if valueList[0] == None or len(valueList[0]) == 0:
            allowDelete = False
            attributeString = '''<font color="red">''' + attributeString + '''</font>'''
            
        tmpList.append('''<td bgcolor="#E5E5E5" width="35%">''' + attributeString + '''</td>''')
        
        attributeIndex = 0
        univAttributeName = x + "__" + unicode(attributeIndex)

        attributeModify = True

        # allow modifying when creating
        if self.smartObject.isValid and not self.entryModel.CREATE:
            if not (valueList[0] == None):
                attributeModify = not self.smartObject.isAttributeValueRDN(x, valueList[0])
        
        if valueList[0] == None or len(valueList[0]) == 0:
            tmpList.append('''<td bgcolor="#E5E5E5" width="60%"><font color="#ff0000">''' + 
                unicode("Value not set.") + '''</font></td>''')
                
            tmpList.append(self.getAttributeModifierString(univAttributeName, 
                allowDelete, False, attributeModify))
        else:
            tmpList.append(self.getAttributeValueString(univAttributeName, valueList[0], 
                attributeIsBinary, attributeIsImage, attributeIsPassword))
        
            tmpList.append(self.getAttributeModifierString(univAttributeName, 
                allowDelete, attributeBinaryExport, attributeModify))
            
        tmpList.append('''</tr>''')
        
        
        for y in valueList[1:]:
            attributeIndex += 1
            univAttributeName = x + "__" + unicode(attributeIndex)
            
            attributeModify = True
            if self.smartObject.isValid and not self.entryModel.CREATE:
                if not (y == None):
                    attributeModify = not self.smartObject.isAttributeValueRDN(x, y)
            
            tmpList.append('''<tr><td width="35%"></td>''')
            
            if y == None or len(y) == 0:
                tmpList.append('''<td bgcolor="#E5E5E5" width="55%"><font color="#ff0000">''' +
                    unicode("Value not set.") + '''</font></td>''')
                    
                tmpList.append(self.getAttributeModifierString(univAttributeName, 
                    allowDelete, False, attributeModify))
            else:
                tmpList.append(self.getAttributeValueString(univAttributeName, y, 
                    attributeIsBinary, attributeIsImage, attributeIsPassword))
                
                tmpList.append(self.getAttributeModifierString(univAttributeName, 
                    allowDelete, attributeBinaryExport, attributeModify))
                
            tmpList.append('''</tr>''')
        return ''.join(tmpList)

    def getAttributeValueString(self, univAttributeName, value, attributeIsBinary, 
        attributeIsImage, attributeIsPassword):
        tmpList = []
        
        # Create the value part
        if attributeIsBinary:
            if attributeIsImage:
                tmpImage = QImage()
                tmpImage.loadFromData(value)
                self.objectWidget.document().addResource(QTextDocument.ImageResource, QUrl(univAttributeName), tmpImage)
                tmpList.append('''<td width="55%"><img source=''' + univAttributeName + '''></td>''')
            elif attributeIsPassword:
                tmpList.append('''<td bgcolor="#E5E5E5" width="55%">''' + value.decode('utf-8') + '''</td>''')
            else:
                #self.mimeFactory.setImage(univAttributeName, self.binaryImage)
                tmpList.append('''<td width="55%"><img source=''' + univAttributeName + '''></td>''')
        else:
            tmpList.append('''<td bgcolor="#E5E5E5" width="55%">''' + value + '''</td>''')
            
        return "".join(tmpList)
        

    def getAttributeModifierString(self, univAttributeName, allowDelete, attributeBinaryExport, attributeModify):
        tmpList = []
        
        tmpList.append('''<td width=20%>''')
        
        if attributeModify:
        #if True:
            editName = univAttributeName + '__edit"'
            tmpList.append('''<a href="''' + editName + '''><img source=":/icons/16/document-edit"></a>''')
        
            if allowDelete:
            #if True:
                deleteName = univAttributeName + '__delete"'
                tmpList.append(''' <a href="''' + deleteName + '''><img source=":/icons/16/edit-delete"></a>''')
            
            if attributeBinaryExport:
                exportName = univAttributeName + '__export"'
                tmpList.append(''' <a href="''' + exportName + '''><img source=":/icons/16/document-export"></a>''')
        
        tmpList.append('''</td>''')
        
            
        return "".join(tmpList)

    def createErrorMessageList(self):
        tmpList = []
        for x in self.smartObject.checkErrorMessageList:
            tmpList.append('''<tr>''')
            tmpList.append('''<td>''' + x + '''</td>''')
            tmpList.append('''</tr>''')
        return ''.join(tmpList)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
