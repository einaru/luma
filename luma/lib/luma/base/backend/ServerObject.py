# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

class ServerObject(object):
    """This class represents a server with all its information.
    
    self.name: The user-visible name of the server (string).
    
    self.host: The hostname of the server (string).
    
    self.port: The port of the server (integer).
    
    self.bindAnon: Indicates if the bind should be anonymously (integer).
    
    self.baseDN: The baseDN of the server (string).
    
    self.bindDN: If not bind anonymously, use this name (string).
    
    self.bindPassword: The password for the bindDN (string).
    
    self.tls: Indicates, if we should use tls to connect to the server 
    (integer).
    
    
    """
    
    __slots__ = ('nameP', 'hostP', 'portP', 'bindAnonP', 'baseDNP', 'bindDNP', 
        'bindPasswordP', 'tlsP', 'authMethodP')
    
    authentificationMethods = [u"Simple", u"SASL Plain", u"SASL CRAM-MD5", 
        u"SASL DIGEST-MD5", u"SASL Login", u"SASL GSSAPI"]

###############################################################################

    def __init__(self):
        self.nameP = ""
        self.hostP = ""
        self.portP = 389
        self.bindAnonP = 0
        self.baseDNP = ""
        self.bindDNP = ""
        self.bindPasswordP = ""
        self.tlsP = 0
        self.authMethodP = "Simple"
        
###############################################################################

    def __repr__(self):
        finalString = []

        finalString.append(unicode("Name: "))
        finalString.append(unicode(self.name))
        finalString.append(unicode("\nHost: "))
        finalString.append(unicode(self.host))
        finalString.append(unicode("\nPort: "))
        finalString.append(unicode(self.port))
        finalString.append(unicode("\nBind anonymously: "))
        finalString.append(unicode(self.bindAnon))
        finalString.append(unicode("\nBase DN: "))
        finalString.append(unicode(self.baseDN))
        finalString.append(unicode("\nBind DN: "))
        finalString.append(unicode(self.bindDN))
        finalString.append(unicode("\nBind Password: "))
        finalString.append(unicode(self.bindPassword))
        finalString.append(unicode("\nTLS: "))
        finalString.append(unicode(self.tls))
        finalString.append(unicode("\nAuthentification method: "))
        finalString.append(unicode(self.authMethod))
        finalString.append(unicode("\n"))

        return "".join(finalString)
        
###############################################################################


    def __setName(self, name):
        if isinstance(name, unicode):
            self.nameP = name
        else:
            raise AttributeError, "Expected an unicode string."
            
    def __getName(self):
        return self.nameP
            
    
    name = property(__getName, __setName, None, "Name of the server.")
        
###############################################################################

    def __setHost(self, host):
        if isinstance(host, unicode):
            self.hostP = host
        else:
            raise AttributeError, "Expected an unicode string."
            
    def __getHost(self):
        return self.hostP
            
    
    host = property(__getHost, __setHost, None, "Host address of the server.")
    
###############################################################################

    def __setPort(self, port):
        if not(isinstance(port, int)):
            raise AttributeError, "Expected an integer."
            
        if (port < 0) or (port > 65535):
            raise ValueError, "Port not in range 0-65535"
            
        self.portP = port
            
            
    def __getPort(self):
        return self.portP
            
    
    port = property(__getPort, __setPort, None, "Port of the server.")
    
###############################################################################

    def __setBindAnon(self, value):
        if isinstance(value, bool):
            self.bindAnonP = value
        else:
            raise AttributeError, "Expected a boolean."
            
    def __getBindAnon(self):
        return self.bindAnonP
            
    
    bindAnon = property(__getBindAnon, __setBindAnon, None, "Port of the server.")
    
###############################################################################

    def __setBaseDN(self, value):
        if isinstance(value, unicode):
            self.baseDNP = value
        else:
            raise AttributeError, "Expected an unicode string."
            
    def __getBaseDN(self):
        return self.baseDNP
            
    
    baseDN = property(__getBaseDN, __setBaseDN, None, "Base DN of the server.")
    
###############################################################################

    def __setBindDN(self, value):
        if isinstance(value, unicode):
            self.bindDNP = value
        else:
            raise AttributeError, "Expected an unicode string."
            
    def __getBindDN(self):
        return self.bindDNP
            
    
    bindDN = property(__getBindDN, __setBindDN, None, "Base DN of the server.")
    
###############################################################################

    def __setBindPassword(self, value):
        if isinstance(value, unicode):
            self.bindPasswordP = value
        else:
            raise AttributeError, "Expected an unicode string."
            
    def __getBindPassword(self):
        return self.bindPasswordP
            
    
    bindPassword = property(__getBindPassword, __setBindPassword, None, "Bind password of the server.")

###############################################################################

    def __setTls(self, value):
        if isinstance(value, bool):
            self.tlsP= value
        else:
            raise AttributeError, "Expected a boolean."
            
    def __getTls(self):
        return self.tlsP
            
    
    tls = property(__getTls, __setTls, None, "Connect with/without tls to the server.")

###############################################################################

    def __setMethod(self, value):
        if isinstance(value, unicode):
            self.authMethodP= value
        else:
            raise AttributeError, "Expected an unicode string."
            
        if not(value in self.authentificationMethods):
            raise AttributeError, "Not a supported method."
            
    def __getMethod(self):
        return self.authMethodP
            
    
    authMethod = property(__getMethod, __setMethod, None, "Authentification method.")
