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
        self.serverObject.setName("Test")
        self.assertEqual("Test", self.serverObject.getName())
        
        self.serverObject.setHostname("ldap.ntnu.no")
        self.assertEqual("ldap.ntnu.no", self.serverObject.getHostname())
        
        self.serverObject.setPort(123)
        self.assertEqual(123, self.serverObject.getPort())
        
        self.serverObject.setBindAnon(True)
        self.assertEqual(True, self.serverObject.getBindAnon())
        
        self.serverObject.setAutoBase(False)
        self.assertEqual(False, self.serverObject.getAutoBase())
        
        self.serverObject.setBaseDN(['dc=ntnu,dc=no','dc=example,dc=org'])
        self.assertEqual(['dc=ntnu,dc=no','dc=example,dc=org'], self.serverObject.getBaseDN())
        
        self.serverObject.setBindDN("username")
        self.assertEqual("username", self.serverObject.getBindDN())
        
        self.serverObject.setBindPassword("password")
        self.assertEqual("password", self.serverObject.getBindPassword())
        
        self.serverObject.setEncryptionMethod(0)
        self.assertEqual(0, self.serverObject.getEncryptionMethod())
        
        self.serverObject.setAuthMethod(2)
        self.assertEqual(2, self.serverObject.getAuthMethod())
        
        self.serverObject.setFollowAliases(False)
        self.assertEqual(False, self.serverObject.getFollowAliases())
        
        self.serverObject.setUseCertificate(True)
        self.assertEqual(True, self.serverObject.getUseCertificate())
        
        self.serverObject.setClientCertFile("cerfile.pem")
        self.assertEqual("cerfile.pem", self.serverObject.getClientCertFile())
        
        self.serverObject.setClientCertKeyFile("certkeyfile.pem")
        self.assertEqual("certkeyfile.pem", self.serverObject.getClientCertKeyFile())
        
        self.serverObject.setCheckServerCertificate(3)
        self.assertEqual(3, self.serverObject.getCheckServerCertificate())
        
        self.serverObject.setCurrentBase("base")
        self.assertEqual("base", self.serverObject.getCurrentBase())
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGettersSetters']
    unittest.main()