# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import environment

import os.path
from qtxml import *

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

    def getObjectClasses(self):
        """ Return a list of objectclasses.
        """
        
        return self.objectClasses
        
###############################################################################

    def addObjectClass(self, className):
        if not (className in self.objectClasses):
            self.objectClasses.append(className)

###############################################################################

    def getAttributeInfos(self):
        """ Return a list of attributes together with their propperties.
        """
    
        tmpDict = {}
        for x in self.templateData:
            for y in x["ATTRIBUTES"]:
                tmpDict[y["NAME"]] = {"MUST" : y["MUST"], "SINGLE" : y["SINGLE"] , "SHOW" : y["SHOW"] }
        return tmpDict

###############################################################################

    def getAttributeList(self):
        tmpList = []
        for x in self.attributes.keys():
            tmpList.append(x)
            
        return tmpList
        
###############################################################################

    def setAttributeShow(self, attribute, value):
        """ Set the property 'SHOW' of attribute to value.
        """
    
        for x in self.templateData:
            for y in x['ATTRIBUTES']:
                if y['NAME'] == attribute:
                    y['SHOW'] = value
                    
###############################################################################

    def getDataObject(self):
        """ Create a data structure which can be used by python-ldap and return it.
        """
    
        dataObject = {}
        
        for x in self.templateData:
            objectClass = x["CLASSNAME"]
            if dataObject.has_key(objectClass):
                dataObject["objectClass"].append(objectClass)
            else:
                dataObject["objectClass"] = [objectClass]
                
            for y in x["ATTRIBUTES"]:
                if (y["SHOW"] == 1) or (y["MUST"] == 1):
                    dataObject[y["NAME"]] = [""]
        
        return dataObject
        
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

    def __init__(self, tmpList):
        self.templateFile = os.path.join (environment.userHomeDir, ".luma", "templates")

        self.templateList = tmpList

        #try:
        #    self.read_list()
        #except IOError, data:
        #    print "Template file could not be read. \nReason: " + str(data)

###############################################################################

    def readList(self):
        """ Read template Info from file.
    
        Templates are stored in self.tplList
        """
    
        self.tplList = []
        content = open(self.tplFile, 'r').readlines()
        template = LdapTemplate()
        
        for x in content:
            #x = x.decode("utf-8")
            if x == "\n":
                self.tplList.append(template)
                template = LdapTemplate()
                template.name = []
                template.tData = []
                
            if x[:6] == "Name: ":
                template.name = x[6:-1].decode("utf-8")
                continue
                
            if x[:6] == "class ":
                tmpString = x[6:-1]
                tmpList = tmpString.split(" >> ")
                data = {}
                data['CLASSNAME'] = tmpList[0]
                tmpList = tmpList[1].split(" || ")
                attributeList = []
                
                for y in tmpList:
                    attrInfo = y.split(",")
                    tmpDict = {}
                    tmpDict["NAME"] = attrInfo[0]
                    
                    if attrInfo[1] == "MUST":
                        tmpDict["MUST"] = 1
                    else:
                        tmpDict["MUST"] = 0

                    if attrInfo[2] == "SINGLE":
                        tmpDict["SINGLE"] = 1
                    else:
                        tmpDict["SINGLE"] = 0

                    if attrInfo[3] == "SHOW":
                        tmpDict["SHOW"] = 1
                    else:
                        tmpDict["SHOW"] = 0
                        
                    attributeList.append(tmpDict)
                    
                data["ATTRIBUTES"] = attributeList
                template.tData.append(data)

###############################################################################

    def save(self):
        """ Save template list to file.
        """
        
        document = QDomDocument("Luma template file")
        root = document.createElement( "Luma templates" )
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
        fileHandler.write(unicode(document.toString()))
        fileHandler.close()

###############################################################################

    def addTemplate(self, name):
        pass

###############################################################################

    def deleteTemplate(self, name):
        pass
        
###############################################################################

    def getTemplate(self, templateName):
        """ Get a template given by templateName
        """
        
        for x in self.tplList:
            if x.name == templateName:
                return x
    
    

