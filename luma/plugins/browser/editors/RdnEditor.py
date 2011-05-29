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
import PyQt4
from PyQt4.QtGui import QDialog
from ..gui.RdnEditorDesign import Ui_RdnEditorDesign
from base.util.IconTheme import pixmapFromTheme


class RdnEditor(QDialog, Ui_RdnEditorDesign):

    def __init__(self, parent = None, flags = PyQt4.QtCore.Qt.Widget):
        QDialog.__init__(self,parent,flags)
        self.setupUi(self)

        # Set icon for label
        editorPixmap = pixmapFromTheme(
            "accessories-text-editor", ":/icons/48/accessories-text-editor")
        self.iconLabel.setPixmap(editorPixmap)

        # The complete DN of the object
        self.value = None

        # The base dn where the object should be created
        self.baseDN = None

    def initValue(self, smartObject, attributeName, index):
        """ Initialize the dialog with values for the attribute to be edited.
        """
        self.baseDN = unicode(smartObject.getDN(),"utf-8")

        # Get the list of supported attributes which are possible by the
        # given objectclasses. Filter out binary attributes and fill the
        # combobox.
        mustSet, maySet = smartObject.getPossibleAttributes()
        tmpSet = mustSet.union(maySet)
        possibleAttributes = filter(
            lambda x: not smartObject.isAttributeBinary(x), tmpSet
        )
        possibleAttributes.sort()
        map(self.attributeBox.addItem, possibleAttributes)

    def getValue(self):
        return self.value

    def updateValue(self, newText):
        tmpValue = unicode(self.valueEdit.text())
        attributeName = unicode(self.attributeBox.currentText())

        self.value = attributeName + u"=" + tmpValue + u"," + self.baseDN

        self.dnLabel.setText(self.value)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
