"""
Does some simple (!) testing on LumaConnection
and by extension SmartDataObject.

With proper mock-objects this could be SUBSTANTIALLY
expanded.

@author Christian Forfang
"""

import unittest, ldap

from base.backend.LumaConnection import LumaConnection, LumaConnectionException
from base.backend.ServerObject import ServerObject

class LumaConnectionTest(unittest.TestCase):
    
    def setUp(self):
	pass
    def tearDown(self):
        pass

    def testNoServerObjectException(self):
	self.assertRaises(LumaConnectionException, LumaConnection)

    def testBindToNonexistant(self):
	sO = ServerObject() # defaults to invalid hostname
	l = LumaConnection(sO)
	(success, error) = l.bind() # try bind
	self.assertFalse(success) # Can connect to invalid hostname
	self.assertEqual(str(error),str({"desc":"Can't contact LDAP server"}))

    def testSearchAndSomeSmartObject(self):
	sO = ServerObject()
	sO.name = "Test"
	l = LumaConnection(sO)
	
	# Have LumaConnection use a mock-object for the search
	l.ldapServerObject = MockLDAP() 
	(success, resultList, exception) = l.search()

	# The search was successfull
	self.assertTrue(success)
	self.assertEqual(exception, None)

	# The returned smartdataobject gives correct data
	rso = resultList[0] #smartdataobject returned
	self.assertEqual(rso.getServerAlias(), "Test")
	self.assertEqual(str(rso.getServerMeta()), str(sO))
	self.assertEqual(rso.getObjectClasses(), [])
	self.assertFalse(rso.hasStructuralClass())

	self.assertEqual(rso.getPrettyDN(), "dc=luma")
	self.assertEqual(rso.getPrettyRDN(), "dc=luma")

	self.assertEqual(rso.getAttributeList(),["dc"])
	self.assertRaises(Exception, rso.getAttributeValueList)
	self.assertEqual(rso.getAttributeValueList("dc"), ['l','u','m','a'])
	self.assertEqual(rso.getAttributeValueList("not-ext."), None)

	self.assertRaises(Exception, rso.getAttributeValue)
	self.assertRaises(Exception, rso.getAttributeValue("dc",-1)) #out of range
	self.assertEqual(rso.getAttributeValue("dc",0), "l")

    def testUtilityMethods(self):
	sO = ServerObject()
	l = LumaConnection(sO)
	#Tests cleanDN() and escape_dn_chars
	self.assertEqual(l.cleanDN("dc=l\,\=\+ma,dc=no"),"dc=l\\2C\\3D\\2Bma,dc=no")


class MockLDAP:
    """
    Mocks a simple LDAP-search using search_ext
    """
    def __init__(self):
	self.returns = 0

    def search_ext(self, base, scope, filter, attrList, attrsonly, sizelimit):
	# returns id=0
	return 0

    def result(self, id, arg1, arg2):
	if self.returns == 1:
	    return ("",[])
	# so that the second call to result gives []
	self.returns = self.returns+1
	# first calls gives data
	return (ldap.RES_SEARCH_ENTRY,[("dc=luma",{"dc":"luma"})])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LumaConnectionTest))
    return suite

if __name__ == "__main__":
    unittest.main()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
