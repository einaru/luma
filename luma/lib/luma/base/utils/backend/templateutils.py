# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003,2004 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import environment

import os.path
from qtxml import *
from qt import *
from copy import deepcopy

from base.backend.SmartDataObject import SmartDataObject
from base.utils.backend.LogObject import LogObject

class LdapTemplate(object):
    """ A class for storing template information of ldap-objects.
    """

    def __init__(self, filename=None):
        # Template name
        self.name = ""
        self.description = ""
        self.serverName = ""
        self.objectClasses = []
        self.attributes = {}

        # this is status data of the template
        self.edited = False
        
###############################################################################

    def setAttributeDefaultValue(self, attributeName, value):
        self.attributes[attributeName].defaultValue = value

###############################################################################

    def getObjectClasses(self):
        """ Return a list of objectclasses.
        """
        
        return self.objectClasses
        
###############################################################################

    def deleteAttribute(self, attribute):
        del self.attributes[attribute]
        
###############################################################################

    def deleteObjectClass(self, className):
        self.objectClasses = filter(lambda x: not x == className, self.objectClasses)
        
###############################################################################

    def addObjectClass(self, className):
        if not (className in self.objectClasses):
            self.objectClasses.append(className)

###############################################################################

    def getAttributeList(self):
        return self.attributes.keys()
        

###############################################################################

    def getDataObject(self, serverMeta, baseDN):
        """ Create a data structure which can be used by python-ldap and return it.
        """
    
        dataObject = {}
        dataObject['objectClass'] = deepcopy(self.objectClasses)
        
        for x in self.attributes.keys():
            attributeObject = self.attributes[x]
            if attributeObject.defaultValue == None:
                dataObject[attributeObject.attributeName] = [None]
            else:
                dataObject[attributeObject.attributeName] = [attributeObject.defaultValue.encode("utf-8")]
        
        smartObject = SmartDataObject((baseDN, dataObject), serverMeta)
        
        return smartObject
        
        
###############################################################################

    def addAttribute(self, name, must, single, binary, defaultValue):
        self.attributes[name] = AttributeObject(name, must, single, binary, defaultValue)
    
###############################################################################

class AttributeObject(object):

    def __init__(self, name="", must=False, single=False, binary=False, defaultValue=None):
        self.attributeName = name
        self.must = must
        self.single = single
        self.binary = binary
        self.defaultValue = defaultValue


###############################################################################


class TemplateList:
    """ A class for loading and saving template data to file.
    """

    def __init__(self, tmpList=None):
        self.templateFile = os.path.join (environment.userHomeDir, ".luma", "templates")

        if tmpList == None:
            self.readList()
        else:
            self.templateList = tmpList

###############################################################################

    def readList(self):
        """ Read template Info from file.
    
        Templates are stored in self.tplList
        """
        fileContent = ""
        try:
            fileContent = "".join(open(self.templateFile, "r").readlines())
            fileContent = fileContent.decode("utf-8")
        except IOError, e:
            tmpString = "Could not read template configuration file. Reason:\n"
            tmpString += str(e)
            environment.logMessage(LogObject("Debug", tmpString))
    
        self.templateList = [] 
        
        document = QDomDocument("LumaTemplateFile")
        document.setContent(fileContent)
        
        root = document.documentElement()
        if not (unicode(root.tagName()) == "LumaTemplates"):
            print "Could not parse template file"
            
        child = root.firstChild()
        while (not child.isNull()):
            tmpTemplate = LdapTemplate()
            element = child.toElement()
            if unicode(element.tagName()) == "template":
                tmpTemplate.name = unicode(element.attribute("name"))
                tmpTemplate.serverName = unicode(element.attribute("server"))
                tmpTemplate.description = unicode(element.attribute("description"))
                
                templateChild = child.firstChild()
                while (not templateChild.isNull()):
                    templateElement = templateChild.toElement()
                    tagName = unicode(templateElement.tagName())
                    
                    if tagName == "objectClasses":
                        classNode = templateChild.firstChild()
                        while (not classNode.isNull()):
                            classElement = classNode.toElement()
                            className = str(classElement.tagName())
                            tmpTemplate.objectClasses.append(className)
                            classNode = classNode.nextSibling()
                        
                    if tagName == "attributes":
                        attributeNode = templateChild.firstChild()
                        while (not attributeNode.isNull()):
                            attributeElement = attributeNode.toElement()
                            
                            attributeName = str(attributeElement.tagName())
                            binaryString = attributeElement.attribute("binary")
                            mustString = attributeElement.attribute("must")
                            singleString = attributeElement.attribute("single")
                            
                            binary = False
                            if binaryString == "True":
                                binary = True
                                
                            must = False
                            if mustString == "True":
                                must = True
                                
                            single = False
                            if singleString == "True":
                                single = True
                                
                            defaultValue = None
                            if attributeElement.hasAttribute("defaultValue"):
                                defaultValue = unicode(attributeElement.attribute("defaultValue"))
                                
                            attribute = AttributeObject(attributeName, must, single, binary, defaultValue)
                            tmpTemplate.attributes[attributeName] = attribute
                            attributeNode = attributeNode.nextSibling()
                        
                        
                    templateChild = templateChild.nextSibling()
            
            child = child.nextSibling()
            self.templateList.append(tmpTemplate)
        


###############################################################################

    def save(self):
        """ Save template list to file.
        """
        
        document = QDomDocument("LumaTemplateFile")
        root = document.createElement( "LumaTemplates" )
        document.appendChild(root)
        
        for x in self.templateList:
            templateNode = document.createElement("template")
            templateNode.setAttribute("name", x.name)
            templateNode.setAttribute("server", x.serverName)
            templateNode.setAttribute("description", x.description)
            
            templateClasses = document.createElement("objectClasses")
            for y in x.objectClasses:
                classNode = document.createElement(y)
                templateClasses.appendChild(classNode)
            templateNode.appendChild(templateClasses)
            
            templateAttributes = document.createElement("attributes")
            for y in x.attributes.keys():
                attribute = x.attributes[y]
                attributeNode = document.createElement(attribute.attributeName)
                attributeNode.setAttribute("must", str(attribute.must))
                attributeNode.setAttribute("single", str(attribute.single))
                attributeNode.setAttribute("binary", str(attribute.binary))
                if not (attribute.defaultValue == None):
                    attributeNode.setAttribute("defaultValue", unicode(attribute.defaultValue))
                templateAttributes.appendChild(attributeNode)
            templateNode.appendChild(templateAttributes)
            
            
            root.appendChild(templateNode)
        
        fileHandler = open(self.templateFile, "w")
        fileHandler.write(unicode(document.toString()).encode("utf-8"))
        fileHandler.close()


###############################################################################

    def getTemplate(self, templateName):
        """ Get a template given by templateName
        """
        
        for x in self.templateList:
            if x.name == templateName:
                return deepcopy(x)
    
    

