# -*- coding: utf-8 -*-
#
# base.gui.Dialog
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einar.uvslokk@linux.com>
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

from PyQt4 import QtCore
from PyQt4.QtCore import QModelIndex

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
from ..gui.ServerDialogDesignNew import Ui_ServerDialogDesign
from ..gui.SettingsDialogDesign import Ui_SettingsDialog
from ..model.PluginSettingsModel import PluginSettingsModel
from ..model.ServerListModel import ServerListModel
from ..util.i18n import LanguageHandler
from ..util.icontheme import iconFromTheme, pixmapFromThemeIcon


class SettingsDialog(QDialog, Ui_SettingsDialog):
    """
    The application settings dialog
    
    Contains all the application settings.
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, currentLanguage, languages={}, parent=None):
        """
        The constructor must be given the currentLanguage from the
        Main window to keep things synchronized.
        
        @param currentLanguage: string;
            the iso code for the currently selected application language
        
        @param languages: dictionary;
            This should be a dictionary with iso codes and language names
            for available languages. NOTE: Might want to provide this from
            the main window as it's already loaded.
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
        """
        Loads the application settings from file.
        """
        settings = Settings()

        """ Logging """
        self.showLoggerOnStart.setChecked(settings.showLoggerOnStart)
        self.showErrors.setChecked(settings.showErrors)
        self.showDebug.setChecked(settings.showDebug)
        self.showInfo.setChecked(settings.showInfo)

        """ Language """
        self.languageSelector
        i = 0
        for key, name in self.languages.iteritems():
            self.languageSelector.addItem('%s [%s]' % (name[0], key), key)
            if key == self.currentLanguage:
                self.languageSelector.setCurrentIndex(i)
            i = i + 1

        """ Plugins """
        self.pluginListView.setModel(PluginSettingsModel())

    def pluginSelected(self, index):
        """
        If a plugin has a pluginsettingswidget,
        it will be put into the QStackedWidget.
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
        This slot is called when the ok button is clicked.
        It saves the selected settigns to file.
        """
        settings = Settings()

        """ Logging """
        settings.showLoggerOnStart = self.showLoggerOnStart.isChecked()
        settings.showErrors = self.showErrors.isChecked()
        settings.showDebug = self.showDebug.isChecked()
        settings.showInfo = self.showInfo.isChecked()

        """ Language """
        i = self.languageSelector.currentIndex()
        settings.language = self.languageSelector.itemData(i).toString()

        """ Plugins """
        self.pluginListView.model().saveSettings()

        QDialog.accept(self)

    def cancelSettings(self):
        self.loadSettings()
        QDialog.reject(self)


class ServerDialog(QDialog, Ui_ServerDialogDesign):

    def __init__(self, serverList, parent=None):
        """
        Note:
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
        self._serverListCopy = None
        self._returnList = None

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

        self.connect(self.serverListView.selectionModel(), QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'), self.setBaseDN)

        # Map columns of the model to fields in the gui
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.slm)
        # Handles the comboboxes and to-from the list of custom baseDNs
        self.serverDelegate = ServerDelegate()
        self.mapper.setItemDelegate(self.serverDelegate)

        self.mapper.addMapping(self.hostLineEdit, 1)
        self.mapper.addMapping(self.portSpinBox, 2)
        self.mapper.addMapping(self.anonBindBox, 3)
        self.mapper.addMapping(self.baseDNBox, 4)
        #self.mapper.addMapping(self.baseDNWidget, 5)

        self.mapper.addMapping(self.bindAsLineEdit, 6)
        self.mapper.addMapping(self.passwordLineEdit, 7)
        self.mapper.addMapping(self.encryptionBox, 8)
        self.mapper.addMapping(self.mechanismBox, 9)
        self.mapper.addMapping(self.aliasBox, 10)
        self.mapper.addMapping(self.useClientCertBox, 11)
        self.mapper.addMapping(self.certFileLineEdit, 12)
        self.mapper.addMapping(self.certKeyfileLineEdit, 13)
        self.mapper.addMapping(self.serverCertBox, 14)

        # Select the first servers (as the serverlistview does)
        self.mapper.setCurrentIndex(0)

        # Let the mapper know when another server is selected in the list
        self.serverListView.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex)

        # Workaround to avoid the button stealing the focus from the baseDNView thus invalidating it's selection
        # maning we don't know what do delete
        #self.deleteBaseDNButton.setFocusPolicy(Qt.NoFocus)
        self.setBaseDN()
        self.UNSAVED_STATE = False

    def addBaseDN(self):
        tmpBase = unicode(self.baseDNLineEdit.text()).strip()
        if tmpBase == u'':
            return
        self.baseDNWidget.addItem(QListWidgetItem(tmpBase)) #Add to list

        serverIndex = self.serverListView.selectedIndexes()
        index = self.slm.createIndex(serverIndex[0].row(), 5)
        self.serverDelegate.setModelData(self.baseDNWidget, self.slm, index)
        self.baseDNLineEdit.clear() #Clear textfield
        self.mapper.submit() #Force push to model
        self.UNSAVED_STATE = True
        print self.UNSAVED_STATE

    def deleteBaseDN(self):
        # Delete every selected baseDN
        for tmpItem in self.baseDNWidget.selectedItems():
            if not (None == tmpItem):
                # get the index to the basedn
                index = self.baseDNWidget.indexFromItem(tmpItem)
                # delete (actually steal) the baseDN from the list
                d = self.baseDNWidget.takeItem(index.row())
                if d != 0:
                    del d # Per the QT-docs, someone needs to delete it

        serverIndex = self.serverListView.selectedIndexes()
        index = self.slm.createIndex(serverIndex[0].row(), 5)
        self.serverDelegate.setModelData(self.baseDNWidget, self.slm, index)
        self.mapper.submit() # Force push changes to model
        self.UNSAVED_STATE = True

    def setBaseDN(self):
        serverIndex = self.serverListView.selectedIndexes()
        if len(serverIndex) > 0:
            index = self.slm.createIndex(serverIndex[0].row(), 5)
            self.serverDelegate.setEditorData(self.baseDNWidget, index)

    def addServer(self):
        """
        Create a new ServerObject and add it to the model (thus the list)
        """
        name, ok = QInputDialog.getText(self, self.trUtf8('Add server'), 
                                        self.trUtf8('Name:'))
        if ok:
            if len(name) < 1 or self.__serverList.getServerObject(name) != None:
                QMessageBox.information(self, self.trUtf8('Error'), 
                                self.trUtf8('Invalid name or already used.'))
                return

            sO = ServerObject()
            sO.name = unicode(name)

            # Insert into the model
            m = self.serverListView.model()
            m.beginInsertRows(QModelIndex(), m.rowCount(QModelIndex()), m.rowCount(QModelIndex()) + 1)
            self.__serverList.addServer(sO)
            m.endInsertRows()

            s = m.index(m.rowCount(QModelIndex) - 1, 0) #Index of the newly added server
            self.serverListView.selectionModel().select(s, QItemSelectionModel.ClearAndSelect) #Select it
            self.serverListView.selectionModel().setCurrentIndex(s, QItemSelectionModel.ClearAndSelect) #Mark it as current      
            self.mapper.setCurrentIndex(s.row()) # Update the mapper
            self.tabWidget.setEnabled(True) # Make sure editing is enabled
            self.UNSAVED_STATE = True

    def deleteServer(self):
        """
        Delete a server from the model/list
        """
        if self.serverListView.selectionModel().currentIndex().row() < 0:
            #No server selected
            return

        r = QMessageBox.question(self, self.trUtf8('Delete'), 
                                 self.trUtf8('Are you sure?'), 
                                 QMessageBox.Yes, QMessageBox.No)
        #r = self.__question(Strings.DELETE, Strings.ARE_YOU_SURE)
        if r == QMessageBox.Yes:
            index = self.serverListView.selectionModel().currentIndex() #Currently selected

            # Delete the server
            self.serverListView.model().beginRemoveRows(QModelIndex(), index.row(), index.row())
            self.serverListView.model().removeRows(index.row(), 1)
            self.serverListView.model().endRemoveRows()

            # When deleting, the view gets updated and selects a new current.
            # Get it and give it to the mapper
            newIndex = self.serverListView.selectionModel().currentIndex()
            self.mapper.setCurrentIndex(newIndex.row())
            self.UNSAVED_STATE = True

        if self.slm.rowCount(QModelIndex()) == 0:
            self.tabWidget.setEnabled(False) #Disable editing if no servers left

    def saveServers(self):
        """
        Called when the Save-button is clicked.
        
        What should happen when the user clicks Save then Cancel?
        """
        self.__serverList.writeServerList()
        self._serverListCopy = copy.deepcopy(self.__serverList)

    def reject(self):
        """
        Called when the users clicks cancel or presses escape
        
        SOMETHING LOGICAL SHOULD PROBABLY BE DONE HER
        """
        if self.UNSAVED_STATE:
            r = QMessageBox.question(self, self.trUtf8('Exit?'), 
                self.trUtf8('Are you sure you want to exit the server editor?\
                            \nAny unsaved changes will be lost!'), 
                QMessageBox.Ok | QMessageBox.Cancel)
            if not r == QMessageBox.Ok:
                return
        if self._serverListCopy:
            self._returnList = self._serverListCopy
            QDialog.accept(self)
            return
        QDialog.reject(self)

    def accept(self):
        """
        Called when OK-button is clicked
        
        SOMETHING LOGICAL SHOULD PROBABLY BE DONE HER
        """
        self.__serverList.writeServerList()
        self._returnList = self.__serverList
        QDialog.accept(self)

    def getResult(self):
        return self._returnList

    def certFileDialog(self):
        filename = QFileDialog.getOpenFileName(self, self.trUtf8('Open file'), '')
        self.certFileEdit.setText(filename)
        self.mapper.submit()
        self.UNSAVED_STATE = True

    def certKeyfileDialog(self):
        filename = QFileDialog.getOpenFileName(self, self.trUtf8('Open file'), '')
        self.certKeyFileEdit.setText(filename)
        self.mapper.submit()
        self.UNSAVED_STATE = True


class AboutDialog(QDialog, Ui_AboutDialog):
    """
    A simple about dialog.
    
    It includes basic application information, a short outline of the 
    application license, and of course credit is given where credit is due.
    """

    def __init__(self, parent=None):

        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(iconFromTheme('help-about', ':/icons/about'))
        self.label.setPixmap(QPixmap(':/icons/luma-64'))

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
