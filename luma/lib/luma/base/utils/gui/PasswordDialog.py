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

from base.utils.gui.PasswordDialogDesign import PasswordDialogDesign
import environment
from base.utils.backend.mkpasswd import mkpasswd

class PasswordDialog(PasswordDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        PasswordDialogDesign.__init__(self,parent,name,modal,fl)
        
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons")
        
        passwordPixmap = QPixmap(os.path.join(iconDir, "password_big.png"))
        self.iconLabel.setPixmap(passwordPixmap)
        
        self.supportedAlgorithms = environment.getAvailableHashMethods()
        map(self.methodBox.insertItem, self.supportedAlgorithms)
        
        self.okButton.setEnabled(False)
        
        # the new password
        self.passwordHash = ""
        
        

###############################################################################

    def checkPassword(self):
        tmpPassword = unicode(self.passwordEdit.text())
        method = str(self.methodBox.currentText())
        if method == 'cleartext':
            self.passwordHash = tmpPassword
        else:
            self.passwordHash = mkpasswd(tmpPassword, 3, method)
           
        self.passwordHash = self.passwordHash.encode("utf-8")
        self.accept()

###############################################################################

    def passwordChanged(self, pwString):
        firstPW = unicode(self.passwordEdit.text())
        secondPW = unicode(self.passwordSaveEdit.text())
        
        enable = False
        if (firstPW == secondPW) and (len(firstPW) > 0):
            enable = True
            self.passwordLabel.setText(self.trUtf8("Passwords match"))
        else:
            self.passwordLabel.setText(self.trUtf8("Passwords do not match"))
        
        self.okButton.setEnabled(enable)


            
            
            
            
            
            
            
