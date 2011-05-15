# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004,2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

#from qt import *
#from base.utils.gui.editors.RdnEditorDesign import RdnEditorDesign
#from base.backend.SmartDataObject import SmartDataObject
#import environment
#import os

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
        
###############################################################################
        
    def initValue(self, smartObject, attributeName, index):
        """ Initialize the dialog with values for the attribute to be edited.
        """
        self.baseDN = unicode(smartObject.getDN(),"utf-8")
        
        # Get the list of supported attributes which are possible by the 
        # given objectclasses. Filter out binary attributes and fill the 
        # combobox.
        mustSet, maySet = smartObject.getPossibleAttributes()
        tmpSet = mustSet.union(maySet)
        possibleAttributes = filter(lambda x: not smartObject.isAttributeBinary(x), tmpSet)
        possibleAttributes.sort()
        map(self.attributeBox.addItem, possibleAttributes)
            
        
        
        
###############################################################################

    def getValue(self):
        return self.value
        
###############################################################################

    def updateValue(self, newText):
        tmpValue = unicode(self.valueEdit.text())
        attributeName = unicode(self.attributeBox.currentText())
        
        self.value = attributeName + u"=" + tmpValue + u"," + self.baseDN
        
        self.dnLabel.setText(self.value)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
