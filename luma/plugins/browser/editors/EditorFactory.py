# -*- coding: utf-8 -*-
#
# browser.editors.EditorFactory
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
from base.backend.SmartDataObject import SmartDataObject
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from .StandardEditor import StandardEditor
from .PasswordEditor import PasswordEditor
from .BinaryEditor import BinaryEditor
from .RdnEditor import RdnEditor


# Warning. All attributes listed here must be lowercase
attributeDictionary = {'rdn': RdnEditor}


def getEditorWidget(parent, smartObject, attributeName, index=0):
    dialog = None

    # Do we have a direct mapping from attribute to editor?
    global attributeDictionary
    if attributeDictionary.has_key(attributeName.lower()):
        dialog = attributeDictionary[attributeName.lower()](parent)
        dialog.initValue(smartObject, attributeName, index)

    # We don't have a direct mapping
    else:
        # Is attribute password?
        if smartObject.isAttributePassword(attributeName):
            dialog = PasswordEditor(parent)

        # Is attribute binary?
        elif smartObject.isAttributeBinary(attributeName):
            dialog = BinaryEditor(parent)
            dialog.initValue(smartObject, attributeName, index)

        # Attribute is not binary. Use standard editor.
        else:
            dialog = StandardEditor(parent)
            dialog.initValue(smartObject, attributeName, index)

    if dialog == None:
        raise Exception("No suitable editor dialog found")

    return dialog


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
