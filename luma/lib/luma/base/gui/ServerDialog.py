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
    """ Show the dialog for managing all server information.
    """

    def __init__(self, parent= None):
        ServerDialogDesign.__init__(self, parent)

        self._PREFIX = environment.lumaInstallationPrefix

        self.guiParent = parent

        self.saveButton.setEnabled(0)

        self.serverListObject = ServerList()
        self.serverList = self.serverListObject.SERVERLIST

        self.serverListIconView = []

        self.reloadServer()

        self.setInputEnabled(0)
        
###############################################################################

    def serverSelectionChanged(self):
        """ Change server information if another server has been selected.
        """
        
        selectedServerString = str(self.serverIconView.currentItem().text())

        x = self.serverListObject.get_serverobject(selectedServerString)
        self.nameLineEdit.setText(x.name)
        self.hostLineEdit.setText(x.host)
        self.portSpinBox.setValue(x.port)
        self.bindAnonBox.setChecked(int(x.bindAnon))
        self.baseLineEdit.setText(x.baseDN)
        self.bindLineEdit.setText(x.bindDN)
        self.bindLineEdit.setEnabled(1)
        self.passwordLineEdit.setText(x.bindPassword)
        self.passwordLineEdit.setEnabled(1)
        self.tlsCheckBox.setChecked(int(x.tls))

        self.setInputEnabled(0)
        
###############################################################################

    def setInputEnabled(self, inputMutex):
        """ Change attributes of input fields to enable/disable input.
        """
        
        self.nameLineEdit.setEnabled(1)
        self.nameLineEdit.setReadOnly(not(inputMutex))
        self.hostLineEdit.setReadOnly(not(inputMutex))
        self.portSpinBox.setEnabled(inputMutex)
        self.bindAnonBox.setEnabled(inputMutex)
        if self.bindAnonBox.isChecked():
            self.passwordLineEdit.setEnabled(0)
            self.bindLineEdit.setEnabled(0)
        else:
            self.passwordLineEdit.setEnabled(1)
            self.bindLineEdit.setEnabled(1)
        self.bindLineEdit.setReadOnly(not(inputMutex))
        self.baseLineEdit.setReadOnly(not(inputMutex))
        self.passwordLineEdit.setReadOnly(not(inputMutex))
        self.tlsCheckBox.setEnabled(inputMutex)
        self.saveButton.setEnabled(inputMutex)
        self.basednButton.setEnabled(inputMutex)
        
###############################################################################

    def modifyServer(self):
        self.setInputEnabled(1)
        self.nameLineEdit.setEnabled(0)

###############################################################################

    def addServer(self):
        """ Set content of input fields if a new server is created.
        """
        
        self.nameLineEdit.setText("")
        self.hostLineEdit.setText("")
        self.portSpinBox.setValue(389)
        self.bindAnonBox.setChecked(1)
        self.baseLineEdit.setText("")
        self.bindLineEdit.setText("")
        self.passwordLineEdit.setReadOnly(1)
        self.bindLineEdit.setReadOnly(1)
        self.passwordLineEdit.setText("")
        self.tlsCheckBox.setChecked(0)
        self.setInputEnabled(1)
        
###############################################################################

    def reloadServer(self):
        """ Re-read the server list from config file and get updated data.
        """
        
        self.serverIconView.clear()
        self.serverListObject.readServerList()
        if self.serverListObject.SERVERLIST == None:
            self.serverList = []
        else:
            self.serverList = self.serverListObject.SERVERLIST
        self.serverListIconView = []
        tmpIcon = QPixmap(os.path.join(self._PREFIX, "share", "luma", "icons", "server.png"))
        for x in self.serverList:
            self.serverListIconView.append(QIconViewItem(self.serverIconView, x.name, tmpIcon))
        self.serverIconView.setCurrentItem(self.serverIconView.firstItem())
        self.setInputEnabled(0)
        
###############################################################################

    def saveServer(self):
        """ Save the changed values of the currently selected server.
        """
        
        if len(self.serverList) > 0:
            self.serverListObject.deleteServer(str(self.nameLineEdit.text()))
        self.serverListObject.addServer(str(self.nameLineEdit.text()),
                str(self.hostLineEdit.text()),
                int(self.portSpinBox.value()),
                bool(self.bindAnonBox.isChecked()),
                str(self.baseLineEdit.text()),
                str(self.bindLineEdit.text()),
                str(self.passwordLineEdit.text()),
                bool(self.tlsCheckBox.isChecked()))
        self.reloadServer()
        
###############################################################################

    def deleteServer(self):
        """ Delete the currently selected server.
        """
        
        selectedServerString = self.serverIconView.currentItem().text()
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
            self.reloadServer()

###############################################################################

    def bind_anon(self):
        """ Change authentification info if anonoumus authentification is
        selected/de-selected.
        """
        
        if self.bindAnonBox.isChecked():
            self.passwordLineEdit.setEnabled(0)
            self.bindLineEdit.setEnabled(0)
        else:
            self.passwordLineEdit.setEnabled(1)
            self.bindLineEdit.setEnabled(1)

###############################################################################

    def searchBaseDN(self):
        
        serverMeta = ServerObject()
        serverMeta.name = str(self.hostLineEdit.text())
        serverMeta.host = str(self.hostLineEdit.text())
        serverMeta.port = int(self.portSpinBox.value())
        serverMeta.tls = bool(self.tlsCheckBox.isChecked())
        serverMeta.bindAnon = True
        serverMeta.baseDN = ""
        serverMeta.bindDN = ""
        serverMeta.bindPassword = ""
        
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

