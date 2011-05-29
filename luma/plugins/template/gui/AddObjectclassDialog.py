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
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from .AddObjectclassDialogDesign import Ui_AddObjectclassDialog

class AddObjectclassDialog(QDialog, Ui_AddObjectclassDialog):

    def __init__(self, ocai, templateObject):
        QDialog.__init__(self)
        self.setupUi(self)

        self.ocai = ocai
        objectclassesList = templateObject.objectclasses
        list = []
        for objectclasses in self.ocai.getObjectClasses():
            if not objectclasses in objectclassesList:
                list.append(objectclasses)
        list.sort(key = str.lower)
        self.listWidgetObjectclasses.addItems(list)
        self.labelMainIcon.setPixmap(QPixmap(':/icons/64/objectclass'))
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
