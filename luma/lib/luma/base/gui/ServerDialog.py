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
        
        self.authentificationMethods = [u"Simple", u"SASL Plain", u"SASL CRAM-MD5", 
        u"SASL DIGEST-MD5", u"SASL Login", u"SASL GSSAPI"]

        self._PREFIX = environment.lumaInstallationPrefix
        
        self.iconPath = os.path.join(self._PREFIX, "share", "luma", "icons")
        self.networkLabel.setPixmap(QPixmap(os.path.join(self.iconPath, "worldmedium.png")))
        self.authLabel.setPixmap(QPixmap(os.path.join(self.iconPath, "passwordmedium.png")))
        self.guiParent = parent

        self.applyButton.setEnabled(0)

        self.serverListObject = ServerList()
        
        # Server which is currently selected.
        self.currentServer = None

        
        self.serverListObject.readServerList()
          
        if self.serverListObject.serverList == None:
            self.infoGroupBox.setEnabled(False)
        elif len(self.serverListObject.serverList) == 0:
            self.infoGroupBox.setEnabled(False)

        self.serverIcon = QPixmap(os.path.join(self._PREFIX, "share", "luma", "icons", "server.png"))
        
        # Indicates if the serverlist has been permanently edited.
        # Needed when we use the apply button and cancel the dialog afterwards.
        # But the changes have to be applied. 
        # 'dialog.result() == QDialog.Accepted' is not enough.
        self.SAVED = False
        
        # Will be set to the currently selected server
        self.currentServer = None
        
        self.displayServerList()
        
###############################################################################

    def displayServerList(self):
        self.serverListView.clear()
        
        if self.serverListObject.serverList == None:
            return
        
        for x in self.serverListObject.serverList:
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
        
        
        x = self.serverListObject.getServerObject(selectedServerString)
        self.currentServer = x
        
        self.hostLineEdit.blockSignals(True)
        self.portSpinBox.blockSignals(True)
        self.bindAnonBox.blockSignals(True)
        self.baseLineEdit.blockSignals(True)
        self.bindLineEdit.blockSignals(True)
        self.passwordLineEdit.blockSignals(True)
        self.tlsCheckBox.blockSignals(True)
        self.methodBox.blockSignals(True)
        
        self.infoGroupBox.setTitle(x.name)
        self.hostLineEdit.setText(x.host)
        self.portSpinBox.setValue(x.port)
        self.bindAnonBox.setChecked(int(x.bindAnon))
        self.baseLineEdit.setText(x.baseDN)
        self.bindLineEdit.setText(x.bindDN)
        self.passwordLineEdit.setText(x.bindPassword)
        self.tlsCheckBox.setChecked(int(x.tls))
        self.methodBox.setCurrentItem(self.authentificationMethods.index(x.authMethod))
        self.bindAnonChanged(x.bindAnon, True)
        
        self.hostLineEdit.blockSignals(False)
        self.portSpinBox.blockSignals(False)
        self.bindAnonBox.blockSignals(False)
        self.baseLineEdit.blockSignals(False)
        self.bindLineEdit.blockSignals(False)
        self.passwordLineEdit.blockSignals(False)
        self.tlsCheckBox.blockSignals(False)
        self.methodBox.blockSignals(False)
        
        if (self.currentServer.authMethod == u"SASL GSSAPI") or x.bindAnon :
            self.passwordLineEdit.setEnabled(False)
            self.bindLineEdit.setEnabled(False)
        else:
            self.passwordLineEdit.setEnabled(True)
            self.bindLineEdit.setEnabled(True)

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

        self.infoGroupBox.setEnabled(True)
        self.infoGroupBox.setTitle(result[0])
        
        serverObject = ServerObject()
        serverObject.name = unicode(result[0])
        
        if self.serverListObject.serverList == None:
            self.serverListObject.serverList = [serverObject]
        else:
            self.serverListObject.serverList.append(serverObject)
        
        self.applyButton.setEnabled(1)
        
        tmpItem = QListViewItem(self.serverListView, result[0])
        tmpItem.setPixmap(0, self.serverIcon)
        self.serverListView.insertItem(tmpItem)
        self.serverListView.setSelected(tmpItem, True)
        
###############################################################################

    def saveServer(self):
        """ Save the changed server values.
        """
        
        if self.currentServer.authMethod == u"SASL GSSAPI":
            self.currentServer.bindDN = u""
            self.currentServer.bindPassword = u""
        
        self.serverListObject.saveSettings(self.serverListObject.serverList)
        
        self.displayServerList()
        self.applyButton.setEnabled(0)
        self.SAVED = True
        
###############################################################################

    def saveCloseDialog(self):
        """ Save server settings and close the dialog.
        """
        
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
            self.serverListObject.deleteServer(unicode(selectedServerString))
            if len(self.serverListObject.serverList) == 0:
                self.infoGroupBox.setEnabled(False)
            
            self.displayServerList()
            self.applyButton.setEnabled(1)

###############################################################################

    def searchBaseDN(self):
        """ Retrieve the baseDN for a given LDAP server.
        
            Currently OpenLDAP, Novell and UMich are supported.
        """
        
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
            result = conObject.search("", ldap.SCOPE_BASE, "(objectClass=*)", ["namingContexts"])
            dnList = result[0][1]['namingContexts']
        
            # Check for Novell
            if dnList[0] == '':
                result = conObject.search("", ldap.SCOPE_BASE)
                dnList = result[0][1]['dsaName']
            
            # Univertity of Michigan aka umich
            # not jet tested
            if dnList[0] == '':
                result = conObject.search("", ldap.SCOPE_BASE, "(objectClass=*)",['database'])
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
        
        widgetBool = True
        if tmpBool or (self.currentServer.authMethod == u"SASL GSSAPI"):
            widgetBool = False
            
        self.passwordLineEdit.setEnabled(widgetBool)
        self.bindLineEdit.setEnabled(widgetBool)
        self.methodBox.setEnabled(widgetBool)
        
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
        
###############################################################################

    def methodChanged(self, position):
        self.currentServer.authMethod = self.authentificationMethods[position]
        
        self.bindLineEdit.blockSignals(True)
        self.passwordLineEdit.blockSignals(True)
        
        if self.currentServer.authMethod == u"SASL GSSAPI":
            self.passwordLineEdit.setEnabled(False)
            self.bindLineEdit.setEnabled(False)
            self.passwordLineEdit.clear()
            self.bindLineEdit.clear()
        else:
            self.passwordLineEdit.setEnabled(True)
            self.bindLineEdit.setEnabled(True)
            self.bindLineEdit.setText(self.currentServer.bindDN)
            self.passwordLineEdit.setText(self.currentServer.bindPassword)
            
        self.bindLineEdit.blockSignals(False)
        self.passwordLineEdit.blockSignals(False)
            
        self.applyButton.setEnabled(1)
