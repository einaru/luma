# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from base.backend.ServerObject import ServerObject

def addPreProcess(serverMeta, dn, objectValues, groupName):
    try:
        import UsermanagementExtra
        UsermanagementExtra.addPreProcess(serverMeta, dn, objectValues, groupName)
    except ImportError, e:
        print "Could not execute addPreProcess. Reason:"
        print e
    
###############################################################################

def addPostProcess(serverMeta, dn, objectValues, groupName):
    try:
        import UsermanagementExtra
        UsermanagementExtra.addPostProcess(serverMeta, dn, objectValues, groupName)
    except ImportError, e:
        print "Could not execute addPostProcess. Reason:"
        print e
        
###############################################################################

def deletePreProcess(serverMeta, dn):
    try:
        import UsermanagementExtra
        UsermanagementExtra.deletePreProcess(serverMeta, dn)
    except ImportError, e:
        print "Could not execute deletePreProcess. Reason:"
        print e
    
###############################################################################

def deletePostProcess(serverMeta, dn):
    try:
        import UsermanagementExtra
        UsermanagementExtra.deletePostProcess(serverMeta, dn)
    except ImportError, e:
        print "Could not execute deletePostProcess. Reason:"
        print e

###############################################################################

def modifyPreProcess(serverMeta, dn, objectValues):
    try:
        import UsermanagementExtra
        UsermanagementExtra.modifyPreProcess(serverMeta, dn, objectValues)
    except ImportError, e:
        print "Could not execute modifyPreProcess. Reason:"
        print e
    
###############################################################################

def modifyPostProcess(serverMeta, dn, objectValues):
    try:
        import UsermanagementExtra
        UsermanagementExtra.modifyPostProcess(serverMeta, dn, objectValues)
    except ImportError, e:
        print "Could not execute modifyPostProcess. Reason:"
        print e
