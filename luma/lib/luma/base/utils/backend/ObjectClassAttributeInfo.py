###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <wido.depping@tu-clausthal.de>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *

import ldap
import ldap.schema
import re
import string

from base.backend.ServerList import ServerList

class ObjectClassAttributeInfo(object):

    def __init__(self, server):
        self.OBJECTCLASSES = {}
        self.ATTRIBUTELIST = {}
        self.SERVER = server[:]
        self.retrieve_info_from_server()

###############################################################################

    def retrieve_info_from_server(self):
        tmpObject = ServerList()
        tmpObject.readServerList()
        serverMeta = ""
        serverMeta = tmpObject.get_serverobject(self.SERVER)

        mainWin = qApp.mainWidget()
        mainWin.set_busy()

        try:
            tmpUrl = "ldap://" + serverMeta.host + ":" + str(serverMeta.port)
            subschemasubentry_dn,schema = ldap.schema.urlfetch(tmpUrl)
            oidList = schema.listall(ldap.schema.ObjectClass)
            for x in oidList:
                mainWin.update_ui()
                y = schema.get_obj(ldap.schema.ObjectClass, x)
                name = y.names[0]
                desc = ""
                if not (y.desc == None):
                    desc = y.desc
                must = []
                if not (len(y.must) == 0):
                    must = y.must
                may = []
                if not (len(y.may) == 0):
                    may = y.may
                self.OBJECTCLASSES[name] = {"DESC": desc, "MUST": must, "MAY": may}

            oidList = schema.listall(ldap.schema.AttributeType)
            for x in oidList:
                mainWin.update_ui()
                y = schema.get_obj(ldap.schema.AttributeType, x)
                name = y.names
                desc = ""
                if not (y.desc == None):
                    desc = y.desc
                single = y.single_value
                for y in name:
                    self.ATTRIBUTELIST[y] = {"DESC": desc, "SINGLE": single}
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            
        mainWin.set_busy(0)

###############################################################################

    def set_server(self, server):
        self.SERVER = server[:]

###############################################################################

    def update(self):
        self.OBJECTCLASSES = {}
        self.ATTRIBUTELIST = []
        self.retrieve_info_from_server()

###############################################################################

    def get_all_attributes(self, classList = None):
        allAttributes = []
        for x in classList:
            must = self.OBJECTCLASSES[x]["MUST"]
            may = self.OBJECTCLASSES[x]["MAY"]
            if not (len(must) == 0):
                for y in must:
                    allAttributes.append(y)
            if not (len(may) == 0):
                for y in may:
                    allAttributes.append(y)
        return allAttributes

###############################################################################

    def get_all_musts(self, classList = None):
        allAttributes = []
        for x in classList:
            must = self.OBJECTCLASSES[x]["MUST"]
            if not (len(must) == 0):
                for y in must:
                    allAttributes.append(y)
        return allAttributes

###############################################################################

    def get_all_mays(self, classList = None):
        allAttributes = []
        for x in classList:
            may = self.OBJECTCLASSES[x]["MAY"]
            if not (len(may) == 0):
                for y in may:
                    allAttributes.append(y)
        return allAttributes

###############################################################################

    def is_single(self, attribute = ""):
        if self.ATTRIBUTELIST.has_key(attribute):
             val = self.ATTRIBUTELIST[attribute]["SINGLE"]
             return val
        else:
            return 0

###############################################################################

    def is_must(self, attribute="", objectClasses = None):
        if objectClasses == None:
            raise "Missing Arguments to Funktion 'is_must(attribute, objectClasses)"
        else:
            for x in objectClasses:
                for y in self.OBJECTCLASSES[x]["MUST"]:
                    if y == attribute:
                        return 1
        return 0

###############################################################################

    def update_ui(self):
        """ Updates the progress bar of the GUI and keeps it responsive."""
        qApp.processEvents()
        progress = self.pBar.progress()
        self.pBar.setProgress(progress + 1)









