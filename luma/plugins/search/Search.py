# -*- coding: utf-8 -*-
#
# plugins.search.Search
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

import logging
import re
import gc

from PyQt4.QtCore import (QSettings, Qt, QTimer, QVariant)
from PyQt4.QtGui import (QWidget, qApp)

from base.backend.ServerList import ServerList
from base.backend.Connection import LumaConnection
from base.backend.Exception import (ServerCertificateException,
                                    InvalidPasswordException)
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.util.IconTheme import iconFromTheme

from .gui.SearchPluginDesign import Ui_SearchPlugin
from .gui.SearchPluginSettingsDesign import Ui_SearchPluginSettings
from .FilterWizard import FilterWizard
from .SearchForm import SearchForm
from .SearchResult import ResultView

class SearchPlugin(QWidget, Ui_SearchPlugin):
    """The Luma Search plugin.
    
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !! NOTE: This plugin implementation still uses the experimental  !!
    !!       Connection module. On deployment we might consider      !!
    !!       switching back to the more safer LumaConnection module. !!      
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, parent=None):
        super(SearchPlugin, self).__init__(parent)
        self.setupUi(self)

        self.openTabs = {}
        self.completer = None
        self.currentServer = None
        self.connection = None

        self.serverListObject = ServerList()
        self.serverList = self.serverListObject.getTable()

        self.searchForm = SearchForm(parent=self)
        self.filterWizard = FilterWizard(parent=self)

        searchIcon = iconFromTheme('system-search', ':/icons/search_plugin-plugin')
        filterIcon = iconFromTheme('filter', ':/icons/filter')
        secureIcon = iconFromTheme('changes-prevent', ':/icons/secure')

        self.left.addTab(self.searchForm, searchIcon, '')
        self.left.addTab(self.filterWizard, filterIcon, '')

        self.__loadSettings()
        self.__connectSlots()
        # TODO: maybe we allways want to return a list from ServerList,
        #       eliminating the 'NoneType is not iterable' exceptions.
        if not self.serverList is None:
            for server in self.serverList:
                # As documendted in the ServerObject class:
                # 0 = Unencrypted, 1 = TLS, 2 = SSL
                if server.encryptionMethod == 0:
                    self.searchForm.serverBox.addItem(server.name)
                else:
                    self.searchForm.serverBox.addItem(secureIcon, server.name)

    def __connectSlots(self):
        """Connects signals and slots.
        """
        self.searchForm.searchButton.clicked.connect(self.onSearchButtonClicked)
        self.searchForm.filterWizardToolButton.clicked.connect(self.onFilterWizardButtonClicked)
        self.searchForm.serverBox.currentIndexChanged[int].connect(self.onServerChanged)
        self.right.tabCloseRequested[int].connect(self.onTabClose)

    def __loadSettings(self):
        """Loads the plugin settings if available.
        """
        settings = QSettings()
        self.autocompleteIsEnabled = settings.value('plugin/search/autocomplete', QVariant(True)).toBool()
        self.searchForm.scope = settings.value('plugin/search/scope', 2).toInt()[0]
        self.searchForm.sizeLimit = settings.value('plugin/search/limit', 0).toInt()[0]
        

    def __initFilterBookmarks(self):
        """TODO: document
        """
        configPrefix = self.settings.value('application/config_prefix')
        msg = 'Implement the __initFilterBookmarks using prefix:%s' % \
              configPrefix.toString()
        self.__logger.debug(msg)


    def onTabClose(self, index):
        """Slot for the tabCloseRequested signal.
        """
        widget = self.right.widget(index)
        self.right.removeTab(index)

        # Unparent the widget since it was reparented by the QTabWidget
        # so it's gargabe collected
        widget.setParent(None)
        QTimer.singleShot(0, gc.collect)

    def onServerChanged(self, index):
        """Slot for the server combo box.
        
        When the selected index changes, we want to fetch the baseDN
        list off of the selected server, and populate the baseDN combo
        box.
        
        @param index:
            The index of the server entry in the combobox.
        """
        serverString = self.searchForm.server

        # No need to try to fetch the base dn list off of no server.
        if serverString == '':
            return

        # Get the server object for the selected server.
        # And return if this object is None
        self.currentServer = self.serverListObject.getServerObject(serverString)

        if self.currentServer is None:
            return

        self.connection = LumaConnection(self.currentServer)

        if self.currentServer.autoBase:
            success, baseDNList, e = self.connection.getBaseDNList()
            if not success:
                # TODO: give some visual feedback to the user, regarding
                #       the unsuccessful bind operation
                msg = 'Could not retrieve baseDN. Reason:\n%s' % (str(e))
                self.__logger.error(msg)
        else:
            baseDNList = [self.currentServer.baseDN]

        # Try to populate it with the newly fetched baseDN list.       
        # We need make sure the baseDN combo box is cleared before we
        self.searchForm.populateBaseDNBox(baseDNList)

        # Try to fetch the list of available attributes, for use in the
        # filter wizard and for autocompletion.
        serverMeta = self.serverListObject.getServerObject(serverString)
        # Jippi ay o' what a beutiful var name!!
        ocai = ObjectClassAttributeInfo(serverMeta)
        attributes = ocai.getAttributeList()
        objectClasses = ocai.getObjectClasses()

        self.filterWizard.onServerChanged(objectClasses, attributes)
        
        if self.autocompleteIsEnabled:
            self.searchForm.initAutoComplete(attributes)

    def onFilterWizardButtonClicked(self):
        """Slot for the filter wizard tool button.
        
        Display the filter bookmark wizard.
        """
        self.left.setCurrentIndex(1)

    def onSearchButtonClicked(self):
        """Slot for the search button.
        
        The text string in the search line is validated and prepared
        for the actual search.
        """
        filter = self.searchForm.filter
        filterPattern = re.compile("\(\w*=")
        tmpList = filterPattern.findall(filter)

        criterialist = map(lambda x: x[1:-1], tmpList)

        self.search(filter, criterialist)

    def search(self, filter, criteria):
        """Starts the search for the given server and search filter.
        
        Emits the signal "ldap_result". Given arguments are the
        servername, the search result and the criterias used for the filter.
        """
        # Return was pressed but no server selected. So we don't want 
        # to search.
        # FIXME: This won't happen as off now, because you can never
        #        _not_ select a server :) Might want to change it though.
        if self.connection == None:
            return

        # NOTE:
        # This is the initial testing of the refactored Connection
        # class, where we use Exception to inform about operations gone
        # wrong. This is an atempt to get rid of the PyQt4 dependencies
        # in the backend package.
        # TODO: Might want to do some quering on the exceptions.
        #       Try to come up with a nice way to return missing stuff
        #       (i.e. password, certificate rules, etc)
        try:
            bindSuccess, e = self.connection.bind()
        except ServerCertificateException, sce:
            self.__logger.error(str(sce))
            return
        except InvalidPasswordException, ipe:
            self.__logger.error(str(ipe))
            return

        if not bindSuccess:
            # TODO: give some visual feedback to the user, regarding
            #       the unsuccessful bind operation
            msg = 'Unable to bind to %s. Reason\n%s' % \
                  (self.searchForm.server, str(e))
            self.__logger.error(msg)
            return

        # The scope selection works based on the index:
        # 0 = SCOPE_BASE
        # 1 = SCOPE_ONELEVEL
        # 2 = SCOPE_SUBTREE
        scope = self.searchForm.scope
        limit = self.searchForm.sizeLimit
        base = self.searchForm.baseDN

        self.currentServer.currentBase = base

        # To give some user feedback we manually set the WaitCursor
        # and disable the searchForm widget, while doing the actual
        # LDAP search.
        # On search returned we restore these states to normal.
        qApp.setOverrideCursor(Qt.WaitCursor)
        self.searchForm.setEnabled(False)
        success, result, e = self.connection.search(base=base,
                                                    scope=scope,
                                                    filter=filter,
                                                    sizelimit=limit)
        qApp.restoreOverrideCursor()
        self.searchForm.setEnabled(True)
        # Remember to unbind
        self.connection.unbind()

        if success: # and len(result) > 0:
            resultTab = ResultView(filter, criteria, result, self.right)
            self.right.addTab(resultTab, 'Search result')
        else:
            msg = 'Error during search operation. Reason:\n%s' % str(e)
            self.__logger.error(msg)


class SearchPluginSettings(QWidget, Ui_SearchPluginSettings):
    """The settings widget for the search plugin.
    """

    def __init__(self, parent=None):
        super(SearchPluginSettings, self).__init__(parent)
        self.setupUi(self)
        # TODO: Implement loading and saving of plugin settings
