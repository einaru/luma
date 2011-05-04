'''
Created on 16. mars 2011

@author: Simen
'''
import os.path
import logging
import copy

from PyQt4.QtXml import QDomDocument

import stat
from .TemplateObject import TemplateObject, AttributeObject

class TemplateList(object):
    """
    Object for managing the list of available templates.
    """

    _logger = logging.getLogger(__name__)
    
#    # The cache for the client side ssl certificates
#    # The filename is the key. In a tupel are the modification time and the 
#    # cert as StringIO objects
#    certCache = {}

    def __init__(self, configPrefix = None, templateFileName = "templatelist.xml"):
        if configPrefix == None:
            #TODO Should get default
            configPrefix = "/tmp"
        self._templateList = []
        self._configPrefix = configPrefix
        self._configFile = os.path.join(self._configPrefix, templateFileName)
        
        if os.path.isfile(self._configFile):
            self._readTemplateList()


    def getTable(self):
        """
        Return the list of TemplateObject
        """
        return self._templateList


    def setTable(self, templateList):
        """
        Sets the list of TemplateObjets
        """
        self._templateList = templateList


    def getTemplateObject(self, templateName):
        """ 
        Get a template object by its name.
        """
        for x in self._templateList:
            if x.templateName == templateName:
                return x


    def addTemplate(self, templateObject):
        """ 
        Add a template to the template list.
        """
        self._logger.debug("Adding template to self.templateList")
        
        if self._templateList == None:
            self._templateList = [templateObject]
        else:
            self._templateList.append(templateObject)


    def deleteTemplate(self, templateName):
        """ Delete a template from the template list.
        """
        self._logger.debug("Deleting template from self.templateList")
        self._templateList = filter(lambda x: not (x.name == templateName), self._templateList)


    def deleteTemplateByIndex(self, index):
        """ Delete a template from the template list.
        """
        self._logger.debug("Deleting template (using an index) from self.templateList")
        self._templateList.pop(index)
        #del self._templateList.pop(index)



    def _readTemplateList(self):
        """
        Read template Info from file.
        Templates are stored in self.templateList
        """
        self._logger.debug("Calling _readTemplateList")
        
        self._templateList = []

        fileContent = ""
        try:
            fileContent = "".join(open(self._configFile, "r").readlines())
        except IOError, e:
            errorString = "Could not read template configuration file. Reason:\n"
            errorString += str(e)
            self._logger.error(errorString)
    
        
        document = QDomDocument("LumaTemplateFile")
        document.setContent(fileContent)
        
        root = document.documentElement()
        if not (unicode(root.tagName()) == "LumaTemplates"):
            self._logger.debug("Could not parse template file.")
            
        child = root.firstChild()
        while (not child.isNull()):
            template = TemplateObject()
            element = child.toElement()
            if unicode(element.tagName()) == "template":
                template.templateName = unicode(element.attribute("name"))
                template.server = unicode(element.attribute("server"))
                template.description = unicode(element.attribute("description"))
                
                templateChild = child.firstChild()
                while (not templateChild.isNull()):
                    templateElement = templateChild.toElement()
                    tagName = unicode(templateElement.tagName())
                    
                    if tagName == "objectClasses":
                        classNode = templateChild.firstChild()
                        while (not classNode.isNull()):
                            classElement = classNode.toElement()
                            className = str(classElement.tagName())
                            template.addObjectclass(className)
                            classNode = classNode.nextSibling()
                        
                    if tagName == "attributes":
                        attributeNode = templateChild.firstChild()
                        while (not attributeNode.isNull()):
                            attributeElement = attributeNode.toElement()
                            
                            attributeName = str(attributeElement.tagName())
                            binaryString = attributeElement.attribute("binary")
                            mustString = attributeElement.attribute("must")
                            customMustString = attributeElement.attribute("customMust")
                            singleString = attributeElement.attribute("single")
                            
                            binary = False
                            if binaryString == "True":
                                binary = True
                                
                            must = False
                            if mustString == "True":
                                must = True
                                
                            customMust = False
                            if customMustString == "True":
                                customMust = True
                                
                            single = False
                            if singleString == "True":
                                single = True
                                
                            defaultValue = None
                            if attributeElement.hasAttribute("defaultValue"):
                                defaultValue = unicode(attributeElement.attribute("defaultValue"))
                                
                            attribute = AttributeObject(attributeName, must, single, binary, defaultValue, customMust)
                            template.attributes[attributeName] = attribute
                            attributeNode = attributeNode.nextSibling()
                        
                        
                    templateChild = templateChild.nextSibling()
            
            child = child.nextSibling()
            self._templateList.append(template)
        

    def save(self):
        """
        Save template list to file.
        """

        self._logger.debug("Saving template list to disk")
        
        document = QDomDocument("LumaTemplateFile")
        root = document.createElement( "LumaTemplates" )
        document.appendChild(root)
        
        for x in self._templateList:
            templateNode = document.createElement("template")
            templateNode.setAttribute("name", x.templateName)
            templateNode.setAttribute("server", x.server)
            templateNode.setAttribute("description", x.description)
            
            templateClasses = document.createElement("objectClasses")
            for y in x.objectclasses:
                classNode = document.createElement(y)
                templateClasses.appendChild(classNode)
            templateNode.appendChild(templateClasses)
            
            templateAttributes = document.createElement("attributes")
            for y in x.attributes.keys():
                attribute = x.attributes[y]
                attributeNode = document.createElement(attribute.attributeName)
                attributeNode.setAttribute("must", str(attribute.must))
                attributeNode.setAttribute("customMust", str(attribute.customMust))
                attributeNode.setAttribute("single", str(attribute.single))
                attributeNode.setAttribute("binary", str(attribute.binary))
                if not attribute.defaultValue == None and len(attribute.defaultValue):
                    attributeNode.setAttribute("defaultValue", unicode(attribute.defaultValue))
                templateAttributes.appendChild(attributeNode)
            templateNode.appendChild(templateAttributes)
            
            
            root.appendChild(templateNode)
        
        fileHandler = open(self._configFile, "w")
        fileHandler.write(unicode(document.toString()).encode("utf-8"))
        fileHandler.close()


'''henta fra serverlist''' 
#    def writeTemplateList(self):
#        """ 
#        Save the template list to configuration file.
#        """
#        
#        self._logger.debug("Saving templatelist to disk")
#            
##        document = QDomDocument("LumaTemplateFile")
##        root = document.createElement( "LumaTemplateList" )
##        root.setAttribute("version", "1.2")
##        document.appendChild(root)
##        
##        for templateObject in self._templateList:
##            templateNode = document.createElement("LumaLdapTemplate")
##            templateNode.setAttribute("name", templateObject.name)
##            templateNode.setAttribute("host", templateObject.hostname)
##            templateNode.setAttribute("port", templateObject.port)
##            templateNode.setAttribute("bindAnon", templateObject.bindAnon)
##            templateNode.setAttribute("bindDN", templateObject.bindDN)
##            templateNode.setAttribute("bindPassword", templateObject.bindPassword)
##            templateNode.setAttribute("encryptionMethod", templateObject.encryptionMethod)
##            templateNode.setAttribute("authMethod", templateObject.authMethod)
##            templateNode.setAttribute("autoBase", templateObject.autoBase)
##            templateNode.setAttribute("followAliases", templateObject.followAliases)
##            templateNode.setAttribute("checkTemplateCertificate", templateObject.checkTemplateCertificate)
##            templateNode.setAttribute("useCertificate", templateObject.useCertificate)
##            templateNode.setAttribute("clientCertFile", templateObject.clientCertFile)
##            templateNode.setAttribute("clientCertKeyFile", templateObject.clientCertKeyFile)
##            
##            
##            baseNode = document.createElement("baseDNs")
##            for tmpBase in templateObject.baseDN:
##                tmpNode = document.createElement("base")
##                tmpNode.setAttribute("dn", tmpBase)
##                baseNode.appendChild(tmpNode)
##                
##            templateNode.appendChild(baseNode)
##            
##            root.appendChild(templateNode)
##            
##        if not os.path.exists(self._configPrefix):
##            os.makedirs(self._configPrefix)
##            
##        fileHandler = open(self._configFile, "w")
##        fileHandler.write(unicode(document.toString()).encode("utf-8"))
##        fileHandler.close()
##        
##        # Only the user should be able to access the file since we store 
##        # passwords in it.
##        # If we can't change it, leave it as it is since the user must have 
##        # changed it manually. 
##        try:
##            #os.chmod(self._configFile, 0600)
##            os.chmod(self._configFile, stat.S_IRUSR|stat.S_IWUSR)
##        except:
##            self._logger.debug("Couldn't set permissions on file "+self._configFile)
#
#
#    def readTemplateList(self):
#        self._readTemplateList()
#
#
#    def _readTemplateList(self):
#        """ 
#        Read the template list from configuration file.
#        """
#        self._logger.debug("Reading template list from disk")
#        
#        if not os.path.isfile(self._configFile):
#            self._logger.error("Templatelist not found")
#            self._templateList = []
#            return
#        
#        templateList = self._readFromXML()
#        self._templateList = templateList
#
#
#    def _readFromXML(self):
#
#        self._logger.debug("Calling _readFromXML() to load templatelist from disk")
#
#        fileContent = ""
#        try:
#            fileContent = "".join(open(self._configFile, "r").readlines())
#            # If this is uncommentet, non-ascii characters stops working.
#            # It's probably also decoded by QDomDocument, so decoding now means it's decoded
#            # twice - which doesn't work.
#            #fileContent = fileContent.decode("utf-8")
#        except IOError, e:
#            errorString = "Could not read template configuration file. Reason:\n"
#            errorString += str(e)
#            self._logger.warning(errorString)
#
#        document = QDomDocument("LumaTemplateFile")
#        document.setContent(fileContent)
#        
#        root = document.documentElement()
#        if not (unicode(root.tagName()) == "LumaTemplateList"):
#            errorString = "Could not parse template configuration file."
#            self._logger.error(errorString)
#            
#        templateList = None
#        
#        if root.attribute("version") == "1.0":
#            self._logger.error("Can't read old templateconfig")
#            #templateList = self._readFromXMLVersion1_0(fileContent)
#        elif root.attribute("version") == "1.1":
#            self._logger.error("Can't read old templateconfig")
#            #templateList = self._readFromXMLVersion1_1(fileContent)
#        elif root.attribute("version") == "1.2":
#            self._logger.info("Reading new template-list-format for Luma3")
#            templateList = self._readFromXMLVersion1_2(fileContent)
#             
#        return templateList
#
#
#    def _readFromXMLVersion1_2(self, fileContent):
#        
#        self._logger.debug("Using _readFromXMLVersion1_2() to load templatelist from disk")
#        
#        document = QDomDocument("LumaTemplateFile")
#        document.setContent(fileContent)
#        root = document.documentElement()
#        
#        templateList = []
#        
#        child = root.firstChild()
#        while (not child.isNull()):
#            template = TemplateObject()
#            element = child.toElement()
#            if unicode(element.tagName()) == "LumaLdapTemplate":
#                template.name = unicode(element.attribute("name"))
#                template.hostname = unicode(element.attribute("host"))
#                template.port = int(str(element.attribute("port")))
#                
#                tmpVal = unicode(element.attribute("bindAnon"))
#                template.bindAnon = int(tmpVal)
#                    
#                tmpVal = unicode(element.attribute("autoBase"))
#                template.autoBase = int(tmpVal)   
#                    
#                template.bindDN = unicode(element.attribute("bindDN"))
#                template.bindPassword = unicode(element.attribute("bindPassword"))
#                
#                template.encryptionMethod = int(element.attribute("encryptionMethod"))
#                    
#                template.checkTemplateCertificate = int(element.attribute("checkTemplateCertificate"))
#                template.clientCertFile = unicode(element.attribute("clientCertFile"))
#                template.clientCertKeyFile = unicode(element.attribute("clientCertKeyFile"))
#                
#                tmpVal = unicode(element.attribute("useCertificate"))
#                template.useCertificate = int(tmpVal)   
#                    
#                tmpVal = unicode(element.attribute("followAliases"))
#                template.followAliases = int(tmpVal)
#                
#                template.authMethod = int(element.attribute("authMethod"))
#                
#                templateChild = child.firstChild()
#                templateElement = templateChild.toElement()
#                tagName = unicode(templateElement.tagName())
#                    
#                if "baseDNs" == tagName:
#                    baseDN = []
#                    baseNode = templateChild.firstChild()
#                    while (not baseNode.isNull()):
#                        baseElement = baseNode.toElement()
#                        tmpBase = unicode(baseElement.tagName())
#                        if "base" == tmpBase:
#                            baseDN.append(unicode(baseElement.attribute("dn")))
#                        baseNode = baseNode.nextSibling()
#                template.baseDN = baseDN
#                
#            templateList.append(template)
#            child = child.nextSibling()
#        
#        return templateList