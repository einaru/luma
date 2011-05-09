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
import os

from PyQt4 import QtCore
from PyQt4.QtGui import (QWidget, QTextCursor)

from .gui.FilterBuilderDesign import Ui_FilterBuilder
from .Search import (encodeUTF8, PluginSettings)
from .FilterHighlighter import LumaFilterHighlighter


class FilterBuilder(QWidget, Ui_FilterBuilder):
    """The Luma filter wizard widget

    Widget for building simple and complex LDAP search filters.

    .. todo::
        - implement better solution for the filters file. Maybe use
          some sort of syntax (i.e. xml, json, ect.), so that we easily
          can map filters to servers and so on.
        - implement the server selection so that it is shared between
          the search form _and_ the filter builder.
    """

    objectClassOptions = ['*']
    filterTypes = [
        '= (equals)',
        '~= (approximately)',
        '>= (greater than)',
        '<= (less than)'
    ]
    specialChars = {
        'NUL': r'\00',
        '"': r'\22',
        '(': r'\28',
        ')': r'\29',
        '*': r'\2A',
        '+': r'\2B',
        ',': r'\2C',
        '/': r'\2F',
        ';': r'\3B',
        '<': r'\3C',
        '=': r'\3D',
        '>': r'\3E',
        '\\': r'\5C',
    }

    filterSaved = QtCore.pyqtSignal(name='filterSaved')
    useFilterRequest = QtCore.pyqtSignal('QString', name='useFilterRequest')

    __logger = logging.getLogger(__name__)

    def __init__(self, objectClasses=[], attributes=[], parent=None):
        """Initializes the `FilterBuilder`.

        Parameters:

        - `objectClasses`: a list of available object classes for the
          selected LDAP server.
        - `attributes`: a list of available attributes for the selected
          LDAP server.
        """
        super(FilterBuilder, self).__init__(parent)
        self.setupUi(self)

        self.objectClassOptions.extend(objectClasses)
        self.attributeOptions = attributes

        self.filterTypeBox.addItems(self.filterTypes)
        self.__populateSpecialCharBox()
        self.__connectSlots()

        # Force populate the object class options as this is the one
        # selected on default
        self.setOptions(objectClass=True)

    def __connectSlots(self):
        """Connects signals and slots.
        """
        self.addSpecialCharButton.clicked.connect(
            self.onAddSpecialCharButtonClicked)
        self.andButton.clicked.connect(self.onAndButtonClicked)
        self.clearButton.clicked.connect(self.onClearButtonClicked)
        self.assertionEdit.returnPressed.connect(
            self.insertButton.animateClick)
        self.assertionEdit.textChanged.connect(self.onAssertionChanged)
        self.filterEdit.undoAvailable[bool].connect(self.undoButton.setEnabled)
        self.filterEdit.redoAvailable[bool].connect(self.redoButton.setEnabled)
        self.filterEdit.textChanged.connect(self.onFilterChanged)
        self.insertButton.clicked.connect(self.onInsertButtonClicked)
        self.orButton.clicked.connect(self.onOrButtonClicked)
        self.notButton.clicked.connect(self.onNotButtonClicked)
        self.rbAttribute.toggled[bool].connect(self.onAttributeButtonToggled)
        self.rbObjectClass.toggled[bool].connect(
            self.onObjectClassButtonToggled)
        self.redoButton.clicked.connect(self.filterEdit.redo)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.undoButton.clicked.connect(self.filterEdit.undo)
        self.useButton.clicked.connect(self.onUseButtonClicked)

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

        Returns the escaped filter `item`.

        Parameters:

        - `item`: the filter item to be excaped.
        """
        item = encodeUTF8(item)
        if not item.startswith('('):
            item = '({0}'.format(item)
        if not item.endswith(')'):
            item = '{0})'.format(item)
        return item

    def __addFilterComponent(self, assertion):
        """Builds the search assertion based on the various selections
        in the widgets, and insert it in the main filter edit widget.
        """
        self.filterEdit.insertPlainText(self.__escapeFilterItem(assertion))

    def __filterType(self, index):
        """Return the appropriate filter type for the given index.

        The returned type is based on the items in the filter type box.

        Returns the corrosponding filter type
        """
        return encodeUTF8(self.filterTypeBox.itemText(index)).split(' ')[0]

    def __moveCursor(self, operation, n=1):
        """Elegant way of moving the position of the text edit cursor
        multiple chars in the direction defined by operation.

        Parameters:

        - `operation`: a ``QTextCursor.MoveOperation``, which is the
          direction of the move operation to apply on the text cursor.
        - `n`: an integer indicating how many times the `operation`
          should be applied
        """
        for _ in xrange(0, n):
            self.filterEdit.moveCursor(operation)

    def setOptions(self, objectClass):
        """Slot for the objectClass radio button.

        Populates the option combo box with available object classes,
        or attributes, depending on the `objectClass` parameter.

        - `objectClass`: a boolean value indicating wheter the object
          class radio button is selected or not.
        """
        self.optionBox.clear()
        if objectClass:
            self.optionBox.addItems(self.objectClassOptions)
        else:
            self.optionBox.addItems(self.attributeOptions)

    def setFilterHighlighter(self, bool):
        """Registers the filter highligher if bool is True.
        """
        if bool:
            LumaFilterHighlighter(self.filterEdit.document(),
                                  self.attributeOptions)

    def onServerChanged(self, objectClasses, attributes):
        """This method is called when the server in the main search
        plugin form is changed. This ensures we are working with the
        correct object classes and attributes, when build a filter.

        Parameters:

        - `objectClasses`: a list of available object classes for the
          selected server.
        - `attributes`: a list of available attributes for the selected
          server.
        """
        self.objectClassOptions = ['*']
        self.objectClassOptions.extend(sorted(objectClasses, key=str.lower))
        self.attributeOptions = sorted(attributes, key=str.lower)
        self.setOptions(self.rbObjectClass.isChecked())

    def onAttributeButtonToggled(self, bool):
        """Slot for the attribute radio button.
        """
        if bool:
            self.onAssertionChanged(self.assertionEdit.text())

    def onObjectClassButtonToggled(self, bool):
        """Slot for the object class radio button.
        """
        self.setOptions(objectClass=bool)
        self.assertionEdit.setDisabled(bool)
        self.filterTypeBox.setDisabled(bool)
        self.insertButton.setEnabled(True)

    def onAssertionChanged(self, text):
        """Slot for the assertion edit widget.

        If text is empty the insert button is disabled, if not it is
        enabled.
        """
        self.insertButton.setDisabled(text == '')

    def onFilterChanged(self):
        """Slot for the filter edit widget.

        Enable or disable the save button and clear button.
        """
        # As long as something has changed there is something in the
        # undo|redo buffer, and we have something that can be cleared.
        self.clearButton.setEnabled(True)
        currentFilterState = self.filterEdit.toPlainText() == ''
        self.saveButton.setDisabled(currentFilterState)
        # If there is nothing to save, there is nothing to use
        self.useButton.setDisabled(currentFilterState)

    def onNotButtonClicked(self):
        """Slot for the not button.

        If the assertion line edit widget is empty, all we do is insert,
        the ! operator::

            (!)

        If it is not empty we need to insert it and properly escape the
        text already present::

           ...(!(<selected text>))...

        Either way we also need to position the cursor.
        """
        cursor = self.filterEdit.textCursor()
        tmp = cursor.selectedText()
        if tmp == '':
            self.filterEdit.insertPlainText('(!())')
            self.__moveCursor(QTextCursor.Left, 2)
        else:
            tmp = self.__escapeFilterItem(tmp)
            self.filterEdit.insertPlainText('(!{0})'.format(tmp))

    def onAndButtonClicked(self):
        """Slot for the and button.

        If the assertion line edit widget is empty all we do is insert,
        the & operator::

            (&)

        If is not empty er need to insert it and properly escape the
        text already present::

            ...(&(<selected text>)...

        """
        cursor = self.filterEdit.textCursor()
        tmp = cursor.selectedText()
        if tmp == '':
            self.filterEdit.insertPlainText('(&())')
            self.__moveCursor(QTextCursor.Left, 2)
        else:
            tmp = self.__escapeFilterItem(tmp)
            self.filterEdit.insertPlainText('(&{0})'.format(tmp))

    def onOrButtonClicked(self):
        """Slot for the or button.

        If the assertion line edit widget is empty all we do is insert,
        the | operator::

            (|(<cursor>))

        If is not empty er need to insert it and properly escape the
        text already present::

            ...(|(<selected text>)<cursor>...

        """
        cursor = self.filterEdit.textCursor()
        tmp = cursor.selectedText()
        if tmp == '':
            self.filterEdit.insertPlainText('(|())')
            self.__moveCursor(QTextCursor.Left, 2)
        else:
            tmp = self.__escapeFilterItem(tmp)
            self.filterEdit.insertPlainText('(|{0})'.format(tmp))

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

        Get the selected values from the filter component group,
        concatenate them, and insert the string into the main filter
        edit widget.
        """
        if self.rbObjectClass.isChecked():
            obj = encodeUTF8(self.optionBox.currentText())
            component = 'objectClass={0}'.format(obj)
        elif self.rbAttribute.isChecked():
            attr = encodeUTF8(self.optionBox.currentText())
            eq = self.__filterType(self.filterTypeBox.currentIndex())
            component = encodeUTF8(self.assertionEdit.text())
            if component == '':
                return
            component = u'{0}{1}{2}'.format(attr, eq, component)

        self.__addFilterComponent(component)
        self.filterEdit.setFocus()

    def onUseButtonClicked(self):
        """Slot for the use button.

        Emits the useFilterRequest signal.
        """
        self.useFilterRequest.emit(self.filterEdit.toPlainText())

    def onSaveButtonClicked(self):
        """Slot for the save button.
        """
        self.__logger.debug('Implement save method')
        settings = PluginSettings('search')
        prefix = settings.configPrefix
        filterFile = os.path.join(prefix, 'filters')
        filterToSave = self.filterEdit.toPlainText()
        # Set the mode flag depending on the state of the file. If it
        # exists we open the file in append mode, if not we need to use
        # the write flag to make sure it's created.
        if os.path.exists(filterFile):
            flag = 'a'
        else:
            flag = 'w'
        # Try to save the file.
        with open(filterFile, flag) as f:
            f.write('{0}\n'.format(filterToSave))

        # We emit the filterSaved signal after the file is closed
        self.filterSaved.emit()
        # Disable the save button so we limit the number of
        # duplicate entries in the filters file.
        self.saveButton.setEnabled(False)

    def onClearButtonClicked(self):
        """Slot for the clear button

        When we click the clear button we clear the content of the
        filter edit widget, and disables the button. The button will be
        enabled again when the filter edit text changes.
        """
        self.filterEdit.clear()
        self.clearButton.setEnabled(False)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
