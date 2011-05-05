# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004,2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

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
        
###############################################################################
        
    def initValue(self, smartObject, attributeName, index):
        """ Initialize the dialog with values for the attribute to be edited.
        """
        
        # Init label with attribute name
        tmpText = self.attributeLabel.text().arg(attributeName)
        self.attributeLabel.setText(tmpText)
        
        # Set old value
        oldValue = smartObject.getAttributeValue(attributeName, index)
        
        if not (oldValue == None):
            self.value = oldValue
            self.valueEdit.setText(oldValue)
        
###############################################################################

    def getValue(self):
        return self.value
        
###############################################################################

    def updateValue(self, newText):
        self.value = unicode(newText)
