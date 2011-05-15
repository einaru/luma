# -*- coding: utf-8 -*-
#
# plugins.search.SearchResult
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

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import (QAbstractItemView, QSizePolicy, QSortFilterProxyModel,
                         QSpacerItem, QStandardItemModel, QTreeView, QWidget)

from base.gui.Dialog import ExportDialog, DeleteDialog
from base.util.IconTheme import pixmapFromTheme


class ResultView(QWidget):
    """This class represent a search result view.
    """

    def __init__(self, filter='', attributes=[], resultlist=[], parent=None):
        """Initialize a result view for the `SearchPlugin`.

        :param filter: the filter applied on the search
        :type filter: string
        :param attributes: a list containing the attributes used in the
         search operation. Usually extracted from the `filter`.
        :type attributes: list
        :param resultlist: a list of `SmartDataObject` from the search
         operation.
        :type resultlist: list
        :param parent: the parent for this widget.
        :type parent: QWidget
        """
        super(ResultView, self).__init__(parent)
        self.setObjectName('ResultView')
        self.layout = QtGui.QVBoxLayout(self)

        # Only display the no-result message if resultlist is empty
        if len(resultlist) == 0:
            self.retranslate(all=False)
            self.onNoResult()
            return

        # The proxy model is used for sort and filter support
        self.proxymodel = QSortFilterProxyModel(self)
        self.proxymodel.setDynamicSortFilter(True)

        self.headerdata = ['dn']
        self.headerdata.extend(attributes)
        self.resultdata = resultlist

        # FIXME: should we create a custom item model ?
        self.model = QStandardItemModel(0, len(self.headerdata), parent=self)
        #self.model = ResultItemModel(self)
        #self.model = ResultItemModel(self.headerdata, self.resultdata, self)
        self.proxymodel.setSourceModel(self.model)

        self.resultview = QTreeView(self)
        self.resultview.setUniformRowHeights(True)
        self.resultview.setRootIsDecorated(False)
        self.resultview.setAlternatingRowColors(True)
        self.resultview.setSortingEnabled(True)

        self.resultview.setModel(self.proxymodel)

        # For right-click context menu
        self.resultview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.resultview.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.layout.addWidget(self.resultview)
        # The filter box enables the user to filter the returned search
        # results. It becomes accessible with Ctrl-F (QKeySequence.Find)
        self.filterBox = ResultFilterWidget(self.headerdata, parent=self)
        self.filterBox.setVisible(False)

        self.layout.addWidget(self.filterBox)

        # We need to call the retranslate method before populating
        # the result data
        self.retranslate()
        #self.model.populateHeader(self.headerdata)
        #self.model.populateModel(self.resultdata)
        self.setHeaderData(self.headerdata)
        self.setResultData(self.resultdata)
        self.resultview.resizeColumnToContents(0)
        self.__createContextMenu()
        self.__connectSlots()

    def __connectSlots(self):
        """Connect signal and slots.
        """
        self.resultview.customContextMenuRequested.connect(
            self.onContextMenuRequested)
        self.filterBox.inputEdit.textChanged['QString'].connect(
            self.onFilterInputChanged)
        self.filterBox.columnBox.currentIndexChanged[int].connect(
            self.onFilterColumnChanged)

    def __getVSpacer(self):
        return QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                 QtGui.QSizePolicy.Minimum)

    def __createContextMenu(self):
        """Display the context menu.
        """
        self.contextMenu = QtGui.QMenu()
        self.contextMenuView = QtGui.QAction(self)
        self.contextMenuDelete = QtGui.QAction(self)
        self.contextMenuExport = QtGui.QAction(self)
        self.contextMenu.addAction(self.contextMenuView)
        self.contextMenu.addAction(self.contextMenuDelete)
        self.contextMenu.addAction(self.contextMenuExport)

        # Connect the context menu actions to the correct slots
        self.contextMenuView.triggered.connect(self.onViewItemsSelected)
        self.contextMenuDelete.triggered.connect(self.onDeleteItemsSelected)
        self.contextMenuExport.triggered.connect(self.onExportItemsSelected)

    def onNoResult(self):
        """Adds a styled *no result* message to the main layout.
        """
        font = QtGui.QFont()
        font.setBold(True)
        sadface = QtGui.QLabel(self)
        sadface.setPixmap(pixmapFromTheme('face-sad', ':/icons/48/face-sad'))
        noresult = QtGui.QLabel(self)
        noresult.setText(self.str_NO_RESULT)
        noresult.setFont(font)
        hlayout = QtGui.QHBoxLayout()
        hlayout.addItem(self.__getVSpacer())
        hlayout.addWidget(sadface)
        hlayout.addWidget(noresult)
        hlayout.addItem(self.__getVSpacer())

        self.layout.addLayout(hlayout)

    def setHeaderData(self, data=[]):
        """Populates the ``resultview`` model with header data.

        Parameters:

        - `data`: a list with header items. Usually this is the
          attributelist from the LDAP search.
        """
        i = 0
        for header in data:
            self.model.setHeaderData(i, QtCore.Qt.Horizontal, header)
            i += 1

    def setResultData(self, data=[]):
        """Populates the ``resultview`` model with result data.

        Parameters:

        - `data`: a list containing the SmartDataObjects representing
          items in the LDAP search result.
        """
        row = 0
        for obj in data:
            self.model.insertRow(row)
            col = 0
            for attr in self.headerdata:
                if self.isDistinguishedName(attr):
                    modelData = obj.getPrettyDN()
                elif self.isObjectClass(attr):
                    modelData = ','.join(obj.getObjectClasses())
                elif obj.hasAttribute(attr):
                    if obj.isAttributeBinary(attr):
                        modelData = self.str_BINARY_DATA
                    else:
                        modelData = ','.join(obj.getAttributeValueList(attr))

                self.model.setData(self.model.index(row, col), modelData)
                col += 1

            row += 1

    def isDistinguishedName(self, attr):
        """Returns ``True`` if `attr` is a distinguished name,
        ``False`` otherwise.

        Parameters:

        - `attr`: the LDAP string attribute value to check.
        """
        return attr.lower() == 'dn'

    def isObjectClass(self, attr):
        """Returns ``True`` if `attr` is an object class, ``False``
        otherwise.

        Parameters:

        - `attr`: the LDAP string attribute value to check.
        """
        return attr.lower() == 'objectclass'

    def onContextMenuRequested(self, point):
        """Display the context menu
        """

        # FIXME: In order to be able to export, delete and view search
        # result entries. We should make use of the various dialogs in
        # the Browser plugin. Unitl we have refactored the design in a
        # way that allow us to use these without accessing the browser
        # modules, we simple don't provide these options yet.
        return

        self.selection = self.resultview.selectedIndexes()

        deleteSupport = True
        exportSupport = True

        rowsselected = len(self.selection) / len(self.headerdata)

        if not rowsselected > 0:
            self.contextMenu.setEnabled(False)
            self.contextMenu.exec_(self.resultview.mapToGlobal(point))
            return

        self.contextMenu.setEnabled(True)
        # Look over at Browser plugin for implementation of
        # multiselect and operation support validation
        print rowsselected

        self.contextMenuView.setEnabled(True)
        if rowsselected == 1:
            self.contextMenuView.setText(self.str_VIEW_ITEM)
        else:
            self.contextMenuView.setText(self.str_VIEW_ITEMS)

        if deleteSupport:
            self.contextMenuDelete.setEnabled(True)
            if rowsselected == 1:
                self.contextMenuDelete.setText(self.str_DELETE_ITEM)
            else:
                self.contextMenuDelete.setText(self.str_DELETE_ITEMS)

        if exportSupport:
            self.contextMenuExport.setEnabled(True)
            if rowsselected == 1:
                self.contextMenuExport.setText(self.str_EXPORT_ITEM)
            else:
                self.contextMenuExport.setText(self.str_EXPORT_ITEMS)

        # Finally we execute the context menu
        self.contextMenu.exec_(self.resultview.mapToGlobal(point))

    def onViewItemsSelected(self):
        """Slot for the *view* context menu action.
        """
        raise NotImplementedError(
            'Need to implement a proper model for this to be supported')

    def onDeleteItemsSelected(self):
        """Slot for the *delete* context menu action.
        """
        msg = 'Delete from the Search Plugin is not implemented jet.'
        dialog = DeleteDialog(self, msg)
        dialog.setDeleteItems([])
        dialog.exec_()

    def onExportItemsSelected(self):
        """Slot for the 'export' context menu action.
        """
        msg = 'Export from the Search Plugin is not implemented jet.'
        dialog = ExportDialog(self, msg)
        # Only for proof of concept
        dialog.setExportData([])
        dialog.exec_()

    def onFilterBoxVisibilityChanged(self, visible):
        """Slot for the QKeySequence.Find.

        - `visible`: a boolean value indicating wether or not to toggle
          the filter box widget visibility on or off.
        """
        if visible:
            self.filterBox.setVisible(True)
            self.filterBox.inputEdit.setFocus()
        else:
            # I belive it's common practise to clear the filter when
            # the filter box is closed. This is at least the way the
            # filter boxes works for most webbrowsers.
            self.filterBox.inputEdit.clear()
            self.filterBox.setVisible(False)
            self.resultview.setFocus()

    def onFilterInputChanged(self, filter=''):
        """Slot for the filter input in the result filter widget.

        We get the selected syntax from the syntax combobox
        """
        # The PyQt4 QVariant is causing some problems here, when we try
        # to use the <combobox>.itemData directly, even though the data
        # holds valid QRexExp.PatternSyntax values.
        # We therefore need to explicitly make the QVariant and integer.
        i = self.filterBox.syntaxBox.currentIndex()
        syntaxIndex = self.filterBox.syntaxBox.itemData(i).toInt()[0]
        syntax = QtCore.QRegExp.PatternSyntax(syntaxIndex)
        # As of now we do filtering in a case insensitive way, until we
        # come up with a way to introduce case sensitivity selection in a
        # UI inexpensive way. We want to keep the filter widget as clean
        # and simple as possible.
        regex = QtCore.QRegExp(filter, QtCore.Qt.CaseInsensitive, syntax)
        self.proxymodel.setFilterRegExp(regex)

    def onFilterColumnChanged(self, index):
        """Slot for the column combobox in the filter box widget.
        """
        self.proxymodel.setFilterKeyColumn(index)

    def retranslate(self, all=True):
        """For dynamic translation support.
        """
        self.str_VIEW_ITEM = QtGui.QApplication.translate(
            'ResultView', 'View Item')
        self.str_VIEW_ITEMS = QtGui.QApplication.translate(
            'ResultView', 'View Items')
        self.str_DELETE_ITEM = QtGui.QApplication.translate(
            'ResultView', 'Delete Item')
        self.str_DELETE_ITEMS = QtGui.QApplication.translate(
            'ResultView', 'Delete Items')
        self.str_EXPORT_ITEM = QtGui.QApplication.translate(
            'ResultView', 'Export Item')
        self.str_EXPORT_ITEMS = QtGui.QApplication.translate(
            'ResultView', 'Export Items')
        self.str_NO_RESULT = QtGui.QApplication.translate(
            'ResultView', 'Sorry, no result to display!')
        self.str_BINARY_DATA = QtGui.QApplication.translate(
            'ResultView', 'Binary Data')
        if all:
            self.filterBox.retranslate()


class ResultFilterWidget(QWidget):
    """A Widget for basic filter input on a result view.

    This class provide a simple and clean filter widget, enabling the
    user to filter the returned results. It provide several filter
    syntax potions, a column selector and a filter input widget.

    I aims at beeing simple, small and out of the way.
    """

    syntaxOptions = {
        'Fixed String': QtCore.QRegExp.FixedString,
        'Regular Expression': QtCore.QRegExp.RegExp,
        'Wildcard': QtCore.QRegExp.Wildcard,
    }

    def __init__(self, columns=[], parent=None):
        """
        Parameters:
        - `columns`: a list containing the columns to populate the
          column selector. Usually the main model headerdata (search
          attributelist).
        """
        super(ResultFilterWidget, self).__init__(parent)

        self.layout = QtGui.QHBoxLayout(self)
        self.syntaxBox = QtGui.QComboBox(self)
        self.columnBox = QtGui.QComboBox(self)
        self.inputEdit = QtGui.QLineEdit(self)

        spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Minimum)

        for text, syntax in sorted(self.syntaxOptions.iteritems()):
            self.syntaxBox.addItem(text, userData=syntax)

        self.columnBox.addItems(columns)

        self.layout.addItem(spacer)
        self.layout.addWidget(self.syntaxBox)
        self.layout.addWidget(self.columnBox)
        self.layout.addWidget(self.inputEdit)

        self.retranslate()

    def retranslate(self):
        """For dynamic translation support.
        """
        self.syntaxBox.setToolTip(QtGui.QApplication.translate(
            'ResultFilterWidget', 'Choose filter syntax.'))
        self.columnBox.setToolTip(QtGui.QApplication.translate(
            'ResultFilterWidget', 'Choose filter column.'))


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
