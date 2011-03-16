# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Christian Forfang
#     Simen Natvig
#
# Copyright (c) 2003
#     Wido Depping, <widod@users.sourceforge.net>
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
import os.path
import logging
import copy

from PyQt4.QtXml import QDomDocument

import stat
from base.backend.ServerObject import ServerObject

class ServerList(object):
    """Object for managing the list of available servers.
    """
    
    _logger = logging.getLogger(__name__)
    
    # The cache for the client side ssl certificates
    # The filename is the key. In a tupel are the modification time and the 
    # cert as StringIO objects
    certCache = {}
    
    def __init__(self, configPrefix = None, serverFileName = "serverlist.xml"):
        if configPrefix == None:
            #TODO Should get default (or remove this feature alltogheter)
            #possible not in use currentlt
            configPrefix = "/tmp"
        self._serverList = []
        self._configPrefix = configPrefix
        self._configFile = os.path.join(self._configPrefix, serverFileName)
        
        if os.path.isfile(self._configFile):
            self._readServerList()            

    def getTable(self):
        """
        Return the list of ServerObject
        """
        return self._serverList
    
    def setTable(self, serverList):
        """
        Sets the list of ServerObjets
        """

        self._serverList = serverList
    
    def getServerObject(self, serverName):
        """ 
        Get a server object by its name.
        """
        
        retVal = None
        for x in self._serverList:
            if x.name == serverName:
                retVal = x
                break  
        return retVal

    def addServer(self, serverObject):
        """ 
        Add a server to the server list.
        """

        self._logger.debug("Adding server so self.serverList")
        
        if self._serverList == None:
            self._serverList = [serverObject]
        else:
            self._serverList.append(serverObject)
            
    def deleteServer(self, serverName):
        """ Delete a server from the server list.
        """
        self._logger.debug("Deleting server from self.serverList")
        self._serverList = filter(lambda x: not (x.name == serverName), self._serverList)
        
    def deleteServerByIndex(self, index):
        """ Delete a server from the server list.
        """
        self._logger.debug("Deleting server (using an index) from self.serverList")
        del self._serverList[index]
        
    def writeServerList(self):
        """ 
        Save the server list to configuration file.
        """
        
        self._logger.debug("Saving serverlist to disk")
            
        document = QDomDocument("LumaServerFile")
        root = document.createElement( "LumaServerList" )
        root.setAttribute("version", "1.2")
        document.appendChild(root)
        
        for serverObject in self._serverList:
            serverNode = document.createElement("LumaLdapServer")
            serverNode.setAttribute("name", serverObject.name)
            serverNode.setAttribute("host", serverObject.hostname)
            serverNode.setAttribute("port", serverObject.port)
            serverNode.setAttribute("bindAnon", serverObject.bindAnon)
            serverNode.setAttribute("bindDN", serverObject.bindDN)
            serverNode.setAttribute("bindPassword", serverObject.bindPassword)
            serverNode.setAttribute("encryptionMethod", serverObject.encryptionMethod)
            serverNode.setAttribute("authMethod", serverObject.authMethod)
            serverNode.setAttribute("autoBase", serverObject.autoBase)
            serverNode.setAttribute("followAliases", serverObject.followAliases)
            serverNode.setAttribute("checkServerCertificate", serverObject.checkServerCertificate)
            serverNode.setAttribute("useCertificate", serverObject.useCertificate)
            serverNode.setAttribute("clientCertFile", serverObject.clientCertFile)
            serverNode.setAttribute("clientCertKeyFile", serverObject.clientCertKeyFile)
            
            
            baseNode = document.createElement("baseDNs")
            for tmpBase in serverObject.baseDN:
                tmpNode = document.createElement("base")
                tmpNode.setAttribute("dn", tmpBase)
                baseNode.appendChild(tmpNode)
                
            serverNode.appendChild(baseNode)
            
            root.appendChild(serverNode)
            
        if not os.path.exists(self._configPrefix):
            os.makedirs(self._configPrefix)
            
        try:
            fileHandler = open(self._configFile, "w")
            fileHandler.write(unicode(document.toString()).encode("utf-8"))
            fileHandler.close()
        except:
            self._logger.error("Couldn't write to file: "+self._configFile)
        
        # Only the user should be able to access the file since we store 
        # passwords in it.
        # If we can't change it, leave it as it is since the user must have 
        # changed it manually. 
        try:
            #os.chmod(self._configFile, 0600)
            os.chmod(self._configFile, stat.S_IRUSR|stat.S_IWUSR)
        except:
            self._logger.debug("Couldn't set permissions on file "+self._configFile)
    
    def readServerList(self):
        self._readServerList()

    def _readServerList(self):
        """ 
        Read the server list from configuration file.
        """
        self._logger.debug("Reading serverlist from disk")
        
        if not os.path.isfile(self._configFile):
            self._logger.error("Serverlist not found")
            self._serverList = []
            return
        
        serverList = self._readFromXML()
        self._serverList = serverList

    def _readFromXML(self):

        self._logger.debug("Calling _readFromXML() to load serverlist from disk")

        fileContent = ""
        try:
            fileContent = "".join(open(self._configFile, "r").readlines())
            # If this is uncommentet, non-ascii characters stops working.
            # It's probably also decoded by QDomDocument, so decoding now means it's decoded
            # twice - which doesn't work.
            #fileContent = fileContent.decode("utf-8")
        except IOError, e:
            errorString = "Could not read server configuration file. Reason:\n"
            errorString += str(e)
            self._logger.error(errorString)

        document = QDomDocument("LumaServerFile")
        document.setContent(fileContent)
        
        root = document.documentElement()
        if not (unicode(root.tagName()) == "LumaServerList"):
            errorString = "Could not parse server configuration file."
            self._logger.error(errorString)
            
        serverList = None
        
        if root.attribute("version") == "1.0":
            self._logger.error("Can't read old serverconfig")
            #serverList = self._readFromXMLVersion1_0(fileContent)
        elif root.attribute("version") == "1.1":
            self._logger.error("Can't read old serverconfig")
            #serverList = self._readFromXMLVersion1_1(fileContent)
        elif root.attribute("version") == "1.2":
            self._logger.info("Reading new server-list-format for Luma3")
            serverList = self._readFromXMLVersion1_2(fileContent)
             
        return serverList


    def _readFromXMLVersion1_2(self, fileContent):
        
        self._logger.debug("Using _readFromXMLVersion1_2() to load serverlist from disk")
        
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
                server.bindAnon = int(tmpVal)
                    
                tmpVal = unicode(element.attribute("autoBase"))
                server.autoBase = int(tmpVal)   
                    
                server.bindDN = unicode(element.attribute("bindDN"))
                server.bindPassword = unicode(element.attribute("bindPassword"))
                
                server.encryptionMethod = int(element.attribute("encryptionMethod"))
                    
                server.checkServerCertificate = int(element.attribute("checkServerCertificate"))
                server.clientCertFile = unicode(element.attribute("clientCertFile"))
                server.clientCertKeyFile = unicode(element.attribute("clientCertKeyFile"))
                
                tmpVal = unicode(element.attribute("useCertificate"))
                server.useCertificate = int(tmpVal)   
                    
                tmpVal = unicode(element.attribute("followAliases"))
                server.followAliases = int(tmpVal)
                
                server.authMethod = int(element.attribute("authMethod"))
                
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
    
"""
    def _readFromXMLVersion1_1(self, fileContent):
        
        self._logger.debug("Using _readFromXMLVersion1_1() to load serverlist from disk")
        
        document = QDomDocument("LumaServerFile")
        document.setContent(fileContent)
        root = document.documentElement()
        
        serverList = []
        
        child = root.firstChild()
        while (not child.isNull()):
            server = ServerObject()
            element = child.toElement()
            if unicode(element.tagName()) == "LumaLdapServer":
                server.setName(unicode(element.attribute("name")))
                server.setHostname(unicode(element.attribute("host")))
                server.setPort(int(str(element.attribute("port"))))
                
                tmpVal = unicode(element.attribute("bindAnon"))
                if "True" == tmpVal:
                    server.setBindAnon(True)
                else:
                    server.setBindAnon(False)
                    
                tmpVal = unicode(element.attribute("autoBase"))
                if "True" == tmpVal:
                    server.setAutoBase(True)
                else:
                    server.setAutoBase(False)
                    
                    
                server.setBindAnon(unicode(element.attribute("bindDN")))
                server.setBindPassword(unicode(element.attribute("bindPassword")))
                
                server.setEncryptionMethod(unicode(element.attribute("encryptionMethod")))
                #if server.encryptionMethod == "":
                #    server.encryptionMethod = "None"
                    
                server.setCheckServerCertificate(unicode(element.attribute("checkServerCertificate")))
                server.setClientCertFile(unicode(element.attribute("clientCertFile")))
                server.setClientCertKeyFile(unicode(element.attribute("clientCertKeyfile")))
                
                tmpVal = unicode(element.attribute("useCertificate"))
                if tmpVal == "True":
                    server.setUseCertificate(True)
                else:
                    server.setUseCertificate(False)
                    
                tmpVal = unicode(element.attribute("followAliases"))
                if "True" == tmpVal:
                    server.setFollowAliases(True)
                else:
                    server.setFollowAliases(False)
                
                server.setAuthMethod((element.attribute("authMethod")))
                
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
                server.setBaseDN(baseDN)
                
            serverList.append(server)
            child = child.nextSibling()
        
        return serverList
    """
