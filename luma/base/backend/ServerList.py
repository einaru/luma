# -*- coding: utf-8 -*-
#
# lumaWithOptions
#
# Copyright (c) 2011
#     Christian Forfang, <simen.natvig@gmail.com>
#     Simen Natvig, <cforfang@gmail.com>
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# Copyright (c) 2003
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

import os.path
import logging
import stat
import tempfile

from PyQt4.QtXml import QDomDocument

from ..backend.ServerObject import ServerObject
from base.backend.ServerObject import ServerEncryptionMethod,\
    ServerCheckCertificate, ServerAuthMethod
from base.util.Paths import getConfigPrefix

class ServerList(object):
    """
    Object for managing the list of available servers.
    """

    __logger = logging.getLogger(__name__)

    # The cache for the client side ssl certificates. 
    # The filename is the key; a tupel containing the modification time
    # and the cert as StringIO objects.
    certCache = {}

    def __init__(self, configPrefix=None, serverlist="serverlist.xml"):
        """
        @param configPrefix: string filepath;
            The configuration filepath prefix to the location of the
            serverlist
        @param serverlist: string;
            The filename of the serverlist.
        """
        if configPrefix == None:
            #TODO: Should get default (or remove this feature alltogheter)
            #      possible not in use currently.
            # Using the python tempfile module to get the temp dir in a
            # cross-platform manner
            success, path = getConfigPrefix()
            if success:
                configPrefix = path
            else:
                configPrefix = tempfile.gettempdir()
            
        self.__serverList = []
        self.__configPrefix = configPrefix
        self.__configFile = os.path.join(self.__configPrefix, serverlist)
        
        # Read the existing serverlist, if any
        if os.path.isfile(self.__configFile):
            self.__readServerList()
            
    def getConfigFilePath(self):
        """
        @return: a string with the path to serverlist.xml
        """
        return self.__configFile

    def getTable(self):
        """
        @return: a list of server objects
        """
        return self.__serverList

    def setTable(self, serverList):
        """
        Sets the list of server objets
        
        @param serverList: a list;
            a list of server objects
        """
        self.__serverList = serverList

    def getServerObject(self, serverName):
        """ 
        Get a server object by its name.
        
        @param serverName: string;
            the name of the server to get object attributes from
        @return: the server object for the matching serverName.
            If the serverlist is empty or no match is found,
            None is returned.
        """
        if self.__serverList != None:
            for x in self.__serverList:
                if x.name == serverName:
                    return  x
        return None

    def addServer(self, serverObject):
        """ 
        Add a server to the server list.
        
        @param serverObject: ServerObject;
            the server object to add to the server list.
        """
        self.__logger.debug('Adding server so self.serverList')

        if self.__serverList == None:
            self.__serverList = [serverObject]
        else:
            self.__serverList.append(serverObject)
    
    def getIndexByName(self, serverName):
        
        for i in xrange(len(self.__serverList)):
            if self.__serverList[i].name == serverName:
                return i
        return -1

    def deleteServer(self, serverName):
        """
        Delete a server from the server list.
        
        @param serverName: string;
            the name of the server to delete.
        """
        self.__logger.debug('Deleting server from self.serverList')
        self.__serverList = filter(lambda x: not (x.name == serverName), self.__serverList)

    def deleteServerByIndex(self, index):
        """
        Delete a server from the server list. 
        
        @param index: integer;
            the index of the server to delete.
        """
        self.__logger.debug('Deleting server (using an index) from self.serverList')
        del self.__serverList[index]

    def writeServerList(self):
        """ 
        Save the server list to configuration file.
        """
        self.__logger.debug('Saving serverlist to disk')

        document = QDomDocument('LumaServerFile')
        root = document.createElement('LumaServerList')
        root.setAttribute('version', '1.2')
        document.appendChild(root)
        
        for serverObject in self.__serverList:
            node = document.createElement('LumaLdapServer')
            node.setAttribute('name', serverObject.name)
            node.setAttribute('host', serverObject.hostname)
            node.setAttribute('port', serverObject.port)
            node.setAttribute('bindAnon', serverObject.bindAnon)
            node.setAttribute('bindDN', serverObject.bindDN)
            node.setAttribute('bindPassword', serverObject.bindPassword)
            node.setAttribute('encryptionMethod', serverObject.encryptionMethod)
            node.setAttribute('authMethod', serverObject.authMethod)
            node.setAttribute('autoBase', serverObject.autoBase)
            node.setAttribute('followAliases', serverObject.followAliases)
            node.setAttribute('checkServerCertificate', serverObject.checkServerCertificate)
            node.setAttribute('useCertificate', serverObject.useCertificate)
            node.setAttribute('clientCertFile', serverObject.clientCertFile)
            node.setAttribute('clientCertKeyFile', serverObject.clientCertKeyFile)

            baseNode = document.createElement('baseDNs')
            
            for tmpBase in serverObject.baseDN:
                tmpNode = document.createElement('base')
                tmpNode.setAttribute('dn', tmpBase)
                baseNode.appendChild(tmpNode)
            
            node.appendChild(baseNode)
            root.appendChild(node)

        if not os.path.exists(self.__configPrefix):
            os.makedirs(self.__configPrefix)

        try:
            fileHandler = open(self.__configFile, 'w')
            fileHandler.write(unicode(document.toString()).encode('utf-8'))
            fileHandler.close()
        except:
            debug = 'Could not write to file: %s' % self.__configFile
            self.__logger.error(debug)

        # Only the user should be able to access the file since we store 
        # passwords in it. If we can't change it, leave it as it is since
        # the user must have changed it manually. 
        try:
            #os.chmod(self.__configFile, 0600)
            os.chmod(self.__configFile, stat.S_IRUSR | stat.S_IWUSR)
        except:
            debug = 'Could not set permission on: %s' % self.__configFile
            self.__logger.debug(debug)

    def readServerList(self):
        """ 
        Read the server list from configuration file.
        """
        self.__readServerList()

    def __readServerList(self):
        """ 
        Read the server list from configuration file.
        """
        self.__logger.debug("Reading serverlist from disk")

        if not os.path.isfile(self.__configFile):
            self.__logger.error("Serverlist not found")
            self.__serverList = []
            return

        serverList = self.__readFromXML()
        if serverList != None:
            self.__serverList = serverList

    def __readFromXML(self):
        """
        Reads the serverlist from disk.
        """
        debug = 'Calling __readFromXML() to load serverlist from disk'
        self.__logger.debug(debug)

        fileContent = ''
        try:
            fileContent = ''.join(open(self.__configFile, "r").readlines())
            # If this is uncommentet, non-ascii characters stops working.
            # It's probably also decoded by QDomDocument, so decoding now 
            # means it's decoded twice - which doesn't work.
            #fileContent = fileContent.decode("utf-8")
        except IOError, e:
            error = 'Could not read server configuration file. Reason:\n%s' \
                    % str(e)
            self.__logger.error(error)

        document = QDomDocument('LumaServerFile')
        document.setContent(fileContent)

        root = document.documentElement()
        if not (unicode(root.tagName()) == 'LumaServerList'):
            error = 'Could not parse server configuration file.'
            self.__logger.error(error)

        serverList = None

        if root.attribute('version') == '1.0':
            self.__logger.error('Can not read old serverconfig')
            #serverList = self._readFromXMLVersion1_0(fileContent)
        elif root.attribute('version') == '1.1':
            self.__logger.info('Loaded serverlist from Luma 2.x. This will be automatically converted on next save.')
            serverList = self._readFromXMLVersion1_1(fileContent)
        elif root.attribute('version') == '1.2':
            serverList = self.__readFromXMLVersion1_2(fileContent)

        return serverList

    def __readFromXMLVersion1_2(self, fileContent):
        """
        Reads serverlist version 1.2 from disk.
        """
        debug = 'Using __readFromXMLVersion1_2 to load serverlist from disk'
        self.__logger.debug(debug)

        document = QDomDocument('LumaServerFile')
        document.setContent(fileContent)
        root = document.documentElement()

        serverList = []

        child = root.firstChild()
        while (not child.isNull()):
            server = ServerObject()
            element = child.toElement()
            if unicode(element.tagName()) == 'LumaLdapServer':
                server.name = unicode(element.attribute('name'))
                server.hostname = unicode(element.attribute('host'))
                server.port = int(str(element.attribute('port')))

                tmpVal = unicode(element.attribute('bindAnon'))
                server.bindAnon = int(tmpVal)

                tmpVal = unicode(element.attribute('autoBase'))
                server.autoBase = int(tmpVal)

                server.bindDN = unicode(element.attribute('bindDN'))
                server.bindPassword = unicode(element.attribute('bindPassword'))

                server.encryptionMethod = int(element.attribute('encryptionMethod'))

                server.checkServerCertificate = int(element.attribute('checkServerCertificate'))
                server.clientCertFile = unicode(element.attribute('clientCertFile'))
                server.clientCertKeyFile = unicode(element.attribute('clientCertKeyFile'))

                tmpVal = unicode(element.attribute('useCertificate'))
                server.useCertificate = int(tmpVal)

                tmpVal = unicode(element.attribute('followAliases'))
                server.followAliases = int(tmpVal)

                server.authMethod = int(element.attribute('authMethod'))

                serverChild = child.firstChild()
                serverElement = serverChild.toElement()
                tagName = unicode(serverElement.tagName())

                if 'baseDNs' == tagName:
                    baseDN = []
                    baseNode = serverChild.firstChild()
                    while (not baseNode.isNull()):
                        baseElement = baseNode.toElement()
                        tmpBase = unicode(baseElement.tagName())
                        if 'base' == tmpBase:
                            baseDN.append(unicode(baseElement.attribute('dn')))
                        baseNode = baseNode.nextSibling()
                server.baseDN = baseDN

            serverList.append(server)
            child = child.nextSibling()

        return serverList


    def _readFromXMLVersion1_1(self, fileContent):
        
        self.__logger.debug("Using _readFromXMLVersion1_1() to load serverlist from disk")
        
        document = QDomDocument("LumaServerFile")
        document.setContent(fileContent)
        root = document.documentElement()
        
        serverList = []
        
        child = root.firstChild()
        while (not child.isNull()):
            server = ServerObject()
            element = child.toElement()
            if unicode(element.tagName()) == "LumaLdapServer":
                server.name = unicode(element.attribute("name"))
                server.hostname = unicode(element.attribute("host"))
                server.port = int(str(element.attribute("port")))
                
                tmpVal = unicode(element.attribute("bindAnon"))
                if "True" == tmpVal:
                    server.bindAnon = 1
                else:
                    server.bindAnon = 0
                    
                tmpVal = unicode(element.attribute("autoBase"))
                if "True" == tmpVal:
                    server.autoBase = 1
                else:
                    server.autoBase = 0
                    
                    
                server.bindDN = unicode(element.attribute("bindDN"))
                server.bindPassword = unicode(element.attribute("bindPassword"))
                
                tmp = unicode(element.attribute("encryptionMethod"))
                if tmp == "None":
                    server.encryptionMethod = ServerEncryptionMethod.Unencrypted
                elif tmp == "SSL":
                    server.encryptionMethod = ServerEncryptionMethod.SSL
                elif tmp == "TLS":
                    server.encryptionMethod = ServerEncryptionMethod.TLS
                    
                tmp = unicode(element.attribute("checkServerCertificate"))
                if tmp == "never":
                    server.checkServerCertificate = ServerCheckCertificate.Never
                elif tmp == "try":
                    server.checkServerCertificate = ServerCheckCertificate.Try
                elif tmp == "demand":
                    server.checkServerCertificate = ServerCheckCertificate.Demand
                elif tmp == "allow":
                    server.checkServerCertificate = ServerCheckCertificate.Allow
                
                
                server.clientCertFile = unicode(element.attribute("clientCertFile"))
                server.clientCertKeyFile = unicode(element.attribute("clientCertKeyfile"))
                
                tmpVal = unicode(element.attribute("useCertificate"))
                if tmpVal == "True":
                    server.useCertificate = True
                else:
                    server.useCertificate = False
                    
                tmpVal = unicode(element.attribute("followAliases"))
                if "True" == tmpVal:
                    server.followAliases = True
                else:
                    server.followAliases = False
                
                tmp = unicode(element.attribute("authMethod"))
                if tmp == "SASL DIGEST-MD5":
                    server.authMethod = ServerAuthMethod.SASL_DIGEST_MD5
                elif tmp == "SASL CRAM-MD5":
                    server.authMethod = ServerAuthMethod.SASL_CRAM_MD5
                elif tmp == "SASL EXTERNAL":
                    server.authMethod = ServerAuthMethod.SASL_EXTERNAL
                elif tmp == "SASL GSSAPI":
                    server.authMethod = ServerAuthMethod.SASL_GSSAPI
                elif tmp == "SASL Login":
                    server.authMethod = ServerAuthMethod.SASL_LOGIN
                elif tmp == "SASL Plain":
                    server.authMethod = ServerAuthMethod.SASL_PLAIN
                elif tmp == "Simple":
                    server.authMethod = ServerAuthMethod.Simple
                
                serverChild = child.firstChild()
                serverElement = serverChild.toElement()
                tagName = unicode(serverElement.tagName())
                    
                if "baseDNs" == tagName:
                    baseDN = []
                    baseNode = serverChild.firstChild()
                    while (not baseNode.isNull()):
                        baseElement = baseNode.toElement()
                        tmpBase = unicode(baseElement.tagName())
                        if "base" == tmpBase:
                            baseDN.append(unicode(baseElement.attribute("dn")))
                        baseNode = baseNode.nextSibling()
                server.baseDN = baseDN
                
            serverList.append(server)
            child = child.nextSibling()
        
        return serverList
