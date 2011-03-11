'''
Created on 4. feb. 2011

@author: Christian
'''
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