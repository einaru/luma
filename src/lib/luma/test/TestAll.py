'''
Created on 2. feb. 2011

@author: Christian
'''
import unittest
import logging
from test import ServerListTest, ServerObjectTest

#logging.getLogger("base").setLevel(logging.DEBUG)

suite1 = ServerListTest.suite()
suite2 = ServerObjectTest.suite()

suite = unittest.TestSuite()

suite.addTest(suite1)
#suite.addTest(suite2)

unittest.TextTestRunner(verbosity=2).run(suite)

"""
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test.ServerListTest))
    return suite
"""