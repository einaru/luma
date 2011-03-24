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
        
from PyQt4.QtGui import qApp, QInputDialog, QLineEdit, QApplication
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import Qt
        
try:
    import ldap.sasl
except ImportError, e:
    print "Python LDAP module has no SASL support"
    print e
    
import threading
import time
import logging

from ..backend.ServerObject import (ServerObject, ServerCheckCertificate,
                                    ServerEncryptionMethod, ServerAuthMethod)
from ..backend.SmartDataObject import SmartDataObject

#from base.backend.LumaSSLConnection import hasSSLlibrary
hasSSLlibrary = False

#from base.gui.UnknownCertDialog import UnknownCertDialog


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
        
        self.logger = logging.getLogger(__name__)


    def search(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None, attrsonly=0, sizelimit=0):
        """
        Aynchronous search.
        """
        
        # Done by the objects calling the method
        #environment.setBusy(True)
        
        workerThread = WorkerThreadSearch(self.ldapServerObject)
        workerThread.base = base
        workerThread.scope = scope
        workerThread.filter = filter
        workerThread.attrList = attrList
        workerThread.attrsonly = attrsonly
        workerThread.sizelimit = sizelimit
        workerThread.start()
        
        self.logger.debug("Entering waiting-for-search-finished-loop.")
        while not workerThread.FINISHED:
            self.whileWaiting()
        self.logger.debug("Exited waiting-for-search-finished-loop.")

        if None == workerThread.exceptionObject:
            resultList = []
            #for x in workerThread.result:
                # Why copy? :S
                #x = copy.deepcopy(x)
                #ldapObject = SmartDataObject(x, self.serverObject)
                #resultList.append(ldapObject)
            resultList = [SmartDataObject(x, self.serverObject) for x in workerThread.result]
            #environment.setBusy(False)
            message = "Received " + str(len(resultList)) + " item(s) from LDAP search operation."
            self.logger.info(message)
            return (True, resultList, None)
        else:
            # Did we hit the server side search limit?
            if isinstance(workerThread.exceptionObject, ldap.SIZELIMIT_EXCEEDED):
                resultList = []
                #for x in workerThread.result:
                    #x = copy.deepcopy(x)
                    #SmartDataObject(x, self.serverObject)
                    #resultList.append(SmartDataObject(x, self.serverObject))
                resultList = [SmartDataObject(x, self.serverObject) for x in workerThread.result]
                
                #environment.setBusy(False)
                #environment.displaySizeLimitWarning()
                message = "Received " + str(len(resultList)) + " item(s) from LDAP search operation. But server side search limit has been reached."
                self.logger.info(message)
                return (True, resultList, None)
            else:
                #environment.setBusy(False)
                message = "LDAP search operation failed. Reason:\n" + str(workerThread.exceptionObject)
                self.logger.error(message)
                return (False, None, workerThread.exceptionObject)
            
            
            
###############################################################################

    def delete(self, dnDelete=None):
        """ Synchronous delete.
        """
        
        if dnDelete == None:
            return
        
        #environment.setBusy(True)
        
        workerThread = WorkerThreadDelete(self.ldapServerObject)
        workerThread.dnDelete = dnDelete
        workerThread.start()
        
        #Should probably be done by the calling method instead
        #self.setBusy(True)
        while not workerThread.FINISHED:
            self.whileWaiting()
        #self.setBusy(False)
        
        if None == workerThread.exceptionObject:
            message = "LDAP object " + dnDelete + " successfully deleted."
            self.logger.info(message)
            return (True, None)
        else:
            message = "LDAP object " + dnDelete + " could not be deleted. Reason:\n"
            message = message + str(workerThread.exceptionObject)
            self.logger.error(message)
            return (False, workerThread.exceptionObject)
            
###############################################################################

    def modify(self, dn, modlist=None):
        """ Synchronous modify.
        """
        
        if modlist == None:
            return False
        
        #environment.setBusy(True)
        
        workerThread = WorkerThreadModify(self.ldapServerObject)
        workerThread.dn = dn
        workerThread.modlist = modlist
        workerThread.start()
        
        #Should probably be done by the calling method instead
        #self.setBusy(True)
        while not workerThread.FINISHED:
            self.whileWaiting()
        #self.setBusy(False)
        
        if None == workerThread.exceptionObject:
            message = "LDAP object " + dn + " successfully modified."
            self.logger.info(message)
            return (True, None)
        else:
            message = "LDAP object " + dn + " could not be modified. Reason:\n"
            message = message + str(workerThread.exceptionObject)
            self.logger.error(message)
            return (False, workerThread.exceptionObject)

###############################################################################

    def add(self, dn, modlist):
        """Synchronous add.
        """
        
        
        #environment.setBusy(True)
        
        workerThread = WorkerThreadAdd(self.ldapServerObject)
        workerThread.dn = dn
        workerThread.modlist = modlist
        workerThread.start()
        
        #Should probably be done by the calling method instead
        #self.setBusy(True)
        while not workerThread.FINISHED:
            self.whileWaiting()
        #self.setBusy(False)
        
        if None == workerThread.exceptionObject:
            message = "LDAP object " + dn + " successfully added."
            self.logger.info(message)
            return (True, None)
        else:
            message = "LDAP object " + dn + " could not be added. Reason:\n"
            message = message + str(workerThread.exceptionObject)
            self.logger.error(message)
            return (False, workerThread.exceptionObject)
        
###############################################################################

    def updateDataObject(self, dataObject):
        """ Updates the given SmartDataObject on the server. 
        """
        
        success, resultList, exceptionObject = self.search(dataObject.getDN(), ldap.SCOPE_BASE)
        
        if success:
            oldObject = resultList[0]
            modlist =  ldap.modlist.modifyModlist(oldObject.data, dataObject.data, [], 0)
            return self.modify(dataObject.getDN(), modlist)
        else:
            message = "LDAP object " + dataObject.getDN() + " could not be updated. The entry values could not be retrieved from the server. Reason:\n"
            message = message + str(exceptionObject)
            self.logger.error(message)
            return (False, exceptionObject)
        
###############################################################################

    def addDataObject(self, dataObject):
        """ Adds the given SmartDataObject to the server.
        """
        
        return self.add(dataObject.getDN(), ldap.modlist.addModlist(dataObject.data))
        

###############################################################################

    def bind(self):
        """Bind to server.
        """
        workerThread = self.__bind()
        
        # Prompt user to continue if we suspect that the certificate could not
        # be verified
        if self._cert_error(workerThread):
            svar = QMessageBox.No
            if hasSSLlibrary:
                pass
                # TODO
                #dialog = UnknownCertDialog(self.serverObject)
                #accepted = UnknownCertDialog.Accepted
            else:
                # If checkServerCertificate isn't "never" ask to set it
                if not self.serverObject.checkServerCertificate == ServerCheckCertificate.Never:
                    svar = QMessageBox.question(None, QApplication.translate("LumaConnection","Certificate error"), 
                                     QApplication.translate("LumaConnection","Do you want to continue anyway?"), 
                                     QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
                    
            if svar == QMessageBox.Yes:
                self.serverObject.checkServerCertificate = ServerCheckCertificate.Never
                LumaConnection.__certMap[self.serverObject.name] = ServerCheckCertificate.Never
                workerThread = self.__bind()

        # Prompt for password on _invalid_pwd or _blank_pwd
        if self._invalid_pwd(workerThread) or self._blank_pwd(workerThread):
            qApp.setOverrideCursor(Qt.ArrowCursor) #Put the mouse back to normal for the dialog (if needed)
            pw, ret = QInputDialog.getText(None, QApplication.translate("LumaConnection","Password"), QApplication.translate("LumaConnection","Invalid passord. Enter new:"), mode=QLineEdit.Password)
            qApp.restoreOverrideCursor()
            if ret:
                self.serverObject.bindPassword = unicode(pw)
                LumaConnection.__passwordMap[self.serverObject.name] = self.serverObject.bindPassword
                workerThread = self.__bind()

        if workerThread.exceptionObject == None:
            message = "LDAP bind operation successful."
            self.logger.info(message)
            self.ldapServerObject = workerThread.ldapServerObject
            return (True, None)
        else:
            message = "LDAP bind operation not successful. Reason:\n"
            message += str(workerThread.exceptionObject)
            self.logger.error(message)
            # If credentials are still wrong after prompting, remove from passwordmap
            if self._override_pwd(self.serverObject) and self._invalid_pwd(workerThread):
                LumaConnection.__passwordMap.pop(self.serverObject.name)
            return (False, workerThread.exceptionObject)

    def __bind(self):
        if self._override_pwd(self.serverObject):
            self.serverObject.bindPassword = LumaConnection.__passwordMap[self.serverObject.name]
        if self._ignore_cert(self.serverObject):
            self.serverObject.checkServerCertificate = u"never"

        workerThread = WorkerThreadBind(self.serverObject)
        workerThread.start()
        
        #Should probably be done by the calling method instead
        #self.setBusy(True)
        while not workerThread.FINISHED:
            self.whileWaiting()
        #self.setBusy(False)
        
        return workerThread
        
    # Internal helper functions with semi self explaining names
    def _ignore_cert(self, serverObject):
        return LumaConnection.__certMap.has_key(serverObject.name)
    def _override_pwd(self, serverObject):
        return LumaConnection.__passwordMap.has_key(serverObject.name)
    def _cert_error(self, workerThread):
        # With SSL enabled, we get a SERVER_DOWN on wrong certificate
        # With TLS enabled, we get a CONNECT_ERROR on wrong certificate
        # Notice however that server error can be raised on other issues as well
        cert_error = False
        if workerThread.serverObject.encryptionMethod == ServerEncryptionMethod.SSL:
            cert_error = isinstance(workerThread.exceptionObject, ldap.SERVER_DOWN)
        if workerThread.serverObject.encryptionMethod == ServerEncryptionMethod.TLS:
            cert_error = isinstance(workerThread.exceptionObject, ldap.CONNECT_ERROR)
        return cert_error
    def _invalid_pwd(self, workerThread):
        return isinstance(workerThread.exceptionObject, ldap.INVALID_CREDENTIALS)
    def _blank_pwd(self, workerThread):
        # UNWILLING_TO_PERFORM on bind usaually means trying to bind with blank password
        return workerThread.serverObject.bindPassword == "" and \
                isinstance(workerThread.exceptionObject, ldap.UNWILLING_TO_PERFORM)

###############################################################################

    def unbind(self):
        """Unbind from server.
        """
        
        try:
            if not(self.serverObject.bindAnon):
                self.ldapServerObject.unbind()
        except ldap.LDAPError, e:
            message = "LDAP unbind operation not successful. Reason:\n"
            message = message + str(e)
            self.logger.error(message)
            
###############################################################################

    # FIXME: implement better error handling for function which call 
    # getBaseDNList. Error handling inside is okay.
    def getBaseDNList(self):
        #environment.setBusy(True)

        bindSuccess, exceptionObject = self.bind()
            
        if not bindSuccess:
            #environment.setBusy(False)
            print "Bind failed"
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
        #environment.setBusy(False)
            
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
        
    def whileWaiting(self):
        qApp.processEvents()
        time.sleep(0.05)
        
    def setBusy(self, bool):
        # Do nothing -- should be done by the caller if needed
        """
        if bool:
            qApp.setOverrideCursor(Qt.WaitCursor)
        else:
            qApp.restoreOverrideCursor()
        """
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
        self.logger.debug("Started LDAP-search.")
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
        self.logger.debug("Search finished.")
        
###############################################################################

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

###############################################################################

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
    
###############################################################################
    
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
    
###############################################################################

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
            
            self.ldapServerObject = ldap.initialize(url.initializeUrl())
            self.ldapServerObject.protocol_version = 3
            
            # If we're going to present client certificates, this must be set as an option
            if self.serverObject.useCertificate and encryption:
                try:
                    self.ldapServerObject.set_option(ldap.OPT_X_TLS_CERTFILE,self.serverObject.clientCertFile)
                    self.ldapServerObject.set_option(ldap.OPT_X_TLS_KEYFILE,self.serverObject.clientCertKeyfile)
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
