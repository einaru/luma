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

from base.backend.ServerObject import ServerObject
import environment


class ServerList:
    """Object for managing the list of available servers.
    
    self.serverList:  List of servers.
    
    
    """
    serverList = None
    
    def __init__(self):
        self.configPrefix = os.path.join(environment.userHomeDir, ".luma")
        self.configFile = os.path.join(self.configPrefix, "serverlist")

###############################################################################

    def addServer(self, serverName, hostName, port, bindAnon, baseDN, bindDN, password, tls):
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
        
        if self.serverList == None:
            self.serverList = [server]
        else:
            self.serverList.append(server)
            
        self.saveSettings(self.serverList)
        self.readServerList()

###############################################################################

    def saveSettings(self, serverList):
        """ Save the server list to configuration file.
        """

        configParser = ConfigParser()
            
        for x in serverList:
            if not configParser.has_section(x.name):
                configParser.add_section(x.name)
            configParser.set(x.name, "hostname", x.host)
            configParser.set(x.name, "port", x.port)
            configParser.set(x.name, "bindAnon", x.bindAnon)
            configParser.set(x.name, "baseDN", x.baseDN)
            configParser.set(x.name, "bindDN", x.bindDN)
            configParser.set(x.name, "bindPassword", x.bindPassword)
            configParser.set(x.name, "tls", x.tls)
            configParser.set(x.name, "authMethod", x.authMethod)
        configParser.write(open(self.configFile, 'w'))
        
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
        
        self.serverList = None

        configParser = ConfigParser()
        
        try:
            configParser.readfp(open(self.configFile, 'r'))
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
                server.baseDN = unicode(configParser.get(x, "baseDN"))
                server.bindDN = unicode(configParser.get(x, "bindDN"))
                server.bindPassword = unicode(configParser.get(x, "bindPassword"))
                server.tls = configParser.getboolean(x, "tls")
                server.authMethod = unicode(configParser.get(x, "authMethod"))
            except NoOptionError:
                pass
                
            self.serverList.append(server)
