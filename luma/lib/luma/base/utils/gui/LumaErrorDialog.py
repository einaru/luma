# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2005 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path

from base.utils.gui.LumaErrorDialogDesign import LumaErrorDialogDesign
import environment


class LumaErrorDialog(LumaErrorDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        LumaErrorDialogDesign.__init__(self,parent,name,modal,fl)
        
        iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        errorPixmap = QPixmap(os.path.join(iconPath, "error.png"))
        self.pixmapLabel.setPixmap(errorPixmap)
        
        
###############################################################################

    def setErrorMessage(self, errorMessage):
        """ Sets the error message for the dialog.
        """
        
        self.errorLabel.setText(errorMessage)
