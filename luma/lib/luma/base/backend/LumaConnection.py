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
    
import threading
import copy
import time

import environment
from base.backend.ServerObject import ServerObject
from base.backend.SmartDataObject import SmartDataObject
from base.utils.backend.LogObject import LogObject
from base.utils.gui.PromptPasswordDialog import PromptPasswordDialog

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
    _passwordMap = {}
    
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

    def search(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None, attrsonly=0, sizelimit=0):
        """Aynchronous search.
        """
        
        environment.setBusy(True)
        
        workerThread = WorkerThreadSearch(self.ldapServerObject)
        workerThread.base = base
        workerThread.scope = scope
        workerThread.filter = filter
        workerThread.attrList = attrList
        workerThread.attrsonly = attrsonly
        workerThread.sizelimit = sizelimit
        workerThread.start()
        
        while not workerThread.FINISHED:
            environment.updateUI()
            time.sleep(0.05)
            
        if None == workerThread.exceptionObject:
            resultList = []
            for x in workerThread.result:
                copyItem = copy.deepcopy(x)
                ldapObject = SmartDataObject(copyItem, self.serverMeta)
                resultList.append(ldapObject)
                
            environment.setBusy(False)
            message = "Received " + str(len(resultList)) + " item(s) from LDAP search operation."
            environment.logMessage(LogObject("Info", message))
            return (True, resultList, None)
        else:
            # Did we hit the server side search limit?
            if isinstance(workerThread.exceptionObject, ldap.SIZELIMIT_EXCEEDED):
                resultList = []
                for x in workerThread.result:
                    copyItem = copy.deepcopy(x)
                    resultList.append(SmartDataObject(copyItem, self.serverMeta))
                
                environment.setBusy(False)
                environment.displaySizeLimitWarning()
                message = "Received " + str(len(resultList)) + " item(s) from LDAP search operation. But server side search limit has been reached."
                environment.logMessage(LogObject("Info", message))
                return (True, resultList, None)
            else:
                environment.setBusy(False)
                message = "LDAP search operation failed. Reason:\n" + str(workerThread.exceptionObject)
                environment.logMessage(LogObject("Error", message))
                return (False, None, workerThread.exceptionObject)
            
            
            
###############################################################################

    def delete(self, dnDelete=None):
        """ Synchronous delete.
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
        
        if None == workerThread.exceptionObject:
            message = "LDAP object " + dnDelete + " successfully deleted."
            environment.logMessage(LogObject("Info", message))
            return (True, None)
        else:
            message = "LDAP object " + dnDelete + " could not be deleted. Reason:\n"
            message = message + str(workerThread.exceptionObject)
            environment.logMessage(LogObject("Error", message))
            return (False, workerThread.exceptionObject)
            
###############################################################################

    def modify(self, dn, modlist=None):
        """ Synchronous modify.
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
        
        if None == workerThread.exceptionObject:
            message = "LDAP object " + dn + " successfully modified."
            environment.logMessage(LogObject("Info", message))
            return (True, None)
        else:
            message = "LDAP object " + dn + " could not be modified. Reason:\n"
            message = message + str(workerThread.exceptionObject)
            environment.logMessage(LogObject("Error", message))
            return (False, workerThread.exceptionObject)

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
        
        if None == workerThread.exceptionObject:
            message = "LDAP object " + dn + " successfully added."
            environment.logMessage(LogObject("Info", message))
            return (True, None)
        else:
            message = "LDAP object " + dn + " could not be added. Reason:\n"
            message = message + str(workerThread.exceptionObject)
            environment.logMessage(LogObject("Error", message))
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
            message = message + str(workerThread.exceptionObject)
            environment.logMessage(LogObject("Error", message))
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
        environment.setBusy(True)
        workerThread = self.__bind()
        
        # Prompt for password on INVALID_CREDENTIALS or UNWILLING_TO_PERFORM
        # UNWILLING_TO_PERFORM on bind usaually means trying to bind with blank password
        if  isinstance(workerThread.exceptionObject, ldap.INVALID_CREDENTIALS) or \
            isinstance(workerThread.exceptionObject, ldap.UNWILLING_TO_PERFORM):
            if LumaConnection._passwordMap.has_key(self.serverMeta.name):
                self.serverMeta.bindPassword = LumaConnection._passwordMap[self.serverMeta.name]
                workerThread = self.__bind()
            else:
                environment.setBusy(False)
                dialog = PromptPasswordDialog()
                dialog.exec_loop()
                if dialog.result() == 1:
                    environment.setBusy(False)
                    self.serverMeta.bindPassword = unicode(dialog.passwordEdit.text())
                    LumaConnection._passwordMap[self.serverMeta.name] = self.serverMeta.bindPassword
                    workerThread = self.__bind()

        environment.setBusy(False)

        if workerThread.exceptionObject == None:
            message = "LDAP bind operation successful."
            environment.logMessage(LogObject("Info", message))
            self.ldapServerObject = workerThread.ldapServerObject
            return (True, None)
        else:
            message = "LDAP bind operation not successful. Reason:\n"
            message += str(workerThread.exceptionObject)
            environment.logMessage(LogObject("Error", message))
            # If credentials are still wrong after prompting, remove from passwordmap
            if isinstance(workerThread.exceptionObject, ldap.INVALID_CREDENTIALS):
                if LumaConnection._passwordMap.has_key(self.serverMeta.name):
                    LumaConnection._passwordMap.pop(self.serverMeta.name)
            return (False, workerThread.exceptionObject)

    def __bind(self):
        workerThread = WorkerThreadBind(self.serverMeta)
        workerThread.start()
        
        while not workerThread.FINISHED:
            environment.updateUI()
            time.sleep(0.05)
        return workerThread
        
###############################################################################

    def unbind(self):
        """Unbind from server.
        """
        
        try:
            if not(self.serverMeta.bindAnon):
                self.ldapServerObject.unbind()
        except ldap.LDAPError, e:
            message = "LDAP unbind operation not successful. Reason:\n"
            message = message + str(e)
            environment.logMessage(LogObject("Error", message))
            
###############################################################################

    # FIXME: implement better error handling for function which call 
    # getBaseDNList. Error handling inside is okay.
    def getBaseDNList(self):
        environment.setBusy(True)

        bindSuccess, exceptionObject = self.bind()
            
        if not bindSuccess:
            environment.setBusy(False)
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
        # not jet tested
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
        environment.setBusy(False)
            
        if None == dnList:
            message = "Could not retrieve Base DNs from server. Unknown server type."
            environment.logMessage(LogObject("Error", message))
            return (False, None, "Unknown server type")
        else:
            message = "Base DNs successfully retrieved from server."
            environment.logMessage(LogObject("Info", message))
            return (True, dnList, None)
            
###############################################################################

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
        
###############################################################################

class WorkerThreadSearch(threading.Thread):
        
    def __init__(self, serverObject):
        threading.Thread.__init__(self)
        self.ldapServerObject = serverObject

        self.sizelimit = 0
            
        self.FINISHED = False
        self.result = []
        self.exceptionObject = None
            
    def run(self):
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
        except ldap.LDAPError, e:
            self.exceptionObject = e
            
        self.FINISHED = True
        
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
    
    def __init__(self, serverMeta):
        threading.Thread.__init__(self)
        self.ldapServerObject = None
        self.serverMeta = serverMeta
        
        self.FINISHED = False
        self.result = False
        self.exceptionObject = None
        
    def run(self):
        try:
            urlschemeVal = "ldap"
            if self.serverMeta.encryptionMethod == "SSL":
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
            
            # Check whether we want to validate the server certificate.
            validateMethod = ldap.OPT_X_TLS_DEMAND
            if self.serverMeta.checkServerCertificate == u"demand":
                validateMethod = ldap.OPT_X_TLS_DEMAND
            elif self.serverMeta.checkServerCertificate == u"never":
                validateMethod = ldap.OPT_X_TLS_NEVER
            elif self.serverMeta.checkServerCertificate == u"try":
                validateMethod = ldap.OPT_X_TLS_TRY
            elif self.serverMeta.checkServerCertificate == u"allow":
                validateMethod = ldap.OPT_X_TLS_ALLOW
            
            encryption = False
            if self.serverMeta.encryptionMethod == "SSL":
                encryption = True
            elif self.serverMeta.encryptionMethod == "TLS":
                encryption = True
            
            if encryption:
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, validateMethod)
                #self.ldapServerObject.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, validateMethod)
            
            
            # If we're going to present client certificates, this must be set as an option
            if self.serverMeta.useCertificate and encryption:
                try:
                    self.ldapServerObject.set_option(ldap.OPT_X_TLS_CERTFILE,self.serverMeta.clientCertFile)
                    self.ldapServerObject.set_option(ldap.OPT_X_TLS_KEYFILE,self.serverMeta.clientCertKeyfile)
                except Exception, e:
                    message = "Certificate error. Reason:\n"
                    message += "Could not set client certificate and certificate keyfile. "
                    message += str(e)
                    environment.logMessage(LogObject("Error,",message))
                    
            
            if self.serverMeta.encryptionMethod == "TLS":
                self.ldapServerObject.start_tls_s()
            
            # Enable Alias support
            if self.serverMeta.followAliases:
                self.ldapServerObject.set_option(ldap.OPT_DEREF, ldap.DEREF_ALWAYS)
            
            if self.serverMeta.bindAnon:
                self.ldapServerObject.simple_bind()
            elif self.serverMeta.authMethod == u"Simple":
                self.ldapServerObject.simple_bind_s(whoVal, credVal)
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
                elif self.serverMeta.authMethod == u"SASL EXTERNAL":
                    sasl_mech = "EXTERNAL"
                    
                sasl_auth = ldap.sasl.sasl(sasl_cb_value_dict,sasl_mech)
                
                # If python-ldap has no support for SASL, it doesn't have 
                # sasl_interactive_bind_s as a method.
                try:
                    if "EXTERNAL" == sasl_mech:
                        #url = ldapurl.LDAPUrl(urlscheme="ldapi", 
                        #    hostport = self.serverMeta.host.replace("/", "%2f"),
                        #    dn = self.serverMeta.baseDN)
                            
                        url = "ldapi://" + self.serverMeta.host.replace("/", "%2F").replace(",", "%2C")
            
                        #self.ldapServerObject = ldap.initialize(url.initializeUrl())
                        self.ldapServerObject = ldap.initialize(url)
                        self.ldapServerObject.protocol_version = 3
            
                        # Enable Alias support
                        if self.serverMeta.followAliases:
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
            
