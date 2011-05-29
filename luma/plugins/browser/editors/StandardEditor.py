# -*- coding: utf-8 -*-
#
# browser.editors.StandardEditor
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
import PyQt4
from PyQt4.QtGui import QDialog
from ..gui.StandardEditorDesign import Ui_StandardEditorDesign
from base.util.IconTheme import pixmapFromTheme


class StandardEditor(QDialog, Ui_StandardEditorDesign):

    def __init__(self, parent = None, flags = PyQt4.QtCore.Qt.Widget):
        QDialog.__init__(self, parent, flags=flags)
        self.setupUi(self)

        # Set icon for label
        editorPixmap = pixmapFromTheme(
            "accessories-text-editor", ":/icons/48/accessories-text-editor")
        self.iconLabel.setPixmap(editorPixmap)

        self.value = None

    def initValue(self, smartObject, attributeName, index):
        """Initialize the dialog with values for the attribute to be edited.
        """

        # Init label with attribute name
        tmpText = self.attributeLabel.text().arg(attributeName)
        self.attributeLabel.setText(tmpText)

        # Set old value
        oldValue = smartObject.getAttributeValue(attributeName, index)

        if not (oldValue == None):
            self.value = oldValue
            self.valueEdit.setText(oldValue)

    def getValue(self):
        return self.value

    def updateValue(self, newText):
        self.value = unicode(newText)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
