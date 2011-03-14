# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Christian Forfang
#
# Luma is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public Licence as published by 
# the Free Software Foundation; either version 2 of the Licence, or 
# (at your option) any later version.
#
# Luma is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence 
# for more details.
#
# You should have received a copy of the GNU General Public Licence along 
# with Luma; if not, write to the Free Software Foundation, Inc., 
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import logging

class LumaLogHandler(logging.Handler):

    def __init__(self, logTo):
        logging.Handler.__init__(self)
        self.logTo = logTo

    def emit(self, record):
        m = (record.levelname, record.msg)
        self.logTo.log(m)