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

###############################################################################

    def __init__(self):
        self.name = ""
        self.host = ""
        self.port = 389
        self.bindAnon = 0
        self.baseDN = ""
        self.bindDN = ""
        self.bindPassword = ""
        self.tls = 0
        
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
