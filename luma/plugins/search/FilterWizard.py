# -*- coding: utf-8 -*-
#
# plugins.search.FilterWizard
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

import logging

from PyQt4.QtGui import (QWidget, QTextCursor)

from base.util import encodeUTF8
from base.util.IconTheme import iconFromTheme

from gui.FilterWizardDesign import Ui_FilterWizard

class FilterWizard(QWidget, Ui_FilterWizard):
    """The Luma filter wizard widget
    
    Widget for building simple and complex LDAP search filters.
    """

    objectClassOptions = ['*']
    equalityOperators = [
        '= (equals)',
        '-= (approximately)',
        '>= (greater than)',
        '<= (less than)'
    ]
    specialChars = {
        'NUL' : r'\00',
        '"' : r'\22',
        '(' : r'\28',
        ')' : r'\29',
        '*' : r'\2A',
        '+' : r'\2B',
        ',' : r'\2C',
        '/' : r'\2F',
        ';' : r'\3B',
        '<' : r'\3C',
        '=' : r'\3D',
        '>' : r'\3E',
        '\\' : r'\5C',
    }

    __logger = logging.getLogger(__name__)

    def __init__(self, objectClasses=[], attributes=[], parent=None):
        """
        """
        super(FilterWizard, self).__init__(parent)
        self.setupUi(self)
        
        self.undoButton.setIcon(iconFromTheme('edit-undo', ':/icons/undo'))
        self.redoButton.setIcon(iconFromTheme('edit-redo', ':/icons/redo'))
        self.addSpecialCharButton.setIcon(iconFromTheme('list-add', ':/icons/single'))

        self.objectClassOptions.extend(objectClasses)
        #self.objectClassOptions = objectClasses
        self.attributeOptions = attributes


        self.equalityBox.addItems(self.equalityOperators)
        self.__populateSpecialCharBox()
        self.__connectSlots()
        # Force populate the object class options as this is the one
        # selected on default
        self.setOptions(objectClass=True)

    def __connectSlots(self):
        """Connects signals and slots.
        """
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.insertButton.clicked.connect(self.onInsertButtonClicked)
        self.notButton.clicked.connect(self.onNotButtonClicked)
        self.andButton.clicked.connect(self.onAndButtonClicked)
        self.orButton.clicked.connect(self.onOrButtonClicked)
        self.rbObjectClass.toggled[bool].connect(self.setOptions)
        self.addSpecialCharButton.clicked.connect(self.onAddSpecialCharButtonClicked)

    def __populateSpecialCharBox(self):
        """Populate the special char combo box with the defined special
        chars.
        """
        for key, value in self.specialChars.iteritems():
            self.specialCharBox.addItem(key, value)

    def __escapeFilterItem(self, item):
        """Escapes part of a filter properly.
        
        First we checks if it already is properly escapes and simply
        returns the pased parameter if it is.
        If not we append ( at the start and ) at the end.
        
        @return:
            The escaped filter item
        """
        item = encodeUTF8(item)
        if not item.startswith('('):
            item = '(%s' % item
        if not item.endswith(')'):
            item = '%s)' % item
        return item

    def __addSearchCriteria(self, criteria):
        """Builds the search criteria based on the various selections
        in the widgets, and insert it in the main filter edit widget.
        """
        self.filterEdit.insertPlainText(self.__escapeFilterItem(criteria))

    def __equalityOperator(self, index):
        """Return the appropriate equality operator for the given index.
        
        The returned operator is based on the items in the equality box.
        
        @return:
            the corrosponding equality operator
        """
        return encodeUTF8(self.equalityBox.itemText(index)).split(' ')[0]

    def __moveCursor(self, operation, n=1):
        """Elegant way of moving the position of the text edit cursor
        multiple chars in the direction defined by operation.
        
        @param operation: QTextCursor.MoveOperation;
            the move operation to apply on the text cursor
        @param n; integer;
            the number of times the operation should be applied
        """
        for _ in xrange(0, n):
            self.filterEdit.moveCursor(operation)

    def setOptions(self, objectClass):
        """Slot for the objectClass radio button.
        
        Populates the option combo box with available object classes, 
        or attributes, depending on the objectClass parameter.
        
        @param objectClass: boolean value;
            This value indicates wheter the object class radio button
            is selected or not.
        """
        self.optionBox.clear()
        if objectClass:
            self.optionBox.addItems(self.objectClassOptions)
        else:
            self.optionBox.addItems(self.attributeOptions)

    def onServerChanged(self, objectClasses, attributes):
        """This method is called when the server in the main search
        plugin form is changed. This ensures we are working with the
        correct object classes and attributes, when build a filter.
        """
        self.objectClassOptions = ['*']
        self.objectClassOptions.extend(objectClasses)
        self.attributeOptions = attributes
        self.setOptions(self.rbObjectClass.isChecked())

    def onNotButtonClicked(self):
        """Slot for the not button.
        
        If the criteria line edit widget is empty, all we do is insert,
        the ! operator:
        
            (!)
        
        If it is not empty we need to insert it and properly escape the
        text already present.
            
           ...(!(<selected text>))...
        
        Either way we also need to position the cursor.
        """
        cursor = self.filterEdit.textCursor()
        tmp = cursor.selectedText()
        if tmp == '':
            self.filterEdit.insertPlainText('(!())')
            self.__moveCursor(QTextCursor.Left, 2)
        else:
            self.filterEdit.insertPlainText('(!%s)' % self.__escapeFilterItem(tmp))

    def onAndButtonClicked(self):
        """Slot for the and button.
        
        If the criteria line edit widget is empty all we do is insert,
        the & operator:
            
            (&)
        
        If is not empty er need to insert it and properly escape the
        text already present:
        
            ...(&(<selected text>)...
        
        """
        cursor = self.filterEdit.textCursor()
        tmp = cursor.selectedText()
        if tmp == '':
            self.filterEdit.insertPlainText('(&())')
            self.__moveCursor(QTextCursor.Left, 2)
        else:
            self.filterEdit.insertPlainText('(&%s)' % self.__escapeFilterItem(tmp))

    def onOrButtonClicked(self):
        """Slot for the or button.
        
        If the criteria line edit widget is empty all we do is insert,
        the | operator:
            
            (|)
        
        If is not empty er need to insert it and properly escape the
        text already present:
        
            ...(|(<selected text>)...
        
        """
        cursor = self.filterEdit.textCursor()
        tmp = cursor.selectedText()
        if tmp == '':
            self.filterEdit.insertPlainText('(|())')
            self.__moveCursor(QTextCursor.Left, 2)
        else:
            self.filterEdit.insertPlainText('(|%s)' % self.__escapeFilterItem(tmp))

    def onAddSpecialCharButtonClicked(self):
        """Slot for the add special char button.
        
        Inserts the corresponding escape value of the special char 
        currently selected in the combobox.
        """
        index = self.specialCharBox.currentIndex()
        specialChar = self.specialCharBox.itemData(index).toString()
        self.filterEdit.insertPlainText(specialChar)

    def onInsertButtonClicked(self):
        """Slot for the insert button.
        
        Get the selected values from hte search criteria group,
        concatenate them, and insert the string into the main filter
        edit widget.
        """
        if self.rbObjectClass.isChecked():
            obj = encodeUTF8(self.optionBox.currentText())
            criteria = 'objectClass=%s' % obj
        elif self.rbAttribute.isChecked():
            attr = encodeUTF8(self.optionBox.currentText())
            eq = self.__equalityOperator(self.equalityBox.currentIndex())
            criteria = encodeUTF8(self.criteriaEdit.text())
            if criteria == '':
                return
            criteria = u'%s%s%s' % (attr, eq, criteria)

        self.__addSearchCriteria(criteria)
        self.filterEdit.setFocus()

    def onSaveButtonClicked(self):
        """Slot for the save button.
        """
        self.__logger.debug('Implement save method')
