# -*- coding: utf-8 -*-
#
# base.backend.LumaConnectionImproved
#
# Copyright (c) 2011
#     Christian Forfang, <cforfang@gmail.com>
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# Copyright (C) 2003, 2004
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


from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QMessageBox, qApp)

from ..backend.ServerObject import (ServerObject, ServerCheckCertificate,
                                    ServerEncryptionMethod, ServerAuthMethod)
from ..backend.SmartDataObject import SmartDataObject

class LumaConnectionException(Exception):
    """ This exception class will be raised if no proper server object
    is passed to the constructor.
    """
    pass


class LumaConnection(object):
    """ LumaConnection is a wrapper around the ldap functions.
    It is provided to access ldap data easier.
    
    Public methods:
    
    add:    Synchronous
    delete: Synchronous
    modify: Synchronous
    search: Aynchronous
    
    bind:   Bind to server
    unbind: Unbind from server
    
    getBaseDNList
    """

    # For storing prompted passwords
    __passwordMap = {}
    __certMap = {}

    __logger = logging.getLogger(__name__)

    def __init__(self, serverObject=None):
        """
        @param serverObject: a ServerObject;
            contains all meta information for accessing servers.
        """
        # Throw exception if no ServerObject is passed.
        if not isinstance(serverObject, ServerObject):
            e = u'Expected ServerObject type. Passed object was %s' % \
                (unicode(type(serverObject)))
            raise LumaConnectionException, e

        self.serverObject = serverObject

        # This ldap object will be assigned in the methods.
        # This way we have better control over bind, unbind
        # and open sockets.
        self.ldapServerObject = None

    def bind(self):
        """ 
        Bind to server.
        
        @return: a tuple (success, exceptionObj)
            the boolean success value indicates wheter or not the bind
            operation was successful. If success is True, exceptionObj 
            is None. If success is True, exceptionObj contains the 
            worker thread exception object.
        """
        thread = self.__bind()

        # TODO: LumaConnection uses a lot of QDialogs to prompt for
        #       passwords etc, if needed. The backend module should be 
        #       Qt free (at least QtGui free), so we need to figure out
        #       how to solve these issues.
        # Prompt user to continue if we suspect that the certificate could not
        # be verified
        if self.__certificateError(thread):
            
            if hasSSLlibrary:
                dialog = UnknownCertDialog(self.serverObject)
                accepted = UnknownCertDialog.Accepted
            else:
                dialog = QMessageBox(
                                'Certificate error',
                                'Do you want to continue anyway?',
                                QMessageBox.Question,
                                QMessageBox.Yes,
                                QMessageBox.No,
                                QMessageBox.NoButton,
                                None)
                accepted = 3

            dialog.exec_loop()
            if dialog.result() == accepted:
                self.serverObject.checkServerCertificate = u'never'
                LumaConnection._certMap[self.serverObject.name] = u'never'
                thread = self.__bind()

        # Prompt for password on _invalid_pwd or _blank_pwd
        if self.__invalidPassword(thread) or self.__blankPassword(thread):
            dialog = PromptPasswordDialog()
            #environment.setBusy(False)
            dialog.exec_loop()

            if dialog.result() == 1:
                self.serverObject.bindPassword = unicode(dialog.passwordEdit.text())
                LumaConnection.__passwordMap[self.serverObject.name] = self.serverObject.bindPassword
                thread = self.__bind()

        if thread.exceptionObject == None:
            message = 'LDAP bind operation successful.'
            self.__logger.info(message)
            self.ldapServerObject = thread.ldapServerObject
            return (True, None)
        else:
            msg = 'LDAP bind operation not successful. Reason:\n%s' % \
                  str(thread.exceptionObject)
            self.__logger.error(msg)

            # If credentials are still wrong after prompting,
            # remove from passwordmap
            if self.__overridePassword(self.serverObject) and \
               self.__invalidPassword(thread):

                self.__passwordMap.pop(self.serverObject.name)

            return (False, thread.exceptionObject)

    def unbind(self):
        """ Unbind from server.
        """
        try:
            if not(self.serverObject.bindAnon):
                self.ldapServerObject.unbind()
        except ldap.LDAPError, e:
            msg = 'LDAP unbind operation not successful. Reason:\n%s' % \
                  str(e)
            self.__logger.error(msg)

    def add(self, dn, modlist):
        """Synchronous add.
        
        @param dn: 
        @param modlist:
        
        @return: a tuple (success, exceptionObj)
            the boolean success value indicates wheter or not the add
            operation was successful. If success is True, exceptionObj 
            is None. If success is True, exceptionObj contains the 
            worker thread exception object.
        """

        thread = WorkerThreadAdd(self.ldapServerObject)
        thread.dn = dn
        thread.modlist = modlist
        thread.start()

        #Should probably be done by the calling method instead
        self.__setBusy(True)

        while not thread.FINISHED:
            self.__whileWaiting()

        self.__setBusy(False)

        if None == thread.exceptionObject:
            msg = 'LDAP object %s successfully added' % dn
            self.__logger.info(msg)
            return (True, None)
        else:
            msg = 'LDAP object %s could not be added. Reason:\n%s' % \
                  (dn, str(thread.exceptionObject))
            self.__logger.error(msg)
            return (False, thread.exceptionObject)

    def delete(self, dnDelete=None):
        """ Synchronous delete.
        
        @param dnDelete:
        
        @return: a tuple (success, exceptionObj)
            the boolean success value indicates wheter or not the delete
            operation was successful. If success is True, exceptionObj 
            is None. If success is True, exceptionObj contains the 
            worker thread exception object.
        """

        if dnDelete == None:
            return

        thread = WorkerThreadDelete(self.ldapServerObject)
        thread.dnDelete = dnDelete
        thread.start()

        #Should probably be done by the calling method instead
        self.__setBusy(True)

        while not thread.FINISHED:
            self.__whileWaiting()

        self.__setBusy(False)

        if None == thread.exceptionObject:
            msg = 'LDAP object %s successfully deleted' % \
                  (dnDelete, str(thread.exceptionObject))
            self.__logger.info(msg)
            return (True, None)
        else:
            msg = 'LDAP object %s could not be deleted. Reason\n%s' % \
                  (dnDelete, str(thread.exceptionObject))
            self.__logger.error(msg)
            return (False, thread.exceptionObject)

    def modify(self, dn, modlist=None):
        """ Synchronous modify.
        
        @param dn:
        @param modlist:
        
        @return: a tuple (success, exceptionObj)
            the boolean success value indicates wheter or not the modify
            operation was successful. If success is True, exceptionObj 
            is None. If success is True, exceptionObj contains the 
            worker thread exception object.
        """

        if modlist == None:
            return False

        thread = WorkerThreadModify(self.ldapServerObject)
        thread.dn = dn
        thread.modlist = modlist
        thread.start()

        #Should probably be done by the calling method instead
        self.__setBusy(True)

        while not thread.FINISHED:
            self.__whileWaiting()

        self.__setBusy(False)

        if None == thread.exceptionObject:
            msg = 'LDAP object %s successfully modified.' % dn
            self.__logger.info(msg)
            return (True, None)
        else:
            msg = 'LDAP object %s could not be modified. Reason:\n' % \
                  (dn, str(thread.exceptionObject))
            self.__logger.error(msg)
            return (False, thread.exceptionObject)

    def search(self, base='', scope=ldap.SCOPE_BASE, filter='(objectClass=*)',
               attrList=None, attrsonly=0, sizelimit=0):
        """
        Asynchronous search.
        
        @param base:
        @param scope:
        @param filer:
        @param attrList:
        @param attrsonly:
        @param sizelimit:
        
        @return: a tuple (success, result, exceptionObj)
            the boolean success value indicates wheter or not the search
            operation was successful. If success is True, result contains
            the result list and exceptionObj is None. If success is True,
            result is None and exceptionObj contains the worker thread 
            exception object.
        """

        thread = WorkerThreadSearch(self.ldapServerObject)
        thread.base = base
        thread.scope = scope
        thread.filter = filter
        thread.attrList = attrList
        thread.attrsonly = attrsonly
        thread.sizelimit = sizelimit
        thread.start()

        self.__logger.debug('Entering: waiting-for-search-finished loop')
        while not thread.FINISHED:
            self.__whileWaiting()
        self.__logger.debug('Exiting: waiting-for-search-finished loop')

        if None == thread.exceptionObject:

            result = []
            result = [SmartDataObject(x, self.serverObject) for x in thread.result]

            num = len(result)
            if num == 1:
                msg = 'Received 1 item from LDAP serach operation'
            else:
                msg = 'Received %d items form LDAP search operation' % num

            self.__logger.info(msg)
            return (True, result, None)

        else:
            # Did we hit the server side search limit ?
            if isinstance(thread.exceptionObject, ldap.SIZELIMIT_EXCEEDED):
                result = []
                result = [SmartDataObject(x, self.serverObject) for x in thread.resul]

                num = len(result)
                if num == 1:
                    msg = 'Received 1 item from LDAP serach operation'
                else:
                    msg = 'Received %d items form LDAP search operation' % num

                self.__logger.info(msg)
                return (True, result, None)
            else:
                msg = 'LDAP search operation failed. Reason:\n%s' % \
                      (thread.exceptionObject)
                self.__logger.info(msg)
                return (False, None, thread.exceptionObject)

    def getBaseDNList(self):
        """
        Get the base DN list from the a LDAP server.
        
        FIXME: implement better error handling for function which call 
               getBaseDNList. Error handling inside is okay.
        
        @return: a tuple (success, dnlist, error)
            the boolean success value indicates wheter the operation
            was successfull. If the bind operation is not sucessfull, 
            success is False, dnlist is None and error contains the
            exception object from the bind operation. If success is
            True, dnlist contains the base DN list for the server and
            error is None. If the server type cannot be determined, 
            success is False, dnlist is None and error contains an
            error message.
        """

        bindSuccess, e = self.bind()

        if not bindSuccess:
            print "Bind failed"
            return (False, None, e)

        dnList = None

        # Check for openldap
        success, result, e = self.search('', ldap.SCOPE_BASE, "(objectClass=*)", ["namingContexts"])
        if success and (len(result) > 0):
            resultItem = result[0]
            if resultItem.hasAttribute('namingContexts'):
                dnList = resultItem.getAttributeValueList('namingContexts')

        # Check for Novell
        if None == dnList:
            success, result, e = self.search('', ldap.SCOPE_BASE)
            if success and (len(result) > 0):
                resultItem = result[0]
                if resultItem.hasAttribute('dsaName'):
                    dnList = resultItem.getAttributeValueList('dsaName')

        # Univertity of Michigan aka umich
        # not yet tested
        if None == dnList:
            success, result, e = self.search('', ldap.SCOPE_BASE, "(objectClass=*)", ['database'])
            if success and (len(result) > 0):
                resultItem = result[0]
                if resultItem.hasAttribute('namingContexts'):
                    dnList = resultItem.getAttributeValueList('namingContexts')

        # Check for Oracle
        if None == dnList:
            success, result, e = self.search('', ldap.SCOPE_ONELEVEL, "(objectClass=*)", ['dn'])
            if success and (len(result) > 0):
                dnList = []
                for x in result:
                    dnList.append(x.getDN())

        # Check for Active Directory
        if None == dnList:
            success, result, e = self.search('', ldap.SCOPE_BASE, "(defaultNamingContext=*)", ['defaultNamingContext'])
            if success and (len(result) > 0):
                item = result[0]
                if item.hasAttribute('defaultNamingContext'):
                    dnList = item.getAttributeValueList('defaultNamingContext')

        self.unbind()

        if None == dnList:
            msg = 'Could not retrieve Base DNs from server. ' + \
                  'Unknown server type.'
            self.__logger.error(msg)
            return (False, None, 'Unknown server type')
        else:
            msg = 'Base DNs successfully retrieved from server.'
            self.__logger.info(msg)
            return (True, dnList, None)

    def updateDataObject(self, dataObject):
        """ Updates the given SmartDataObject on the server. 
        
        @return: a tuple (,);
        """

        success, result, e = self.search(dataObject.getDN(), ldap.SCOPE_BASE)

        if success:
            oldObject = result[0]
            modlist = ldap.modlist.modifyModlist(oldObject.data, dataObject.data, [], 0)
            return self.modify(dataObject.getDN(), modlist)
        else:
            msg = 'LDAP object %s could not be updated. The entry values ' + \
                  'could not be retrieved from the server. Reason:\n%s' % \
                  (dataObject.getDN, str(e))
            self.logger.error(msg)
            return (False, e)

    def addDataObject(self, dataObject):
        """ Adds the given SmartDataObject to the server.
        
        @return: a tuple (,);
        """

        return self.add(dataObject.getDN(), ldap.modlist.addModlist(dataObject.data))

    def __bind(self):
        """
        @return:
            a worker thread for the bind operation
        """

        if self.__overridePassword(self.serverObject):
            self.serverObject.bindPassword = self.__passwordMap[self.serverObject.name]

        if self.__ignoreCertificate(self.serverObject):
            self.serverObject.checkServerCertificate = u'never'

        thread = WorkerThreadBind(self.serverObject)
        thread.start()

        #Should probably be done by the calling method instead
        self.__setBusy(True)
        while not thread.FINISHED:
            self.__whileWaiting()

        self.__setBusy(False)

        return thread

    def __ignoreCertificate(self, serverObject):
        """
        @return:
            True is the server name is in the certifiacte map, False
            otherwise.
        """
        return self.__certMap.has_key(serverObject.name)

    def __overridePassword(self, serverObject):
        """
        @return:
            True if the server name is in the password map.
        """
        return self.__passwordMap.has_key(serverObject.name)

    def __certificateError(self, thread):
        """
        Checks if we got a certificate error.
        
        With SSL enabled, we get a SERVER_DOWN on wrong certificate
        With TLS enabled, we get a CONNECT_ERROR on wrong certificate
        Notice however that server error can be raised on other issues
        as well
        
        @return:
            True if we have a SERVER_DOWN exception on a SSL connection, or
            a CONNECT_ERROR on a TLS connection, False otherwise
        """
        error = False
        if thread.serverObject.encryptionMethod == ServerEncryptionMethod.SSL:
            error = isinstance(thread.exceptionObject, ldap.SERVER_DOWN)

        if thread.serverObject.encryptionMethod == ServerEncryptionMethod.TLS:
            error = isinstance(thread.exceptionObject, ldap.CONNECT_ERROR)

        return error

    def __invalidPassword(self, thread):
        """
        @return:
            True if invalid credentials is provided to the LDAP server, 
            False otherwise.
        """
        return isinstance(thread.exceptionObject, ldap.INVALID_CREDENTIALS)

    def __blankPassword(self, thread):
        """
        UNWILLING_TO_PERFORM on bind usaually means trying to bind with
        blank password.
        
        @return:
            True if the ServerObject bind password is empty and the DSA
            is unwilling to perfom the operation, False otherwise.
        """
        return thread.serverObject.bindPassword == '' and \
               isinstance(thread.exceptionObject, ldap.UNWILLING_TO_PERFORM)

    def __cleanDN(self, dnString):
        tmpList = []

        for x in ldap.explode_dn(dnString):
            tmpList.append(self.escape_dn_chars(x))

        return ",".join(tmpList)

    def __escapeDNChars(self, s):
        s = s.replace('\,', r'\2C')
        s = s.replace('\=', r'\3D')
        s = s.replace('\+', r'\2B')
        return s

    def __whileWaiting(self):
        qApp.processEvents()
        time.sleep(0.05)

    def __setBusy(self, bool):
        if bool:
            qApp.setOverrideCursor(Qt.WaitCursor)
        else:
            qApp.restoreOverrideCursor()
        pass


class WorkerThreadSearch(threading.Thread):

    def __init__(self, serverObject):
        threading.Thread.__init__(self)
        self.ldapServerObject = serverObject

        self.sizelimit = 0

        self.FINISHED = False
        self.result = []
        self.exceptionObject = None

        self.logger = logging.getLogger(__name__)

    def run(self):
        self.logger.debug('Started LDAP-search.')
        try:
            resultId = self.ldapServerObject.search_ext(
                                                base=self.base,
                                                scope=self.scope,
                                                filterstr=self.filter,
                                                attrlist=self.attrList,
                                                attrsonly=self.attrsonly,
                                                sizelimit=self.sizelimit
                                                )

            while 1:
                # search with a 60 second timeout
                type, data = self.ldapServerObject.result(resultId, 0, 60)

                if (data == []):
                    break
                else:
                    if type == ldap.RES_SEARCH_ENTRY:
                        for x in data:
                            self.result.append(x)

        except ldap.LDAPError, e:
            self.exceptionObject = e

        self.FINISHED = True
        self.logger.debug("Search finished.")


    def __ignoreCertificate(self, serverObject):
        """
        @param serverObject: ServerObject;
            wheter
        """
        return self.__certMap.has_key(serverObject.name)

    def __overridePassword(self, serverObject):
        return LumaConnection._passwordMap.has_key(serverObject.name)

    def __certificateError(self, thread):
        """
        Checks if the worker thread got a certificate error.
        
        With SSL enabled, we get a SERVER_DOWN on wrong certificate.
        With TLS enabled, we get a CONNECT_ERROR on wrong certificate.
        Notice however that server error can be raised on other issues
        as well
        
        @return: boolean value;
            Wheter or not workerThread got a certificate error
        """
        error = False
        if thread.serverObject.encryptionMethod == ServerEncryptionMethod.SSL:
            error = isinstance(thread.exceptionObject, ldap.SERVER_DOWN)
        if thread.serverObject.encryptionMethod == ServerEncryptionMethod.TLS:
            error = isinstance(thread.exceptionObject, ldap.CONNECT_ERROR)
        return error

    def __invalidPassword(self, thread):
        return isinstance(thread.exceptionObject, ldap.INVALID_CREDENTIALS)

    def __blankPassword(self, thread):
        """
        Checks if the worker thread tries to bind with a blank password 
        
        UNWILLING_TO_PERFORM on bind usually means trying to bind with 
        blank password
        
        @return: boolean value;
        """
        return thread.serverObject.bindPassword == u'' and \
               isinstance(thread.exceptionObject, ldap.UNWILLING_TO_PERFORM)


class WorkerThreadDelete(threading.Thread):

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


class WorkerThreadAdd(threading.Thread):

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


class WorkerThreadBind(threading.Thread):

    def __init__(self, serverObject):
        threading.Thread.__init__(self)
        self.ldapServerObject = None
        self.serverObject = serverObject

        self.FINISHED = False
        self.result = False
        self.exceptionObject = None
        self.logger = logging.getLogger(__name__)

    def run(self):
        try:
            # Check wheter we want to validate the server certificate.
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

            self.logger.debug("ldap.initialize() with url: " + url.initializeUrl())

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
                    self.logger.error(message)


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
                if not ServerAuthMethod.SASL_GSSLAPI == self.serverObject.authMethod:
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
                elif self.serverObject.authMethod == ServerAuthMethod.SASL_GSSLAPI:
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
