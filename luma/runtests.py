
import unittest
import logging
from test import LumaConnectionTest, ServerListTest, ServerObjectTest, LumaLogHandlerTest

if __name__ == "__main__":

    # Set up logging
    l = logging.getLogger()
    l.setLevel(logging.ERROR)
    #l.addHandler(logging.StreamHandler()) #Uncomment for logging to console
    try:
        l.addHandler(logging.NullHandler()) #Comment this if adding the above
    except Exception:
        #Null handler is new in 2.7
        pass
    
    # Get the tests
    suite1 = ServerListTest.suite()
    suite2 = ServerObjectTest.suite()
    suite3 = LumaConnectionTest.suite()
    suite4 = LumaLogHandlerTest.suite()

    # Add em'
    suite = unittest.TestSuite()
    suite.addTest(suite1)
    suite.addTest(suite2)
    suite.addTest(suite3)
    suite.addTest(suite4)
    
    # Run
    unittest.TextTestRunner(verbosity=2).run(suite)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
