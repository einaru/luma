# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003, 2004 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import ldap
import ldapurl

import environment
from base.backend.ServerObject import ServerObject

class LumaConnectionException(Exception):
    """This exception class will be raised if no proper server object is passed 
    to the constructor.
    """
    
    pass

    

class LumaConnection(object):
    """ This class is a wrapper around the ldap functions. It is provided to 
    access ldap data easier.
    
    Parameter is a ServerObject which contains all meta information for 
    accessing servers.
    """
    
    def __init__(self, serverMeta=None):
        # Throw exception if no ServerObject is passed.
        if not (isinstance(serverMeta, ServerObject)):
            exceptionString = u"Expected ServerObject type. Passed object was " + unicode(type(serverMeta))
            raise LumaConnectionException, exceptionString
        
        self.serverMeta = serverMeta
        
        # This ldap object will be assigned in the methods.
        # This way we have better control over bind, unbind and open sockets.
        self.ldapServerObject = None
        
###############################################################################

    def search_s(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None):
        """Synchronous search.
        """
        
        searchResult = None
        environment.setBusy(True)
        
        try:
            searchResult = self.ldapServerObject.search_s(base, scope, filter, attrList)
        except ldap.LDAPError, e:
            print "Error during LDAP search request"
            print "Reason: " + str(e)
            
        environment.setBusy(False)
        return searchResult

###############################################################################

    def search(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None, attrsonly=0):
        """Aynchronous search.
        """
    
        searchResult = []
        environment.setBusy(True)
        
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
            print "Error during LDAP search request"
            print "Reason: " + str(e)
         
        environment.setBusy(False)
            
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
        environment.setBusy(True)
        
        try:
            self.ldapServerObject.delete_s(dnDelete)
            environment.setBusy(False)
            return True
        except ldap.LDAPError, e:
            print "Error during LDAP delete request"
            print "Reason: " + str(e)
            environment.setBusy(False)
            return False
            
###############################################################################

    def modify_s(self, dn, modlist=None):
        """Synchronous modify.
        """
        
        if modlist == None:
            return False
            
        environment.setBusy(True)
        try:
            self.ldapServerObject.modify_s(dn, modlist)
            environment.setBusy(False)
            return True
        except ldap.LDAPError, e:
            print "Error during LDAP modify request"
            print "Reason: " + str(e)
            environment.setBusy(False)
            return False

###############################################################################

    def add_s(self, dn, modlist):
        """Synchronous add.
        """
        
        environment.setBusy(True)
        
        
        try:
            searchResult = self.ldapServerObject.add_s(dn, modlist)
            environment.setBusy(False)
            return True
        except ldap.LDAPError, e:
            print "Error during LDAP add request"
            print "Reason: " + str(e)
            environment.setBusy(False)
            return False

###############################################################################

    def bind(self):
        """Bind to server.
        """
        
        try:
            bindAs = ""
            password = ""
            if not (self.serverMeta.bindAnon):
                bindAs = self.serverMeta.bindDN
                password = self.serverMeta.bindPassword
                
            method = "ldap"
            if self.serverMeta.tls:
                method = "ldaps"
                
            url = ldapurl.LDAPUrl(hostport = self.serverMeta.host + ":" + str(self.serverMeta.port),
                    dn = self.serverMeta.baseDN, who = bindAs, 
                    cred = password, urlscheme = method)
                    
            self.ldapServerObject = ldap.initialize(url.initializeUrl())
            self.ldapServerObject.simple_bind(bindAs, password)
            
        except ldap.LDAPError, e:
            print "Error during LDAP bind request"
            print "Reason: " + str(e)
            
###############################################################################

    def unbind(self):
        """Unbind from server.
        """
        
        try:
            if not(self.serverMeta.bindAnon):
                self.ldapServerObject.unbind()
        except ldap.LDAPError, e:
            print "Error during LDAP unbind request"
            print "Reason: " + str(e)
