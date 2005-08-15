# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from os import listdir
import os
import string
import os.path
from ConfigParser import ConfigParser
from ConfigParser import NoOptionError
from qtxml import *

from base.backend.ServerObject import ServerObject
import environment
from base.utils.backend.LogObject import LogObject


class ServerList:
    """Object for managing the list of available servers.
    
    self.serverList:  List of servers.
    
    
    """
    
    serverCache = []
    modifyTime = None
    
    # The cache for the client side ssl certificates
    # The filename is the key. In a tupel are the modification time and the 
    # cert as StringIO objects
    certCache = {}
    
    def __init__(self):
        self.serverList = []
        self.configPrefix = os.path.join(environment.userHomeDir, ".luma")
        self.configFile = os.path.join(self.configPrefix, "serverlist.xml")

###############################################################################

    def addServerObsolete(self, serverName, hostName, port, bindAnon, baseDN, bindDN, 
        password, encryptionMethod, autoBase, followAliases):
        """ Add a server to the server list.
        
        Arguments should be self-explationary.
        
        FIXME: Is this function obsolete?
        """
        
        server = ServerObject()
        server.name = serverName
        server.host = hostName
        server.port = port
        server.bindAnon = bindAnon
        server.baseDN = baseDN
        server.bindDN = bindDN
        server.bindPassword = password
        server.encryptionMethod = encryptionMethod
        server.autoBase = autoBase
        server.followAliases = followAliases
        
        if self.serverList == None:
            self.serverList = [server]
        else:
            self.serverList.append(server)
            
        self.saveSettings(self.serverList)
        self.readServerList()

###############################################################################

    def saveSettings(self, serverList=None):
        """ Save the server list to configuration file.
        """
        
        if None == serverList:
            serverList = self.serverList
            
        document = QDomDocument("LumaServerFile")
        root = document.createElement( "LumaServerList" )
        root.setAttribute("version", "1.1")
        document.appendChild(root)
        
        for x in serverList:
            serverNode = document.createElement("LumaLdapServer")
            serverNode.setAttribute("name", x.name)
            serverNode.setAttribute("host", x.host)
            serverNode.setAttribute("port", unicode(x.port))
            serverNode.setAttribute("bindAnon", unicode(x.bindAnon))
            serverNode.setAttribute("bindDN", x.bindDN)
            serverNode.setAttribute("bindPassword", x.bindPassword)
            serverNode.setAttribute("encryptionMethod", unicode(x.encryptionMethod))
            serverNode.setAttribute("authMethod", x.authMethod)
            serverNode.setAttribute("autoBase", unicode(x.autoBase))
            serverNode.setAttribute("followAliases", unicode(x.followAliases))
            serverNode.setAttribute("checkServerCertificate", unicode(x.checkServerCertificate))
            serverNode.setAttribute("useCertificate", unicode(x.useCertificate))
            serverNode.setAttribute("clientCertFile", unicode(x.clientCertFile))
            serverNode.setAttribute("clientCertKeyfile", unicode(x.clientCertKeyfile))
            
            
            baseNode = document.createElement("baseDNs")
            for tmpBase in x.baseDN:
                tmpNode = document.createElement("base")
                tmpNode.setAttribute("dn", tmpBase)
                baseNode.appendChild(tmpNode)
                
            serverNode.appendChild(baseNode)
            
            root.appendChild(serverNode)
            
        fileHandler = open(self.configFile, "w")
        fileHandler.write(unicode(document.toString()).encode("utf-8"))
        fileHandler.close()
        
        # Only the user should be able to access the file since we store 
        # passwords in it.
        # If we can't change it, leave it as it is since the user must have 
        # changed it manually. 
        try:
            os.chmod(self.configFile, 0600)
        except:
            pass
            

###############################################################################

    def deleteServer(self, serverName):
        """ Delete a server from the server list.
        """

        self.serverList = filter(lambda x: not (x.name == serverName), self.serverList)



###############################################################################

    def getServerObject(self, serverName):
        """ Get a server object by its name.
        """
        
        retVal = None
        
        for x in self.serverList:
            if x.name == serverName:
                retVal = x
                break
                
        return retVal

###############################################################################

    def readServerList(self):
        """ Read the server list from configuration file.
        """
        
        serverList = None
        
        modificationTime = None
        try:
            modificationTime = os.stat(self.configFile).st_mtime
        except OSError, e:
            pass
        
        if self.modifyTime == None:
            if self.checkConfig("CURRENT"):
                serverList = self.readFromXML()
            elif self.checkConfig("OLD"):
                serverList = self.readFromOld()
                self.saveSettings()
                modificationTime = os.stat(self.configFile).st_mtime
            else:
                serverList = []
                
            self.serverList = serverList
            
            # write cache information
            self.serverCache = self.serverList
            self.modifyTime = modificationTime
        else:
            if not (modificationTime == self.modifyTime):
                if self.checkConfig("CURRENT"):
                    serverList = self.readFromXML()
                elif self.checkConfig("OLD"):
                    serverList = self.readFromOld()
                    self.saveSettings()
                    modificationTime = os.stat(self.configFile).st_mtime
                else:
                    serverList = []
                
                self.serverList = serverList
            
                # write cache information
                self.serverCache = self.serverList
                self.modifyTime = modificationTime
            else:
                self.serverList = self.serverCache
                
        if None == self.serverList:
            self.serverList = []
        
###############################################################################

    def checkConfig(self, formatName="CURRENT"):
        if "CURRENT" == formatName:
            if os.path.exists(self.configFile):
                return True
            else:
                return False
        elif "OLD" == formatName:
            oldConfig = os.path.join(self.configPrefix, "serverlist")
            if os.path.exists(oldConfig):
                return True
            else:
                return False
        else:
            return False
            
###############################################################################

    def readFromOld(self):
        configParser = ConfigParser()
        
        try:
            oldConfig = os.path.join(self.configPrefix, "serverlist")
            configParser.readfp(open(oldConfig, 'r'))
        except IOError, error:
            tmpString = "Could not read server config file. Reason:"
            tmpString += str(error)
            environment.logMessage(LogObject("Debug", tmpString))
            
        sections = configParser.sections()
            
        if len(sections) == 0:
            return
            
        serverList = []
        for x in sections:
            server = ServerObject()
            server.name = unicode(x)
            try:
                server.host = unicode(configParser.get(x, "hostname"))
                server.port = configParser.getint(x, "port")
                server.bindAnon = configParser.getboolean(x, "bindAnon")
                server.baseDN = [unicode(configParser.get(x, "baseDN"))]
                server.autoBase = False
                server.bindDN = unicode(configParser.get(x, "bindDN"))
                server.bindPassword = unicode(configParser.get(x, "bindPassword"))
                server.tls = configParser.getboolean(x, "tls")
                server.authMethod = unicode(configParser.get(x, "authMethod"))
            except NoOptionError:
                pass
                
            serverList.append(server)
            
        return serverList
        
        
###############################################################################

    def readFromXML(self):
        fileContent = ""
        try:
            fileContent = "".join(open(self.configFile, "r").readlines())
            fileContent = fileContent.decode("utf-8")
        except IOError, e:
            errorString = "Could not read server configuration file. Reason:\n"
            errorString += str(e)
            environment.logMessage(LogObject("Error", errorString))
        
        document = QDomDocument("LumaServerFile")
        document.setContent(fileContent)
        
        root = document.documentElement()
        if not (unicode(root.tagName()) == "LumaServerList"):
            errorString = "Could not parse server configuration file."
            environment.logMessage(LogObject("Error", errorString))
            
        serverList = None
        
        if root.attribute("version") == "1.0":
            serverList = self.readFromXMLVersion1_0(fileContent)
        elif root.attribute("version") == "1.1":
            serverList = self.readFromXMLVersion1_1(fileContent)
            
        return serverList
            
###############################################################################

    def readFromXMLVersion1_0(self, fileContent):
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
                server.host = unicode(element.attribute("host"))
                server.port = int(str(element.attribute("port")))
                
                tmpVal = unicode(element.attribute("bindAnon"))
                if "True" == tmpVal:
                    server.bindAnon = True
                else:
                    server.bindAnon = False
                    
                tmpVal = unicode(element.attribute("autoBase"))
                if "True" == tmpVal:
                    server.autoBase = True
                else:
                    server.autoBase = False
                    
                    
                server.bindDN = unicode(element.attribute("bindDN"))
                server.bindPassword = unicode(element.attribute("bindPassword"))
                
                tmpVal = unicode(element.attribute("tls"))
                if "True" == tmpVal:
                    server.tls = True
                else:
                    server.tls = False
                    
                tmpVal = unicode(element.attribute("followAliases"))
                if "True" == tmpVal:
                    server.followAliases = True
                else:
                    server.followAliases = False
                
                server.authMethod = unicode(element.attribute("authMethod"))
                
                serverChild = child.firstChild()
                serverElement = serverChild.toElement()
                tagName = unicode(serverElement.tagName())
                    
                if "baseDNs" == tagName:
                    server.baseDN = []
                    baseNode = serverChild.firstChild()
                    while (not baseNode.isNull()):
                        baseElement = baseNode.toElement()
                        tmpBase = unicode(baseElement.tagName())
                        if "base" == tmpBase:
                            server.baseDN.append(unicode(baseElement.attribute("dn")))
                        baseNode = baseNode.nextSibling()
                
            serverList.append(server)
            child = child.nextSibling()
        
        return serverList
        
###############################################################################

    def readFromXMLVersion1_1(self, fileContent):
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
                server.host = unicode(element.attribute("host"))
                server.port = int(str(element.attribute("port")))
                
                tmpVal = unicode(element.attribute("bindAnon"))
                if "True" == tmpVal:
                    server.bindAnon = True
                else:
                    server.bindAnon = False
                    
                tmpVal = unicode(element.attribute("autoBase"))
                if "True" == tmpVal:
                    server.autoBase = True
                else:
                    server.autoBase = False
                    
                    
                server.bindDN = unicode(element.attribute("bindDN"))
                server.bindPassword = unicode(element.attribute("bindPassword"))
                
                server.encryptionMethod = unicode(element.attribute("encryptionMethod"))
                #if server.encryptionMethod == "":
                #    server.encryptionMethod = "None"
                    
                server.checkServerCertificate = unicode(element.attribute("checkServerCertificate"))
                server.clientCertFile = unicode(element.attribute("clientCertFile"))
                server.clientCertKeyfile = unicode(element.attribute("clientCertKeyfile"))
                
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
                
                server.authMethod = unicode(element.attribute("authMethod"))
                
                serverChild = child.firstChild()
                serverElement = serverChild.toElement()
                tagName = unicode(serverElement.tagName())
                    
                if "baseDNs" == tagName:
                    server.baseDN = []
                    baseNode = serverChild.firstChild()
                    while (not baseNode.isNull()):
                        baseElement = baseNode.toElement()
                        tmpBase = unicode(baseElement.tagName())
                        if "base" == tmpBase:
                            server.baseDN.append(unicode(baseElement.attribute("dn")))
                        baseNode = baseNode.nextSibling()
                
            serverList.append(server)
            child = child.nextSibling()
        
        return serverList
