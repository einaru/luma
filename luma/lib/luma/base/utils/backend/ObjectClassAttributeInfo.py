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

from base.backend.ServerList import ServerList
import environment

class ObjectClassAttributeInfo(object):
    """ A class for getting information about objectclasses and attributes 
    from a server.
    """

###############################################################################
    
    def __init__(self, server=None):
        self.BINARY_SYNTAXES = {
            '1.3.6.1.4.1.1466.115.121.1.4':None,  # Audio
            '1.3.6.1.4.1.1466.115.121.1.5':None,  # Binary
            '1.3.6.1.4.1.1466.115.121.1.6':None,  # Bit String
            '1.3.6.1.4.1.1466.115.121.1.8':None,  # Certificate
            '1.3.6.1.4.1.1466.115.121.1.9':None,  # Certificate List
            '1.3.6.1.4.1.1466.115.121.1.10':None, # Certificate Pair
            '1.3.6.1.4.1.1466.115.121.1.23':None, # G3 FAX
            '1.3.6.1.4.1.1466.115.121.1.28':None, # JPEG
            '1.3.6.1.4.1.1466.115.121.1.40':None, # Octet String
            '1.3.6.1.4.1.1466.115.121.1.49':None, # Supported Algorithm
            }
        self.OBJECTCLASSES = {}
        self.ATTRIBUTELIST = {}
        self.SERVER = server
        
        if not (server == None):
            self.retrieve_info_from_server()

###############################################################################

    def retrieve_info_from_server(self):
        """ Retrieve all information of objectclasses and attributes from the
        server.
        """
        
        tmpObject = ServerList()
        tmpObject.readServerList()
        serverMeta = ""
        serverMeta = tmpObject.get_serverobject(self.SERVER)

        environment.set_busy(1)

        try:
            tmpUrl = "ldap://" + serverMeta.host + ":" + str(serverMeta.port)
            subschemasubentry_dn,schema = ldap.schema.urlfetch(tmpUrl)
            oidList = schema.listall(ldap.schema.ObjectClass)
            
            for x in oidList:
                environment.update_ui()
                y = schema.get_obj(ldap.schema.ObjectClass, x)
                name = y.names[0]
                desc = ""
                
                
                if not (y.desc == None):
                    desc = y.desc
                must = []
                
                if not (len(y.must) == 0):
                    must = y.must
                may = []
                
                if not (len(y.may) == 0):
                    may = y.may
                    
                self.OBJECTCLASSES[name] = {"DESC": desc, "MUST": must, "MAY": may}

            oidList = schema.listall(ldap.schema.AttributeType)
            
            for x in oidList:
                environment.update_ui()
                y = schema.get_obj(ldap.schema.AttributeType, x)
                name = y.names
                desc = ""
                
                if not (y.desc == None):
                    desc = y.desc
                    
                single = y.single_value
                
                for z in name:
                    self.ATTRIBUTELIST[z] = {"DESC": desc, "SINGLE": single, "SYNTAX": y.syntax}
                    
                    
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            
        environment.set_busy(0)

###############################################################################

    def set_server(self, server):
        """ Set the server from which we want to get the infos.
        """
        
        self.SERVER = server[:]

###############################################################################

    def update(self):
        """ Re-read all informations.
        """
        
        self.OBJECTCLASSES = {}
        self.ATTRIBUTELIST = []
        self.retrieve_info_from_server()

###############################################################################

    def get_all_attributes(self, classList = None):
        """ Return a list of all attributes which the server supports.
        """
        
        allAttributes = []
        
        for x in classList:
            if not(self.OBJECTCLASSES.has_key(x)):
                continue
            must = self.OBJECTCLASSES[x]["MUST"]
            may = self.OBJECTCLASSES[x]["MAY"]
            
            if not (len(must) == 0):
                for y in must:
                    allAttributes.append(y)
                    
            if not (len(may) == 0):
                for y in may:
                    allAttributes.append(y)
                    
        return allAttributes

###############################################################################

    def get_all_musts(self, classList = None):
        """ Returns a list of all attributes which are needed by the 
        objectclasses given by classList.
        """
        
        allAttributes = []
        
        for x in classList:
            must = self.OBJECTCLASSES[x]["MUST"]
            
            if not (len(must) == 0):
                for y in must:
                    allAttributes.append(y)
                    
        return allAttributes

###############################################################################

    def get_all_mays(self, classList = None):
        """ Returns a list of all attributes which are optional for the 
        objectclasses given by classList.
        """
        
        allAttributes = []
        for x in classList:
            may = self.OBJECTCLASSES[x]["MAY"]
            
            if not (len(may) == 0):
                for y in may:
                    allAttributes.append(y)
                    
        return allAttributes

###############################################################################

    def is_single(self, attribute = ""):
        """ Check if a attribute must be single.
        """
        
        if self.ATTRIBUTELIST.has_key(attribute):
             val = self.ATTRIBUTELIST[attribute]["SINGLE"]
             return val
        else:
            return 0

###############################################################################

    def is_must(self, attribute="", objectClasses = None):
        """ Check if the given attribute must be set.
        """
        
        if objectClasses == None:
            raise "Missing Arguments to Funktion 'is_must(attribute, objectClasses)"
        else:
            for x in objectClasses:
                for y in self.OBJECTCLASSES[x]["MUST"]:
                    if y == attribute:
                        return 1
        return 0
        
###############################################################################

    def is_binary(self, attribute=""):
        """ Check if the given attribute has binary values.
        """
    
        if self.ATTRIBUTELIST.has_key(attribute):
            syntax = self.ATTRIBUTELIST[attribute]["SYNTAX"]
            if self.BINARY_SYNTAXES.has_key(syntax):
                return 1
            else:
                return 0
        else:
            return 0

###############################################################################

    def has_objectClass(self, objectClass):
        if objectClass in self.OBJECTCLASSES.keys():
            return 1
        else:
            return 0
        
###############################################################################

    def update_ui(self):
        """ Updates the progress bar of the GUI and keeps it responsive.
        """
        
        qApp.processEvents()
        progress = self.pBar.progress()
        self.pBar.setProgress(progress + 1)









