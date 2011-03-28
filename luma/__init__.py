# -*- coding: utf-8 -*-
#
# __init__
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
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

import sys
import os

__all__ = ['ORGNAME', 'APPNAME', 'VERSION', 'DESCRIPTION']

def getRealLumaRootPath():
    import version
    return str(version).split()[3][1:-13]

sys.path.append(getRealLumaRootPath())

ORGNAME = APPNAME = 'luma'
VERSION = '3.0.3-sprint3'
DESCRIPTION = 'LDAP browser and administration utility'

