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
    
    def __init__(self):
        
        # Holds the data about the server
        # Used for easy mapping to model-columns

        self._dataHolder = [
                #Index - Description (Options)
        u"name",    # 0 Template name
        u"server",    # 1 Server
        u"desc",    # 2 Description
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
        if not self.objectclasses.contains(objectclass):
            self.objectclasses.append(objectclass)
    
    def deleteObjectclass(self, objectclass):
        self.objectclasses.remove(objectclass)

    def addAttribute(self, name, must, single, binary, defaultValue):
        self.attributes[name] = AttributeObject(name, must, single, binary, defaultValue)

    def deleteAttribute(self, attributeName):
        self.attributes.pop(attributeName, None)
        
    def setAttributeDefaultValue(self, attributeName, value):
        self.attributes[attributeName].defaultValue = value

    def getDataObject(self, serverMeta, baseDN):
        """
        Create a data structure which can be used by python-ldap and return it.
        """
    
        dataObject = {}
        dataObject['objectClass'] = copy.deepcopy(self.objectClasses)
        
        for x in self.attributes.keys():
            attributeObject = self.attributes[x]
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
    def __init__(self, name="", must=False, single=False, binary=False, defaultValue=None):
        self.attributeName = name
        self.must = must
        self.single = single
        self.binary = binary
        self.defaultValue = defaultValue
        