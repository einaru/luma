# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003, 2004 by Wido Depping                                      
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
    
    # schema-cache of all servers whose schema has been requested already
    serverMetaCache = {}
    
    def __init__(self, server=None):
        # Dictionaries with lowercase names of attributes and objectclasses
        self.objectClassesDict = {}
        self.attributeDict = {}
        
        # alias name of the current server
        self.SERVER = server
        
        # automaticly retrieve schema info if server data is passed 
        # upon initialization
        if not (server == None):
            self.retrieveInfoFromServer()

###############################################################################

    def retrieveInfoFromServer(self):
        """ Retrieve all information of objectClassesDict and attributes from the
        server.
        """
        
        environment.setBusy(True)
        
        # Try to get server schema information from the cache
        if self.SERVER in self.serverMetaCache.keys():
            self.objectClassesDict = self.serverMetaCache[self.SERVER]["objectClassesDict"]
            self.attributeDict = self.serverMetaCache[self.SERVER]["attributeDict"]
        else:
            tmpObject = ServerList()
            tmpObject.readServerList()
            serverMeta = tmpObject.getServerObject(self.SERVER)

            try:
                # FIXME: is this right? it only checks normal and ssl transport
                # what about other methods?
                method = "ldap://"
                if serverMeta.tls:
                    method = "ldaps://"
                tmpUrl = method + serverMeta.host + ":" + str(serverMeta.port)
                
                subschemasubentry_dn,schema = ldap.schema.urlfetch(tmpUrl)
                
                # get objectclass information
                oidList = schema.listall(ldap.schema.ObjectClass)
                for x in oidList:
                    environment.updateUI()
                    y = schema.get_obj(ldap.schema.ObjectClass, x)
                
                    # detect kind of objectclass
                    kind = ""
                    if 0 == y.kind:
                        kind = "STRUCTURAL"
                    elif 1 == y.kind:
                        kind = "ABSTRACT"
                    elif 2 == y.kind:
                        kind = "AUXILIARY"
                
                    # name of objectclass
                    desc = ""
                    if not (y.desc == None):
                        desc = y.desc
                    
                    # must attributes of the objectclass
                    must = []
                    if not (len(y.must) == 0):
                        must = y.must
                    
                    # may attributes of the objectclass
                    may = []
                    if not (len(y.may) == 0):
                        may = y.may
                     
                    # parents of the objectclass
                    # beware that not the whole class chain is given. only
                    # the first class above the current
                    parents = []
                    for parent in y.sup:
                        # filter out objectclass top. all classes are 
                        # derived from top
                        if not ("top" == string.lower(parent)):
                            parents.append(string.lower(parent))
                    
                    # store values for each name the current class has.
                    # IMPORTANT: the key is always lowercase
                    for name in y.names:
                        self.objectClassesDict[string.lower(name)] = {"DESC": desc, 
                            "MUST": must, "MAY": may, "NAME": name, "KIND": kind,
                            "PARENTS": parents}
                                
                
                # get attribute information
                oidList = schema.listall(ldap.schema.AttributeType)
                for x in oidList:
                    environment.updateUI()
                    y = schema.get_obj(ldap.schema.AttributeType, x)
                    
                    nameList = y.names
                    for z in nameList:
                        self.attributeDict[string.lower(z)] = {"DESC": y.desc, 
                            "SINGLE": y.single_value, "SYNTAX": y.syntax,
                            "NAME": z}
            
                #oidList = schema.listall(ldap.schema.LDAPSyntax)
                #for x in oidList:
                #    environment.updateUI()
                #    y = schema.get_obj(ldap.schema.LDAPSyntax, x)
                #    print y.desc
                
                # store retrieved information in the cache
                metaData = {}
                metaData['objectClassesDict'] = self.objectClassesDict
                metaData['attributeDict'] = self.attributeDict
                self.__class__.serverMetaCache[self.SERVER] = metaData
                
            except ldap.LDAPError, e:
                print "Error during LDAP request"
                print "Reason: " + str(e)
            
        environment.setBusy(False)

###############################################################################

    def getAllAttributes(self, classList = None):
        """ Return two sets of all attributes which the server supports for the 
        given classList.
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
        """ Returns two sets of objectClasses that either MUST
            or MAY use the given attribute
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
                    may.add(self.objectClassesDict[key]["NAME"])

        return must, may

        
###############################################################################

    def isSingle(self, attribute = ""):
        """ Check if an attribute is single.
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
            tmpList = self.objectClassesDict[string.lower(x)]["MUST"]
            tmpList = map(lambda tmpString: string.lower(tmpString), tmpList)
            if attribute in tmpList:
                value = True
                break
        
        return value
        
###############################################################################

    def isStructural(self, objectClass):
        """ Check if the given objectClass is structural.
        """
        
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
        """ Returns a boolean wether the given objectClass is present 
        in the schema.
        """

        return self.objectClassesDict.has_key(string.lower(objectClass))

###############################################################################

    def getObjectClasses(self):
        """ Returns a list of all objectClasses the schema supports.
        """
        
        return map(lambda x: self.objectClassesDict[x]["NAME"],self.objectClassesDict.keys())

###############################################################################

    def matchingRule(self, attribute):
        """ Return which syntax the attribute has.
        """
        
        attribute = string.lower(attribute)
        if not self.attributeDict.has_key(attribute):
            return None
            
        return self.attributeDict[attribute]["SYNTAX"]

###############################################################################

    def getParents(self, className=None):
        """ Returns the complete parentclass chain for className, except 'top'.
        """
        
        if None == className:
            return None
          
        className = string.lower(className)
    
        parentList = []
        tmpList = self.objectClassesDict[className]["PARENTS"]
        
        while len(tmpList) > 0:
            currentClass = string.lower(tmpList[0])
            tmpList += self.objectClassesDict[currentClass]["PARENTS"]
            parentList.append(self.objectClassesDict[currentClass]['NAME'])
            del tmpList[0]
        
        return parentList
        
###############################################################################

    def sameObjectClassChain(self, firstClass, secondClass):
        """ Returns if two objectClasses belong to the same class chain.
        """
        
        firstClass = string.lower(firstClass)
        secondClass = string.lower(secondClass)
        
        firstParents = self.getParents(firstClass)
        secondParents = self.getParents(secondClass)
        
        if self.objectClassesDict[firstClass]['NAME'] in secondParents:
            return True
        elif self.objectClassesDict[secondClass]['NAME'] in firstParents:
            return True
        else:
            return False

###############################################################################

    def classAllowed(self, className, classList):
        """ Returns if className can be added to classList.
        """
        
        allowedBool = True
                
        for x in classList:
            if not self.sameObjectClassChain(className, x):
                allowedBool = False
                        
        return allowedBool

