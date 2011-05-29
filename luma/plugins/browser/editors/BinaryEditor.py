# -*- coding: utf-8 -*-
#
# browser.editors.BinaryEditor
#
# Copyright (c) 2004, 2005
#     Wido Depping, <widod@users.sourceforge.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/
import os

import PyQt4
from PyQt4.QtCore import QString
from PyQt4.QtGui import QDialog, QFileDialog, QIcon
from ..gui.BinaryEditorDesign import Ui_BinaryEditorDesign
from base.util.IconTheme import pixmapFromTheme

class BinaryEditor(QDialog, Ui_BinaryEditorDesign):

    def __init__(self, parent = None, flags = PyQt4.QtCore.Qt.Widget):
        QDialog.__init__(self, parent, flags)
        self.setupUi(self)

        self.informationLabel.setText("")
        self.okButton.setEnabled(False)

        # Set icon for label and button
        editorPixmap = pixmapFromTheme("document-encrypted", ":/icons/64/document-encrypted", 64, 64)
        self.iconLabel.setPixmap(editorPixmap)

        folderPixmap = pixmapFromTheme("folder", ":/icons/16/folder", 16, 16)
        self.fileButton.setIcon(QIcon(folderPixmap))

        self.value = None
        self.fileName = ""

###############################################################################

    def updateValue(self, tmpString):
        self.fileName = unicode(tmpString).strip()

        enable = True

        # Check the given filename
        self.informationLabel.setText("")
        if not os.path.exists(self.fileName):
            self.informationLabel.setText(self.trUtf8("Given file does not exist. Please check the filename."))
            enable = False
        elif os.path.isdir(self.fileName):
            self.informationLabel.setText(self.trUtf8("Given file is a directory. Please check the filename."))
            enable = False
        else:
            try:
                open(self.fileName, "r")
            except IOError, e:
                self.informationLabel.setText(self.trUtf8("Can't open file. Please check file permissions."))
                enable = False

        self.okButton.setEnabled(enable)

###############################################################################

    def showFileDialog(self):
        tmpFileName = QFileDialog.getOpenFileName(\
                            self,
                            self.trUtf8("Select file to change binary value"),
                            QString(""),
                            "All files (*)",
                            None)

        self.fileName = unicode(tmpFileName).strip()
        self.valueEdit.setText(self.fileName)

###############################################################################

    def initValue(self, dataObject, attributeName, index):
        """ Initialize the dialog with values for the attribute to be edited.
        """

        # Init label with attribute name
        tmpText = self.attributeLabel.text().arg(attributeName)
        self.attributeLabel.setText(tmpText)

###############################################################################

    def getValue(self):
        """ Return the content of the selected filename.
        """

        # if cancel button has been pressed, leave function
        if self.fileName == "":
            return None

        content = open(self.fileName, "r").readlines()
        self.value = "".join(content)

        return self.value




# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
