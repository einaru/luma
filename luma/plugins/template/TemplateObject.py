'''
Created on 16. mars 2011

@author: Simen
'''
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
        [],     # 4 Attributes
        ]
    
    #Returns the entire list
    def getList(self):
        return self._dataHolder
    
    #Given an index to the _dataHolder, sets the value
    def setIndexToValue(self, index, value):
        self._dataHolder[index] = value

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
    def port(self, description):
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