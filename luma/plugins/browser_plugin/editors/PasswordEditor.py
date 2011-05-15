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
from PyQt4.QtGui import QDialog, QPalette, QLineEdit
from ..gui.PasswordEditorDesign import Ui_PasswordEditorDesign
from ..utils.mkpasswd import mkpasswd, check_strength, get_available_hash_methods
from ..utils.mkpasswd import check_strength
from base.util.IconTheme import pixmapFromTheme


class PasswordEditor(QDialog, Ui_PasswordEditorDesign):

    def __init__(self, parent = None, flags = PyQt4.QtCore.Qt.Widget):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)
        
        editorPixmap = pixmapFromTheme(
            "dialog-password", ":/icons/48/dialog-password")
        self.iconLabel.setPixmap(editorPixmap)
        
        self.supportedAlgorithms = get_available_hash_methods()
        map(self.methodBox.addItem, self.supportedAlgorithms)
        self.methodBox.currentIndexChanged[str].connect(self.methodChanged)
        
        self.okButton.setEnabled(False)
        self.progressBar.setValue(0)
        
        self.asciiInput = True
        self.asciiBox.clicked.connect(self.asciiBoxClicked)
        self.hiddenBox.clicked.connect(self.hiddenBoxClicked)
        
        # The new password in cleartext
        self.password = None

        self.methodBox.currentIndexChanged[str].emit(self.methodBox.currentText())

###############################################################################

    def methodChanged(self, string):
        if str(string) == 'cleartext':
            self.asciiBox.setEnabled(True)
            self.asciiBox.setChecked(self.asciiInput)
        else:
            self.asciiBox.setChecked(True)
            self.asciiBox.setEnabled(False)
        self.passwordEdit.textChanged.emit(self.passwordEdit.text())
        self.passwordSaveEdit.textChanged.emit(self.passwordSaveEdit.text())

###############################################################################

    def asciiBoxClicked(self, checked):
        # if checked, only ascii characters are allowed
        self.asciiInput = checked
        self.passwordEdit.textChanged.emit(self.passwordEdit.text())
        self.passwordSaveEdit.textChanged.emit(self.passwordSaveEdit.text())
        

###############################################################################

    def hiddenBoxClicked(self, checked):
        # if checked, no text will be displayed in the input box
        if checked:
            self.passwordEdit.setEchoMode(QLineEdit.NoEcho)
            self.passwordSaveEdit.setEchoMode(QLineEdit.NoEcho)
        else:
            self.passwordEdit.setEchoMode(QLineEdit.Password)
            self.passwordSaveEdit.setEchoMode(QLineEdit.Password)

###############################################################################

    def passwordChanged(self, pwString):
        firstPW = unicode(self.passwordEdit.text())
        secondPW = unicode(self.passwordSaveEdit.text())
        if self.asciiBox.isChecked():
            # only ascii characters are allowed
            pwOK = True
            try:
                str(firstPW)
                self.passwordEdit.setStyleSheet(QString(""))
            except UnicodeError:
                pwOK = False
                self.passwordEdit.setStyleSheet(QString("QLineEdit { background: red }"))
            try:
                str(secondPW)
                self.passwordSaveEdit.setStyleSheet(QString(""))
            except UnicodeError:
                pwOK = False
                self.passwordSaveEdit.setStyleSheet(QString("QLineEdit { background: red }"))
            if not pwOK:
                self.okButton.setEnabled(False)
                self.passwordLabel.setText(self.trUtf8("Non-ascii character"))
                return

        self.progressBar.setValue(check_strength(firstPW))
        
        self.password = unicode(self.passwordEdit.text())

        if (firstPW == secondPW) and (len(firstPW) > 0):
            self.passwordLabel.setText(self.trUtf8("Passwords match"))
            self.passwordEdit.setStyleSheet(QString(""))
            self.passwordSaveEdit.setStyleSheet(QString("QLineEdit { background: green }"))
            self.okButton.setEnabled(True)
        else:
            self.passwordLabel.setText(self.trUtf8("Passwords do not match"))
            self.passwordEdit.setStyleSheet(QString(""))
            self.passwordSaveEdit.setStyleSheet(QString("QLineEdit { background: red }"))
            self.okButton.setEnabled(False)

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



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
