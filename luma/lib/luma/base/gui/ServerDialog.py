# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import os
import ldap

from qt import *


from base.gui.ServerDialogDesign import ServerDialogDesign
from base.backend.ServerObject import ServerObject
from base.backend.ServerList import ServerList
import environment
from base.gui.BaseSelector import BaseSelector
from base.backend.LumaConnection import LumaConnection

class ServerDialog(ServerDialogDesign):
    """The dialog for managing all server information.
    """

    def __init__(self, parent= None):
        ServerDialogDesign.__init__(self, parent)

        self._PREFIX = environment.lumaInstallationPrefix
        
        self.iconPath = os.path.join(self._PREFIX, "share", "luma", "icons")
        self.networkLabel.setPixmap(QPixmap(os.path.join(self.iconPath, "worldmedium.png")))
        self.authLabel.setPixmap(QPixmap(os.path.join(self.iconPath, "passwordmedium.png")))
        self.guiParent = parent

        self.applyButton.setEnabled(0)

        self.serverListObject = ServerList()
        self.serverList = None
        
        # Server which is currently selected.
        self.currentServer = None

        
        self.serverListObject.readServerList()
        if self.serverListObject.SERVERLIST == None:
            self.serverList = []
        else:
            self.serverList = self.serverListObject.SERVERLIST

        self.serverIcon = QPixmap(os.path.join(self._PREFIX, "share", "luma", "icons", "server.png"))
        
        self.displayServerList()
        
###############################################################################

    def displayServerList(self):
        self.serverListView.clear()
        
        for x in self.serverList:
            tmpItem = QListViewItem(self.serverListView, x.name)
            tmpItem.setPixmap(0, self.serverIcon)
            self.serverListView.insertItem(tmpItem)
            
        self.serverListView.setSelected(self.serverListView.firstChild(), True)
        
###############################################################################

    def serverSelectionChanged(self, tmpItem):
        """ Change server information if another server has been selected.
        """
        
        #selectedServerString = unicode(self.serverIconView.currentItem().text())
        selectedServerString = unicode(tmpItem.text(0))
        
        
        x = self.serverListObject.get_serverobject(selectedServerString)
        self.currentServer = x
        
        self.hostLineEdit.blockSignals(True)
        self.portSpinBox.blockSignals(True)
        self.bindAnonBox.blockSignals(True)
        self.baseLineEdit.blockSignals(True)
        self.bindLineEdit.blockSignals(True)
        self.passwordLineEdit.blockSignals(True)
        self.tlsCheckBox.blockSignals(True)
        
        self.infoGroupBox.setTitle(x.name)
        self.hostLineEdit.setText(x.host)
        self.portSpinBox.setValue(x.port)
        self.bindAnonBox.setChecked(int(x.bindAnon))
        self.baseLineEdit.setText(x.baseDN)
        self.bindLineEdit.setText(x.bindDN)
        self.passwordLineEdit.setText(x.bindPassword)
        self.tlsCheckBox.setChecked(int(x.tls))
        self.bindAnonChanged(True, True)
        
        self.hostLineEdit.blockSignals(False)
        self.portSpinBox.blockSignals(False)
        self.bindAnonBox.blockSignals(False)
        self.baseLineEdit.blockSignals(False)
        self.bindLineEdit.blockSignals(False)
        self.passwordLineEdit.blockSignals(False)
        self.tlsCheckBox.blockSignals(False)

###############################################################################

    def addServer(self):
        """ Set content of input fields if a new server is created.
        """
        
        result = QInputDialog.getText(\
            self.trUtf8("New server"),
            self.trUtf8("Please enter a name for the new server:"),
            QLineEdit.Normal)
        
        if result[1] == False:
            return

        self.infoGroupBox.setTitle(result[0])
        
        serverObject = ServerObject()
        serverObject.name = unicode(result[0])
        
        self.serverList.append(serverObject)
        #self.displayServerList()
        
        self.applyButton.setEnabled(1)
        
        tmpItem = QListViewItem(self.serverListView, result[0])
        tmpItem.setPixmap(0, self.serverIcon)
        self.serverListView.insertItem(tmpItem)
        self.serverListView.setSelected(tmpItem, True)
        
###############################################################################

    def saveServer(self):
        """ Save the changed server values.
        """
        
        self.serverListObject.SERVERLIST = self.serverList
        self.serverListObject.save_settings(self.serverListObject.SERVERLIST)
        
        self.displayServerList()
        self.applyButton.setEnabled(0)
        
###############################################################################

    def saveCloseDialog(self):
        self.saveServer()
        self.accept()
        
###############################################################################

    def deleteServer(self):
        """ Delete the currently selected server.
        """
        
        selectedServerString = self.serverListView.currentItem().text(0)
        reallyDelete = QMessageBox(self.trUtf8("Delete Server?"),
                self.trUtf8("Do your really want to delete the Server?"),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.Cancel,
                QMessageBox.NoButton,
                self)
        reallyDelete.setIconPixmap(QPixmap(os.path.join(self._PREFIX, "share", "luma", "icons", "error.png")))
        reallyDelete.exec_loop()
        if (reallyDelete.result() == 1):
            self.serverListObject.deleteServer(str(selectedServerString))
            self.serverList = self.serverListObject.SERVERLIST
            
            self.displayServerList()
            self.applyButton.setEnabled(1)

###############################################################################

    def searchBaseDN(self):
        
        serverMeta = ServerObject()
        serverMeta.name = unicode(self.hostLineEdit.text())
        serverMeta.host = unicode(self.hostLineEdit.text())
        serverMeta.port = int(self.portSpinBox.value())
        serverMeta.tls = bool(self.tlsCheckBox.isChecked())
        serverMeta.bindAnon = True
        serverMeta.baseDN = unicode("")
        serverMeta.bindDN = unicode("")
        serverMeta.bindPassword = unicode("")
        
        try:
            conObject = LumaConnection(serverMeta)
            conObject.bind()
            
            dnList = None
        
            # Check for openldap
            result = conObject.search_s("", ldap.SCOPE_BASE, "(objectClass=*)", ["namingContexts"])
            dnList = result[0][1]['namingContexts']
        
            # Check for Novell
            if dnList[0] == '':
                result = conObject.search_s("", ldap.SCOPE_BASE)
                dnList = result[0][1]['dsaName']
            
            # Univertity of Michigan aka umich
            # not jet tested
            if dnList[0] == '':
                result = conObject.search_s("", ldap.SCOPE_BASE, "(objectClass=*)",['database'])
                dnList = result[0][1]['namingContexts']
                
            conObject.unbind()
        
            dialog = BaseSelector()
            dialog.setList(dnList)
            dialog.exec_loop()
            if dialog.result() == QDialog.Accepted:
                self.baseLineEdit.setText(dialog.dnBox.currentText())
                self.applyButton.setEnabled(1)
                
        except:
            QMessageBox.warning(None,
                self.trUtf8("Error"),
                self.trUtf8("""Could not retrieve BaseDN for server. 
Maybe the server data is not correct. 
Please see console output for more information."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)

###############################################################################

    def tlsChanged(self, tmpBool):
        self.applyButton.setEnabled(1)
        
        tlsBool = self.tlsCheckBox.isChecked()
        
        if tlsBool:
            self.portSpinBox.setValue(636)
        else:
            self.portSpinBox.setValue(389)
            
        self.currentServer.tls = tlsBool
            
###############################################################################

    def hostChanged(self, tmpString):
        self.applyButton.setEnabled(1)
        self.currentServer.host = unicode(tmpString)
        
###############################################################################

    def portChanged(self, tmpInt):
        self.applyButton.setEnabled(1)
        self.currentServer.port = tmpInt
        
###############################################################################

    def bindAnonChanged(self, tmpBool, firstTime=False):
        """ Change authentification info if anonoumus authentification is
        selected/de-selected.
        """
        
        if not firstTime:
            self.applyButton.setEnabled(1)
        
        tmpBool = self.bindAnonBox.isChecked()
        if tmpBool:
            self.passwordLineEdit.setEnabled(0)
            self.bindLineEdit.setEnabled(0)
        else:
            self.passwordLineEdit.setEnabled(1)
            self.bindLineEdit.setEnabled(1)
            
        self.currentServer.bindAnon = tmpBool

###############################################################################

    def bindDNChanged(self, tmpString):
        self.applyButton.setEnabled(1)
        self.currentServer.bindDN = unicode(tmpString)
        
###############################################################################

    def bindPasswordChanged(self, tmpString):
        self.applyButton.setEnabled(1)
        self.currentServer.bindPassword = unicode(tmpString)
        
###############################################################################

    def baseDNChanged(self, tmpString):
        self.applyButton.setEnabled(1)
        self.currentServer.baseDN = unicode(tmpString)
