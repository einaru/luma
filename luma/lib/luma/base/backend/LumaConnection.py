# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import ldap

import environment
from base.backend.ServerObject import ServerObject

class LumaConnectionException(Exception):
    """Will be raised is no proper server object is passed to the constructor.
    """
    pass

    

class LumaConnection(object):
    """ This class is a wrapper around the ldap functions. It is provided to access ldap 
    data easier.
    
    Parameter is a ServerObject which contains all meta information for accessing servers.
    """
    
    def __init__(self, serverMeta=None):
        # Throw exception if no ServerObject is passed.
        if not (isinstance(serverMeta, ServerObject)):
            exceptionString = "Expected ServerObject type. Passed object was "
            exceptionString = exceptionString + str(type(serverMeta))
            raise LumaConnectionException, exceptionString
        
        self.server = serverMeta
        
        # This ldap object will be assigned in the methods.
        # This way we have better control over bind, unbind and open sockets.
        self.ldapServerObject = None
        
###############################################################################

    def search_s(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None):
        """Synchronous search.
        """
        
        searchResult = None
        environment.setBusy(1)
        
        try:
            searchResult = self.ldapServerObject.search_s(base, scope, filter, attrList)
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            
        environment.setBusy(0)
        return searchResult

###############################################################################

    def search(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None, attrsonly=0):
        """Aynchronous search.
        """
    
        searchResult = []
        environment.setBusy(1)
        
        try:
            resultId = self.ldapServerObject.search(base, scope, filter, attrList, attrsonly)
            
            while 1:
                environment.updateUI()
                result_type, result_data = self.ldapServerObject.result(resultId, 0)
                
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        for x in result_data:
                            searchResult.append(x)

        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
         
        environment.setBusy(0)
            
        if len(searchResult) == 0:
            return None
        else:
            return searchResult
            
###############################################################################

    def delete_s(self, dnDelete=None):
        """Synchronous delete.
        """
        
        if dnDelete == None:
            return
            
        result = None
        environment.setBusy(1)
        
        try:
            self.ldapServerObject.delete_s(dnDelete)
            environment.setBusy(0)
            return 1
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            environment.setBusy(0)
            return 0
            
###############################################################################

    def modify_s(self, dn, modlist=None):
        """Synchronous modify.
        """
        
        if modlist == None:
            return 0
            
        environment.setBusy(1)
        try:
            self.ldapServerObject.modify_s(dn, modlist)
            environment.setBusy(0)
            return 1
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            environment.setBusy(0)
            return 0

###############################################################################

    def add_s(self, dn, modlist):
        """Synchronous add.
        """
        
        environment.setBusy(1)
        
        
        try:
            searchResult = self.ldapServerObject.add_s(dn, modlist)
            environment.setBusy(0)
            return 1
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            environment.setBusy(0)
            return 0

###############################################################################

    def bind(self):
        """Bind to server.
        """
        
        try:
            self.ldapServerObject = ldap.open(self.server.host, self.server.port)
            self.ldapServerObject.protocol_version = ldap.VERSION3
            if self.server.tls:
                self.ldapServerObject.start_tls_s()
            if not(self.server.bindAnon):
                self.ldapServerObject.simple_bind_s(self.server.bindDN,self.server.bindPassword)
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            
###############################################################################

    def unbind(self):
        """Unbind from server.
        """
        
        try:
            if not(self.server.bindAnon):
                self.ldapServerObject.unbind()
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
