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
    
    __slots__ = ('nameP', 'hostP', 'portP', 'bindAnonP', 'baseDNP', 'bindDNP', 'bindPasswordP', 'tlsP')

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
        
###############################################################################

    def __repr__(self):
        finalString = ""

        finalString = "Name: " + self.name
        finalString = finalString + "\nHost: " + self.host
        portString = str(self.port)
        finalString = finalString + "\nPort: " + portString
        finalString = finalString + "\nBind anonymously: " + str(self.bindAnon)
        finalString = finalString + "\nBase DN: " + self.baseDN
        finalString = finalString + "\nBind DN: " + self.bindDN
        finalString = finalString + "\nBind Password: " + self.bindPassword
        finalString = finalString + "\nTLS: " + str(self.tls) + "\n"

        return finalString
        
###############################################################################


    def __setName(self, name):
        if isinstance(name, str):
            self.nameP = name
        else:
            raise AttributeError, "Expected a string."
            
    def __getName(self):
        return self.nameP
            
    
    name = property(__getName, __setName, None, "Name of the server.")
        
###############################################################################

    def __setHost(self, host):
        if isinstance(host, str):
            self.hostP = host
        else:
            raise AttributeError, "Expected a string."
            
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
        if isinstance(value, str):
            self.baseDNP = value
        else:
            raise AttributeError, "Expected a string."
            
    def __getBaseDN(self):
        return self.baseDNP
            
    
    baseDN = property(__getBaseDN, __setBaseDN, None, "Base DN of the server.")
    
###############################################################################

    def __setBindDN(self, value):
        if isinstance(value, str):
            self.bindDNP = value
        else:
            raise AttributeError, "Expected a string."
            
    def __getBindDN(self):
        return self.bindDNP
            
    
    bindDN = property(__getBindDN, __setBindDN, None, "Base DN of the server.")
    
###############################################################################

    def __setBindPassword(self, value):
        if isinstance(value, str):
            self.bindPasswordP = value
        else:
            raise AttributeError, "Expected a string."
            
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


