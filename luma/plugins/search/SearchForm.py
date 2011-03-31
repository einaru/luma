# -*- coding: utf-8 -*-
#
# plugins.search.SearchForm
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

from PyQt4.QtCore import (Qt)
from PyQt4.QtGui import (QCompleter, QWidget)

from .Search import encodeUTF8
from .gui.SearchFormDesign import Ui_SearchForm

class SearchForm(QWidget, Ui_SearchForm):
    """The Luma search form widget.
    
    This class provides easy getters for the various input and
    selection options provided by the widget.
    """
    availableScopes = [
        'SCOPE_BASE',
        'SCOPE_ONELEVEL',
        'SCOPE_SUBTREE'
    ]

    def __init__(self, parent=None):
        super(SearchForm, self).__init__(parent)
        self.setupUi(self)
        self.scopeBox.addItems(self.availableScopes)
        self.__connectSlots()

    def __connectSlots(self):
        """Connect signals and slots.
        """
        self.filterBoxEdit.currentIndexChanged['QString'].connect(self.onSearchCriteriaChanged)
        self.filterBoxEdit.editTextChanged['QString'].connect(self.onSearchCriteriaChanged)
        self.filterBoxEdit.lineEdit().returnPressed.connect(self.searchButton.animateClick)

    def __escape(self, text):
        """FIXME: Dummy escaping
        """
        if not text.startswith('('):
            text = '({0}'.format(text)
        if not text.endswith(')'):
            text = '{0})'.format(text)
        return text

    def onSearchCriteriaChanged(self, text):
        """Slot for the search edit widget
        
        Enable or disable the search button. If text is empty the
        search button is disabled. If not it is enabled.
        """
        self.searchButton.setDisabled(text == '')

    def populateBaseDNBox(self, baseDNList=[]):
        """Populate the base DN combo box with a available base DNs.
        
        @param baseDNList: list;
            A list containing base DN.
        """
        self.baseDNBox.clear()
        # This should fix the no-network bug
        if not baseDNList is None:
            for x in baseDNList:
                self.baseDNBox.addItem(x)

    def populateFilterBookmarks(self, filterBookmarks):
        """Populates the search edit combobox with saved search
        filters.
        """
        tmp = [self.filterBoxEdit.currentText()]
        self.filterBoxEdit.clear()
        tmp.extend(filterBookmarks)
        self.filterBoxEdit.addItems(tmp)

    def initAutoComplete(self, attributes):
        """Initialize the filter input auto completion.
        
        Try to fetches the list of available attributes from the server
        selected in the server combo box. This list will be used to
        give the user auto complete options while building search
        filters.
        """
        # If we get an attribute list off the server we set up the
        # attribute auto completer.  
        if len(attributes) > 0:
            self.completer = QCompleter(attributes, self)
            self.completer.setCaseSensitivity(Qt.CaseSensitive)
            self.completer.setCompletionPrefix(',')
            self.filterBoxEdit.setCompleter(self.completer)

    def setAndUseFilter(self, filter):
        """Insert, set as current, and search with the filter.
        """
        self.filterBoxEdit.insertItem(0, filter)
        self.filterBoxEdit.setCurrentIndex(0)
        self.searchButton.clicked.emit(True)

    @property
    def server(self):
        return encodeUTF8(self.serverBox.currentText())

    @property
    def baseDN(self):
        return encodeUTF8(self.baseDNBox.currentText())

    @property
    def scope(self):
        return self.scopeBox.currentIndex()

    @scope.setter
    def scope(self, index):
        self.scopeBox.setCurrentIndex(index)

    @property
    def sizeLimit(self):
        return self.sizeLimitSpinBox.value()

    @sizeLimit.setter
    def sizeLimit(self, limit):
        self.sizeLimitSpinBox.setValue(limit)

    @property
    def filter(self):
        # TODO: run some validation on the filter
        return self.__escape(encodeUTF8(self.filterBoxEdit.currentText()))


class AttributeCompleter(QCompleter):
    """Attribute Completer for the search plugin.
    
    Subclassing and customizing the QCompleter inorder to provide smart
    autocomplete options on the available attribute list for a selected
    server.
    """

    def __init__(self, attributeList=[], parent=None):
        super(AttributeCompleter, self).__init__(parent)
        self.setCaseSensitivity(Qt.CaseSensitive)
        self.__attributeList = set(attributeList)
