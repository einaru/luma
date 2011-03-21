# -*- coding: utf-8 -*-
#
# base.gui.Dialog
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#     Christian Forfang, <cforfang@gmail.com>
#     Simen Natvig, <simen.natvig@gmail.com>
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
This module contains Luma dialog widgets:

SettingsDialog:
    The settings dialog provide configuration options to the user.

ServerDialog:
    A dialog for managing the serverlist and various server settings

AboutDialog:
    A simple application information dialog.
"""
import copy
import logging

from PyQt4.QtCore import QModelIndex

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog, QDataWidgetMapper
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QInputDialog, QItemSelectionModel
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPixmap

from .ServerDelegate import ServerDelegate
from ..backend.ServerObject import ServerObject
from ..gui.Settings import Settings
from ..gui.AboutDialogDesign import Ui_AboutDialog
from ..gui.AboutLicenseDesign import Ui_AboutLicense
from ..gui.AboutCreditsDesign import Ui_AboutCredits
from ..gui.EinarServerDialogDesign import Ui_ServerDialogDesign
from ..gui.SettingsDialogDesign import Ui_SettingsDialog
from ..model.PluginSettingsModel import PluginSettingsModel
from ..model.ServerListModel import ServerListModel
from ..util.i18n import LanguageHandler
from ..util.IconTheme import iconFromTheme, pixmapFromThemeIcon


class ServerDialog(QDialog, Ui_ServerDialogDesign):

    def __init__(self, serverList, parent=None):
        """ Note:
        the input-ServerList-object is used directly by both the methods
        here and the model so beware of changes to it. It's probably not
        a good idea to pass a ServerList if one of its ServerObjects are
        in use.
        """
        super(ServerDialog, self).__init__(parent)
        self.setupUi(self)

        self.networkIcon.setPixmap(pixmapFromThemeIcon('network-server', ':/icons/network-server'))
        self.authIcon.setPixmap(pixmapFromThemeIcon('dialog-password', ':/icons/passwordmedium'))
        self.securityIcon.setPixmap(pixmapFromThemeIcon('preferences-system', ':/icons/config'))


        self.__serverList = copy.deepcopy(serverList)
        self.__serverListCopy = None
        self.__returnList = None

        # Create the model used by the views
        self.slm = ServerListModel(self.__serverList)

        # Add the model to the list of servers
        self.serverListView.setModel(self.slm)

        # Enable/disable editing depending on if we have a server to edit
        if self.slm.rowCount(QModelIndex()) > 0:
            self.tabWidget.setEnabled(True)
        else:
            self.tabWidget.setEnabled(False)

        self.splitter.setStretchFactor(0, 1)

        # Select the first server in the model)
        index = self.serverListView.model().index(0, 0)
        # Select it in the view
        self.serverListView.selectionModel().select(index, QItemSelectionModel.ClearAndSelect)
        self.serverListView.selectionModel().setCurrentIndex(index, QItemSelectionModel.ClearAndSelect)

        self.serverListView.selectionModel().selectionChanged.connect(self.setBaseDN)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.slm)
        self.serverDelegate = ServerDelegate()
        self.mapper.setItemDelegate(self.serverDelegate)

        # Map columns of the table to fields in the gui
        self.mapper.addMapping(self.hostEdit, 1)
        self.mapper.addMapping(self.portSpinBox, 2)
        self.mapper.addMapping(self.bindAnonBox, 3)
        self.mapper.addMapping(self.baseDNBox, 4)
        self.mapper.addMapping(self.baseDNListWidget, 5)
        self.mapper.addMapping(self.bindAsEdit, 6)
        self.mapper.addMapping(self.passwordEdit, 7)
        self.mapper.addMapping(self.encryptionBox, 8)
        self.mapper.addMapping(self.mechanismBox, 9)
        self.mapper.addMapping(self.aliasBox, 10)
        self.mapper.addMapping(self.useClientCertBox, 11)
        self.mapper.addMapping(self.certFileEdit, 12)
        self.mapper.addMapping(self.certKeyfileEdit, 13)
        self.mapper.addMapping(self.validateBox, 14)

        # Select the first servers (as the serverlistview does)
        self.mapper.setCurrentIndex(0)

        # Let the mapper know when another server is selected in the list
        self.serverListView.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex)

        # Workaround to avoid the button stealing the focus from the 
        # baseDNView thus invalidating it's selection maning we don't
        # know what do delete
        #self.deleteBaseDNButton.setFocusPolicy(Qt.NoFocus)
        self.setBaseDN()

        self.UNSAVED_STATE = False

    def addBaseDN(self):
        """ Slot for adding a base DN
        """
        tmpBase = unicode(self.baseDNEdit.text()).strip()

        if tmpBase == u'':
            return

        self.baseDNListWidget.addItem(QListWidgetItem(tmpBase))

        serverIndex = self.serverListView.selectedIndexes()
        index = self.slm.createIndex(serverIndex[0].row(), 5)
        self.serverDelegate.setModelData(self.baseDNListWidget, self.slm, index)

        self.baseDNEdit.clear()
        # Force push to model
        self.mapper.submit()

    def deleteBaseDN(self):
        """ Slot for deleting a base DN
        """
        # Delete every selected base DN
        for tmpItem in self.baseDNListWidget.selectedItems():
            if not (None == tmpItem):
                # We first get the index of the base DN, and then we
                # delete (or actually steal) the baseDN from the list
                # As per the Qt docs, someone also needs to delete it:
                # http://doc.qt.nokia.com/4.7-snapshot/qlistwidget.html#takeItem
                index = self.baseDNListWidget.indexFromItem(tmpItem)
                d = self.baseDNListWidget.takeItem(index.row())
                if d != 0:
                    del d

        serverIndex = self.serverListView.selectedIndexes()
        index = self.slm.createIndex(serverIndex[0].row(), 5)
        self.serverDelegate.setModelData(self.baseDNListWidget, self.slm, index)
        self.mapper.submit() #Force push changes to model

    def setBaseDN(self):
        """ Slot for setting the base DN.
        """
        serverIndex = self.serverListView.selectedIndexes()
        if len(serverIndex) > 0:
            index = self.slm.createIndex(serverIndex[0].row(), 5)
            self.serverDelegate.setEditorData(self.baseDNListWidget, index)

    def addServer(self):
        """ Create a new ServerObject and add it to the model, and thus
        the server list.
        """
        name, ok = QInputDialog.getText(self, 'Add server', 'Name:')
        if ok:
            if len(name) < 1 or self.__serverList.getServerObject(name) != None:
                QMessageBox.information(self, 'Error', 'Invalid name or already used.')
                return

            sO = ServerObject()
            sO.name = unicode(name)

            # Insert into the model
            m = self.serverListView.model()
            m.beginInsertRows(QModelIndex(), m.rowCount(QModelIndex()), m.rowCount(QModelIndex()) + 1)
            self.__serverList.addServer(sO)
            m.endInsertRows()

            # Get the index of the newly added server, make sure it is
            # selected and marked as current
            s = m.index(m.rowCount(QModelIndex) - 1, 0)
            self.serverListView.selectionModel().select(s, QItemSelectionModel.ClearAndSelect)
            self.serverListView.selectionModel().setCurrentIndex(s, QItemSelectionModel.ClearAndSelect)

            # Update the mapper
            self.mapper.setCurrentIndex(s.row())

            # Make sure editing is enabled
            self.tabWidget.setEnabled(True)

    def deleteServer(self):
        """ Delete a server from the model/list
        """
        if self.serverListView.selectionModel().currentIndex().row() < 0:
            # Return if no server is selected
            return

        re = QMessageBox.question(self, 'Delete', 'Are you sure?', QMessageBox.Yes, QMessageBox.No)
        if re == QMessageBox.Yes:
            # Get the index of the currently selected server
            index = self.serverListView.selectionModel().currentIndex()

            # Delete the server
            self.serverListView.model().beginRemoveRows(QModelIndex(), index.row(), index.row())
            self.serverListView.model().removeRows(index.row(), 1)
            self.serverListView.model().endRemoveRows()

            # When deleting, the view gets updated and selects a new current.
            # Get it and give it to the mapper
            newIndex = self.serverListView.selectionModel().currentIndex()
            self.mapper.setCurrentIndex(newIndex.row())

        if self.slm.rowCount(QModelIndex()) == 0:
            # Disable editing if no servers left
            self.tabWidget.setEnabled(False)


    def saveServerlist(self):
        """ Called when the Save-button is clicked.
        
        What should happen when the user clicks Save then Cancel?
        """
        self.__serverList.writeServerList()
        self.__serverListCopy = copy.deepcopy(self.__serverList)

    def reject(self):
        """ Called when the users clicks cancel or presses escape
        
        TODO: SOMETHING LOGICAL SHOULD PROBABLY BE DONE HERE
        """
        r = QMessageBox.question(self, 'Exit?', 'Are you sure you want to exit the server editor?\n Any unsaved changes will be lost!', QMessageBox.Ok | QMessageBox.Cancel)
        if not r == QMessageBox.Ok:
            return
        if self.__serverListCopy:
            self.__returnList = self.__serverListCopy
            QDialog.accept(self)
            return
        QDialog.reject(self)

    def accept(self):
        """ Called when OK-button is clicked
        
        TODO: SOMETHING LOGICAL SHOULD PROBABLY BE DONE HERE
        """
        self.__serverList.writeServerList()
        self.__returnList = self.__serverList
        QDialog.accept(self)

    def getResult(self):
        return self.__returnList

    def certFileDialog(self):
        certFile = QFileDialog.getOpenFileName(self, self.trUtf8('Select certificate file'), '')

        if not certFile is None:
            self.certFileEdit.setText(certFile)
            self.mapper.submit()

    def certKeyfileDialog(self):
        certKeyfile = QFileDialog.getOpenFileName(self, self.trUtf8('Select certificate keyfile'), '')

        if not certKeyfile is None:
            self.certKeyfileEdit.setText(certKeyfile)
            self.mapper.submit()


class SettingsDialog(QDialog, Ui_SettingsDialog):
    """ The application settings dialog
    
    Contains all the application settings.
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, currentLanguage, languages={}, parent=None):
        """ The constructor must be given the currentLanguage from the
        Main window to keep things synchronized.
        
        @param currentLanguage: string;
            the iso code for the current selected application language
        
        @param languages: dictionary;
            This should be a dictionary with iso codes and language
            names for available languages. NOTE: Might want to provide
            this from the main window as it's already loaded.
        """
        super(SettingsDialog, self).__init__(parent)

        self.setupUi(self)
        self.languages = languages
        self.currentLanguage = currentLanguage
        if self.currentLanguage == {}:
            """ If the list of languages is empty we fetch the list
            with the LanguageHelper. """
            lh = LanguageHandler()
            self.currentLanguage = lh.availableLanguages
        self.loadSettings()

    def loadSettings(self):
        """ Loads the application settings from file.
        """
        settings = Settings()

        # Logging
        self.showLoggerOnStart.setChecked(settings.showLoggerOnStart)
        self.showErrors.setChecked(settings.showErrors)
        self.showDebug.setChecked(settings.showDebug)
        self.showInfo.setChecked(settings.showInfo)

        # Language
        self.languageSelector
        i = 0
        for key, name in self.languages.iteritems():
            self.languageSelector.addItem('%s [%s]' % (name[0], key), key)
            if key == self.currentLanguage:
                self.languageSelector.setCurrentIndex(i)
            i = i + 1

        # Plugins
        self.pluginListView.setModel(PluginSettingsModel())

    def pluginSelected(self, index):
        """ If a plugin has a pluginsettingswidget, it will be put into
        the QStackedWidget.
        """

        plugin = self.pluginListView.model().itemFromIndex(index).plugin

        widget = plugin.getPluginSettingsWidget(self.pluginSettingsStack)

        if not widget:
            return

        if self.pluginSettingsStack.indexOf(widget) == -1:
            self.pluginSettingsStack.addWidget(widget)

        if self.pluginSettingsStack.currentWidget() != widget:
            self.pluginSettingsStack.setCurrentWidget(widget)

    def saveSettings(self):
        """
        This slot is called when the ok button is clicked. It saves the
        selected settigns to file.
        """
        settings = Settings()

        # Logging
        settings.showLoggerOnStart = self.showLoggerOnStart.isChecked()
        settings.showErrors = self.showErrors.isChecked()
        settings.showDebug = self.showDebug.isChecked()
        settings.showInfo = self.showInfo.isChecked()

        # Language
        i = self.languageSelector.currentIndex()
        settings.language = self.languageSelector.itemData(i).toString()

        # Plugins
        self.pluginListView.model().saveSettings()

        QDialog.accept(self)

    def cancelSettings(self):
        self.loadSettings()
        QDialog.reject(self)


class AboutDialog(QDialog, Ui_AboutDialog):
    """ A simple about dialog.
    
    It includes basic application information, a short outline of the
    application license, and of course credit is given where credit is
    due.
    """

    def __init__(self, parent=None):

        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(iconFromTheme('help-about', ':/icons/about'))
        self.logo.setPixmap(QPixmap(':/icons/luma-64'))
        version = QApplication.applicationVersion() 
        self.nameAndVersion.setText(u'Luma %s' % version)

    def showLicense(self):
        """
        Displays a simple dialog containing the application license
        """
        license = QDialog()
        Ui_AboutLicense().setupUi(license)
        license.exec_()

    def giveCreditWhereCreditIsDue(self):
        """
        Displays a simple dialog containing developer information, and
        credit is given where credit is due
        """
        credits = QDialog()
        Ui_AboutCredits().setupUi(credits)
        credits.exec_ ()
