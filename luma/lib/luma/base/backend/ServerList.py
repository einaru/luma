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


class ServerList:
    """Object for managing the list of available servers.
    
    self.serverList:  List of servers.
    
    
    """
    
    def __init__(self):
        self.serverList = None
        self.configPrefix = os.path.join(environment.userHomeDir, ".luma")
        self.configFile = os.path.join(self.configPrefix, "serverlist.xml")

###############################################################################

    def addServer(self, serverName, hostName, port, bindAnon, baseDN, bindDN, 
        password, tls, autoBase, followAliases):
        """ Add a server to the server list.
        
        Arguments should be self-explationary.
        """
        
        server = ServerObject()
        server.name = serverName
        server.host = hostName
        server.port = port
        server.bindAnon = bindAnon
        server.baseDN = baseDN
        server.bindDN = bindDN
        server.bindPassword = password
        server.tls = tls
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
        root.setAttribute("version", "1.0")
        document.appendChild(root)
        
        for x in serverList:
            serverNode = document.createElement("LumaLdapServer")
            serverNode.setAttribute("name", x.name)
            serverNode.setAttribute("host", x.host)
            serverNode.setAttribute("port", unicode(x.port))
            serverNode.setAttribute("bindAnon", unicode(x.bindAnon))
            serverNode.setAttribute("bindDN", x.bindDN)
            serverNode.setAttribute("bindPassword", x.bindPassword)
            serverNode.setAttribute("tls", unicode(x.tls))
            serverNode.setAttribute("authMethod", x.authMethod)
            serverNode.setAttribute("autoBase", unicode(x.autoBase))
            serverNode.setAttribute("followAliases", unicode(x.followAliases))
            
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
        
        if self.checkConfig("CURRENT"):
            self.readFromXML()
        elif self.checkConfig("OLD"):
            self.readFromOld()
        else:
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
            print "WARNING: Could not read server config file. Reason:"
            print error
            
        sections = configParser.sections()
            
        if len(sections) == 0:
            return
            
        self.serverList = []
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
                
            self.serverList.append(server)
            
        self.saveSettings()
        
###############################################################################

    def readFromXML(self):
        fileContent = ""
        try:
            fileContent = "".join(open(self.configFile, "r").readlines())
            fileContent = fileContent.decode("utf-8")
        except IOError, e:
            print "Could not read server configuration file. Reason:"
            print e
        
        self.serverList = []
        
        document = QDomDocument("LumaServerFile")
        document.setContent(fileContent)
        
        root = document.documentElement()
        if not (unicode(root.tagName()) == "LumaServerList"):
            print "Could not parse server file"
            
        if "1.0" == root.attribute("version"):
            self.readFromXMLVersion1_0(fileContent)
            
###############################################################################

    def readFromXMLVersion1_0(self, fileContent):
        document = QDomDocument("LumaServerFile")
        document.setContent(fileContent)
        root = document.documentElement()
        
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
                
            self.serverList.append(server)
            child = child.nextSibling()
