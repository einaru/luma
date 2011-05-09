# -*- coding: utf-8 -*-
#
# base.gui.Dialog
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
"""
This module contains various dialogs that can be used by plugins
for performing various LDAP related tasks.
"""
import logging
import StringIO
from string import replace

import dsml

from PyQt4 import QtCore, QtGui

from .design.ExportDialogDesign import Ui_ExportDialog
from ..util import encodeUTF8
from ..util.IconTheme import pixmapFromTheme, iconFromTheme
from ..util.Paths import getUserHomeDir


class ExportDialog(QtGui.QDialog, Ui_ExportDialog):
    """Dialog for exporting a selection of LDAP entries to disk.

    TODO: better feedback if something goes wrong, perhaps not accept(), if
          not all checked items get exported ?
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, parent=None, msg=''):
        """
        :param items: the list of items to export.
        :type items: list
        :param msg: a message to display in the dialog. Might be
         information about problems with fetching all the LDAP
         entries, etc.
        :type msg: string
        """
        super(ExportDialog, self).__init__(parent)
        self.setupUi(self)

        self.iconLabel.setPixmap(pixmapFromTheme(
            'document-save', ':/icons/32/document-save'))
        self.fileButton.setIcon(iconFromTheme(
            'document-open', ':/icons/32/document-save'))
        self.messageLabel.setText(msg)

        self.model = QtGui.QStandardItemModel()
        self.exportItemView.setModel(self.model)
        self.exportItemView.setAlternatingRowColors(True)
        self.exportItemView.setUniformItemSizes(True)
        self.exportDict = {}

        # Disabled until path set
        self.exportButton.setEnabled(False)

        self.__connectSlots()

    def __connectSlots(self):
        """Connect signal and slots.
        """
        # If the users manually edits the path, we'll trust him
        #self.outputEdit.textEdited.connect(self.enableExport)
        # The signal textEdit is not emitted if the text is changed
        # programmatically, we therefore use textChanged instead.
        self.outputEdit.textChanged['QString'].connect(self.onFilenameChanged)

    def __writeLDIF(self, file):
        """Write the export list to LDIF format.
        """
        with open(file, 'w') as f:
            for x in self.exportList:
                try:
                    f.write(x.convertToLdif())
                except IOError, e:
                    msg = 'Could not export {0}. Reason\n{1}'
                    self.__logger.error(msg.format((str(x), str(e))))

    def __writeDSMl(self, file):
        """Write the export list to DSML format.
        """
        with open(file, 'w') as f:
            # DSML need some header info.
            header = StringIO.StringIO()
            dsmlWriter = dsml.DSMLWriter(header)
            dsmlWriter.writeHeader()
            f.write(header.getvalue())
            header.close()

            # Write the actuall export entries
            for x in self.exportList:
                try:
                    f.write(x.convertToDsml())
                except IOError, e:
                    msg = 'Could not export {0}. Reason\n{1}'
                    self.__logger.error(msg.format((str(x), str(e))))

            # DSML need additional footer info, to close the format
            footer = StringIO.StringIO()
            dsmlWriter = dsml.DSMLWriter(footer)
            dsmlWriter.writeFooter()
            f.write(footer.getvalue())
            footer.close()

    def enableExport(self):
        """Enable the export-button.
        """
        self.exportButton.setEnabled(True)

    def setExportItems(self, data):
        """Sets the items to be exported, and populates the model.

        :param data: the data to be exported.
        :type data: list
        """
        self.data = data
        for item in self.data:
            prettyDN = item.getPrettyDN()
            modelItem = QtGui.QStandardItem(prettyDN)
            modelItem.setEditable(False)
            modelItem.setCheckable(True)

            self.exportDict[prettyDN] = [item, modelItem]
            modelItem.setCheckState(QtCore.Qt.Checked)
            self.model.appendRow(modelItem)

    def openFileDialog(self):
        """Slot for the file button.

        Opens a File Dialog to let the user choose where to export.
        """
        userdir = getUserHomeDir()
        ldifFilter = 'LDIF files (*ldif)'
        dsmlFilter = 'DSML files (*dsml)'
        filter = "{0};;{1}"
        if self.formatBox.currentIndex() == 0:
            filter = filter.format(ldifFilter, dsmlFilter)
        else:
            filter = filter.format(dsmlFilter, ldifFilter)

        opt = dict(caption='Select export File',
                   directory=userdir,
                   filter=filter)

        filename = QtGui.QFileDialog.getSaveFileName(self, **opt)
        # Return if the user canceled the dialog
        if filename == "":
            return

        filename = encodeUTF8(filename, strip=True)
        filter = encodeUTF8(self.formatBox.currentText(), strip=True)
        if filter.startswith('LDIF') and not filename.endswith('.ldif'):
            filename = '{0}.ldif'.format(filename)
        elif filter.startswith('DSML') and not filename.endswith('.dsml'):
            filename = '{0}.dsml'.format(filename)

        self.outputEdit.setText(filename)
        #self.exportButton.setEnabled(True)

    def onFormatChanged(self, format):
        """Slot for the format combobox.

        Checks if the output file is defined and wether its filending
        matches the choosen export format. If not defined the method
        returns. If the filening doesn't match, it is switched.
        """
        if self.outputEdit.text() == '':
            return

        format = encodeUTF8(format, strip=True)
        oldname = self.outputEdit.text()

        if format == 'LDIF':
            newname = replace(oldname, '.dsml', '.ldif')
        elif format == 'DSML':
            newname = replace(oldname, '.ldif', '.dsml')

        self.outputEdit.setText(newname)

    def onFilenameChanged(self, filename):
        """Slot for the filename edit.

        Enabels|disables the export button.
        """
        if encodeUTF8(filename, strip=True) == '':
            self.exportButton.setEnabled(False)
        else:
            self.exportButton.setEnabled(True)

    def export(self):
        """Slot for the export button.

        Exports all checked items to the file defined in the outputEdit
        widget.
        """
        # Iterate through the modelitems and remove unchekced items
        # from the export dictionary, which will be used later.
        for i in xrange(self.model.rowCount()):
            item = self.model.itemFromIndex(self.model.index(i, 0))
            if item.checkState() != QtCore.Qt.Checked:
                del self.exportDict[encodeUTF8(item.text(), strip=True)]

        # Map the dictionary keys
        self.exportList = map(lambda x: self.exportDict[x][0],
                                        self.exportDict.keys())
        self.exportList.sort()
        try:
            file = self.outputEdit.text()
            format = encodeUTF8(self.formatBox.currentText(), strip=True)

            if format == 'LDIF':
                self.__writeLDIF(file)
            elif format == 'DSML':
                self.__writeDSMl(file)
            else:
                msg = 'Format: {0} is unsupported.'.format(format)
                self.__logger.debug(msg)

        except IOError, e:
            msg = 'Problems writing to {0}. Reason:\n{1}'.format(file, str(e))
            self.__logger.error(msg)

        # TODO: implpement some sort of feedback to the user upon
        #       finishing an export session.
        self.accept()

    def cancel(self):
        """Slot for the cancel button.
        """
        del self.exportDict
        self.reject()


class DeleteDialog(QtGui.QDialog):
    """Dialog for deleting a selection of LDAP entries.
    """
    def __init__(self, parnet=None):
        raise NotImplementedError(
            'Implement this dialog (move from Brower plugin).')


class BrowseDialog(QtGui.QDialog):
    """Dialog for browsing a spesific LDAP entry.
    """
    def __init__(self, parnet=None):
        raise NotImplementedError(
            'Implemnt this dialog (steal from Browser plugin)')


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
