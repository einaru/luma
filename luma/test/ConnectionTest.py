# -*- coding: utf-8 -*-
#
# test.ConnectionTest
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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
from base.backend.Connection import LumaConnection
from base.backend.ServerObject import ServerObject

class ConnectionTest(unittest.TestCase):
    
    def setUp(self):
        pass

so = ServerObject()
so.name = 'test server'
so.hostname = 'liquid.forfang.net'
so.port = 50000
so.bindAnon = False
so.clientCertFile=""
so.followAliases=False
so.bindPassword="secret"
so.useCertificate="0"
so.clientCertKeyFile=""
so.bindDN="cn=manager,dc=forfang,dc=net"
so.host="liquid.forfang.net"
so.authMethod=0
so.bindAnon=False
so.encryptionMethod="0"
so.autoBase="1"
so.checkServerCertificate=True

con = LumaConnection(so)
print con.bind()
print con.search()
print con.unbind()


