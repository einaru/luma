# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004,2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
from base.utils.gui.editors.RdnEditorDesign import RdnEditorDesign
from base.backend.SmartDataObject import SmartDataObject
import environment
import os


class RdnEditor(RdnEditorDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        RdnEditorDesign.__init__(self,parent,name,modal,fl)
        
        # Set icon for label
        iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        editorPixmap = QPixmap(os.path.join(iconPath, "editor.png"))
        self.iconLabel.setPixmap(editorPixmap)
        
        # The complete DN of the object
        self.value = None
        
        # The base dn where the object should be created
        self.baseDN = None
        
###############################################################################
        
    def initValue(self, dataObject, attributeName, index):
        """ Initialize the dialog with values for the attribute to be edited.
        """
        
        self.baseDN = dataObject.getDN()
        
        # Get the list of supported attributes which are possible by the 
        # given objectclasses. Filter out binary attributes and fill the 
        # combobox.
        mustSet, maySet = dataObject.getPossibleAttributes()
        tmpSet = mustSet.union(maySet)
        possibleAttributes = filter(lambda x: not dataObject.isAttributeBinary(x), tmpSet)
        possibleAttributes.sort()
        map(lambda x: self.attributeBox.insertItem(x) , possibleAttributes)
            
        
        
        
###############################################################################

    def getValue(self):
        return self.value
        
###############################################################################

    def updateValue(self, newText):
        tmpValue = unicode(self.valueEdit.text())
        attributeName = unicode(self.attributeBox.currentText())
        
        self.value = attributeName + u"=" + tmpValue + u"," + unicode(self.baseDN)
        
        self.dnLabel.setText(self.value)
