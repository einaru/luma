# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <wido.depping@tu-clausthal.de>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path

from base.utils.gui.FilterWizardDesign import FilterWizardDesign
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.backend.ServerList import ServerList
from base.backend.ServerObject import ServerObject
import environment

class FilterWizard(FilterWizardDesign):

    bookmarkFile = None

    def __init__(self,server = None, parent = None,name = None,modal = 0,fl = 0):
        FilterWizardDesign.__init__(self,parent,name,modal,fl)

        self.objectInfo = ObjectClassAttributeInfo(server)
        self.objectInfo.retrieve_info_from_server()

        self.objectSelection = "CLASS"
        self.classButton.setChecked(1)
        self.filterTypeBox.setEnabled(0)
        self.expressionEdit.setEnabled(0)
        self.init_object_combo()

        self.bookmarkFile = os.path.join(environment.userHomeDir, ".luma", "filterBookmarks")
        self.init_filter_bookmarks()

###############################################################################

    def class_choice_changed(self):
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
        self.init_object_combo()

###############################################################################

    def attribute_choice_changed(self):
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
        self.init_object_combo()

###############################################################################

    def init_object_combo(self):
        if self.objectSelection == "CLASS":
            self.objectBox.clear()
            tmpList = self.objectInfo.OBJECTCLASSES.keys()
            tmpList.sort()
            self.objectBox.insertItem("*")
            for x in tmpList:
                self.objectBox.insertItem(x)
        else:
            self.objectBox.clear()
            tmpList = self.objectInfo.ATTRIBUTELIST.keys()
            tmpList.sort()
            for x in tmpList:
                self.objectBox.insertItem(x)

###############################################################################

    def add_criteria(self):
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

    def add_concat(self):
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

    def init_filter_bookmarks(self):
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

    def bookmark_selected(self):
        self.searchFilterEdit.setText(self.bookmarkBox.currentText())

###############################################################################

    def add_bookmark(self):
        self.bookmarkBox.insertItem(self.searchFilterEdit.text())
        self.save_bookmarks()
        self.bookmarkBox.setCurrentItem(self.bookmarkBox.count()-1)

###############################################################################

    def delete_bookmark(self):
        if not(self.bookmarkBox.count() == 0):
            self.bookmarkBox.removeItem(self.bookmarkBox.currentItem())
            self.save_bookmarks()
            if not (self.bookmarkBox.count() == 0):
                self.bookmarkBox.setCurrentItem(0)

###############################################################################

    def save_bookmarks(self):
        try:
            fileHandler = open(self.bookmarkFile, 'w')
            for x in range(0, self.bookmarkBox.count()):
                fileHandler.write(str(self.bookmarkBox.text(x)) + "\n")
            fileHandler.close()
        except:
            print "Bookmark saving failed"
















