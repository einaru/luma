# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import ldap
import re
import os.path

from base.utils.gui.SearchFormDesign import SearchFormDesign
from base.utils.gui.FilterWizard import FilterWizard
from base.backend.ServerObject import ServerObject
from base.backend.ServerList import ServerList
import environment
from base.backend.LumaConnection import LumaConnection

class SearchForm(SearchFormDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        SearchFormDesign.__init__(self,parent,name,fl)

        tmpFile  = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons", "secure.png")
        securePixmap = QPixmap(tmpFile)

        self.serverListObject = ServerList()
        self.serverListObject.readServerList()
        self.serverList = self.serverListObject.serverList
        self.currentServer = None
        
        self.connection = None
        
        
        if not (self.serverList == None):
            for x in self.serverList:
                if x.tls == 1:
                    self.serverBox.insertItem(securePixmap, x.name)
                else:
                    self.serverBox.insertItem(x.name)

        self.serverChanged()
        self.initFilterBookmarks()

        self.searchEdit.installEventFilter(self)

###############################################################################

    def startSearch(self):
        """Starts the search for the given server and search filter.
        
        Emits the signal "ldap_result". Given arguments are the servername, the 
        search result and the criterias used for the filter.
        """
        
        self.groupBox2.setEnabled(False)

        criteriaList = self.getSearchCriteria()
    
        self.connection.bind()
        self.currentServer.currentBase = unicode(self.baseBox.currentText())
        searchResult = self.connection.search(self.currentServer.currentBase, ldap.SCOPE_SUBTREE,
                unicode(self.searchEdit.currentText()).encode('utf-8'))
        self.connection.unbind()
        
        self.groupBox2.setEnabled(True)

        self.emit(PYSIGNAL("ldap_result"), (self.currentServer.name, searchResult,criteriaList, ))

###############################################################################

    def startFilterWizard(self):
        server = unicode(self.serverBox.currentText())
        if self.serverList == None:
            print "Warning: Please set up some servers to connect to."
            return
            
        serverMeta = self.serverListObject.getServerObject(server)
            
        dialog = FilterWizard(server)
        dialog.exec_loop()
        
        if dialog.result() == QDialog.Accepted:
            self.initFilterBookmarks()
            self.searchEdit.setCurrentText(dialog.searchFilterEdit.text())


###############################################################################

    def initFilterBookmarks(self):
        bookmarkFile = os.path.join(environment.userHomeDir, ".luma", "filterBookmarks")
        try:
            fileHandler = open(bookmarkFile, 'r')
            text = fileHandler.readlines()
            fileHandler.close()
            self.searchEdit.clear()
            for x in text:
                self.searchEdit.insertItem(x[:-1])
        except:
            print "Bookmark loading failed"

###############################################################################

    def getSearchCriteria(self):
        filterString = unicode(self.searchEdit.currentText())
        filterPattern = re.compile("\(\w*=")
        tmpList = filterPattern.findall(filterString)

        return map(lambda x: x[1:-1], tmpList)

###############################################################################

    def eventFilter(self, object, event):
        if (event.type() == QEvent.KeyRelease):
            if (event.key() == Qt.Key_Return):
                self.startSearch()
                
        return 0

###############################################################################

    def serverChanged(self, serverString=""):
        serverString = unicode(self.serverBox.currentText())
        self.currentServer = self.serverListObject.getServerObject(serverString)
        
        self.connection = LumaConnection(self.currentServer)
        
        baseList = None
        if self.currentServer.autoBase:
            baseList = self.connection.getBaseDNList()
        else:
            baseList = self.currentServer.baseDN
            
        self.baseBox.clear()
        for x in baseList:
            self.baseBox.insertItem(x)
        
