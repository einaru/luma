# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <wido.depping@tu-clausthal.de>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from os import listdir
from os import remove
import string
import os.path
from ConfigParser import ConfigParser

from base.backend.ServerObject import ServerObject
from base.backend.DirUtils import DirUtils

class ServerList:
    """Object for managing the list of available servers.
    
    self.SERVERLIST:  List of servers.
    
    
    """
    SERVERLIST = None
    
    def __init__(self):
        userdir = DirUtils().USERDIR
        self.__configPrefix = os.path.join(userdir, ".luma")
        self.__configFile = os.path.join(self.__configPrefix,  "serverlist")
        self.__checkConfigDir()

###############################################################################

    def __checkConfigDir(self):
        """ Check if configuration directory exists. If not, create it.
        """
        
        if not (os.path.exists(self.__configPrefix)):
            try:
                os.mkdir(self.__configPrefix)
            except IOError, e:
                print "Could not create directory for storing settings"
                print "Reason: " + str(e)

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
        if self.SERVERLIST == None:
            self.SERVERLIST = [server]
        else:
            self.SERVERLIST.append(server)
        self.save_settings(self.SERVERLIST)
        self.readServerList()

###############################################################################

    def save_settings(self, serverList):
        """ Save the server list to configuration file.
        """
        try:
            configParser = ConfigParser()
            for x in self.SERVERLIST:
                configParser.add_section(x.name)
                configParser.set(x.name, "hostname", x.host)
                configParser.set(x.name, "port", x.port)
                configParser.set(x.name, "bindAnon", x.bindAnon)
                configParser.set(x.name, "baseDN", x.baseDN)
                configParser.set(x.name, "bindDN", x.bindDN)
                configParser.set(x.name, "bindPassword", x.bindPassword)
                configParser.set(x.name, "tls", x.tls)
            configParser.write(open(self.__configFile, 'w'))
        except Exception, e:
            print "Could not save server settings. Reason:"
            print e
        

###############################################################################

    def deleteServer(self, serverName):
        """ Delete a server from the server list.
        """
        
        newList = []
        for x in self.SERVERLIST:
            if not(x.name == serverName):
                newList.append(x)
        self.save_settings(newList)
        self.readServerList()

###############################################################################

    def __repr__(self):
        """ String representation for the server list.
        """
        
        finalString = ""
        for x in serverList:
            finalString = finalString + str(x) + "\n"
        return finalString

###############################################################################

    def get_serverobject(self, serverName):
        """ Get a server object by its name.
        """
        
        for x in self.SERVERLIST:
            if x.name == serverName:
                return x

###############################################################################

    def readServerList(self):
        """ Read the server list from configuration file.
        """
        
        self.SERVERLIST = None

        try:
            configParser = ConfigParser()
            configParser.readfp(open(self.__configFile, 'r'))
            sections = configParser.sections()
            if len(sections) > 0:
                self.SERVERLIST = []
                for x in sections:
                    server = ServerObject()
                    server.name = x
                    server.host = configParser.get(x, "hostname")
                    server.port = configParser.getint(x, "port")
                    server.bindAnon = configParser.getint(x, "bindAnon")
                    server.baseDN = configParser.get(x, "baseDN")
                    server.bindDN = configParser.get(x, "bindDN")
                    server.bindPassword = configParser.get(x, "bindPassword")
                    server.tls = configParser.getint(x, "tls")
                    self.SERVERLIST.append(server)
        except Exception, e:
            print "Could not read server settings. Reason:"
            print e
