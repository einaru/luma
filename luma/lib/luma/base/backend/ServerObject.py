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

    self.useCertificate: Indicates, if we should use clientside certificates

    self.clientCertFile: The Client certificate. PEM-file (string)

    self.clientCertKeyfile: The Client certificate private key. PEM-file (string)
    
    
    """
    
    authentificationMethods = [u"Simple", u"SASL Plain", u"SASL CRAM-MD5", 
        u"SASL DIGEST-MD5", u"SASL Login", u"SASL GSSAPI"]

###############################################################################

    def __init__(self):
        self.name = u""
        self.host = u""
        self.port = 389
        self.bindAnon = True
        self.autoBase = True
        self.baseDN = []
        self.bindDN = u""
        self.bindPassword = u""
        self.tls = False
        self.authMethod = u"Simple"
        self.followAliases = False
        self.useCertificate = False
        self.clientCertFile = u""
        self.clientCertKeyfile = u""
        
        # This value will only set during runtime
        self.currentBase = u""
        
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
        map(lambda x: finalString.append(unicode(x) + u", "), self.baseDN)
        finalString.append(unicode("\nCurrent Base: "))
        finalString.append(unicode(self.currentBase))
        finalString.append(unicode("\nBind DN: "))
        finalString.append(unicode(self.bindDN))
        finalString.append(unicode("\nBind Password: "))
        finalString.append(unicode(self.bindPassword))
        finalString.append(unicode("\nTLS: "))
        finalString.append(unicode(self.tls))
        finalString.append(unicode("\nAuthentification method: "))
        finalString.append(unicode(self.authMethod))
        finalString.append(unicode("\nUse Client certificate: "))
        finalString.append(unicode(self.useCertificate))
        finalString.append(unicode("\nClient certificate file: "))
        finalString.append(unicode(self.clientCertFile))
        finalString.append(unicode("\nClient certificate keyfile: "))
        finalString.append(unicode(self.clientCertKeyfile))
        finalString.append(unicode("\n"))

        return "".join(finalString)
