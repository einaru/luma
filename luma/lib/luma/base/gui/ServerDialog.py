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
import copy

from qt import *


from base.gui.ServerDialogDesign import ServerDialogDesign
from base.backend.ServerObject import ServerObject
from base.backend.ServerList import ServerList
import environment
from base.gui.BaseSelector import BaseSelector
from base.backend.LumaConnection import LumaConnection
from base.utils.gui.LumaErrorDialog import LumaErrorDialog
from base.utils.backend.LogObject import LogObject

class ServerDialog(ServerDialogDesign):
    """The dialog for managing all server information.
    """

    def __init__(self, parent= None):
        ServerDialogDesign.__init__(self, parent)
        
        self.authentificationMethods = [u"Simple", u"SASL Plain", u"SASL CRAM-MD5", 
        u"SASL DIGEST-MD5", u"SASL Login", u"SASL GSSAPI", u"SASL EXTERNAL"]

        self._PREFIX = environment.lumaInstallationPrefix
        
        self.iconPath = os.path.join(self._PREFIX, "share", "luma", "icons")
        folderPixmap = QPixmap(os.path.join(self.iconPath, "folder.png"))
        self.certFileButton.setPixmap(folderPixmap)
        self.certKeyFileButton.setPixmap(folderPixmap)
        self.networkLabel.setPixmap(QPixmap(os.path.join(self.iconPath, "worldmedium.png")))
        self.authLabel.setPixmap(QPixmap(os.path.join(self.iconPath, "passwordmedium.png")))
        self.guiParent = parent

        self.applyButton.setEnabled(0)

        self.serverListObject = ServerList()
        
        # Server which is currently selected.
        self.currentServer = None

        
        self.serverListObject.readServerList()
          
        if self.serverListObject.serverList == None:
            self.serverWidget.setEnabled(False)
        elif len(self.serverListObject.serverList) == 0:
            self.serverWidget.setEnabled(False)

        self.serverIcon = QPixmap(os.path.join(self._PREFIX, "share", "luma", "icons", "server.png"))
        
        # Indicates if the serverlist has been permanently edited.
        # Needed when we use the apply button and cancel the dialog afterwards.
        # But the changes have to be applied. 
        # 'dialog.result() == QDialog.Accepted' is not enough.
        self.SAVED = False
        
        # Will be set to the currently selected server
        self.currentServer = None
        
        self.disableBaseLookup = False
        
        self.originalBackGroundColor = self.certFileEdit.paletteBackgroundColor()
        
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
        
        selectedServerString = unicode(tmpItem.text(0))
        x = self.serverListObject.getServerObject(selectedServerString)
        self.currentServer = x
        
        self.hostLineEdit.blockSignals(True)
        self.portSpinBox.blockSignals(True)
        self.bindAnonBox.blockSignals(True)
        self.bindLineEdit.blockSignals(True)
        self.passwordLineEdit.blockSignals(True)
        self.methodBox.blockSignals(True)
        self.aliasBox.blockSignals(True)
        self.validateBox.blockSignals(True)
        self.useClientCertBox.blockSignals(True)
        self.certFileEdit.blockSignals(True)
        self.certKeyfileEdit.blockSignals(True)
        
        self.hostLineEdit.setText(x.host)
        self.portSpinBox.setValue(x.port)
        self.bindAnonBox.setChecked(int(x.bindAnon))
        self.bindLineEdit.setText(x.bindDN)
        self.passwordLineEdit.setText(x.bindPassword)
        
        if x.encryptionMethod == u"None":
            self.encryptionBox.setCurrentItem(0)
            self.validateBox.setEnabled(False)
            self.useClientCertBox.setEnabled(False)
        elif x.encryptionMethod == u"TLS":
            self.encryptionBox.setCurrentItem(1)
            self.validateBox.setEnabled(True)
            self.useClientCertBox.setEnabled(True)
        elif x.encryptionMethod == u"SSL":
            self.encryptionBox.setCurrentItem(2)
            self.validateBox.setEnabled(True)
            self.useClientCertBox.setEnabled(True)
            
        if x.checkServerCertificate == u"never":
            self.validateBox.setCurrentItem(0)
        elif x.checkServerCertificate == u"allow":
            self.validateBox.setCurrentItem(1)
        elif x.checkServerCertificate == u"try":
            self.validateBox.setCurrentItem(2)
        elif x.checkServerCertificate == u"demand":
            self.validateBox.setCurrentItem(3)
            
        self.useClientCertBox.setChecked(x.useCertificate)
        self.certFileEdit.setText(x.clientCertFile)
        self.certKeyfileEdit.setText(x.clientCertKeyfile)
        
        self.enableClientCertWidgets(x.useCertificate)
        
        self.methodBox.setCurrentText(x.authMethod)
        self.bindAnonChanged(x.bindAnon, True)
        self.aliasBox.setChecked(int(x.followAliases))
        
        self.hostLineEdit.blockSignals(False)
        self.portSpinBox.blockSignals(False)
        self.bindAnonBox.blockSignals(False)
        self.bindLineEdit.blockSignals(False)
        self.passwordLineEdit.blockSignals(False)
        self.methodBox.blockSignals(False)
        self.aliasBox.blockSignals(False)
        self.validateBox.blockSignals(False)
        self.useClientCertBox.blockSignals(False)
        self.certFileEdit.blockSignals(False)
        self.certKeyfileEdit.blockSignals(False)
        
        authMethod = self.currentServer.authMethod
        if (authMethod == u"SASL GSSAPI") or (authMethod == u"SASL EXTERNAL") or x.bindAnon :
            self.passwordLineEdit.setEnabled(False)
            self.bindLineEdit.setEnabled(False)
        else:
            self.passwordLineEdit.setEnabled(True)
            self.bindLineEdit.setEnabled(True)
            
        self.manageBaseButton.setEnabled(not self.currentServer.autoBase)
        self.baseBox.blockSignals(True)
        self.baseBox.setChecked(self.currentServer.autoBase)
        self.baseBox.blockSignals(False)
        self.displayBase()

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

        self.serverWidget.setEnabled(True)
        
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
        
        self.currentServer = serverObject
        
        self.disableBaseLookup = True
        self.serverListView.setSelected(tmpItem, True)
        self.disableBaseLookup = False
        
###############################################################################

    def saveServer(self):
        """ Save the changed server values.
        """
        
        authMethod = self.currentServer.authMethod
        if (authMethod == u"SASL GSSAPI") or (authMethod == u"SASL EXTERNAL"):
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
        tmpDialog = QMessageBox(self.trUtf8("Delete Server?"),
                self.trUtf8("Do you really want to delete the Server?"),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.Cancel,
                QMessageBox.NoButton,
                self)
        tmpDialog.setIconPixmap(QPixmap(os.path.join(self._PREFIX, "share", "luma", "icons", "warning_big.png")))
        tmpDialog.exec_loop()
        if (tmpDialog.result() == 1):
            self.serverListObject.deleteServer(unicode(selectedServerString))
            if len(self.serverListObject.serverList) == 0:
                self.serverWidget.setEnabled(False)
            
            self.displayServerList()
            self.applyButton.setEnabled(1)

###############################################################################

    def searchBaseDN(self):
        """ Retrieve the baseDN for a given LDAP server.
        
            Currently OpenLDAP, Novell and UMich are supported.
        """

        connection = LumaConnection(self.currentServer)
        success, baseList, exceptionObject = connection.getBaseDNList()
        
        if success:
            return baseList
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not retrieve baseDN for LDAP server at host/ip:")
            errorMsg.append("<br><b>" + unicode(self.currentServer.host) + "</b><br><br>")
            errorMsg.append("Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            return []

###############################################################################

    def tlsChanged(self, tmpBool):
        tlsBool = self.tlsCheckBox.isChecked()
        
        if tlsBool:
            # Set port value
            self.portSpinBox.setValue(636)
            
            # Enable certificate widgets
            self.useClientCertBox.setEnabled(True)
            
            tmpBool = self.useClientCertBox.isChecked()
            
            self.certFileEdit.setEnabled(tmpBool)
            self.certKeyfileEdit.setEnabled(tmpBool)
            self.certFileButton.setEnabled(tmpBool)
            self.certKeyFileButton.setEnabled(tmpBool)
        else:
            # Set port value
            self.portSpinBox.setValue(389)
            
            # Enable certificate widgets
            self.useClientCertBox.setEnabled(False)
            self.certFileEdit.setEnabled(False)
            self.certKeyfileEdit.setEnabled(False)
            self.certFileButton.setEnabled(False)
            self.certKeyFileButton.setEnabled(False)
            
        self.currentServer.tls = tlsBool
        self.applyButton.setEnabled(True)
            
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
        authMethod = self.currentServer.authMethod
        if tmpBool or (authMethod == u"SASL GSSAPI") or (authMethod == u"SASL EXTERNAL"):
            widgetBool = False
            
        self.passwordLineEdit.setEnabled(widgetBool)
        self.bindLineEdit.setEnabled(widgetBool)
        self.methodBox.setEnabled(not tmpBool)
        
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
        self.currentServer.authMethod = unicode(self.methodBox.currentText())
        #self.currentServer.authMethod = self.authentificationMethods[position]
        
        self.bindLineEdit.blockSignals(True)
        self.passwordLineEdit.blockSignals(True)
        
        authMethod = self.currentServer.authMethod
        if (authMethod == u"SASL GSSAPI") or (u"SASL EXTERNAL" == authMethod):
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
            
        self.applyButton.setEnabled(True)
        
###############################################################################

    def useServerBase(self):
        self.applyButton.setEnabled(True)
        automaticBase = self.baseBox.isChecked()
        self.currentServer.autoBase = automaticBase
        self.manageBaseButton.setEnabled(not automaticBase)
        self.displayBase()
        
###############################################################################

    def displayBase(self):
        self.baseDNView.clear()
        
        if self.disableBaseLookup:
            return
            
        if self.currentServer.autoBase:
            baseList = self.searchBaseDN()
            for x in baseList:
                item = QListViewItem(self.baseDNView, x)
        else:
            for x in self.currentServer.baseDN:
                item = QListViewItem(self.baseDNView, x)

###############################################################################

    def manageBaseDN(self):
        connection = LumaConnection(self.currentServer)
        dialog = BaseSelector()
        
        tmpText = dialog.baseLabel.text().arg(self.currentServer.name)
        dialog.baseLabel.setText(tmpText)
        
        dialog.connection = connection
        dialog.baseList = copy.deepcopy(self.currentServer.baseDN)
        dialog.displayBase()
        dialog.exec_loop()
        if dialog.result() == QDialog.Accepted:
            self.applyButton.setEnabled(1)
            self.currentServer.baseDN = copy.deepcopy(dialog.baseList)
            self.displayBase()

###############################################################################

    def aliasesChanged(self):
        self.applyButton.setEnabled(True)
        self.currentServer.followAliases = self.aliasBox.isChecked()

###############################################################################

    def certFileChanged(self, tmpFileName):
        tmpFileName = unicode(tmpFileName)
        
        fileWarning = False
        # Now do file checking
        if os.path.isdir(tmpFileName):
            fileWarning = True
        else:
            try:
                if os.path.isfile(tmpFileName) or os.path.islink(tmpFileName):
                    open(tmpFileName, "r")
                else:
                    fileWarning = True
            except IOError, e:
                fileWarning = True
                
        if tmpFileName == "":
            fileWarning = False
        
        if fileWarning:
            self.certFileEdit.setPaletteBackgroundColor(Qt.red)
        else:
            self.certFileEdit.unsetPalette()
        
        # Now do internal stuff like updating the ServerObject 
        # and activate apply button
        self.currentServer.clientCertFile = tmpFileName
        self.applyButton.setEnabled(True)
        
###############################################################################

    def certKeyFileChanged(self, tmpFileName):
        tmpFileName = unicode(tmpFileName)
        
        fileWarning = False
        # Now do file checking
        if os.path.isdir(tmpFileName):
            fileWarning = True
        else:
            try:
                if os.path.isfile(tmpFileName) or os.path.islink(tmpFileName):
                    open(tmpFileName, "r")
                else:
                    fileWarning = True
            except IOError, e:
                fileWarning = True
                
        if tmpFileName == "":
            fileWarning = False
        
        if fileWarning:
            self.certKeyfileEdit.setPaletteBackgroundColor(Qt.red)
        else:
            self.certKeyfileEdit.unsetPalette()
        
        # Now do internal stuff like updating the ServerObject 
        # and activate apply button
        self.currentServer.clientCertKeyfile = tmpFileName
        self.applyButton.setEnabled(True)
        
###############################################################################

    def showCertFileDialog(self):
        filename = QFileDialog.getOpenFileName(\
            None,
            None,
            None, None,
            self.trUtf8("Select certificate file"),
            None, 1)
            
        self.certFileEdit.setText(unicode(filename))

        
###############################################################################

    def showCertKeyFileDialog(self):
        filename = QFileDialog.getOpenFileName(\
            None,
            None,
            None, None,
            self.trUtf8("Select certificate key file"),
            None, 1)
            
        self.certKeyfileEdit.setText(unicode(filename))
        
###############################################################################

    def encryptionChanged(self, typeNumber):
        encryptionMethod = u"None"
        
        if typeNumber == 0:
            encryptionMethod = u"None"
        elif typeNumber == 1:
            encryptionMethod = u"TLS"
        elif typeNumber == 2:
            encryptionMethod = u"SSL"
        
        self.currentServer.encryptionMethod = encryptionMethod
        
        tmpBool = False
        if typeNumber > 0:
            tmpBool = True
        self.validateBox.setEnabled(tmpBool)
        self.useClientCertBox.setEnabled(tmpBool)
        
        if self.currentServer.useCertificate:
            self.enableClientCertWidgets(True)
        else:
            self.enableClientCertWidgets(False)
        
        # Set port numbers according to the encryption method
        self.portSpinBox.blockSignals(True)
        
        portValue = 389
        if encryptionMethod == u"SSL":
            portValue = 636
            
        self.portSpinBox.setValue(portValue)
        self.currentServer.port = portValue
            
        self.portSpinBox.blockSignals(True)
        
        self.applyButton.setEnabled(True)
        
###############################################################################

    def validityCheckChanged(self, typeNumber):
        validityType = u"demand"
        
        if typeNumber == 0:
            validityType = u"never"
        elif typeNumber == 1:
            validityType = u"allow"
        elif typeNumber == 2:
            validityType = u"try"
        elif typeNumber == 3:
            validityType = u"demand"
            
        self.currentServer.checkServerCertificate = validityType
        self.applyButton.setEnabled(True)
        
###############################################################################

    def enableClientCerts(self, toggleBool):
        if toggleBool >= 1:
            self.currentServer.useCertificate = True
        else:
            self.currentServer.useCertificate = False
            
        self.applyButton.setEnabled(True)
        self.enableClientCertWidgets(toggleBool)
        
###############################################################################

    def enableClientCertWidgets(self, enableBool):
        self.certFileEdit.setEnabled(enableBool)
        self.certKeyfileEdit.setEnabled(enableBool)
        self.certFileButton.setEnabled(enableBool)
        self.certKeyFileButton.setEnabled(enableBool)
    
    
