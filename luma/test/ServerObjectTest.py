# -*- coding: utf-8 -*-
#
# Copyright (c) 2011:
#     Christian Forfang, <cforgang@gmail.com>
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
import unittest

from base.backend.ServerObject import ServerObject

class Test(unittest.TestCase):

    def setUp(self):
        self.serverObject = ServerObject()

    def testGettersSetters(self):
        self.serverObject.name = "Test"
        self.assertEqual("Test", self.serverObject.name)

        self.serverObject.hostname = "ldap.ntnu.no"
        self.assertEqual("ldap.ntnu.no", self.serverObject.hostname)

        self.serverObject.port = 123
        self.assertEqual(123, self.serverObject.port)

        self.serverObject.bindAnon = True
        self.assertEqual(True, self.serverObject.bindAnon)

        self.serverObject.autoBase = False
        self.assertEqual(False, self.serverObject.autoBase)

        self.serverObject.baseDN = ['dc=ntnu,dc=no','dc=example,dc=org']
        self.assertEqual(['dc=ntnu,dc=no','dc=example,dc=org'], self.serverObject.baseDN)

        self.serverObject.bindDN = "username"
        self.assertEqual("username", self.serverObject.bindDN)

        self.serverObject.bindPassword = "password"
        self.assertEqual("password", self.serverObject.bindPassword)

        self.serverObject.encryptionMethod = 0
        self.assertEqual(0, self.serverObject.encryptionMethod)

        self.serverObject.authMethod = 2
        self.assertEqual(2, self.serverObject.authMethod)

        self.serverObject.followAliases = False
        self.assertEqual(False, self.serverObject.followAliases)

        self.serverObject.useCertificate = True
        self.assertEqual(True, self.serverObject.useCertificate)

        self.serverObject.clientCertFile = "cerfile.pem"
        self.assertEqual("cerfile.pem", self.serverObject.clientCertFile)

        self.serverObject.clientCertKeyfile= "certkeyfile.pem"
        self.assertEqual("certkeyfile.pem", self.serverObject.clientCertKeyfile)

        self.serverObject.checkServerCertificate = 3
        self.assertEqual(3, self.serverObject.checkServerCertificate)

        self.serverObject.currentBase = "base"
        self.assertEqual("base", self.serverObject.currentBase)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGettersSetters']
    unittest.main()
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
