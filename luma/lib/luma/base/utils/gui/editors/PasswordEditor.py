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

from base.utils.gui.editors.PasswordEditorDesign import PasswordEditorDesign
import environment
from base.utils.backend.mkpasswd import mkpasswd
from base.utils.backend.mkpasswd import check_strength

class PasswordEditor(PasswordEditorDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        PasswordEditorDesign.__init__(self,parent,name,modal,fl)
        
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons")
        
        passwordPixmap = QPixmap(os.path.join(iconDir, "password_big.png"))
        self.iconLabel.setPixmap(passwordPixmap)
        
        self.supportedAlgorithms = environment.getAvailableHashMethods()
        map(self.methodBox.insertItem, self.supportedAlgorithms)
        
        self.okButton.setEnabled(False)
        
        # The new password in cleartext
        self.password = None

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
            
        self.strengthBar.setProgress(check_strength(firstPW))
        
        self.password = unicode(self.passwordEdit.text())
        
        if enable:
            self.passwordSaveEdit.unsetPalette()
        else:
            self.passwordSaveEdit.setPaletteBackgroundColor(Qt.red)
        
        self.okButton.setEnabled(enable)

###############################################################################

    def initValue(self, dataObject, attributeName, index):
        pass
        
###############################################################################

    def getValue(self):
        method = str(self.methodBox.currentText())
        
        if method == 'cleartext':
            return self.password.encode("utf-8")
        else:
            return mkpasswd(self.password, 3, method).encode("utf-8")
