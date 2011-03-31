# -*- coding: utf-8 -*-
#
# base.backend.Connection
#
# Copyright (c) 2011
#     Christian Forfang, <cforfang@gmail.com>
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# Copyright (c) 2003, 2004 
#     Wido Depping, <widod@users.sourceforge.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! WARNING                                                                  !!
!!                                                                          !!
!! This version of the LumaConnection class is not finished, and should be  !! 
!! used only in testing environments. This implementation is an attempt to  !!
!! cleanup the old implementation, where one of the goals is to get rid of  !!
!! all PyQt4 dependencies (at least all the PyQt4.QtGui dependencies).      !! 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
import ldap
import ldapurl
import ldap.modlist
try:
    import ldap.sasl
except ImportError, e:
    print "Python LDAP module has no SASL support"
    print e

import threading
import time
import logging

from PyQt4.QtCore import QCoreApplication

from .Exception import *
from .ServerObject import (ServerObject, ServerCheckCertificate,
                           ServerEncryptionMethod, ServerAuthMethod)
from .SmartDataObject import SmartDataObject
from ..util import escapeDnChars

hasSSLlibrary = False

class LumaConnection(object):
    """This class is a wrapper around the ldap functions.
    
    It is provided to access ldap data easier.
    The following public LDAP-wrapper methods is available:
    
    bind -- Binds to an LDAP server
    unbind -- Unbinds from an LDAP server
    search -- Performs an asynchronous search operation
    add -- Performs an synchronous add operation
    modify -- Performs an synchronous modify operation
    delete -- Performs an synchronous delete operation
    
    Every operation is executed in its own worker thread.
    """

    __passwordMap = {}
    __certMap = {}

    def __init__(self, serverObject=None):
        """A LumaConnectionException will be raised if serverObject is
        not a proper server object.
         
        @param serverObject: 
            a ServerObject which contains all meta information for
            accessing servers.
        """
        if not isinstance(serverObject, ServerObject):
            e = 'Expected ServerObject type. Passed object was {0}'
            raise LumaConnectionException, e.format(unicode(type(serverObject)))

        self.serverObject = serverObject

        # This ldap object will be assigned in the methods.
        # This way we have better control over bind, unbind and open sockets.
        self.ldapServerObject = None

        self.__logger = logging.getLogger(__name__)

    def whileWaiting(self):
        """FIXME: replacement for the qApp.processEvents() call.
        """
        QCoreApplication.processEvents()
        time.sleep(0.05)

    def __setBusy(self, busy):
        """FIXME: this should be done by the calling method
        """
        if busy:
            pass #print 'App.setOverrideCursor(Qt.WaitCursor)'
        else:
            pass #print 'App.restoreOverrideCursor()'

    def __invalidPassword(self, workerThread):
        """Checks wheter or not the workerThread ServerObject has an
        invalid password set.
        
        @param workerThread: 
            The worker thread to examine.
        
        @return:
            True if INVALID_CREDENTIALS is caught in the workerThread.
        """
        return isinstance(workerThread.exceptionObject,
                          ldap.INVALID_CREDENTIALS)

    def __blankPassword(self, workerThread):
        """Check wheter or not the workerThread ServerObject bind
        password is blank.
        
        Notice: UNWILLING_TO_PERFORM on bind usaually means trying to
        bind with blank password
        
        @param workerThread: 
            The worker thread to examine.
        
        @return: 
            True if the bind password for the ServerObject in the
            workerThread is empty and UNWILLING_TO_PERFORM is caught, 
            False otherwise.
        """
        return workerThread.serverObject.bindPassword == "" and \
                isinstance(workerThread.exceptionObject,
                           ldap.UNWILLING_TO_PERFORM)

    def __overridePassword(self, serverObject):
        """Validates if we should override the password.
        
        @param serverObject: 
            The ServerObject to test.
        
        @return: 
            True if the ServerObject is found in the password map,
            False otherwise. 
        """
        return LumaConnection.__passwordMap.has_key(serverObject.name)

    def __ignoreCertificate(self, serverObject):
        """Validates if we should ignore the certificate.
        
        @param serverObject: 
            The ServerObject to test.
        
        @return: 
            True if the ServerObject is found in the certificate map,
            False otherwise. 
        """
        return LumaConnection.__certMap.has_key(serverObject.name)

    def __certificateError(self, workerThread):
        """Checks if we have a possible certificate error, not caught
        by default ldap operations.
        
        With SSL enabled, we get a SERVER_DOWN on wrong certificate
        With TLS enabled, we get a CONNECT_ERROR on wrong certificate
        
        Notice that server error can be raised on other issues as well.
        
        @param workerThread: 
            The worker thread to examine.
        
        @return: 
            True if a SERVER_DOWN exception is caught in the worker
            thread with encryption method SSL.
            True if a CONNECT_ERROR exception is caught in the worker
            thread with encryption method TSL.
            False otherwise
        """
        cert_error = False
        if workerThread.serverObject.encryptionMethod == ServerEncryptionMethod.SSL:
            cert_error = isinstance(workerThread.exceptionObject, ldap.SERVER_DOWN)
        if workerThread.serverObject.encryptionMethod == ServerEncryptionMethod.TLS:
            cert_error = isinstance(workerThread.exceptionObject, ldap.CONNECT_ERROR)
        return cert_error

    def __bind(self):
        """Helper method for the LDAP bind operation.
        
        @return:
            The worker thread object.
            
        """
        if self.__overridePassword(self.serverObject):
            self.serverObject.bindPassword = LumaConnection.__passwordMap[self.serverObject.name]

        if self.__ignoreCertificate(self.serverObject):
            self.serverObject.checkServerCertificate = u'never'

        workerThread = WorkerThreadBind(self.serverObject)
        workerThread.start()

        self.__setBusy(True)
        while not workerThread.FINISHED:
            self.whileWaiting()
        self.__setBusy(False)

        return workerThread

    def bind(self):
    #def bind(self, checkCert=ServerCheckCertificate.Never, password=''):
        """Bind to LDAP server.
        
        Exceptions will be raised on certificate error and invalid or blank
        passwords.
        
        @return: a tuple, (success, exceptionObj)
            The boolean success value indicates wheter the bind
            operation was successfull or not. If success is True, 
            exceptionObj is None. If success is False, exceptionObj
            will contain the worker thread excpetion object.
        """
        workerThread = self.__bind()

        # Raise exception if we suspect the certificate could not be
        # verified
        if self.__certificateError(workerThread):
            if hasSSLlibrary:
                # TODO
                pass
            else:
                if not self.serverObject.checkServerCertificate == ServerCheckCertificate.Never:
                    e = 'Certificate error'
                    raise ServerCertificateException, e

        # Raise exception on invalid or blank password
        if self.__invalidPassword(workerThread) or self.__blankPassword(workerThread):
            e = 'Invalid or blank password provided'
            raise InvalidPasswordException, e

        if workerThread.exceptionObject is None:
            msg = 'LDAP bind operation successful.'
            self.__logger.info(msg)
            self.ldapServerObject = workerThread.ldapServerObject
            return (True, None)
        else:
            msg = 'LDAP bind operation not successfull. Reason\n{0}'
            self.__logger.error(msg.format(str(workerThread.exceptionObject)))

            if self.__overridePassword(self.serverObject) and self.__invalidPassword(workerThread):
                LumaConnection.__passwordMap.pop(self.serverObject.name)

            return (False, workerThread.exceptionObject)

    def unbind(self):
        """Unbind from server.
        """
        try:
            if not(self.serverObject.bindAnon):
                self.ldapServerObject.unbind()
        except ldap.LDAPError, e:
            msg = 'LDAP unbind operation not successful. Reason:\n{0}'
            self.__logger.error(msg.format(str(e)))

    def search(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)",
               attrList=None, attrsonly=0, sizelimit=0):
        """Asynchronous search.
        
        @param base:
            The base entry to start the search from.
        @param scope:
            The search scope. must be one of SCOPE_BASE (0),
            SCOPE_ONELEVEL (1) or SCOPE_SUBTREE (2)
        @param filter:
            The filter string to apply on the search .
        @param attrList: 
        @param attrsonly: 
        @param sizelimit:
            The limit for entries to retrive
        
        @return: a tuple, (success, result, exceptionObj)
            The boolean success value indicates wheter the search
            operation was successfull or not. If success is True, 
            result will contain the returnes result as a list, and
            exceptionObj is None. If success is False, result is None,
            and exceptionObj will contain the worker thread excpetion
            object.
        """
        workerThread = WorkerThreadSearch(self.ldapServerObject)
        workerThread.base = base
        workerThread.scope = scope
        workerThread.filter = filter
        workerThread.attrList = attrList
        workerThread.attrsonly = attrsonly
        workerThread.sizelimit = sizelimit
        workerThread.start()

        self.__logger.debug('Entering waiting-for-search-finished-loop.')
        while not workerThread.FINISHED:
            self.whileWaiting()
        self.__logger.debug('Exited waiting-for-search-finished-loop.')

        if None == workerThread.exceptionObject:
            resultList = []
            resultList = [SmartDataObject(x, self.serverObject) for x in workerThread.result]

            rcount = len(resultList)
            if rcount == 1:
                msg = 'Received 1 item from LDAP search operation.'
            else:
                msg = 'Received {0} items from LDAP search operation.'.format(rcount)

            self.__logger.info(msg)
            return (True, resultList, None)
        else:
            # Did we hit the server side search limit?
            if isinstance(workerThread.exceptionObject, ldap.SIZELIMIT_EXCEEDED):
                resultList = []
                resultList = [SmartDataObject(x, self.serverObject) for x in workerThread.result]

                rcount = len(resultList)
                if rcount == 1:
                    msg = 'Received 1 item from LDAP search operation.'
                else:
                    msg = 'Received {0} items from LDAP search operation.'.format(rcount)

                msg = '{0} But server side search limit has been reached.'
                self.__logger.info(msg.format(msg))

                return (True, resultList, None)

            else:
                msg = 'LDAP search operation failed. Reason:\n{0}'
                self.__logger.error(msg.format(str(workerThread.exceptionObject)))

                return (False, None, workerThread.exceptionObject)

    def add(self, dn, modlist):
        """Synchronous add.
        
        @param dn: 
        @param modlist: 
        
        @return: a tuple, (success, exceptionObj)
            The boolean success value indicates wheter the add
            operation was successfull or not. If success is True, 
            exceptionObj is None. If success is False, exceptionObj
            will contain the worker thread excpetion object.
        """
        workerThread = WorkerThreadAdd(self.ldapServerObject)
        workerThread.dn = dn
        workerThread.modlist = modlist
        workerThread.start()

        #Should probably be done by the calling method instead
        self.setBusy(True)
        while not workerThread.FINISHED:
            self.whileWaiting()
        self.setBusy(False)

        if None == workerThread.exceptionObject:
            msg = 'LDAP object {0} successfully added.'.format(dn)
            self.__logger.info(msg)

            return (True, None)

        else:
            msg = 'LDAP object {0} could not be added. Reason:\n{1}'
            self.__logger.error(msg.format(dn , str(workerThread.exceptionObject)))

            return (False, workerThread.exceptionObject)

    def modify(self, dn, modlist=None):
        """Synchronous modify.
        
        @param dn: 
        @param modlist
        
        @return: a tuple, (success, exceptionObj)
            The boolean success value indicates wheter the modify
            operation was successfull or not. If success is True, 
            exceptionObj is None. If success is False, exceptionObj
            will contain the worker thread excpetion object.
        """

        if modlist == None:
            return False

        workerThread = WorkerThreadModify(self.ldapServerObject)
        workerThread.dn = dn
        workerThread.modlist = modlist
        workerThread.start()

        #Should probably be done by the calling method instead
        self.setBusy(True)
        while not workerThread.FINISHED:
            self.whileWaiting()
        self.setBusy(False)

        if None == workerThread.exceptionObject:
            msg = 'LDAP object {0} successfully modified.'
            self.__logger.info(msg.format(dn))

            return (True, None)

        else:
            msg = 'LDAP object {0} could not be modified. Reason:\n{1}'
            self.__logger.error(msg.format(dn, str(workerThread.exceptionObject)))

            return (False, workerThread.exceptionObject)

    def delete(self, dnDelete=None):
        """Synchronous delete.
        
        @param dnDelete: 
        
        @return: a tuple, (success, exceptionObj)
            The boolean success value indicates wheter the delete
            operation was successfull or not. If success is True, 
            exceptionObj is None. If success is False, exceptionObj
            will contain the worker thread excpetion object.
        """

        if dnDelete == None:
            return

        workerThread = WorkerThreadDelete(self.ldapServerObject)
        workerThread.dnDelete = dnDelete
        workerThread.start()

        #Should probably be done by the calling method instead
        self.setBusy(True)
        while not workerThread.FINISHED:
            self.whileWaiting()
        self.setBusy(False)

        if None == workerThread.exceptionObject:
            msg = 'LDAP object {0} successfully deleted.'
            self.__logger.info(msg.format(dnDelete))

            return (True, None)

        else:
            msg = 'LDAP object {0} could not be deleted. Reason:\n{1}'
            self.__logger.error(msg.format(dnDelete, str(workerThread.exceptionObject)))

            return (False, workerThread.exceptionObject)

    def updateDataObject(self, dataObject):
        """Updates the given SmartDataObject, by doing search for the dn, 
        and modify on the object entry. 

        @return: a tuple, (dn|False, modlist|exceptionObj)
            If the procedure is successfull, the dn and the modlist
            will be returned, if not False, and the worker thread
            exception object is returned.
        """
        success, resultList, exceptionObject = self.search(dataObject.getDN(), ldap.SCOPE_BASE)

        if success:
            oldObject = resultList[0]
            modlist = ldap.modlist.modifyModlist(oldObject.data, dataObject.data, [], 0)
            return self.modify(dataObject.getDN(), modlist)
        else:
            msg = 'LDAP object {0} could not be updated. '+ \
                  'The entry values could not be retrieved from the server. ' \
                  'Reason:\n{1}'
            self.__logger.error(msg.format(dataObject.getDN(), str(exceptionObject)))
            return (False, exceptionObject)

    def addDataObject(self, dataObject):
        """Adds the given SmartDataObject to the server.
        
        @return: [same as add()]
        """
        return self.add(dataObject.getDN(), ldap.modlist.addModlist(dataObject.data))

    def getBaseDNList(self):
        """Get the baseDN list off of an LDAP server.
        
        FIXME: implement better error handling for function which call 
               getBaseDNList. Error handling inside is okay.
        
        @return: a tuple, (success, result, exceptionObj|error)
            The boolean success value indicates wheter the search
            operation was successfull or not. If success is True, 
            result contains the list of baseDN from the server, and
            exceptionObj is None. If success is False, result is None,
            end exceptionObj will contain the worker thread excpetion
            object.
        """
        bindSuccess, exceptionObject = self.bind()

        if not bindSuccess:
            #print "Bind failed"
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
            success, resultList, exceptionObject = self.search("", ldap.SCOPE_BASE, "(objectClass=*)", ['database'])
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
            success, resultList, exceptionObject = self.search("", ldap.SCOPE_BASE, "(defaultNamingContext=*)" , ['defaultNamingContext'])
            if success and (len(resultList) > 0):
                resultItem = resultList[0]
                if resultItem.hasAttribute('defaultNamingContext'):
                    dnList = resultItem.getAttributeValueList('defaultNamingContext')

        self.unbind()

        if None == dnList:
            message = "Could not retrieve Base DNs from server. Unknown server type."
            self.__logger.error(message)
            return (False, None, [{"desc":"Unknown server type"}])
        else:
            message = "Base DNs successfully retrieved from server."
            self.__logger.info(message)
            return (True, dnList, None)

    def cleanDN(self, dnString):
        tmpList = []

        for x in ldap.explode_dn(dnString):
            tmpList.append(escapeDnChars(x))

        return ",".join(tmpList)


class WorkerThreadBind(threading.Thread):
    """A worker thread for the LDAP bind operation.
    """

    def __init__(self, serverObject):
        threading.Thread.__init__(self)
        self.ldapServerObject = None
        self.serverObject = serverObject

        self.FINISHED = False
        self.result = False
        self.exceptionObject = None
        self.__logger = logging.getLogger(__name__)

    def run(self):
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
                hostport=self.serverObject.hostname + ":" + str(self.serverObject.port),
                dn=self.serverObject.baseDN, who=whoVal,
                cred=credVal)

            self.__logger.debug("ldap.initialize() with url: " + url.initializeUrl())

            self.ldapServerObject = ldap.initialize(url.initializeUrl())
            self.ldapServerObject.protocol_version = 3

            # If we're going to present client certificates, this must be set as an option
            if self.serverObject.useCertificate and encryption:
                try:
                    self.ldapServerObject.set_option(ldap.OPT_X_TLS_CERTFILE, self.serverObject.clientCertFile)
                    self.ldapServerObject.set_option(ldap.OPT_X_TLS_KEYFILE, self.serverObject.clientCertKeyfile)
                except Exception, e:
                    message = "Certificate error. Reason:\n"
                    message += "Could not set client certificate and certificate keyfile. "
                    message += str(e)
                    self.__logger.error(message)


            if self.serverObject.encryptionMethod == ServerEncryptionMethod.TLS:
                self.ldapServerObject.start_tls_s()

            # Enable Alias support
            if self.serverObject.followAliases:
                self.ldapServerObject.set_option(ldap.OPT_DEREF, ldap.DEREF_ALWAYS)

            if self.serverObject.bindAnon:
                self.ldapServerObject.simple_bind()
            elif self.serverObject.authMethod == ServerAuthMethod.Simple:
                self.ldapServerObject.simple_bind_s(whoVal, credVal)
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

                sasl_auth = ldap.sasl.sasl(sasl_cb_value_dict, sasl_mech)

                # If python-ldap has no support for SASL, it doesn't have 
                # sasl_interactive_bind_s as a method.
                try:
                    if "EXTERNAL" == sasl_mech:
                        #url = ldapurl.LDAPUrl(urlscheme="ldapi", 
                        #    hostport = self.serverObject.hostname.replace("/", "%2f"),
                        #    dn = self.serverObject.baseDN)

                        url = "ldapi://" + self.serverObject.hostname.replace("/", "%2F").replace(",", "%2C")

                        #self.ldapServerObject = ldap.initialize(url.initializeUrl())
                        self.ldapServerObject = ldap.initialize(url)
                        self.ldapServerObject.protocol_version = 3

                        # Enable Alias support
                        if self.serverObject.followAliases:
                            self.ldapServerObject.set_option(ldap.OPT_DEREF, ldap.DEREF_ALWAYS)

                    self.ldapServerObject.sasl_interactive_bind_s("", sasl_auth)
                except AttributeError, e:
                    self.result = False
                    self.exceptionObject = e
                    self.FINISHED = True
                    return

            self.result = True
            self.FINISHED = True

        except ldap.LDAPError, e:
            self.result = False
            self.exceptionObject = e
            self.FINISHED = True


class WorkerThreadSearch(threading.Thread):
    """A worker thread for the LDAP search operation.
    """

    def __init__(self, serverObject):
        threading.Thread.__init__(self)
        self.ldapServerObject = serverObject

        self.sizelimit = 0

        self.FINISHED = False
        self.result = []
        self.exceptionObject = None

        self.__logger = logging.getLogger(__name__)

    def run(self):
        self.__logger.debug("Started LDAP-search.")
        try:
            resultId = self.ldapServerObject.search_ext(self.base, self.scope, self.filter, self.attrList, self.attrsonly, sizelimit=self.sizelimit)

            while 1:
                # search with a 60 second timeout
                result_type, result_data = self.ldapServerObject.result(resultId, 0, 60)

                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        for x in result_data:
                            self.result.append(x)
            #self.result = self.ldapServerObject.search_ext_s(self.base, self.scope, self.filter, self.attrList, self.attrsonly, sizelimit=self.sizelimit)
        except ldap.LDAPError, e:
            self.exceptionObject = e

        self.FINISHED = True
        self.__logger.debug("Search finished.")


class WorkerThreadAdd(threading.Thread):
    """A worker thread for the LDAP add operation.
    """

    def __init__(self, serverObject):
        threading.Thread.__init__(self)
        self.ldapServerObject = serverObject

        self.FINISHED = False
        self.result = False
        self.exceptionObject = None

    def run(self):
        try:
            searchResult = self.ldapServerObject.add_s(self.dn, self.modlist)
            self.result = True
        except ldap.LDAPError, e:
            self.exceptionObject = e
            self.result = False

        self.FINISHED = True


class WorkerThreadModify(threading.Thread):
    """A worker thread for the LDAP modify operation.
    """

    def __init__(self, serverObject):
        threading.Thread.__init__(self)
        self.ldapServerObject = serverObject

        self.FINISHED = False
        self.result = False
        self.exceptionObject = None

    def run(self):
        try:
            self.ldapServerObject.modify_s(self.dn, self.modlist)
            self.result = True
        except ldap.LDAPError, e:
            self.exceptionObject = e
            self.result = False

        self.FINISHED = True


class WorkerThreadDelete(threading.Thread):
    """A worker thread for the LDAP delete operation.
    """

    def __init__(self, serverObject):
        threading.Thread.__init__(self)
        self.ldapServerObject = serverObject

        self.FINISHED = False
        self.result = False
        self.exceptionObject = None

    def run(self):
        try:
            self.ldapServerObject.delete_s(self.dnDelete)
            self.result = True
        except ldap.LDAPError, e:
            self.exceptionObject = e
            self.result = False

        self.FINISHED = True

