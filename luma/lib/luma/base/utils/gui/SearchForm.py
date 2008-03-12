# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4.QtGui import *
import ldap
import re
import os.path

from base.utils.gui.SearchFormDesign import SearchFormDesign
from base.utils.gui.FilterWizard import FilterWizard
from base.backend.ServerObject import ServerObject
from base.backend.ServerList import ServerList
import environment
from base.backend.LumaConnection import LumaConnection
from base.backend.SmartDataObject import SmartDataObject
from base.utils.gui.LumaErrorDialog import LumaErrorDialog
from base.utils.backend.LogObject import LogObject

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
            tmpDict = {}
            for x in self.serverList:
                if not (x.encryptionMethod == u"None"):
                    tmpDict[x.name] = True
                else:
                    tmpDict[x.name] = False
                    
            self.serverBox.insertItem("")
            
            tmpList = tmpDict.keys()
            tmpList.sort()
            for x in tmpList:
                if tmpDict[x]:
                    self.serverBox.insertItem(securePixmap, x)
                else:
                    self.serverBox.insertItem(x)

        self.serverChanged()
        self.initFilterBookmarks()

        self.searchEdit.installEventFilter(self)

###############################################################################

    def startSearch(self):
        """Starts the search for the given server and search filter.
        
        Emits the signal "ldap_result". Given arguments are the servername, the 
        search result and the criterias used for the filter.
        """
        
        # Returns was pressed but no server selected. So we don't want 
        # to search.
        if self.connection == None:
            return
        
        self.groupFrame.setEnabled(False)

        criteriaList = self.getSearchCriteria()
    
        bindSuccess, exceptionObject = self.connection.bind()
        
        if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                self.groupBox2.setEnabled(True)
                return
                
        self.currentServer.currentBase = unicode(self.baseBox.currentText())
        success, resultList, exceptionObject = self.connection.search(self.currentServer.currentBase, ldap.SCOPE_SUBTREE,
                unicode(self.searchEdit.currentText()).encode('utf-8'))
        self.connection.unbind()
        
        self.groupFrame.setEnabled(True)
        
        if success:
            self.emit(PYSIGNAL("ldap_result"), (self.currentServer, resultList, criteriaList, ))
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Error during search operation.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()

###############################################################################

    def startFilterWizard(self):
        server = unicode(self.serverBox.currentText())
        if self.serverList == None:
            print "Warning: Please set up some servers to connect to."
            return
            
        serverMeta = self.serverListObject.getServerObject(server)
            
        dialog = FilterWizard(serverMeta)
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
        except IOError, e:
            logMessage = "Search filter bookmark loading failed. Reason:\n"
            logMessage += str(e)
            environment.logMessage(LogObject("Debug", logMessage))

###############################################################################

    def getSearchCriteria(self):
        filterString = unicode(self.searchEdit.currentText()).encode('utf-8')
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
        
        if serverString == "":
            return 
            
        self.currentServer = self.serverListObject.getServerObject(serverString)
        
        if self.currentServer == None:
            return
        
        self.connection = LumaConnection(self.currentServer)
        
        baseList = None
        if self.currentServer.autoBase:
            success, baseList, exceptionObject = self.connection.getBaseDNList()
            
            if not success:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not retrieve baseDN.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                
        else:
            baseList = self.currentServer.baseDN
            
        if baseList == None:
            self.startButton.setEnabled(False)
            baseList = []
        else:
            self.startButton.setEnabled(True)
            
        self.baseBox.clear()
        for x in baseList:
            self.baseBox.insertItem(x)
        
