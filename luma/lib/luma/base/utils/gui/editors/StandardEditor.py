# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004,2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
from base.utils.gui.editors.StandardEditorDesign import StandardEditorDesign
from base.backend.SmartDataObject import SmartDataObject
import environment
import os


class StandardEditor(StandardEditorDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        StandardEditorDesign.__init__(self,parent,name,modal,fl)
        
        # Set icon for label
        iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        editorPixmap = QPixmap(os.path.join(iconPath, "editor.png"))
        self.iconLabel.setPixmap(editorPixmap)
        
        self.value = None
        
###############################################################################
        
    def initValue(self, dataObject, attributeName, index):
        """ Initialize the dialog with values for the attribute to be edited.
        """
        
        # Init label with attribute name
        tmpText = self.attributeLabel.text().arg(attributeName)
        self.attributeLabel.setText(tmpText)
        
        # Set old value
        oldValue = dataObject.getAttributeValue(attributeName, index)
        
        if not (None == oldValue):
            self.value = oldValue
            self.valueEdit.setText(oldValue)
            self.valueEdit.selectAll()
        
###############################################################################

    def getValue(self):
        return self.value
        
###############################################################################

    def updateValue(self, newText):
        self.value = unicode(newText)
