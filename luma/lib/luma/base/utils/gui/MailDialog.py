# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path

import environment
from base.utils.gui.MailDialogDesign import MailDialogDesign


class MailDialog(MailDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        MailDialogDesign.__init__(self,parent,name,modal,fl)
        
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons")
        mailIcon = QPixmap (os.path.join (iconDir, "email.png"))
        self.mailIconLabel.setPixmap(mailIcon)
