# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Simen Natvig, <simen.natvig@gmail.com>
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
from PyQt4.QtGui import QDialog, QPixmap
from .AddAttributeDialogDesign import Ui_AddAttributeDialog
from ..model.AttributeTableModel import AttributeTableModel

class AddAttributeDialog(QDialog, Ui_AddAttributeDialog):

    def __init__(self, ocai, templateObject):
        QDialog.__init__(self)
        self.setupUi(self)
        self.attributeTM = AttributeTableModel()
        self.tableView.setModel(self.attributeTM)
        self.ocai = ocai
        objectclassesList = templateObject.objectclasses
        attributeNameList = self.ocai.getAllMays(objectclassesList)
        self.labelMainIcon.setPixmap(QPixmap(':/icons/64/attribute'))
        for name in attributeNameList:
            if not name in templateObject.attributes.keys():
                single = self.ocai.isSingle(name)
                binary = self.ocai.isBinary(name)
                self.attributeTM.addRow(name, False, single, binary, "", False)

        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
