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

from base.backend.ServerObject import ServerObject
from base.backend.DirUtils import DirUtils

class ServerList:
    """Object for managing the list of available servers.
    
    self.SERVERLIST:  List of servers.
    
    
    """
    
    def __init__(self):
        self.SERVERLIST = []
        self.__configPrefix = DirUtils().USERDIR + "/.luma"
        self.__configFile = DirUtils().USERDIR + "/.luma/servers"
        self.__checkConfigDir()

###############################################################################

    def __checkConfigDir(self):
        """ Check if configuration directory exists. If not, create it.
        """
        
        if not (os.path.exists(self.__configPrefix)):
            try:
                os.mkdir(DirUtils().USERDIR + "/.luma")
            except IOError, e:
                print "Could not create directory for storing settings"
                print "Reason: " + str(e)

###############################################################################

    def readServerList(self):
        """ Read the server list from configuration file.
        """
        
        self.SERVERLIST = None

        fileContent = None
        try:
            fileContent = open(self.__configFile, 'r').readlines()
            self.SERVERLIST = self.__process_data(fileContent)
        except IOError, e:
            print "Could not open configuration file for server-options"
            print "Reason: " + str(e)

###############################################################################

    def __process_data(self, fileContent):
        """ Retrieve all server information from fileContent.
        """
        
        serverList = []
        serverListRaw = []
        tmpServer = []
        process = 0
        for x in fileContent:
            if x == "SERVER BEGIN\n":
                process = 1
            elif x == "SERVER END\n":
                process = 0
                serverListRaw.append(tmpServer)
                tmpServer = []
            elif x == "\n":
                continue
            elif process:
                tmpServer.append(x[:-1])

        serverDictionary = {}
        for x in serverListRaw:
            for y in x:
                pairs = string.split(y, ":=")
                if not (len(pairs) == 2):
                    continue
                else:
                    serverDictionary[pairs[0]] = pairs[1]
            server = ServerObject()
            try:
                server.name = serverDictionary['NAME']
                server.host = serverDictionary['HOSTNAME']
                server.port = string.atoi(serverDictionary['PORT'])
                server.bindAnon = serverDictionary['BINDANON']
                server.baseDN = serverDictionary['BASEDN']
                server.bindDN = serverDictionary['BINDDN']
                server.bindPassword = serverDictionary['BINDPW']
                server.tls = serverDictionary['TLS']
                serverList.append(server)
            except KeyError, e:
                print "Error during import of server preferences."
                print "The following option was not given: " + str(e)
            serverDictionary = {}
        return serverList

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
            datei = open(self.__configFile, 'w')
            for x in serverList:
                datei.write("SERVER BEGIN\n")
                datei.write("NAME:=" + x.name + "\n")
                datei.write("HOSTNAME:=" + x.host + "\n")
                datei.write("PORT:=" + str(x.port) + "\n")
                datei.write("BINDANON:=" + str(x.bindAnon) + "\n")
                datei.write("BASEDN:=" + x.baseDN + "\n")
                datei.write("BINDDN:=" + x.bindDN + "\n")
                datei.write("BINDPW:=" + x.bindPassword + "\n")
                datei.write("TLS:=" + str(x.tls) + "\n")
                datei.write("SERVER END\n\n")
            datei.close()
        except IOError, e:
            print "Could not save server prefernces."
            print "Reason: " + str(e)

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

