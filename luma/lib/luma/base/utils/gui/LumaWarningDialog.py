# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2005 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4.QtGui import *
import os.path

from base.utils.gui.LumaErrorDialogDesign import LumaErrorDialogDesign
import environment


class LumaWarningDialog(LumaErrorDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        LumaErrorDialogDesign.__init__(self,parent,name,modal,fl)
        
        iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        errorPixmap = QPixmap(os.path.join(iconPath, "warning_big.png"))
        self.pixmapLabel.setPixmap(errorPixmap)
        
        
###############################################################################

    def setMessage(self, errorMessage):
        """ Sets the error message for the dialog.
        """
        
        self.errorLabel.setText(errorMessage)
