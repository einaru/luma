###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <wido.depping@tu-clausthal.de>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import ldap

class LumaConnection(object):
    
    def __init__(self, serverMeta=None):
        self.server = None
        if not (serverMeta == None):
            self.server = serverMeta
            
###############################################################################

    def search_s(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None):
        searchResult = None
        
        try:
            ldapServerObject = ldap.open(self.server.host, self.server.port)
            ldapServerObject.protocol_version = ldap.VERSION3
            if self.server.tls:
                ldapServerObject.start_tls_s()
            if len(self.server.bindDN) > 0:
                ldapServerObject.simple_bind_s(self.server.bindDN,self.server.bindPassword)
                
            searchResult = ldapServerObject.search_s(base, scope, filter, attrList)
            if len(self.server.bindDN) > 0:
                ldapServerObject.unbind()
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            
        return searchResult
