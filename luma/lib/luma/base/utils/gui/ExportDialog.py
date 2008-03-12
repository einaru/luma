# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004, 2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4.QtGui import *
import os
import os.path
import dsml
import StringIO
import ldap

from base.utils.gui.ExportDialogDesign import ExportDialogDesign
import environment
from base.utils import getSortedDnList, stripSpecialChars, explodeDN
from base.backend.LumaConnection import LumaConnection


class ExportDialog(ExportDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        ExportDialogDesign.__init__(self,parent,name,modal,fl)
        
        self.iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        self.exportIcon = QPixmap(os.path.join(self.iconPath, "export_big.png"))
        self.iconLabel.setPixmap(self.exportIcon)
        folderPixmap = QPixmap(os.path.join(self.iconPath, "folder.png"))
        self.fileButton.setPixmap(folderPixmap)
        
        self.fileLabel.setText("")
        self.resultLabel.setText("")
        
        self.okIcon = QPixmap(os.path.join(self.iconPath, "ok.png"))
        self.failureIcon = QPixmap(os.path.join(self.iconPath, "no.png"))
        
        self.itemView.setColumnText(0, "")
        self.itemView.setColumnWidth(0, 32)
        self.itemView.setSorting(-1, False) 
        
        self.startButton.setEnabled(False)
        
        # Dictionary of items which should be exported.
        # Key is the prettyDN; value is as list with the normal dn 
        # and the QListViewItem
        self.exportDictionary = {}
        
        # Filename where to export the entries
        self.fileName = None
        
###############################################################################

    def initData(self, itemList):
        """ Initializaion of the dialog with data.
        """
        
        itemList.sort()
        
        for x in itemList[::-1]:
            prettyDN = x.getPrettyDN()
            
            tmpItem = QListViewItem(self.itemView)
            tmpItem.setText(1, prettyDN)
            self.exportDictionary[prettyDN] = [x, tmpItem]
            
###############################################################################

    def showFileDialog(self):
        tmpFileName = QFileDialog.getSaveFileName(\
                        QString.null,
                        "LDIF Files (*.ldif);; DSML Files (*.dsml);; All files (*)",
                        None, None,
                        self.trUtf8("Select file for exporting"),
                        None, 1)

                            
        self.fileName = unicode(tmpFileName).strip()
        self.fileEdit.setText(self.fileName)
        
###############################################################################

    def updateFileName(self, tmpString):
        self.fileName = unicode(tmpString).strip()
        
        enable = True
        
        # Check the given filename
        self.fileLabel.setText("")
        if os.path.isdir(self.fileName):
            self.fileLabel.setText(self.trUtf8("Given file is a directory. Please check the filename."))
            enable = False
        else:
            try:
                if os.path.isfile(self.fileName) or os.path.islink(self.fileName):
                    open(self.fileName, "r")
                else:
                    fileHandler = open(self.fileName, "w")
                    fileHandler.close()
                    os.remove(self.fileName)
            except IOError, e:
                self.fileLabel.setText(self.trUtf8("Can't open file. Please check file system permissions."))
                enable = False
                
        if enable:
            self.fileEdit.unsetPalette()
        else:
            self.fileEdit.setPaletteBackgroundColor(Qt.red)
        
        self.startButton.setEnabled(enable)
        
###############################################################################

    def removeItems(self):
        """ Remove the currently selected items from the list of items to 
        be exported.
        """
        
        selectedList = []
        
        listIterator = QListViewItemIterator(self.itemView)
        while listIterator.current():
            item = listIterator.current()
            if item.isSelected():
                selectedList.append(item)
            listIterator += 1
        
        for x in selectedList:
            name = unicode(x.text(1))
            self.itemView.takeItem(self.exportDictionary[name][1])
            del self.exportDictionary[name]

###############################################################################

    def exportItems(self):
        environment.setBusy(True)
        
        itemList = map(lambda x: self.exportDictionary[x][0], self.exportDictionary.keys())
        itemList.sort()
        
        allExported = True
        
        try:
            fileHandler = open(self.fileName, "w")
                
            format = str(self.formatBox.currentText())
            
            if format == "DSML":
                tmpString = StringIO.StringIO()
                dsmlWriter = dsml.DSMLWriter(tmpString)
                dsmlWriter.writeHeader()
                fileHandler.write(tmpString.getvalue())
            
            for x in itemList:
                try:
                    if format == "LDIF":
                        fileHandler.write(x.convertToLdif())
                    elif format == "DSML":
                        fileHandler.write(x.convertToDsml())
            
                    self.displayItemStatus(self.exportDictionary[x.getPrettyDN()][1], True, None)
                except IOError, e:
                    self.displayItemStatus(self.exportDictionary[x.getPrettyDN()][1], False, None)
                    allExported = False
            
            if format == "DSML": 
                tmpString = StringIO.StringIO()
                dsmlWriter = dsml.DSMLWriter(tmpString)
                dsmlWriter.writeFooter()
                fileHandler.write(tmpString.getvalue())
            
            fileHandler.close()
            
            if not allExported:
                self.resultLabel.setText(self.trUtf8("Could not export all entires. Please check messages."))
            else:
                self.resultLabel.setText(self.trUtf8("All items exported successfully."))
                
        except IOError, e:
            self.resultLabel.setText(self.trUtf8("Can't open file. Please check file system permissions."))

        environment.setBusy(False)
        
        if allExported:
            self.accept()
        
        

###############################################################################

    def displayItemStatus(self, listItem, success, exceptionObject):
        if success:
            listItem.setPixmap(0, self.okIcon)
            listItem.setText(2, self.trUtf8("Item exported successfully."))
        else:
            listItem.setPixmap(0, self.failureIcon)
            listItem.setText(2, str(exceptionObject))
            
