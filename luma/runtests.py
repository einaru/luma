# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Christian Forfang, <cforfang@gmail.com>
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
from test import (LumaConnectionTest, ServerListTest, ServerObjectTest,
                  LumaLogHandlerTest)

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
