###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <wido.depping@tu-clausthal.de>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import ldap
from qt import *

class LumaConnection(object):
    
    def __init__(self, serverMeta=None):
        self.server = None
        if not (serverMeta == None):
            self.server = serverMeta
        
        self.mainWin = qApp.mainWidget()
            
###############################################################################

    def search_s(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None):
        searchResult = None
        
        self.mainWin.set_busy(1)
        
        try:
            ldapServerObject = ldap.open(self.server.host, self.server.port)
            ldapServerObject.protocol_version = ldap.VERSION3
            if int(self.server.tls) == 1:
                ldapServerObject.start_tls_s()
            if len(self.server.bindDN) > 0:
                ldapServerObject.simple_bind_s(self.server.bindDN,self.server.bindPassword)
                
            searchResult = ldapServerObject.search_s(base, scope, filter, attrList)
            if len(self.server.bindDN) > 0:
                ldapServerObject.unbind()
            self.mainWin.set_busy(0)
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            self.mainWin.set_busy(0)
            
        return searchResult

###############################################################################

    def search(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None, attrsonly=0):
        searchResult = []
        
        self.mainWin.set_busy(1)
        
        try:
            ldapServerObject = ldap.open(self.server.host, self.server.port)
            ldapServerObject.protocol_version = ldap.VERSION3
            if int(self.server.tls) == 1:
                ldapServerObject.start_tls_s()
            if len(self.server.bindDN) > 0:
                ldapServerObject.simple_bind_s(self.server.bindDN,self.server.bindPassword)
            
            resultId = ldapServerObject.search(base, scope, filter, attrList)
            
            while 1:
                self.mainWin.update_ui()

                result_type, result_data = ldapServerObject.result(resultId, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        for x in result_data:
                            searchResult.append(x)
                
            if len(self.server.bindDN) > 0:
                ldapServerObject.unbind()
            self.mainWin.set_busy(0)
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            self.mainWin.set_busy(0)
            
        if len(searchResult) == 0:
            return None
        else:
            return searchResult
