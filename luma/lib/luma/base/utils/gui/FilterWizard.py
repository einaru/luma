# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path

from base.utils.gui.FilterWizardDesign import FilterWizardDesign
from base.backend.ServerList import ServerList
from base.backend.ServerObject import ServerObject
import environment
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo

class FilterWizard(FilterWizardDesign):

    bookmarkFile = None

    def __init__(self,serverMeta=None, parent=None, name=None, modal=0, fl=0):
        FilterWizardDesign.__init__(self,parent,name,modal,fl)

        self.objectInfo = ObjectClassAttributeInfo(serverMeta)

        self.objectSelection = "CLASS"
        self.classButton.setChecked(1)
        self.filterTypeBox.setEnabled(0)
        self.expressionEdit.setEnabled(0)
        self.initObjectCombo()

        self.bookmarkFile = os.path.join(environment.userHomeDir, ".luma", "filterBookmarks")
        self.initFilterBookmarks()

###############################################################################

    def classChoiceChanged(self):
        if self.classButton.isChecked():
            self.attributeButton.setChecked(0)
            self.objectSelection = "CLASS"
            self.filterTypeBox.setEnabled(0)
            self.expressionEdit.setEnabled(0)
        else:
            self.classButton.setChecked(0)
            self.attributeButton.setChecked(1)
            self.objectSelection = "ATTRIBUTE"
            self.filterTypeBox.setEnabled(1)
            self.expressionEdit.setEnabled(1)
        self.initObjectCombo()

###############################################################################

    def attributeChoiceChanged(self):
        if self.attributeButton.isChecked():
            self.classButton.setChecked(0)
            self.objectSelection = "ATTRIBUTE"
            self.filterTypeBox.setEnabled(1)
            self.expressionEdit.setEnabled(1)
        else:
            self.attributeButton.setChecked(0)
            self.classButton.setChecked(1)
            self.objectSelection = "CLASS"
            self.filterTypeBox.setEnabled(0)
            self.expressionEdit.setEnabled(0)
        self.initObjectCombo()

###############################################################################

    def initObjectCombo(self):
        if self.objectSelection == "CLASS":
            self.objectBox.clear()
            tmpList = self.objectInfo.objectClassesDict.keys()
            tmpList.sort()
            self.objectBox.insertItem("*")
            for x in tmpList:
                self.objectBox.insertItem(x)
        else:
            self.objectBox.clear()
            tmpList = self.objectInfo.attributeDict.keys()
            tmpList.sort()
            for x in tmpList:
                self.objectBox.insertItem(x)

###############################################################################

    def addCriteria(self):
        if self.objectSelection == "CLASS":
            tmpString = "(objectClass=" + str(self.objectBox.currentText()) + ")"
            position = self.searchFilterEdit.cursorPosition()
            text = str(self.searchFilterEdit.text())
            newString = text[:position] + tmpString + text[position:]
            self.searchFilterEdit.setText(newString)
        else:
            objectText =    str(self.objectBox.currentText())
            filterTypeText = str(self.filterTypeBox.currentText())[:2]
            if filterTypeText[1] == " ":
                filterTypeText = filterTypeText[0]
            expressionText = str(self.expressionEdit.text())
            tmpString = "(" + objectText + filterTypeText + expressionText + ")"
            position = self.searchFilterEdit.cursorPosition()
            text = str(self.searchFilterEdit.text())
            newString = text[:position] + tmpString + text[position:]
            self.searchFilterEdit.setText(newString)

###############################################################################

    def addConcat(self):
        position = self.searchFilterEdit.cursorPosition()
        text = str(self.searchFilterEdit.text())

        boxId = self.concatBox.currentItem()
        val = None
        if boxId == 0:
            val = "(& )"
        elif boxId == 1:
            val = "(| )"
        elif boxId == 2:
            val = "(! )"
            
        newString = text[:position] + val + text[position:]
        self.searchFilterEdit.setText(newString)

###############################################################################

    def initFilterBookmarks(self):
        try:
            fileHandler = open(self.bookmarkFile, 'r')
            text = fileHandler.readlines()
            fileHandler.close()
            self.bookmarkBox.clear()
            for x in text:
                self.bookmarkBox.insertItem(x[:-1])
        except:
            print "Bookmark loading failed"

###############################################################################

    def bookmarkSelected(self):
        self.searchFilterEdit.setText(self.bookmarkBox.currentText())

###############################################################################

    def addBookmark(self):
        self.bookmarkBox.insertItem(self.searchFilterEdit.text())
        self.saveBookmarks()
        self.bookmarkBox.setCurrentItem(self.bookmarkBox.count()-1)

###############################################################################

    def deleteBookmark(self):
        if not(self.bookmarkBox.count() == 0):
            self.bookmarkBox.removeItem(self.bookmarkBox.currentItem())
            self.saveBookmarks()
            if not (self.bookmarkBox.count() == 0):
                self.bookmarkBox.setCurrentItem(0)

###############################################################################

    def saveBookmarks(self):
        try:
            fileHandler = open(self.bookmarkFile, 'w')
            for x in range(0, self.bookmarkBox.count()):
                fileHandler.write(str(self.bookmarkBox.text(x)) + "\n")
            fileHandler.close()
        except:
            print "Bookmark saving failed"
















