# -*- coding: utf-8 -*-
#
# Copyright (c) 2011:
#     Christian Forfang, <cforgang@gmail.com>
#     Simen Natvig, <simen.natvig@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/
"""
Tests ServerList.py's ability to read and write the serverlist to disk,
as well as to add, get and delete objects from it.
"""
import unittest
from base.backend.ServerList import ServerList
from base.backend.ServerObject import ServerObject
import tempfile
import logging

class SLTest(unittest.TestCase):

    """
    Store the serverlist in this directory.
    """
    def setUp(self):
        #print "setUp"
        self.sl = ServerList(tempfile.gettempdir(), "serverlisttest.xml")
        #self.sl.__configFile = os.path.join(self.sl._configPrefix, "serverlist.xml")

    def tearDown(self):
        pass


    """
    Writes a serverlist in the current format to disk.
    """
    def writeList(self):
        #print "writeList"
        try:
            f = open(self.sl.getConfigFilePath(), "w")
            f.write("""
<!DOCTYPE LumaServerFile>
<LumaServerList version="1.2">
 <LumaLdapServer port="1337" clientCertFile="" followAliases="0" clientCertKeyfile="" bindPassword="pw" useCertificate="0" bindDN="" host="directory.d-trust.de" authMethod="1" bindAnon="1" encryptionMethod="0" name="d-trust" autoBase="0" checkServerCertificate="1">
  <baseDNs>
   <base dn="dc=d-trust,dc=de"/>
   <base dn="dc=ntnu,dc=no.TULL"/>
  </baseDNs>
 </LumaLdapServer>
 <LumaLdapServer port="389" clientCertFile="" followAliases="0" clientCertKeyfile="" bindPassword="secret" useCertificate="0" bindDN="" host="at.ntnu.no" authMethod="6" bindAnon="1" encryptionMethod="2" name="ntnu" autoBase="1" checkServerCertificate="2">
  <baseDNs>
   <base dn="dc=lol,dc=com"/>
   <base dn="dc=ntnu,dc=no"/>
  </baseDNs>
 </LumaLdapServer>
 <LumaLdapServer port="392" clientCertFile="" followAliases="1" clientCertKeyfile="" bindPassword="password" useCertificate="0" bindDN="" host="x500.bund.de" authMethod="0" bindAnon="1" encryptionMethod="1" name="bund" autoBase="0" checkServerCertificate="0">
  <baseDNs>
   <base dn="dc=bund,dc=de"/>
  </baseDNs>
 </LumaLdapServer>
</LumaServerList>
        """)
            f.close()
        except IOError:
            print "----------------------"
            print "WRITE TO DISK FAILED!"
            print "----------------------"
            raise

    def getEmptyServerObject(self):
        #print "getEmptryServerObject"
        return ServerObject()

    """
    Read and write and emtpy serverlist to/from disk.
    """
    def testEmptyList(self):
        #print "testEmptyList"
        self.sl.setTable([])
        self.sl.writeServerList()
        self.sl.readServerList()
        self.assertEqual(self.sl.getTable(), [])

    """
    Tests for Read, delete, add and write, better than one BIG test, but each test is still a bit to dependent on the previous tests
    """

    def testAdd(self):
        #print "testAdd"
        # Remove and add back the removed item
        self.sl.addServer(self.getEmptyServerObject())

        # Check if it has been added correctly
        self.assertNotEqual(None, self.sl.getServerObject(""))


    def testDelete(self):
        #print "testDelete"
        # Delete and see if object still in list
        self.sl.setTable([self.getEmptyServerObject()])
        self.assertNotEqual(None, self.sl.getServerObject(""))
        self.sl.deleteServer("")
        self.assertEqual(None, self.sl.getServerObject(""))


    def testRead(self):
        #print "testRead"
        # Write the list to disk and have ServerList read it.
        self.writeList()
        self._modifyTime = None #IMPORTANT - FORCES READ FROM DISK
        self.sl.readServerList()

        # Check that the server list was read correctly
        self.assertNotEqual(None, self.sl.getServerObject("d-trust"))
        self.assertNotEqual(None, self.sl.getServerObject("bund"))
        self.assertNotEqual(None, self.sl.getServerObject("ntnu"))

    def testWrite(self):
        #print "testWrite"
        # Write the list back to disk and read it back
        self.sl.setTable([self.getEmptyServerObject()])
        self.sl.writeServerList()


        f = open(self.sl.getConfigFilePath(), "r")
        s = """
<!DOCTYPE LumaServerFile>
<LumaServerList version="1.2">
 <LumaLdapServer port="389" clientCertFile="" followAliases="0" bindPassword="" useCertificate="0" clientCertKeyFile="" bindDN="" host="" authMethod="0" bindAnon="1" encryptionMethod="0" name="" autoBase="1" checkServerCertificate="0">
  <baseDNs/>
 </LumaLdapServer>
</LumaServerList>
    """
        #Verify the list is good
        read = f.read()
        f.close()
        s = s.strip()
        r = read.strip()
        self.assertEqual(s, r)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SLTest))
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testServerList']
    # create logger
    logger = logging.getLogger("base")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    unittest.main()
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
