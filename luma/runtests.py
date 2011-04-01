
import unittest
import logging
from test import LumaConnectionTest, ServerListTest, ServerObjectTest

if __name__ == "__main__":

    # Set up logging
    l = logging.getLogger()
    l.setLevel(logging.ERROR)
    #l.addHandler(logging.StreamHandler()) #Uncomment for logging to console
    l.addHandler(logging.NullHandler()) #Comment this if adding the above
    
    # Get the tests
    suite1 = ServerListTest.suite()
    suite2 = ServerObjectTest.suite()
    suite3 = LumaConnectionTest.suite()

    # Add em'
    suite = unittest.TestSuite()
    suite.addTest(suite1)
    suite.addTest(suite2)
    suite.addTest(suite3)
    
    # Run
    unittest.TextTestRunner(verbosity=2).run(suite)
