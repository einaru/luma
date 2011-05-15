'''
Created on 16. mars 2011

@author: Simen
'''
import os.path
import logging
import copy
from base.gui.Settings import PluginSettings

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
            settings = PluginSettings('template')
            configPrefix = settings.configPrefix
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


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
