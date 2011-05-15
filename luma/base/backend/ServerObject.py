# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Christian Forfang
#     Simen Natvig
#
# Luma is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public Licence as published by 
# the Free Software Foundation; either version 2 of the Licence, or 
# (at your option) any later version.
#
# Luma is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence 
# for more details.
#
# You should have received a copy of the GNU General Public Licence along 
# with Luma; if not, write to the Free Software Foundation, Inc., 
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

class ServerEncryptionMethod:
    Unencrypted = 0
    TLS = 1
    SSL = 2
    
class ServerAuthMethod:
    Simple = 0
    SASL_CRAM_MD5 = 1
    SASL_DIGEST_MD5 = 2
    SASL_EXTERNAL = 3
    SASL_GSSAPI = 4
    SASL_LOGIN = 5
    SASL_PLAIN = 7 
    
class ServerCheckCertificate:
    Never = 0
    Allow = 1
    Try = 2
    Demand = 3

class ServerObject(object):
    """
    This class represents a server with all its information.
    """
    
    #authentificationMethods = [u"Simple", u"SASL Plain", u"SASL CRAM-MD5", 
    #    u"SASL DIGEST-MD5", u"SASL Login", u"SASL GSSAPI"]

    numFields = 16 # Models need to know
    
    def __init__(self):
        
        # Holds the data about the server
        # Used for easy mapping to model-columns

        self._dataHolder = [
            #Index - Description (Options)
            u"",    # 0 Servername
            u"",    # 1 Hostname
            389,    # 2 Port
            True,   # 3 BindAnon
            True,   # 4 AutoBase
            [],     # 5 BaseDN
            u"",    # 6 BindDN ("username")
            u"",    # 7 BindPassword
            0,      # 8 encryptionMethod 8 (0=Unencrypted, 1=TLS, 2=SSL)
            0,      # 9 authMetod (0=simple, 1=SASL CRAM-MD5,
                    #              2=SASL DIGEST-MD5, 3=SASL EXTERNAL, 
                    #              4=SASL GSSLAPI, 5=SASL LOGIN,6=SASL Plain)
            False,  # 10 followAliases 
            False,  # 11 useCertificate 
            u"",    # 12 clientCertFile
            u"",    # 13 clientCertKeyfile
            0,      # 14 checkServerCertificate (0=never, 1=allow, 2=try, 3=demand)
            u""     # 15 currentBase
        ]
        
    
    #Returns the entire list
    def getList(self):
        return self._dataHolder
    
    #Given an index to the _dataHolder, sets the value
    def setIndexToValue(self, index, value):
        self._dataHolder[index] = value
        
    """
    Getterns and setters
    """
    @property
    def name(self):
        return unicode(self._dataHolder[0])
    
    @property
    def hostname(self):
        return unicode(self._dataHolder[1])
    
    @property
    def port(self):
        return self._dataHolder[2]
    
    @property
    def bindAnon(self):
        return self._dataHolder[3]
    
    @property
    def autoBase(self):
        return self._dataHolder[4]
    
    @property
    def baseDN(self):
        return self._dataHolder[5]
    
    @property
    def bindDN(self):
        return unicode(self._dataHolder[6])
    
    @property
    def bindPassword(self):
        return unicode(self._dataHolder[7])
    
    @property
    def encryptionMethod(self):
        return self._dataHolder[8]
    
    @property
    def authMethod(self):
        return self._dataHolder[9]
    
    @property
    def followAliases(self):
        return self._dataHolder[10]
    
    @property
    def useCertificate(self):
        return self._dataHolder[11]
    
    @property
    def clientCertFile(self):
        return unicode(self._dataHolder[12])
    
    @property
    def clientCertKeyFile(self):
        return unicode(self._dataHolder[13])
    
    @property
    def checkServerCertificate(self):
        return self._dataHolder[14]
    
    @property
    def currentBase(self):
        return self._dataHolder[15]
    
    @name.setter
    def name(self, name):
        self._dataHolder[0] = name
    
    @hostname.setter
    def hostname(self, host):
        self._dataHolder[1] = host
    
    @port.setter
    def port(self, port):
        self._dataHolder[2] = port
    
    @bindAnon.setter    
    def bindAnon(self, value):
        if value == True or value == False:
            self._dataHolder[3] = value
    
    @autoBase.setter   
    def autoBase(self, value):
        if value == True or value == False:
            self._dataHolder[4] = value
    
    @baseDN.setter
    def baseDN(self, value):
        self._dataHolder[5] = value
    
    @bindDN.setter
    def bindDN(self, value):
        self._dataHolder[6] = value
    
    @bindPassword.setter
    def bindPassword(self, value):
        self._dataHolder[7] = value
    
    @encryptionMethod.setter
    def encryptionMethod(self, value):
        self._dataHolder[8] = value
    
    @authMethod.setter
    def authMethod(self, value):
        self._dataHolder[9] = value
    
    @followAliases.setter
    def followAliases(self, value):
        if value == True or value == False:
            self._dataHolder[10] = value
    
    @useCertificate.setter
    def useCertificate(self, value):
        if value == True or value == False:
            self._dataHolder[11] = value

    @clientCertFile.setter
    def clientCertFile(self, value):
        self._dataHolder[12] = value
    
    @clientCertKeyFile.setter
    def clientCertKeyFile(self, value):
        self._dataHolder[13] = value
    
    @checkServerCertificate.setter
    def checkServerCertificate(self, value):
        self._dataHolder[14] = value
    
    @currentBase.setter
    def currentBase(self, value):
        self._dataHolder[15] = value
    
    def __repr__(self):
        finalString = []
        finalString.append(unicode("Name: "))
        finalString.append(unicode(self.name))
        finalString.append(unicode("\nHost: "))
        finalString.append(unicode(self.hostname))
        finalString.append(unicode("\nPort: "))
        finalString.append(unicode(self.port))
        finalString.append(unicode("\nBind anonymously: "))
        finalString.append(unicode(self.bindAnon))
        finalString.append(unicode("\nAutobase: "))
        finalString.append(unicode(self.autoBase))
        finalString.append(unicode("\nBase DN: "))
        map(lambda x: finalString.append(unicode(x) + u", "), self.baseDN)
        finalString.append(unicode("\nCurrent Base: "))
        finalString.append(unicode(self.currentBase))
        finalString.append(unicode("\nBind DN: "))
        finalString.append(unicode(self.bindDN))
        finalString.append(unicode("\nBind Password: "))
        finalString.append(unicode(self.bindPassword))
        finalString.append(unicode("\nEncryption method: "))
        finalString.append(unicode(self.encryptionMethod))
        finalString.append(unicode("\nAuthentification method: "))
        finalString.append(unicode(self.authMethod))
        finalString.append(unicode("\nUse Client certificate: "))
        finalString.append(unicode(self.useCertificate))
        finalString.append(unicode("\nClient certificate file: "))
        finalString.append(unicode(self.clientCertFile))
        finalString.append(unicode("\nClient certificate keyfile: "))
        finalString.append(unicode(self.clientCertKeyFile))
        finalString.append(unicode("\nCheck server certificate: "))
        finalString.append(unicode(self.checkServerCertificate))
        finalString.append(unicode("\n"))
        return "".join(finalString)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
