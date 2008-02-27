# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003, 2004 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import threading
import time

import environment
from base.backend.ServerObject import ServerObject
#from base.backend.SmartDataObject import SmartDataObject
from base.utils.backend.LogObject import LogObject

# For OpenSSL
hasSSLlibrary = 0 # Where 1 is true, and 0 is false
try:
    import socket
    import OpenSSL
    hasSSLlibrary = 1
except ImportError:
    hasSSLlibrary = 0

class LumaSSLConnectionException(Exception):
    """This exception class will be raised if no proper server object is passed 
    to the constructor."""
    pass

###############################################################################

class LumaSSLConnection(object):
    """ This class is a wrapper around the OpenSSL functions. It is provided to 
    access ssl enabled services to retrive certificates.
    
    Parameter is a ServerObject which contains all meta information for 
    accessing servers.
    """
    
    def __init__(self, serverMeta=None):
        global hasSSLlibrary
        # Throw exception if no ServerObject is passed.
        if not isinstance(serverMeta, ServerObject):
            exceptionString = u"Expected ServerObject type. Passed object was " + unicode(type(serverMeta))
            raise LumaSSLConnectionException, exceptionString

        if not hasSSLlibrary:
            raise LumaSSLConnectionException, "No SSL library available"
        
        self.certificate = None
        self.sslServerObject = None
        self.serverMeta = serverMeta
        
###############################################################################

    def connect(self):
        """Connect to server.
        """

        environment.setBusy(True)
        
        workerThread = WorkerThreadConnect(self.serverMeta)
        workerThread.start()
        
        while not workerThread.FINISHED:
            environment.updateUI()
            time.sleep(0.05)
        
        environment.setBusy(False)
        
        if workerThread.exceptionObject == None:
            message = "Connected successful."
            environment.logMessage(LogObject("Info", message))
            self.sslServerObject = workerThread.serverObject
            self.certificate = workerThread.certificate
            return (True, None)
        else:
            message = "SSL connection not successful. Reason:\n"
            message += str(workerThread.exceptionObject)
            environment.logMessage(LogObject("Error", message))
            return (False, workerThread.exceptionObject)
            
###############################################################################

    def getCertDetails(self):
        """Return details of certificate"""
        result = {}

        cert = self.certificate
        subject = cert.get_subject()
        issuer = cert.get_issuer()

        result["cnTo"]   = subject.CN
        result["oTo"]    = subject.O
        result["ouTo"]   = subject.OU
        result["serial"] = "%d" % cert.get_serial_number()
        result["cnBy"]   = issuer.CN
        result["oBy"]    = issuer.O
        result["ouBy"]   = issuer.OU
        result["valid"]  = cert.has_expired() and 1 or 0
        result["sha1"]   = cert.digest("sha1")
        result["md5"]    = cert.digest("md5")

        return result
            
###############################################################################

    def getPemDump(self):
        """Get PEM encoded certificate."""
        cert = self.certificate
        return OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM,cert)

###############################################################################

    def close(self):
        """Disconnect from server."""
        try:
            self.sslServerObject.close()
        except OpenSSL.SSL.Error, e:
            message = "SSL close connection not successful. Reason:\n"
            message += str(workerThread.exceptionObject)
            environment.logMessage(LogObject("Error", message))
            return (False, workerThread.exceptionObject)
        return (True, None)
            
###############################################################################

class WorkerThreadConnect(threading.Thread):
        
    def __init__(self, serverMeta):
        threading.Thread.__init__(self)

        self.FINISHED = False
        self.certificate = None
        self.serverObject = None
        self.exceptionObject = None
        self.serverMeta = serverMeta

    def run(self):
        try:
            if self.serverMeta.encryptionMethod == 'TLS':
                # TODO: Unable to handle TLS for the moment
                context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
            else:
                context = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv3_METHOD)
            self.serverObject = OpenSSL.SSL.Connection(context,socket.socket())
            self.serverObject.connect((self.serverMeta.host,self.serverMeta.port))
            self.serverObject.do_handshake()
            self.certificate = self.serverObject.get_peer_certificate()
        except OpenSSL.SSL.Error, e:
            self.exceptionObject = e
        except socket.error, e:
            self.exceptionObject = e
            
        self.FINISHED = True
        
###############################################################################
