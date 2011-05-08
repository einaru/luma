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
import ldap.modlist
try:
    import ldap.sasl
except ImportError, e:
    print "Python LDAP module has no SASL support"
    print e
    
import logging

from ..backend.ServerObject import (ServerObject, ServerCheckCertificate,
                                    ServerEncryptionMethod, ServerAuthMethod)
from ..backend.SmartDataObject import SmartDataObject

class LumaConnectionException(Exception):
    """This exception class will be raised if no proper server object is passed 
    to the constructor.
    """
    pass

###############################################################################


class LumaConnection(object):
    """ This class is a wrapper around the LDAP functions. It is provided to 
    access ldap data easier.
    
    All methods are blocking.
    
    Parameter is a ServerObject which contains all meta information for 
    accessing servers.
    """

    # For storing prompted passwords
    __passwordMap = {}
    __certMap = {}
    
    def __init__(self, serverObject=None):

        # Throw exception if no ServerObject is passed.
        if not isinstance(serverObject, ServerObject):
            exceptionString = u"Expected ServerObject type. Passed object was " + unicode(type(serverObject))
            raise LumaConnectionException, exceptionString
        
        self.serverObject = serverObject
        
        # This ldap object will be assigned in the methods.
        # This way we have better control over bind, unbind and open sockets.
        self.ldapServerObject = None
        
        # Used for logging
        self.logger = logging.getLogger(__name__)


    def search(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None, attrsonly=0, sizelimit=0):
        """ Does a search on the currently bound-to server.
        @return (bool, [], Exception)
        """

        self.logger.debug("Started LDAP-search.")
        exceptionObject = None
        result = []    
        try:
            resultId = self.ldapServerObject.search_ext(base, scope, filter, attrList, attrsonly, sizelimit=sizelimit)
            while 1:
                # Search with a 60 second timeout
                result_type, result_data = self.ldapServerObject.result(resultId, 0, 60)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        for x in result_data:
                            result.append(x)
        except ldap.TIMEOUT, e:
            exceptionObject = [{"desc":"Search timed out"}]
        except ldap.LDAPError, e:
            exceptionObject = e
        self.logger.debug("Search finished.")
        
        if None == exceptionObject:
            # Everything went well
            message = "Received " + str(len(result)) + " item(s) from LDAP search operation."
            self.logger.info(message)

            returnList = [SmartDataObject(x, self.serverObject) for x in result]
            return (True, returnList, None)
            
        else:
            if isinstance(exceptionObject, ldap.SIZELIMIT_EXCEEDED):
                # Did we hit the server side search limit?
                message = "Received " + str(len(result)) + " item(s) from LDAP search operation. But server side search limit has been reached."
                self.logger.info(message)

                returnList = [SmartDataObject(x, self.serverObject) for x in result]
                return (True, returnList, None)

            else:
                # Return error
                message = "LDAP search operation failed. Reason:\n" + str(exceptionObject)
                self.logger.error(message)
                return (False, [], exceptionObject)
            
            
    def delete(self, dnDelete=None):
        """ Deleted the given DN from the currently bound-to server.
        @return (bool, Exception)
        """
        exceptionObject = None
        try:
            self.ldapServerObject.delete_s(dnDelete)
        except ldap.LDAPError, e:
            exceptionObject = e
            
        if None == exceptionObject:
            message = "LDAP object " + dnDelete + " successfully deleted."
            self.logger.info(message)
            return (True, None)
        else:
            message = "LDAP object " + dnDelete + " could not be deleted. Reason:\n"
            message = message + str(exceptionObject)
            self.logger.error(message)
            return (False, exceptionObject)
            

    def modify(self, dn, modlist=None):
        """ Synchronous modify.
        @return (bool, Exception)
        """
        exceptionObject = None
        try:
            self.ldapServerObject.modify_s(dn, modlist)
        except ldap.LDAPError, e:
            exceptionObject = e
        if None == exceptionObject:
            message = "LDAP object " + dn + " successfully modified."
            self.logger.info(message)
            return (True, None)
        else:
            message = "LDAP object " + dn + " could not be modified. Reason:\n"
            message = message + str(exceptionObject)
            self.logger.error(message)
            return (False, exceptionObject)


    def add(self, dn, modlist):
        """Synchronous add.
        @return (bool, Exception)
        """
        exceptionObject = None
        try:
            searchResult = self.ldapServerObject.add_s(dn, modlist)
        except ldap.LDAPError, e:
            self.exceptionObject = e
        if None == exceptionObject:
            message = "LDAP object " + dn + " successfully added."
            self.logger.info(message)
            return (True, None)
        else:
            message = "LDAP object " + dn + " could not be added. Reason:\n"
            message = message + str(exceptionObject)
            self.logger.error(message)
            return (False, exceptionObject)
        

    def updateDataObject(self, smartDataObject):
        """ Updates the given SmartDataObject on the server. 
        @return (bool, Exception)
        """
        success, resultList, exceptionObject = self.search(smartDataObject.getDN(), ldap.SCOPE_BASE)
        if success:
            message = "LDAP object " + smartDataObject.getDN() + " was successfully updated on the server.)"
            self.logger.info(message)
            oldObject = resultList[0]
            modlist =  ldap.modlist.modifyModlist(oldObject.data, smartDataObject.data, [], 0)
            return self.modify(smartDataObject.getDN(), modlist)
        else:
            message = "LDAP object " + smartDataObject.getDN() + " could not be updated. The entry values could not be retrieved from the server. Reason:\n"
            message = message + str(exceptionObject)
            self.logger.error(message)
            return (False, exceptionObject)
        

    def addDataObject(self, dataObject):
        """ Adds the given SmartDataObject to the server.
        """
        return self.add(dataObject.getDN(), ldap.modlist.addModlist(dataObject.data))

    def overridePassword(self, tempPassword):
        """ Sets a temporary password to use when connection to the server
            and binds.
        """
        self.serverObject.bindPassword = unicode(tempPassword)
        LumaConnection.__passwordMap[self.serverObject.name] = self.serverObject.bindPassword

    def overrideCertificate(self):
        self.serverObject.checkServerCertificate = ServerCheckCertificate.Never
        LumaConnection.__certMap[self.serverObject.name] = ServerCheckCertificate.Never
            

    def bind(self):
        """
        @return (bool, exception)
        """
        
        success, exception, ldapServerObject = self.__createLDAPObject()
        
        if success:
            message = "LDAP bind operation successful."
            self.logger.info(message)
            self.ldapServerObject = ldapServerObject
            return (True, None)
        else:
            message = "LDAP bind operation not successful. Reason:\n"
            message += str(exception)
            self.logger.error(message)

            # If credentials are overriden but wrong, remove
            if self._override_pwd(self.serverObject) and self._invalid_pwd(exception):
                LumaConnection.__passwordMap.pop(self.serverObject.name)

            return (False, exception)

    def __createLDAPObject(self):
        """ Creates and binds to the server
        @return (bool, exception, ldapServerObject)
        """

        if self._override_pwd(self.serverObject):
            self.serverObject.bindPassword = LumaConnection.__passwordMap[self.serverObject.name]
        if self._ignore_cert(self.serverObject):
            self.serverObject.checkServerCertificate = ServerCheckCertificate.Never

        try:
            # Check whether we want to validate the server certificate.
            validateMethod = ldap.OPT_X_TLS_DEMAND
            if self.serverObject.checkServerCertificate == ServerCheckCertificate.Demand:
                validateMethod = ldap.OPT_X_TLS_DEMAND
            elif self.serverObject.checkServerCertificate == ServerCheckCertificate.Never:
                validateMethod = ldap.OPT_X_TLS_NEVER
            elif self.serverObject.checkServerCertificate == ServerCheckCertificate.Try:
                validateMethod = ldap.OPT_X_TLS_TRY
            elif self.serverObject.checkServerCertificate == ServerCheckCertificate.Allow:
                validateMethod = ldap.OPT_X_TLS_ALLOW
            
            encryption = False
            if self.serverObject.encryptionMethod == ServerEncryptionMethod.SSL:
                encryption = True
            elif self.serverObject.encryptionMethod == ServerEncryptionMethod.TLS:
                encryption = True
            
            if encryption:
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, validateMethod)

            urlschemeVal = "ldap"
            if self.serverObject.encryptionMethod == ServerEncryptionMethod.SSL:
                urlschemeVal = "ldaps"
              
            whoVal = None
            credVal = None
            if not (self.serverObject.bindAnon):
                whoVal = self.serverObject.bindDN
                credVal = self.serverObject.bindPassword
                
            url = ldapurl.LDAPUrl(urlscheme=urlschemeVal, 
                hostport = self.serverObject.hostname + ":" + str(self.serverObject.port),
                dn = self.serverObject.baseDN, who = whoVal,
                cred = credVal)
            
            self.logger.debug("ldap.initialize() with url: "+url.initializeUrl())
           
            try:
                ldapServerObject = ldap.initialize(url.initializeUrl())
            except ldap.LDAPError, e:
                # This throws an empty exception, so we make our own
                exceptionObject = [{"desc": "Invalid hostname/URL"}]
                return (False, exceptionObject, None)

            ldapServerObject.protocol_version = 3
            
            # If we're going to present client certificates, this must be set as an option
            if self.serverObject.useCertificate and encryption:
                try:
                    ldapServerObject.set_option(ldap.OPT_X_TLS_CERTFILE,self.serverObject.clientCertFile)
                    ldapServerObject.set_option(ldap.OPT_X_TLS_KEYFILE,self.serverObject.clientCertKeyfile)
                except Exception, e:
                    message = "Certificate error. Reason:\n"
                    message += "Could not set client certificate and certificate keyfile. "
                    message += str(e)
                    self.logger.error(message)
            
            if self.serverObject.encryptionMethod == ServerEncryptionMethod.TLS:
                ldapServerObject.start_tls_s()
            
            # Enable Alias support
            if self.serverObject.followAliases:
                ldapServerObject.set_option(ldap.OPT_DEREF, ldap.DEREF_ALWAYS)
            
            if self.serverObject.bindAnon:
                ldapServerObject.simple_bind()
            elif self.serverObject.authMethod == ServerAuthMethod.Simple:
                ldapServerObject.simple_bind_s(whoVal, credVal)
            elif not self.serverObject.authMethod == ServerAuthMethod.Simple:
                sasl_cb_value_dict = {}
                if not ServerAuthMethod.SASL_GSSAPI == self.serverObject.authMethod:
                    sasl_cb_value_dict[ldap.sasl.CB_AUTHNAME] = whoVal
                    sasl_cb_value_dict[ldap.sasl.CB_PASS] = credVal
                    
                sasl_mech = None
                if self.serverObject.authMethod == ServerAuthMethod.SASL_PLAIN:
                    sasl_mech = "PLAIN"
                elif self.serverObject.authMethod == ServerAuthMethod.SASL_CRAM_MD5:
                    sasl_mech = "CRAM-MD5"
                elif self.serverObject.authMethod == ServerAuthMethod.SASL_DIGEST_MD5:
                    sasl_mech = "DIGEST-MD5"
                elif self.serverObject.authMethod == ServerAuthMethod.SASL_LOGIN:
                    sasl_mech = "LOGIN"
                elif self.serverObject.authMethod == ServerAuthMethod.SASL_GSSAPI:
                    sasl_mech = "GSSAPI"
                elif self.serverObject.authMethod == ServerAuthMethod.SASL_EXTERNAL:
                    sasl_mech = "EXTERNAL"
                    
                sasl_auth = ldap.sasl.sasl(sasl_cb_value_dict,sasl_mech)
                
                # If python-ldap has no support for SASL, it doesn't have 
                # sasl_interactive_bind_s as a method.
                try:
                    if "EXTERNAL" == sasl_mech:
                        #url = ldapurl.LDAPUrl(urlscheme="ldapi", 
                        #    hostport = self.serverObject.hostname.replace("/", "%2f"),
                        #    dn = self.serverObject.baseDN)
                            
                        url = "ldapi://" + self.serverObject.hostname.replace("/", "%2F").replace(",", "%2C")
            
                        ldapServerObject = ldap.initialize(url)
                        ldapServerObject.protocol_version = 3
            
                        # Enable Alias support
                        if self.serverObject.followAliases:
                            ldapServerObject.set_option(ldap.OPT_DEREF, ldap.DEREF_ALWAYS)

                    ldapServerObject.sasl_interactive_bind_s("", sasl_auth)
                except AttributeError, e:
                    return (False, e, None)

            # Everything went well        
            return (True, None, ldapServerObject)
                
        except ldap.LDAPError, e:
            return (False, e, None)
        
    # Internal helper functions with semi self explaining names
    def _ignore_cert(self, serverObject):
        return LumaConnection.__certMap.has_key(serverObject.name)
    def _override_pwd(self, serverObject):
        return LumaConnection.__passwordMap.has_key(serverObject.name)
    def _cert_error(self, exceptionObject, serverObject):
        # With SSL enabled, we get a SERVER_DOWN on wrong certificate
        # With TLS enabled, we get a CONNECT_ERROR on wrong certificate
        # Notice however that server error can be raised on other issues as well
        cert_error = False
        if serverObject.encryptionMethod == ServerEncryptionMethod.SSL:
            cert_error = isinstance(exceptionObject, ldap.SERVER_DOWN)
        if serverObject.encryptionMethod == ServerEncryptionMethod.TLS:
            cert_error = isinstance(exceptionObject, ldap.CONNECT_ERROR)
        return cert_error
    def _invalid_pwd(self, exceptionObject):
        return isinstance(exceptionObject, ldap.INVALID_CREDENTIALS)
    def _blank_pwd(self, exceptionObject, serverObject):
        # UNWILLING_TO_PERFORM on bind usaually means trying to bind with blank password
        return serverObject.bindPassword == "" and \
                isinstance(exceptionObject, ldap.UNWILLING_TO_PERFORM)

###############################################################################

    def unbind(self):
        """Unbind from server.
        """
        try:
            if self.ldapServerObject != None:
                self.ldapServerObject.unbind()
        except ldap.LDAPError, e:
            message = "LDAP unbind operation not successful. Reason:\n"
            message = message + str(e)
            self.logger.error(message)
            
###############################################################################

    def getBaseDNList(self):

        bindSuccess, exceptionObject = self.bind()
            
        if not bindSuccess:
            return (False, None, exceptionObject)
            
        dnList = None
        
        # Check for openldap
        success, resultList, exceptionObject = self.search("", ldap.SCOPE_BASE, "(objectClass=*)", ["namingContexts"])
        if success and (len(resultList) > 0):
            resultItem = resultList[0]
            if resultItem.hasAttribute('namingContexts'):
                dnList = resultItem.getAttributeValueList('namingContexts')
        
        # Check for Novell
        if None == dnList:
            success, resultList, exceptionObject = self.search("", ldap.SCOPE_BASE)
            if success and (len(resultList) > 0):
                resultItem = resultList[0]
                if resultItem.hasAttribute('dsaName'):
                    dnList = resultItem.getAttributeValueList('dsaName')
            
        # Univertity of Michigan aka umich
        # not yet tested
        if None == dnList:
            success, resultList, exceptionObject = self.search("", ldap.SCOPE_BASE, "(objectClass=*)",['database'])
            if success and (len(resultList) > 0):
                resultItem = resultList[0]
                if resultItem.hasAttribute('namingContexts'):
                    dnList = resultItem.getAttributeValueList('namingContexts')
                    
        # Check for Oracle
        if None == dnList:
            success, resultList, exceptionObject = self.search("", ldap.SCOPE_ONELEVEL, "(objectClass=*)", ['dn'])
            if success and (len(resultList) > 0):
                dnList = []
                for x in resultList:
                    dnList.append(x.getDN())
                #if resultItem.hasAttribute('namingContexts'):
                #    dnList = resultItem.getAttributeValueList('namingContexts')
                
        # Check for Active Directory
        if None == dnList:
            success, resultList, exceptionObject = self.search("", ldap.SCOPE_BASE, "(defaultNamingContext=*)" ,['defaultNamingContext'])
            if success and (len(resultList) > 0):
                resultItem = resultList[0]
                if resultItem.hasAttribute('defaultNamingContext'):
                    dnList = resultItem.getAttributeValueList('defaultNamingContext')
                    
                    
        self.unbind()
            
        if None == dnList:
            message = "Could not retrieve Base DNs from server. Unknown server type."
            self.logger.error(message)
            return (False, None, [{"desc":"Unknown server type"}])
        else:
            message = "Base DNs successfully retrieved from server."
            self.logger.info(message)
            return (True, dnList, None)
            
            
    def cleanDN(self, dnString):
        tmpList = []
        
        for x in ldap.explode_dn(dnString):
            tmpList.append(self.escape_dn_chars(x))
            
        return ",".join(tmpList)
            
            
    def escape_dn_chars(self, s):
        s = s.replace('\,', r'\2C')
        s = s.replace('\=', r'\3D')
        s = s.replace('\+', r'\2B')
        return s
