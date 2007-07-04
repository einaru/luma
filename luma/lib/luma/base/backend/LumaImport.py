# -*- coding: <utf-8> -*-

###########################################################################
#    Copyright (C) 2007 by Bjorn Ove Grotan 
#    <bgrotan@users.sourceforge.net> 
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import ldap
import ldif
import dsml
import base64

from cStringIO import StringIO

"""
Backend-class for parsing misc files (ldif,dsml,csv) 
and import them to LDAP.
"""

class LumaCSVParser:
    """Not implemented yet! """

    def __init__(self,io):
        pass

class LumaDSMLParser(dsml.DSMLParser):
    """Not implemented yet! """

    def __init__(self,inputfile):
        """DSML-Parser. Input-argument is a file-handle/StringIO-object.
        """
        pass

    def handle(self,dn,entry):
        self.objects.append((dn,entry))

    def get_records(self):
        """Returns a list of tuples (dn,entry) """
        return self.objects

class LumaLDIFParser(ldif.LDIFParser):
    def __init__(self,io):
        """LDIF-parser. Input-argument is a file-handle/StringIO-object.
        """
        ldif.LDIFParser.__init__(self, io)
        self.objects = []

    def handle(self,dn,entry):
        self.objects.append((dn,entry))

    def get_records(self):
        """Returns a list of tuples (dn,entry) """
        return self.objects
