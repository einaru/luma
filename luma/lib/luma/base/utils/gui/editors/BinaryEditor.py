# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004,2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4.QtGui import *
import os

from base.utils.gui.editors.BinaryEditorDesign import BinaryEditorDesign
import environment



class BinaryEditor(BinaryEditorDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        BinaryEditorDesign.__init__(self,parent,name,modal,fl)
        
        self.informationLabel.setText("")
        self.okButton.setEnabled(False)
        
        # Set icon for label and button
        iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        editorPixmap = QPixmap(os.path.join(iconPath, "binary_big.png"))
        self.iconLabel.setPixmap(editorPixmap)
        
        folderPixmap = QPixmap(os.path.join(iconPath, "folder.png"))
        self.fileButton.setPixmap(folderPixmap)
        
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
                            QString.null,
                            "All files (*)",
                            self, None,
                            self.trUtf8("Select file to change binary value"),
                            None, 1)
                            
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
        
        
        
