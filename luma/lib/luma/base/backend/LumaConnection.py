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

try:
    import ldap.sasl
except ImportError, e:
    print "Python LDAP module has no SASL support"
    print e
    
import threading
import time

import environment
from base.backend.ServerObject import ServerObject
from base.backend.SmartDataObject import SmartDataObject


class LumaConnectionException(Exception):
    """This exception class will be raised if no proper server object is passed 
    to the constructor.
    """
    
    pass

###############################################################################


class LumaConnection(object):
    """ This class is a wrapper around the ldap functions. It is provided to 
    access ldap data easier.
    
    Parameter is a ServerObject which contains all meta information for 
    accessing servers.
    """
    
    def __init__(self, serverMeta=None):
        # Throw exception if no ServerObject is passed.
        if not isinstance(serverMeta, ServerObject):
            exceptionString = u"Expected ServerObject type. Passed object was " + unicode(type(serverMeta))
            raise LumaConnectionException, exceptionString
        
        self.serverMeta = serverMeta
        
        # This ldap object will be assigned in the methods.
        # This way we have better control over bind, unbind and open sockets.
        self.ldapServerObject = None
        
###############################################################################

    def search(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None, attrsonly=0):
        """Aynchronous search.
        """
    
        environment.setBusy(True)
        workerThread = WorkerThreadSearch(self.ldapServerObject)
        workerThread.base = base
        workerThread.scope = scope
        workerThread.filter = filter
        workerThread.attrList = attrList
        workerThread.attrsonly = attrsonly
        workerThread.start()
        
        while not workerThread.FINISHED:
            environment.updateUI()
            time.sleep(0.05)
        
        environment.setBusy(False)
            
        if len(workerThread.result) == 0:
            return None
        else:
            return workerThread.result
            
            
###############################################################################

    def delete(self, dnDelete=None):
        """Synchronous delete.
        """
        
        if dnDelete == None:
            return
            
        environment.setBusy(True)
        workerThread = WorkerThreadDelete(self.ldapServerObject)
        workerThread.dnDelete = dnDelete
        workerThread.start()
        
        while not workerThread.FINISHED:
            environment.updateUI()
            time.sleep(0.01)
            
        environment.setBusy(False)
        return workerThread.result
            
###############################################################################

    def modify(self, dn, modlist=None):
        """Synchronous modify.
        """
        
        if modlist == None:
            return False
            
        environment.setBusy(True)
        workerThread = WorkerThreadModify(self.ldapServerObject)
        workerThread.dn = dn
        workerThread.modlist = modlist
        workerThread.start()
        
        while not workerThread.FINISHED:
            environment.updateUI()
            time.sleep(0.05)
            
        environment.setBusy(False)
        return workerThread.result

###############################################################################

    def add(self, dn, modlist):
        """Synchronous add.
        """
        
        
        environment.setBusy(True)
        workerThread = WorkerThreadAdd(self.ldapServerObject)
        workerThread.dn = dn
        workerThread.modlist = modlist
        workerThread.start()
        
        while not workerThread.FINISHED:
            environment.updateUI()
            time.sleep(0.05)
            
        environment.setBusy(False)
        return workerThread.result

###############################################################################

    def bind(self):
        """Bind to server.
        """
        
        try:
            urlschemeVal = "ldap"
            if self.serverMeta.tls:
                urlschemeVal = "ldaps"
              
            whoVal = None
            credVal = None
            if not (self.serverMeta.bindAnon):
                whoVal = self.serverMeta.bindDN
                credVal = self.serverMeta.bindPassword
                
            url = ldapurl.LDAPUrl(urlscheme=urlschemeVal, 
                hostport = self.serverMeta.host + ":" + str(self.serverMeta.port),
                dn = self.serverMeta.baseDN, who = whoVal,
                cred = credVal)
            
            self.ldapServerObject = ldap.initialize(url.initializeUrl())
            self.ldapServerObject.protocol_version = 3
            
            if self.serverMeta.bindAnon:
                self.ldapServerObject.simple_bind()
            elif self.serverMeta.authMethod == u"Simple":
                self.ldapServerObject.simple_bind(whoVal, credVal)
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
                self.ldapServerObject.sasl_interactive_bind_s("", sasl_auth)
                
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
            
###############################################################################

    def getBaseDNList(self):
        environment.setBusy(True)
        try:
            self.bind()
            
            dnList = None
        
            # Check for openldap
            result = self.search("", ldap.SCOPE_BASE, "(objectClass=*)", ["namingContexts"])
            dnList = result[0][1]['namingContexts']
        
            # Check for Novell
            if dnList[0] == '':
                result = self.search("", ldap.SCOPE_BASE)
                dnList = result[0][1]['dsaName']
            
            # Univertity of Michigan aka umich
            # not jet tested
            if dnList[0] == '':
                result = self.search("", ldap.SCOPE_BASE, "(objectClass=*)",['database'])
                dnList = result[0][1]['namingContexts']
                
            self.unbind()
            environment.setBusy(False)
            return dnList
        except Exception, e:
            environment.setBusy(False)
            print e
            return None
        
###############################################################################

class WorkerThreadSearch(threading.Thread):
        
    def __init__(self, serverObject):
        threading.Thread.__init__(self)
        self.ldapServerObject = serverObject
            
        self.FINISHED = False
        self.result = []
            
    def run(self):
        try:
            resultId = self.ldapServerObject.search(self.base, self.scope, self.filter, self.attrList, self.attrsonly)

            
            while 1:
                # search with a 60 second timeout
                result_type, result_data = self.ldapServerObject.result(resultId, 0, 60)
                
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        for x in result_data:
                            self.result.append(x)
        except ldap.LDAPError, e:
            print "Error during LDAP search request"
            print "Reason: " + str(e)
            
        self.FINISHED = True
        
###############################################################################

class WorkerThreadDelete(threading.Thread):
        
    def __init__(self, serverObject):
        threading.Thread.__init__(self)
        self.ldapServerObject = serverObject
            
        self.FINISHED = False
        self.result = False
        
    def run(self):
        try:
            self.ldapServerObject.delete_s(self.dnDelete)
            self.result = True
        except ldap.LDAPError, e:
            print "Error during LDAP delete request"
            print "Reason: " + str(e)
            self.result = False
            
        self.FINISHED = True

###############################################################################

class WorkerThreadAdd(threading.Thread):
        
    def __init__(self, serverObject):
        threading.Thread.__init__(self)
        self.ldapServerObject = serverObject
            
        self.FINISHED = False
        self.result = False
        
    def run(self):
        try:
            searchResult = self.ldapServerObject.add_s(self.dn, self.modlist)
            self.result = True
        except ldap.LDAPError, e:
            print "Error during LDAP add request"
            print "Reason: " + str(e)
            self.result = False
            
        self.FINISHED = True
    
###############################################################################
    
class WorkerThreadModify(threading.Thread):
        
    def __init__(self, serverObject):
        threading.Thread.__init__(self)
        self.ldapServerObject = serverObject
            
        self.FINISHED = False
        self.result = False
        
    def run(self):
        try:
            self.ldapServerObject.modify_s(self.dn, self.modlist)
            self.result = True
        except ldap.LDAPError, e:
            print "Error during LDAP modify request"
            print "Reason: " + str(e)
            self.result = False
            
        self.FINISHED = True
    
