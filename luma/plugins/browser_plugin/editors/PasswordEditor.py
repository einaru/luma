# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


import PyQt4
from PyQt4.QtCore import QString
from PyQt4.QtGui import QDialog, QPalette
from ..gui.PasswordEditorDesign import Ui_PasswordEditorDesign
#from base.utils.backend.mkpasswd import mkpasswd
#from base.utils.backend.mkpasswd import check_strength
from base.util.IconTheme import pixmapFromThemeIcon

class PasswordEditor(QDialog, Ui_PasswordEditorDesign):

    def __init__(self, parent = None, flags = PyQt4.QtCore.Qt.Widget):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)
        
        editorPixmap = pixmapFromThemeIcon("password_big", ":/icons/password_big", 64, 64)
        self.iconLabel.setPixmap(editorPixmap)
        
        #self.supportedAlgorithms = environment.getAvailableHashMethods()
        #map(self.methodBox.insertItem, self.supportedAlgorithms)
        
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
            
        #self.strengthBar.setProgress(check_strength(firstPW))
        #TODO add password strength
        self.strengthBar.setValue( len(firstPW) * 10)
        
        self.password = unicode(self.passwordEdit.text())
        
        if enable:
            self.passwordSaveEdit.setStyleSheet(QString(""))
        else:
            self.passwordSaveEdit.setStyleSheet(QString("QLineEdit { background: red }"))
        
        self.okButton.setEnabled(enable)

###############################################################################

    def initValue(self, dataObject, attributeName, index):
        pass
        
###############################################################################

    def getValue(self):
        method = str(self.methodBox.currentText())
        
        return self.password.encode("utf-8")
        if method == 'cleartext':
            return self.password.encode("utf-8")
        else:
            return mkpasswd(self.password, 3, method).encode("utf-8")
