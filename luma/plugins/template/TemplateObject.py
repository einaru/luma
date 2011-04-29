'''
Created on 16. mars 2011

@author: Simen
'''

from base.backend.SmartDataObject import SmartDataObject
import copy

class TemplateObject(object):
    """
    This class represents a template with all its information.
    """
    
    numFields = 5 # Models need to know
    
    def __init__(self, name = "", server = "", description = ""):
        
        # Holds the data about the server
        # Used for easy mapping to model-columns

        self._dataHolder = [
                #Index - Description (Options)
        unicode(name),    # 0 Template name
        unicode(server),    # 1 Server
        unicode(description),    # 2 Description
        [],     # 3 Objectclasses
        {},     # 4 Attributes
        ]
    
    #Returns the entire list
    def getList(self):
        return self._dataHolder
    
    #Given an index to the _dataHolder, sets the value
    def setIndexToValue(self, index, value):
        self._dataHolder[index] = value

    def addObjectclass(self, objectclass):
        if not objectclass in self.objectclasses:
            self.objectclasses.append(objectclass)
    
    def deleteObjectclass(self, objectclass = None, index = None):
        if objectclass:
            self.objectclasses.remove(objectclass)
        elif index != None:
            self.objectclasses.pop(index)
            
    def objectclassIndex(self, objectclass):
        return self.objectclasses.index(objectclass)

    def getCountObjectclasses(self):
        return len(self.objectclasses)

    def addAttribute(self, name, must = False, single = False, binary = False, defaultValue = None):
        self.attributes[name] = AttributeObject(name, must, single, binary, defaultValue)

    def deleteAttribute(self, attributeName = None, index = None):
        if attributeName:
            self.attributes.pop(attributeName, None)
        elif index != None:
            self.attributes.pop(self.attributes.items()[index][0])
        
    def setAttributeDefaultValue(self, value, attributeName = None, index = None):
        if attributeName:
            self.attributes[attributeName].defaultValue = value
        elif index != None:
            self.attributes.items()[index].defaultValue = value
            
    def attributeIndex(self, attribute):
        return self.attributes.values().index(attribute)

    def getCountAttributes(self):
        return len(self.attributes.keys())

    def getDataObject(self, serverMeta, baseDN):
        """
        Create a data structure which can be used by python-ldap and return it.
        """
    
        dataObject = {}
        dataObject['objectClass'] = copy.deepcopy(self.objectclasses)
        
        for x in self.attributes.items():
            attributeObject = x[1]
            if attributeObject.defaultValue == None:
                dataObject[attributeObject.attributeName] = [None]
            else:
                dataObject[attributeObject.attributeName] = [attributeObject.defaultValue.encode("utf-8")]
        
        smartObject = SmartDataObject((baseDN, dataObject), serverMeta)
        
        return smartObject

    """
    Getterns and setters
    """
    @property
    def templateName(self):
        return self._dataHolder[0]
    
    @property
    def server(self):
        return self._dataHolder[1]
    
    @property
    def description(self):
        return self._dataHolder[2]
    
    @property
    def objectclasses(self):
        return self._dataHolder[3]
    
    @property
    def attributes(self):
        return self._dataHolder[4]

    @templateName.setter
    def templateName(self, name):
        self._dataHolder[0] = name
    
    @server.setter
    def server(self, server):
        self._dataHolder[1] = server
    
    @description.setter
    def description(self, description):
        self._dataHolder[2] = description
    
    @objectclasses.setter    
    def objectclasses(self, objectclasses):
        self._dataHolder[3] = objectclasses
            
    @attributes.setter   
    def attributes(self, attributes):
        self._dataHolder[4] = attributes
        
        


    def __repr__(self):
        finalString = []
        
        finalString.append(unicode("Template name:"))
        finalString.append(unicode(self.templateName))
        finalString.append(unicode("\nServer:"))
        finalString.append(unicode(self.server))
        finalString.append(unicode("\nDescription:"))
        finalString.append(unicode(self.description))
        finalString.append(unicode("\nObjectclasses:"))
        finalString.append(unicode(self.objectclasses))
        finalString.append(unicode("\nAttributes:"))
        finalString.append(unicode(self.attributes))
        finalString.append(unicode("\n"))
        
        return "".join(finalString)
    
    
class AttributeObject(object):
    def __init__(self, name="", must=False, single=False, binary=False, defaultValue=None, customMust=False):
        self.attributeName = name
        self.must = must
        self.single = single
        self.binary = binary
        self.defaultValue = defaultValue
        self.customMust = customMust
        
    def getList(self):
        return [self.attributeName, self.must, self.single, self.binary, self.defaultValue, self.customMust]
    
    def getDataObject(self, serverMeta, baseDN):
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
    