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
import os
import re
import gc

from PyQt4.QtCore import (QEvent, QObject, Qt, QTimer, pyqtSignal)
from PyQt4.QtGui import (QKeySequence, QWidget, qApp)

from base.backend.ServerList import ServerList
# Switching to the LumaConnectionWrapper
#from base.backend.Connection import LumaConnection
from base.backend.LumaConnectionWrapper import LumaConnectionWrapper
from base.backend.Exception import (ServerCertificateException,
                                    InvalidPasswordException)
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.gui.Settings import PluginSettings
from base.util import encodeUTF8
from base.util.IconTheme import iconFromTheme, pixmapFromTheme

from .gui.SearchPluginDesign import Ui_SearchPlugin
from .gui.SearchPluginSettingsDesign import Ui_SearchPluginSettings
from .FilterBuilder import FilterBuilder
from .SearchForm import SearchForm
from .SearchResult import ResultView

class SearchPluginEventFilter(QObject):
    """An Event handler for the Search Plugin.
    
    To act upon widget events, install an instance of this class with
    the target widget, and add the capture logic in the eventFilter
    method.
    """

    def eventFilter(self, target, event):
        """Overrided method to catch and act upon various ``QEvent`s.
        
        Parameters:
        
        - `target`: The target ``QWidget`` where the event was 
          generated from.
        - `event`: The ``QEvent`` that was generated.
        """
        if event.type() == QEvent.KeyPress:
            # If we have a match on the QKeySequence we're looking for
            # we keep things safe by explicitly checking if the target
            # is the correct for our purpose.
            # In the case of the Search plugin, only the tab widget for
            # the search results ('right') is expected to act upon the
            # close event.
            if target.objectName() == 'right':
                index = target.currentIndex()
                if event.matches(QKeySequence.Close):
                    target.tabCloseRequested.emit(index)
                    # When we actually catches and acts upon an event,
                    # we need to inform the eventHandler about this.
                    return True
                elif event.matches(QKeySequence.Find):
                    widget = target.widget(index)
                    state = widget.filterBox.isVisible()
                    #widget.filterBox.setVisible(not state)
                    #widget.filterBox.onVisibilityChanged(not state)
                    widget.onFilterBoxVisibilityChanged(not state)
                    return True
        # Retranslate the ui if we catch the LanguageChange event
        elif event.type() == QEvent.LanguageChange:
            if target.objectName() == 'SearchPlugin':
                target.retranslate()
                return True
        # All events we didn't act upon must be forwarded        
        return QObject.eventFilter(self, target, event)


class SearchPlugin(QWidget, Ui_SearchPlugin):
    """The Luma Search plugin.
    
    .. note::
       This plugin implementation still uses the experimental
       `base.backend.Connection` module. On deployment we might
       consider switching back to the more safer 
       `base.bakend.LumaConnection` module.
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, parent=None):
        super(SearchPlugin, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName('SearchPlugin')
        self.openTabs = {}
        self.completer = None
        self.currentServer = None
        #self.connection = None

        self.serverListObject = ServerList()
        self.serverList = self.serverListObject.getTable()

        self.searchForm = SearchForm(parent=self)
        self.filterBuilder = FilterBuilder(parent=self)

        # Icons
        searchIcon = iconFromTheme(
            'edit-find', ':/icons/32/edit-find')
        filterIcon = iconFromTheme(
            'edit-find-replace', ':/icons/32/edit-find-replace')
        secureIcon = iconFromTheme(
            'object-locked', ':/icons/16/object-locked')
        errorIcon = pixmapFromTheme(
            'dialog-error', ':/icons/48/dialog-error', 24, 24)
        undoIcon = iconFromTheme(
            'edit-undo', ':/icons/32/edit-undo')
        redoIcon = iconFromTheme(
            'edit-redo', ':/icons/32/edit-redo')
        addIcon = iconFromTheme(
            'list-add', ':/icons/32/list-add')

        self.indexSF = self.left.addTab(self.searchForm, searchIcon, '')
        self.indexFB = self.left.addTab(self.filterBuilder, filterIcon, '')

        self.searchForm.filterBuilderToolButton.setIcon(filterIcon)
        self.searchForm.errorIcon.setPixmap(errorIcon)
        self.filterBuilder.undoButton.setIcon(undoIcon)
        self.filterBuilder.redoButton.setIcon(redoIcon)
        self.filterBuilder.addSpecialCharButton.setIcon(addIcon)

        # The search plugin event filter we 
        # use for acting upon various events
        eventFilter = SearchPluginEventFilter(self)
        # Install the eventFilter on desired widgets
        self.installEventFilter(eventFilter)
        self.right.installEventFilter(eventFilter)

        self.__loadSettings()
        self.__connectSlots()

        # Only add text to these class and its children at this time
        self.retranslate(all=False)

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
        self.right.tabCloseRequested[int].connect(self.onTabClose)
        # Filter Builder signals and slots
        self.filterBuilder.filterSaved.connect(self.loadFilterBookmarks)
        self.filterBuilder.useFilterRequest.connect(self.onUseFilterRequested)
        # Search Form signals and slots
        self.searchForm.searchButton.clicked.connect(self.onSearchButtonClicked)
        self.searchForm.filterBuilderToolButton.clicked.connect(self.onFilterBuilderButtonClicked)
        self.searchForm.serverBox.currentIndexChanged[int].connect(self.onServerChanged)

    def __loadSettings(self):
        """Loads the plugin settings if available.
        """
        settings = PluginSettings('search')
        self.autocompleteIsEnabled = settings.pluginValue('autocomplete', False).toBool()
        self.searchForm.scope = settings.pluginValue('scope', 2).toInt()[0]
        self.searchForm.sizeLimit = settings.pluginValue('limit', 0).toInt()[0]
        self.filterBuilder.setFilterHighlighter(settings.pluginValue('highlighting', False).toBool())

        # Try to fetch the luma config prefix from the settings file,
        # and call the loadFilterBookmarks to populate search box
        self.configPrefix = settings.configPrefix
        self.loadFilterBookmarks()

    def loadFilterBookmarks(self):
        """Reads the saved filter bookmarks from disk.
        
        The filter bookmarks is then passed to the search form widget.
        """
        try:
            filterFile = os.path.join(self.configPrefix, 'filters')
            # We only try to read the filters file from disk if it
            # already exists. If not we do nothing, as it will be 
            # created in the filter wizard if the user choose to do so.
            if os.path.isfile(filterFile):
                bookmarks = []
                with open(filterFile, 'r+') as f:
                    #bookmarks = f.readLines()
                    for filter in f:
                        bookmarks.append(filter.strip())

                self.searchForm.populateFilterBookmarks(bookmarks)
        except IOError, e:
            msg = 'Unable to read file: {0} Reason:\n\t{1}'
            self.__logger.error(msg.format(filterFile, str(e)))

    def onTabClose(self, index):
        """Slot for the tabCloseRequested signal.
        
        Parameters:
        
        - `index`: the integer index value of the currently focused
          tab widget.
        """
        # Might happen if QKeySequence.Close is captured when no tabs
        # is open.
        if index < 0:
            return

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
        
        Parameters:
        
        - `index`: the index of the server entry in the combobox.
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

        #self.connection = LumaConnection(self.currentServer)
        con = LumaConnectionWrapper(self.currentServer, self)

        if self.currentServer.autoBase:
            #success, baseDNList, e = self.connection.getBaseDNList()
            success, baseDNList, e = con.getBaseDNListSync()
            if not success:
                # TODO: give some visual feedback to the user, regarding
                #       the unsuccessful bind operation
                msg = 'Could not retrieve baseDN. Reason:\n{0}'
                self.__logger.error(msg.format(str(e)))
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

        self.filterBuilder.onServerChanged(objectClasses, attributes)
        
        if self.autocompleteIsEnabled:
            self.searchForm.initAutoComplete(attributes)

    def onUseFilterRequested(self, filter):
        """Slot for the useFilterRequested signal in the filter builder.
        
        Parameters: 
        
        - `filter`: the filter to use in the searchform.
        """
        # We want to set the filter as the selected filter in the
        # search form, and switch to the search form, but _not_ do the
        # search automatically. We might want to give the search button
        # focus though.
        self.searchForm.filterBoxEdit.insertItem(0, filter)
        self.searchForm.filterBoxEdit.setCurrentIndex(0)
        self.left.setCurrentIndex(0)
        self.searchForm.searchButton.setFocus()

    def onFilterBuilderButtonClicked(self):
        """Slot for the filter builder tool button.
        
        Display the filter builder with the current filter.
        """
        current = self.searchForm.filterBoxEdit.currentText()
        self.filterBuilder.filterEdit.setPlainText(current)
        self.left.setCurrentIndex(1)

    def onSearchButtonClicked(self):
        """Slot for the search button.
        """
        self.searchForm.onSearchError(False)
        filter = self.searchForm.filter
        self.__logger.debug('filter: {0}'.format(filter))
        self.search(filter)

    def search(self, filter):
        """Starts the search operation on the selected server.
        
        Parameters:

        - `filter`: The LDAP searchfilter to be used in the search.
        """
        # Return was pressed but no server is selected, thus we do not
        # perform any search operation.
        if self.currentServer is None:
            return

        scope = self.searchForm.scope
        limit = self.searchForm.sizeLimit
        base = self.searchForm.baseDN

        self.currentServer.currentBase = base

        # Perform an asyncronized search operation. When the search is
        # finished we act upon the LumaConnectionWrapper.searchFinished
        # signal in the onSearchFinished method
        args = dict(base=base, scope=scope, filter=filter, sizelimit=limit)
        search = Search(self.currentServer, **args)
        search.resultsRetrieved.connect(self.onResultsRetrieved)

    def onResultsRetrieved(self, result, e):
        """Slot for the ``LumaConnectionWrapper.searchFinished``
        signal.
        """
        if e is None:
            filter = result.pop()
            attributelist = self.__getAttributeList(filter)
            resultTab = ResultView(filter=filter,
                                   attributelist=attributelist,
                                   resultlist=result,
                                   parent=self.right)
            index = self.right.addTab(resultTab, 'Search result')
            self.right.setCurrentIndex(index)
        else:
            msg = 'Error during search operation.\n{0}'.format(e)
            self.searchForm.onSearchError(True, msg)
    
    def __getAttributeList(self, filter):
        """Returns a list of attributes found in `filter`.

        Parameters:

        - `filter`: a valid LDAP search filter.
        """
        # FIXME: Switch to the methods in the Filter module when it's
        #        finished and ready for use.
        filterPattern = re.compile("\(\w*=")
        tmpList = filterPattern.findall(filter)
        attributeList = map(lambda x: x[1:-1], tmpList)
        for attr in attributeList:
            print attr

        return attributeList

    def retranslate(self, all=True):
        """For dynamic retranslation of the plugin text strings
        """
        self.left.setTabToolTip(self.indexSF, qApp.translate("SearchPlugin", "Search Form"))
        self.left.setTabToolTip(self.indexFB, qApp.translate("SearchPlugin", "Filter Builder"))
        self.searchForm.retranslateUi(self.searchForm)
        self.filterBuilder.retranslateUi(self.searchForm)

        if all:
            self.retranslateUi(self)
            for tab in self.right.children():
                try:
                    tab.retranslate()
                except AttributeError:
                    pass

class Search(QObject):
    """Object representing a search."""

    resultsRetrieved = pyqtSignal(list, object)
    __logger = logging.getLogger(__name__)

    def __init__(self, server, **kwargs):
        """
        Parameters:

        - `connection`: the connection object to perform the search
          operation with.
        - `args`: a tuple with arguments to the search.
        """
        super(Search, self).__init__()
        self.filter = kwargs['filter']
        self.connection = LumaConnectionWrapper(server, self)
        self.connection.searchFinished.connect(self.onSearchFinished)
        
        bindSuccess, e = self.connection.bindSync()
        if not bindSuccess:
            msg = 'Unable to bind to {0}. Reason\n{1}'
            self.__logger.error(msg.format(server, str(e)))
        else:    
            self.connection.searchAsync(**kwargs)

    def onSearchFinished(self, success, result, e):
        """Slot for the searchFinished signal in LumaConnectionWrapper.
        As of now this reemits a signal that SearchPlugin has connected
        to. This is done in order to be able to provide the filter and
        attributes needed for the result view.
        """
        if success:
            result.append(self.filter)
            self.resultsRetrieved.emit(result, None)
        else:
            self.resultsRetreived.emit([], e)


class SearchPluginSettingsWidget(QWidget, Ui_SearchPluginSettings):
    """The settings widget for the search plugin.
    
    .. note::
       The writeSettings method is registered as a slot for the
       settings changed signal in the settings dialog.
    """

    def __init__(self, parent=None):
        super(SearchPluginSettingsWidget, self).__init__(parent)
        self.setupUi(self)
        self.loadSettings()

    def loadSettings(self):
        """Load the possibly saved search plugin settings from diks.
        """
        settings = PluginSettings('search')
        autocomplete = settings.pluginValue('autocomplete', False).toBool()
        highlight = settings.pluginValue('highlighting', False).toBool()
        self.enableCompletionOpt.setChecked(autocomplete)
        self.enableHighlightingOpt.setChecked(highlight)
        self.scopeBox.setCurrentIndex(settings.pluginValue('scope', 2).toInt()[0])
        self.sizeLimitBox.setValue(settings.pluginValue('limit', 0).toInt()[0])
        del settings

    def writeSettings(self):
        """Slot for the onSettingsChanged signal.
        
        Writes the settings values to disk.
        """
        settings = PluginSettings('search')
        settings.setPluginValue('autocomplete', self.enableCompletionOpt.isChecked())
        settings.setPluginValue('highlighting', self.enableHighlightingOpt.isChecked())
        settings.setPluginValue('scope', self.scopeBox.currentIndex())
        settings.setPluginValue('limit', self.sizeLimitBox.value())
        del settings


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
