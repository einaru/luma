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

from PyQt4.QtCore import (QSettings, pyqtSignal, Qt)
from PyQt4.QtGui import (QWidget, QIcon, qApp)

from base.backend.ServerList import ServerList
from base.backend.Connection import LumaConnection
from base.backend.Exception import (ServerCertificateException,
                                    InvalidPasswordException)

from .gui.SearchPluginDesign import Ui_SearchPlugin

class SearchPlugin(QWidget, Ui_SearchPlugin):
    """Luma Search plugin.
    """

    # This signal will be emitted after a successful search operation
    searchResult = pyqtSignal(object, list, name='LumaSearchResult')

    __logger = logging.getLogger(__name__)

    def __init__(self, parent=None):
        super(SearchPlugin, self).__init__(parent)
        self.setupUi(self)

        self.settings = QSettings()

        self.serverListObject = ServerList()
        #self.serverListObject.readServerList() # No need
        self.serverList = self.serverListObject.getTable()
        self.currentServer = None

        self.connection = None

        secureIcon = QIcon(':/icons/secure')
        # TODO: maybe we allways want to return a list from ServerList,
        #       eliminating the 'NoneType is not iterable' exceptions.
        if not self.serverList is None:
            for server in self.serverList:
                # As documendted in the ServerObject class:
                # 0 = Unencrypted, 1 = TLS, 2 = SSL
                if server.encryptionMethod == 0:
                    self.serverBox.addItem(server.name)
                else:
                    self.serverBox.addItem(secureIcon, server.name)
        
        # Keep track of open tabs
        self.openTabs = {}

    def __utf8(self, text):
        """Helper method to get text objects in unicode utf-8 encoding.
        
        @param text: 
            the text object to encode.
        @return: 
            the encoded textobject.
        """
        return unicode(text).encode('utf-8').strip()

    def __initFilterBookmarks(self):
        """TODO: document
        """
        configPrefix = self.settings.value('application/config_prefix')
        msg = 'Implement the __initFilterBookmarks using prefix:%s' % \
              configPrefix.toString()
        self.__logger.debug(msg)

    def __search(self, filter, criteria):
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
            msg = 'Unable to bind to %s. Reason\n%s' % ('LDAP server', str(e))
            self.__logger.error(msg)
            return

        # Because QString suck bigtime we need these additional
        # lines of code.
        i = self.baseDNBox.currentIndex()
        base = self.__utf8(self.baseDNBox.itemText(i))
        self.currentServer.currentBase = base

        # The scope selection works based on the index:
        # 0 = SCOPE_BASE
        # 1 = SCOPE_ONELEVEL
        # 2 = SCOPE_SUBTREE
        scope = self.scopeBox.currentIndex()
        limit = self.sizeLimitSpinBox.value()
        
        qApp.setOverrideCursor(Qt.WaitCursor)
        self.scrollArea.setEnabled(False)
        success, result, e = self.connection.search(
                                        base=self.currentServer.currentBase,
                                        scope=scope,
                                        filter=filter,
                                        sizelimit=limit)
        qApp.restoreOverrideCursor()
        self.scrollArea.setEnabled(True)
        # Remember to unbind
        self.connection.unbind()

        if success:
            #self.parent.getStatusBar()
            self.searchResult.emit(self.currentServer, result)#, criteria)
            resultTab = SearchResultView(self.searchResultWidget)
            self.searchResultWidget.setTabsClosable(True)
            self.searchResultWidget.insertTab(0, resultTab, 'Search result')
        else:
            msg = 'Error during search operation. Reason:\n%s' % str(e)
            self.__logger.error(msg)

    def search(self):
        """Slot for the search button.
        
        The text string in the search line is validated and prepared
        for the actual search.
        """
        #filter = unicode(self.searchEdit.text()).encode('utf-8')
        filter = self.__utf8(self.searchEdit.text())
        filterPattern = re.compile("\(\w*=")
        tmpList = filterPattern.findall(filter)

        criterialist = map(lambda x: x[1:-1], tmpList)

        self.__search(filter, criterialist)

    def showFilterWizard(self):
        """Slot for the filter wizard tool button.
        
        Display the filter bookmark wizard.
        """
        self.__logger.debug('Implement showFilterWizard SLOT')

    def serverChanged(self, index):
        """Slot for the server combo box.
        
        When the selected index changes, we want to fetch the baseDN
        list off of the selected server, and populate the baseDN combo
        box.
        
        @param index:
            The index of the server entry in the combobox.
        """
        serverString = self.serverBox.itemText(index)

        # No need to try to fetch the base dn list off of no server.
        if serverString == '':
            return

        # Get the server object for the selected server.
        # And return if this object is None
        self.currentServer = self.serverListObject.getServerObject(serverString)

        if self.currentServer is None:
            return

        self.connection = LumaConnection(self.currentServer)
        baseDNList = None

        if self.currentServer.autoBase:
            success, baseDNList, e = self.connection.getBaseDNList()
            if not success:
                # TODO: give some visual feedback to the user, regarding
                #       the unsuccessful bind operation
                msg = 'Could not retrieve baseDN. Reason:\n%s' % (str(e))
                self.__logger.error(msg)
        else:
            baseDNList = self.currentServer.baseDN

        # We need make sure the baseDN combo box is cleared before we
        # try to populate it with the newly fetched baseDN list.       
        self.baseDNBox.clear()
        if not baseDNList is None:
            for x in baseDNList:
                self.baseDNBox.addItem(x)


class SearchResultView(QWidget):
    """This class respresent the search result view.
    """

    def __init__(self, parent=None):
        super(SearchResultView, self).__init__(parent)
