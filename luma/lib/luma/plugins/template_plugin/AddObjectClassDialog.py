# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4.QtGui import *
from plugins.template_plugin.AddObjectClassDialogDesign import AddObjectClassDialogDesign

class AddObjectClassDialog(AddObjectClassDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        AddObjectClassDialogDesign.__init__(self,parent,name,modal,fl)
