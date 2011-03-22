
import unittest
import logging
from test import ServerListTest, ServerObjectTest

if __name__ == "__main__":

    # Set up logging
    l = logging.getLogger()
    l.setLevel(logging.ERROR)
    l.addHandler(logging.StreamHandler())
    
    # Get the tests
    suite1 = ServerListTest.suite()
    suite2 = ServerObjectTest.suite()

    # Add em'
    suite = unittest.TestSuite()
    suite.addTest(suite1)
    suite.addTest(suite2)
    
    # Run
    unittest.TextTestRunner(verbosity=2).run(suite)
