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
import ldapurl

import re
import string
from sets import Set
from copy import copy
import threading
import time

from base.backend.ServerList import ServerList
import environment
from base.utils.backend.LogObject import LogObject

SCHEMA_CLASS_MAPPING = ldap.cidict.cidict()
SCHEMA_ATTRS = SCHEMA_CLASS_MAPPING.keys()

class UnknownAttribute(object):
    pass

class ObjectClassAttributeInfo(object):
    """ A class for getting information about objectClassesDict and attributes 
    from a server.
    """
    
    # schema-cache of all servers whose schema has been requested already
    serverMetaCache = {}
    
    def __init__(self, serverMeta=None):
        # Dictionaries with lowercase names of attributes and objectclasses
        self.objectClassesDict = {}
        self.attributeDict = {}
        self.matchingDict = {}
        self.syntaxDict = {}
        
        # Indicates if an error has occured while fetching the schemas
        self.failure = False
        
        # Exception object why fetching schema failed
        self.failureException = None
        
        
        # alias name of the current server
        self.serverMeta = serverMeta
        
        # automaticly retrieve schema info if server data is passed 
        # upon initialization
        if not (serverMeta == None):
            self.retrieveInfoFromServer()

###############################################################################

    def retrieveInfoFromServer(self):
        """ Retrieve all information of objectClassesDict and attributes from the
        server.
        """
        
        environment.setBusy(True)
        
        # Try to get server schema information from the cache
        if self.serverMeta.name in self.serverMetaCache.keys():
            self.objectClassesDict = self.serverMetaCache[self.serverMeta.name]["objectClassesDict"]
            self.attributeDict = self.serverMetaCache[self.serverMeta.name]["attributeDict"]
            self.syntaxDict = self.serverMetaCache[self.serverMeta.name]["syntaxDict"]
            self.matchingDict = self.serverMetaCache[self.serverMeta.name]["matchingDict"]
        else:
            tmpObject = ServerList()
            tmpObject.readServerList()
            serverMeta = self.serverMeta
            
            workerThread = WorkerThreadFetch(serverMeta)
            workerThread.start()
        
            while not workerThread.FINISHED:
                environment.updateUI()
                time.sleep(0.05)
        
            if None == workerThread.exceptionObject:
                self.objectClassesDict = workerThread.objectClassesDict
                self.attributeDict = workerThread.attributeDict
                self.syntaxDict = workerThread.syntaxDict
                self.matchingDict = workerThread.matchingDict
            
                # store retrieved information in the cache
                metaData = {}
                metaData['objectClassesDict'] = self.objectClassesDict
                metaData['attributeDict'] = self.attributeDict
                metaData['syntaxDict'] = self.syntaxDict
                metaData['matchingDict'] = self.matchingDict
                self.__class__.serverMetaCache[self.serverMeta.name] = metaData
                tmpString = "Schema information for server " + self.serverMeta.name + " retrieved."
                environment.logMessage(LogObject("Info", tmpString))
            else:
                tmpString = "Could not fetch LDAP schema from server. Reason:\n"
                tmpString += str(workerThread.exceptionObject)
                environment.logMessage(LogObject("Error", tmpString))

        environment.setBusy(False)

###############################################################################

    def getAttributeList(self):
        """ Returns a list of all attributes the server supports.
        """
        
        return map(lambda x: x["NAME"], self.attributeDict.values())
        
###############################################################################

    def getAllAttributes(self, classList = None):
        """ Return two sets of all attributes which the server supports for the 
        given classList.
        """
        
        must = Set()
        may = Set()
        
        classList = self.getClassesWithParents(classList)
        
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
        
        classList = self.getClassesWithParents(classList)
        
        for x in classList:
            must |= Set(self.objectClassesDict[string.lower(x)]["MUST"])
            
        return must

###############################################################################

    def getAllMays(self, classList = None):
        """ Returns a set of all attributes which are optional for the 
        objectClassesDict given by classList.
        """
        
        may = Set()
        
        classList = self.getClassesWithParents(classList)
        
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
        
        if ";binary" == attribute[-7:]:
            attribute = attribute[:-7]
        
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
        
        if ";binary" == attribute[-7:]:
            attribute = attribute[:-7]
        
        if attribute in self.attributeDict:
            return self.attributeDict[attribute]["SINGLE"]
        else:
            return False

###############################################################################

    def isMust(self, attribute="", classList = None):
        """ Check if the given attribute must be set.
        """
        
        if classList == None:
            raise "Missing Arguments to Funktion 'isMust(attribute, objectClassesDict)"

        attribute = string.lower(attribute)
        
        if ";binary" == attribute[-7:]:
            attribute = attribute[:-7]
        
        classList = self.getClassesWithParents(classList)
        
        value = False
        for x in classList:
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
            
        if ";binary" == attribute[-7:]:
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
        
        if ";binary" == attribute[-7:]:
            attribute = attribute[:-7]
        
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
        
        if "top" == className:
            return []
    
        parentList = []
        tmpList = copy(self.objectClassesDict[className]["PARENTS"])
        
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
        
###############################################################################

    def getClassesWithParents(self, classList):
        """ Returns the given classes together with their parents in a set.
        """
        
        classSet = Set()
        for x in classList:
            tmpList = self.getParents(x)
            classSet.add(x)
            for y in tmpList:
                classSet.add(y)
                
        return classSet
        
###############################################################################

    def attributeAllowed(self, attributeName, classList):
        """ Returns a boolean if the attribute attributeName is allowed with the
        classes given by classList.
        """
        
        classList = self.getClassesWithParents(classList)
        
        mustSet, maySet = self.getAllAttributes(classList)
        newSet = mustSet.union(maySet)
        
        if ";binary" == attributeName[-7:]:
            attributeName = attributeName[:-7]
        
        if attributeName in newSet:
            return True
        else:
            return False

###############################################################################

    def getSyntaxList(self):
        """ Returns the list of supported syntaxes by the server.
        """
        
        return self.syntaxDict.keys()
        
###############################################################################

    def getAttributeListForSyntax(self, syntaxString):
        """ Returns a list of attributes which use the syntax given 
        by syntaxString.
        """
        
        tmpList = self.getAttributeList()
        attributeList = []
        
        for x in tmpList:
            dataDict = self.attributeDict[string.lower(x)]
            if dataDict["SYNTAX"] == syntaxString:
                attributeList.append(x)
                
        return attributeList
        
###############################################################################

    def getMachtingListForSyntax(self, syntaxString):
        """ Returns a list of matching rules for the given syntax.
        """
        
        tmpList = self.getMachtingList()
        matchingList = []
        
        for x in tmpList:
            dataDict = self.matchingDict[string.lower(x)]
            if dataDict["SYNTAX"] == syntaxString:
                matchingList.append(x)
                
        return matchingList
        
###############################################################################

    def getMachtingList(self):
        """ Returns a list of matching rules supported by the server.
        """
        
        return map(lambda x: self.matchingDict[x]['NAME'], self.matchingDict.keys())
        
###############################################################################

    def getMatchingRuleList(self):
        """ Returns a list of matching rules supported by the server.
        """
        
        return map(lambda x: self.matchingDict[x]['NAME'], self.matchingDict.keys())
        
###############################################################################

    def getAttributeListForMatchingRule(self, matchingString):
        """ Returns a list of attributes which use the matching rule given
        by matchingString.
        """
        
        tmpList = self.getAttributeList()
        attributeList = []
        
        for x in tmpList:
            dataDict = self.attributeDict[string.lower(x)]
            if dataDict["EQUALITY"] == matchingString:
                attributeList.append(x)
                
        return attributeList
        
###############################################################################
###############################################################################
        
class WorkerThreadFetch(threading.Thread):
    
    def __init__(self, serverMeta):
        threading.Thread.__init__(self)
        self.serverMeta = serverMeta
            
        self.FINISHED = False
        self.exceptionObject = None
        
        self.objectClassesDict = {}
        self.attributeDict = {}
        self.syntaxDict = {}
        self.matchingDict = {}
        
    def run(self):
        try:
            # Check whether we want to validate the server certificate.
            validateMethod = ldap.OPT_X_TLS_DEMAND
            if self.serverMeta.checkServerCertificate == u"demand":
                validateMethod = ldap.OPT_X_TLS_DEMAND
            elif self.serverMeta.checkServerCertificate == u"never":
                validateMethod = ldap.OPT_X_TLS_NEVER
            elif self.serverMeta.checkServerCertificate == u"try":
                validateMethod = ldap.OPT_X_TLS_TRY
            elif self.serverMeta.checkServerCertificate == u"allow":
                validateMethod = ldap.OPT_X_TLS_ALLOW
                
            if self.serverMeta.encryptionMethod == "SSL":
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, validateMethod)
            elif self.serverMeta.encryptionMethod == "TLS":
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, validateMethod)
            else:
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        
            whoVal = None
            credVal = None
            if not (self.serverMeta.bindAnon):
                whoVal = self.serverMeta.bindDN
                credVal = self.serverMeta.bindPassword
                
                
            ldapSession = None
                
            if u"SASL EXTERNAL" == self.serverMeta.authMethod:
                urlschemeVal = "ldapi"
                url = ldapurl.LDAPUrl(urlscheme=urlschemeVal, 
                hostport = self.serverMeta.host.replace("/", "%2F").replace(",", "%2C"),
                who = whoVal, cred = credVal)
                    
                ldapSession = ldap.initialize(url.initializeUrl())
                ldapSession.protocol_version = ldap.VERSION3
                
                if self.serverMeta.encryptionMethod == "TLS":
                    ldapSession.start_tls_s()
                    
                sasl_cb_value_dict = {}
                sasl_cb_value_dict[ldap.sasl.CB_AUTHNAME] = whoVal
                sasl_cb_value_dict[ldap.sasl.CB_PASS] = credVal
                sasl_auth = ldap.sasl.sasl(sasl_cb_value_dict, "EXTERNAL")
                    
                ldapSession.sasl_interactive_bind_s("", sasl_auth)
            else:
                urlschemeVal = "ldap"
                if self.serverMeta.encryptionMethod == "SSL":
                    urlschemeVal = "ldaps"
                        
                url = ldapurl.LDAPUrl(urlscheme=urlschemeVal, 
                    hostport = self.serverMeta.host + ":" + str(self.serverMeta.port),
                    who = whoVal, cred = credVal)
                    
                ldapSession = ldap.initialize(url.initializeUrl())
                ldapSession.protocol_version = ldap.VERSION3
                
                if self.serverMeta.encryptionMethod == "TLS":
                    ldapSession.start_tls_s()
                
                
                if self.serverMeta.bindAnon:
                    ldapSession.simple_bind()
                elif self.serverMeta.authMethod == u"Simple":
                    ldapSession.simple_bind(whoVal, credVal)
                elif u"SASL" in self.serverMeta.authMethod:
                    sasl_cb_value_dict = {}
                    if not u"GSSAPI" in self.serverMeta.authMethod:
                        sasl_cb_value_dict[ldap.sasl.CB_AUTHNAME] = whoVal
                        sasl_cb_value_dict[ldap.sasl.CB_PASS] = credVal
                    
                    sasl_mech = None
                    if self.serverMeta.authMethod == u"SASL Plain":
                        sasl_mech = "PLAIN"
                    elif self.serverMeta.authMethod == u"SASL CRAM-MD5":
                        sasl_mech = "CRAM-MD5"
                    elif self.serverMeta.authMethod == u"SASL DIGEST-MD5":
                        sasl_mech = "DIGEST-MD5"
                    elif self.serverMeta.authMethod == u"SASL Login":
                        sasl_mech = "LOGIN"
                    elif self.serverMeta.authMethod == u"SASL GSSAPI":
                        sasl_mech = "GSSAPI"
                    
                    sasl_auth = ldap.sasl.sasl(sasl_cb_value_dict,sasl_mech)
                    ldapSession.sasl_interactive_bind_s("", sasl_auth)
                
            subschemasubentry_dn = ldapSession.search_subschemasubentry_s(url.dn)
            if subschemasubentry_dn is None:
                subschemasubentry_entry = None
            else:
                if url.attrs is None:
                    schema_attrs = SCHEMA_ATTRS
                else:
                    schema_attrs = url.attrs
                subschemasubentry_entry = ldapSession.read_subschemasubentry_s(
                    subschemasubentry_dn,attrs=schema_attrs)
            ldapSession.unbind_s()
                
            schema = None
            if subschemasubentry_dn!=None:
                schema = ldap.schema.SubSchema(subschemasubentry_entry)
            else:
                schema = None
                
                
            # get objectclass information
            oidList = schema.listall(ldap.schema.ObjectClass)
            for x in oidList:
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
                            
                oid = ""
                if not (y.oid == None):
                    oid = y.oid
                            
                # store values for each name the current class has.
                # IMPORTANT: the key is always lowercase
                for name in y.names:
                    self.objectClassesDict[string.lower(name)] = {"DESC": desc, 
                        "MUST": must, "MAY": may, "NAME": name, "KIND": kind,
                        "PARENTS": parents, "OID": oid}
                            
                
            # get attribute information
            oidList = schema.listall(ldap.schema.AttributeType)
            for x in oidList:
                y = schema.get_obj(ldap.schema.AttributeType, x)
                    
                nameList = y.names
                for z in nameList:
                    self.attributeDict[string.lower(z)] = {"DESC": y.desc, 
                        "SINGLE": y.single_value, "SYNTAX": y.syntax,
                        "NAME": z, "COLLECTIVE": y.collective, 
                        "EQUALITY": y.equality, "OBSOLETE": y.obsolete,
                        "OID": y.oid, "ORDERING": y.ordering, "SUP": y.sup,
                        "SYNTAX_LEN": y.syntax_len, "USAGE": y.usage}
            
            # get syntax information
            oidList = schema.listall(ldap.schema.LDAPSyntax)
            for x in oidList:
                y = schema.get_obj(ldap.schema.LDAPSyntax, x)
                self.syntaxDict[x] = {"DESC": y.desc, "OID": y.oid}
                        
                
            # get matching information
            oidList = schema.listall(ldap.schema.MatchingRule)
            for x in oidList:
                y = schema.get_obj(ldap.schema.MatchingRule, x)
                for z in y.names:
                    self.matchingDict[string.lower(z)] = {"DESC": y.desc, "OID": y.oid,
                        "OBSOLETE": y.obsolete, "SYNTAX": y.syntax,
                        "NAME": z}
                
            self.FINISHED = True
            
        except Exception, e:
            self.FINISHED = True
            self.exceptionObject = e
        
        
        
        
        
