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
	self.lastLevel, self.lastMessage, self.lastName, self.lastThreadName = message
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


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
