# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import ldap
import ldap.schema
import re
import string
from sets import Set

from base.backend.ServerList import ServerList
import environment

class UnknownAttribute(object):
    pass

class ObjectClassAttributeInfo(object):
    """ A class for getting information about objectClassesDict and attributes 
    from a server.
    """
    
    serverMetaCache = {}
    
    def __init__(self, server=None):
        self.objectClassesDict = {}
        self.attributeDict = {}
        self.SERVER = server
        
        if not (server == None):
            self.retrieveInfoFromServer()

###############################################################################

    def retrieveInfoFromServer(self):
        """ Retrieve all information of objectClassesDict and attributes from the
        server.
        """
        
        # Try to get server schema information from the cache.
        if self.SERVER in self.serverMetaCache.keys():
            self.objectClassesDict = self.serverMetaCache[self.SERVER]["objectClassesDict"]
            self.attributeDict = self.serverMetaCache[self.SERVER]["attributeDict"]
        else:
            tmpObject = ServerList()
            tmpObject.readServerList()
            serverMeta = tmpObject.getServerObject(self.SERVER)

            environment.setBusy(1)

            try:
                method = "ldap://"
                if serverMeta.tls:
                    method = "ldaps://"
                tmpUrl = method + serverMeta.host + ":" + str(serverMeta.port)
                subschemasubentry_dn,schema = ldap.schema.urlfetch(tmpUrl)
            
                oidList = schema.listall(ldap.schema.ObjectClass)
                for x in oidList:
                    environment.updateUI()
                    y = schema.get_obj(ldap.schema.ObjectClass, x)
                
                
                    kind = ""
                    if 0 == y.kind:
                        kind = "STRUCTURAL"
                    elif 1 == y.kind:
                        kind = "ABSTRACT"
                    elif 2 == y.kind:
                        kind = "AUXILIARY"
                
                    desc = ""
                    if not (y.desc == None):
                        desc = y.desc
                    
                    must = []
                    if not (len(y.must) == 0):
                        must = y.must
                    
                    may = []
                    if not (len(y.may) == 0):
                        may = y.may
                
                    for name in y.names:
                        self.objectClassesDict[string.lower(name)] = {"DESC": desc, 
                            "MUST": must, "MAY": may, "NAME": name, "KIND": kind}
                                

                oidList = schema.listall(ldap.schema.AttributeType)
                for x in oidList:
                    environment.updateUI()
                    y = schema.get_obj(ldap.schema.AttributeType, x)
                    name = y.names
                
                    for z in name:
                        self.attributeDict[string.lower(z)] = {"DESC": y.desc, 
                            "SINGLE": y.single_value, "SYNTAX": y.syntax,
                            "NAME": z}
            
                #oidList = schema.listall(ldap.schema.LDAPSyntax)
                #for x in oidList:
                #    environment.updateUI()
                #    y = schema.get_obj(ldap.schema.LDAPSyntax, x)
                #    print y.desc
                
                metaData = {}
                metaData['objectClassesDict'] = self.objectClassesDict
                metaData['attributeDict'] = self.attributeDict
                self.__class__.serverMetaCache[self.SERVER] = metaData
                
            except ldap.LDAPError, e:
                print "Error during LDAP request"
                print "Reason: " + str(e)
            
            environment.setBusy(0)

###############################################################################

    def setServer(self, server):
        """ Set the server from which we want to get the infos.
        """
        
        self.SERVER = server[:]

###############################################################################

    def update(self):
        """ Re-read all informations.
        """
        
        self.objectClassesDict = {}
        self.attributeDict = []
        self.retrieveInfoFromServer()

###############################################################################

    def getAllAttributes(self, classList = None):
        """ Return two sets of all attributes which the server supports.
        """
        must = Set()
        may = Set()
        
        for x in classList:
            x = string.lower(x)
            if not x in self.objectClassesDict:
                continue
            must |= Set(self.objectClassesDict[x]["MUST"])
            may |= Set(self.objectClassesDict[x]["MAY"])
           
        return must, may

###############################################################################

    def getAllMusts(self, classList = None):
        """ Returns a set of all attributes which are needed by the 
        objectClassesDict given by classList.
        """
        
        must = Set()
        
        for x in classList:
            must |= Set(self.objectClassesDict[string.lower(x)]["MUST"])
            
        return must

###############################################################################

    def getAllMays(self, classList = None):
        """ Returns a set of all attributes which are optional for the 
        objectClassesDict given by classList.
        """
        
        may = Set()
        
        for x in classList:
            may |= Set(self.objectClassesDict[string.lower(x)]["MAY"])
            
        return may

###############################################################################
    def getAllObjectclassesForAttr(self,attribute=""):
        """ Returns two sets of objectClassesDict that either MUST
            or MAY use a given attribute
        """
        must = Set()
        may = Set()
        
        attribute = string.lower(attribute)
        
        for (key,value) in self.objectClassesDict.items():
            for x in value['MUST']:
                if attribute == string.lower(x):
                    must.add(self.objectClassesDict[key]["NAME"])
            
            for x in value['MAY']:
                if attribute == string.lower(x):
                    must.add(self.objectClassesDict[key]["NAME"])

        return must, may

        
###############################################################################

    def isSingle(self, attribute = ""):
        """ Check if a attribute must be single.
        """
        
        attribute = string.lower(attribute)
        
        if attribute in self.attributeDict:
            return self.attributeDict[attribute]["SINGLE"]
        else:
            return False

###############################################################################

    def isMust(self, attribute="", objectClassesDict = None):
        """ Check if the given attribute must be set.
        """

        if objectClassesDict == None:
            raise "Missing Arguments to Funktion 'isMust(attribute, objectClassesDict)"

        attribute = string.lower(attribute)
        value = False
        
        for x in objectClassesDict:
            x = string.lower(x)
            for y in self.objectClassesDict[x]["MUST"]:
                if attribute == string.lower(y):
                    value = True
        
        return value
        
###############################################################################

    def isStructural(self, objectClass):
        objectClass = string.lower(objectClass)
        if "STRUCTURAL" == self.objectClassesDict[objectClass]["KIND"]:
            return True
        else:
            return False
        
###############################################################################

    def isBinary(self, attribute=""):
        """ Check if the given attribute has binary values.
        """
        
        retVal = False
        attribute = string.lower(attribute)
    
        if attribute in self.attributeDict:
            syntax = self.attributeDict[attribute]["SYNTAX"]
            if syntax in ldap.schema.NOT_HUMAN_READABLE_LDAP_SYNTAXES : 
                retVal = True
            
        return retVal

###############################################################################

    def hasObjectClass(self, objectClass):
        objectClass = string.lower(objectClass)
        return objectClass in self.objectClassesDict.keys()

###############################################################################

    def getObjectClasses(self):
        return map(lambda x: self.objectClassesDict[x]["NAME"],self.objectClassesDict.keys())

###############################################################################

    def matchingRule(self, attribute):
        """ Return which syntax the attribute has.
        """
        
        if not self.attributeDict.has_key(attribute):
            return None
            
        return self.attributeDict[attribute]["SYNTAX"]

###############################################################################

    def encodeAttributeValue(self, attribute=None, value=None):
        if (attribute == None) or (value == None):
            return None

        returnValue = None
        
        if false:
            pass
        else:
            returnValue = value
        
        return returnValue
###############################################################################

    def decodeAttributeValue(self, attribute=None, value=None):
        if (attribute == None) or (value == None):
            return None
            
        returnValue = None
        
        if false:
            pass
        else:
            returnValue = value
        
        return returnValue
            



