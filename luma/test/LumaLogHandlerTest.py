'''
@author: Christian Forfang
'''
import unittest
import logging
from base.backend.Log import LumaLogHandler

class LLHTest(unittest.TestCase):

    def setUp(self):
	self.llh = LumaLogHandler(self)
	self.lastLevel = None
	self.lastMessage = None

    def tearDown(self):
        self.llh = None


    def log(self, message):
	self.lastLevel, self.lastMessage = message

    def testLogger(self):
	# Set up logging through pythons's logging-system
	l = logging.getLogger()
	l.addHandler(self.llh) # Use the LumaLogHandler
	l.setLevel(logging.DEBUG) # Not logged by default
	
	testStr = "Testing"
	l.debug(testStr) #debug
	self.assertEqual("DEBUG", self.lastLevel)
	self.assertEqual(testStr, self.lastMessage)

	testStr = "Another test"
	l.error(testStr) #error
	self.assertEqual("ERROR", self.lastLevel)
	self.assertEqual(testStr, self.lastMessage)
	
	testStr = "Yes another test"
	l.info(testStr) #info
	self.assertEqual("INFO", self.lastLevel)
	self.assertEqual(testStr, self.lastMessage)

	
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LLHTest))
    return suite

