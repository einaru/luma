# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4.QtGui import *
import os
import copy

from base.gui.ImprovedServerDialogDesign import Ui_ImprovedServerDialogDesign
from base.backend.ServerObject import ServerObject
from base.backend.ServerList import ServerList
from base.backend.LumaConnection import LumaConnection
from base.utils.gui.LumaErrorDialog import LumaErrorDialog
from base.utils.backend.LogObject import LogObject
from base.gui.BaseSelector import BaseSelector
import environment


class ImprovedServerDialog(QDialog, Ui_ImprovedServerDialogDesign):

    def __init__(self):
        QDialog.__init__(self)

        self.setupUi(self)
        
        self.SAVED = False
        
        # List of supported authentification methods
        self.authentificationMethods = [u"Simple", u"SASL Plain", u"SASL CRAM-MD5", 
        u"SASL DIGEST-MD5", u"SASL Login", u"SASL GSSAPI", u"SASL EXTERNAL"]
        
        # Dictionary with QListviewItems corresponding to their server subcategories
        self.categoryDictionary = {}

        self.installationPrefix = environment.lumaInstallationPrefix
        self.iconPath = os.path.join(self.installationPrefix, "share", "luma", "icons")
        
        self.networkPixmap = QIcon(os.path.join(self.iconPath, "network32.png"))
        self.credentialsPixmap = QIcon(os.path.join(self.iconPath, "auth32.png"))
        #self.securityPixmap = QIcon(os.path.join(self.iconPath, "security32.png"))        
        self.certificatePixmap = QIcon(os.path.join(self.iconPath, "certificate32.png"))
        self.ldapOptionsPixmap = QIcon(os.path.join(self.iconPath, "config32.png"))
        folderPixmap = QIcon(os.path.join(self.iconPath, "folder.png"))
        
        self.certFileButton.setIcon(folderPixmap)
        self.certKeyFileButton.setIcon(folderPixmap)
        
        self.renameButton.hide()
        self.editCertButton.hide()
        
        self.disableBaseLookup = False
        
        self.labelDictionary = {self.networkLabel: 1, self.credentialLabel: 2, 
            self.encryptionLabel: 1, self.authLabel: 2, self.ldapOptLabel: 4}
        
        # Listview object corresponding to the widget id for the stack
        self.categoryDictionary = {}
        
        self.saveButton.setEnabled(0)
        
        # Show blank widget first, no server selected
        self.configStack.setCurrentIndex(5)
        
        # FIXME: qt4 migration needed
        #self.originalBackGroundColor = self.networkLabel.paletteBackgroundColor()
        
        self.serverListObject = ServerList()
        self.serverListObject.readServerList()
        
        # Server which is currently selected.
        self.currentServer = None
        
        # Needed for closing the children of the old server
        self.oldServerItem = None
        
        self.currentServerItem = None
        self.currentCategoryItem = None
        
        self.serverListView.setSortingEnabled(True)
        self.serverListView.sortItems(0, QtCore.Qt.AscendingOrder)
        
        self.displayServerList()

        QtCore.QObject.connect(self.serverListView,QtCore.SIGNAL("currentItemChanged (QTreeWidgetItem *,QTreeWidgetItem *)"),self.serverTmpSelected)
        #QtCore.QObject.connect(self.serverListView,QtCore.SIGNAL("itemSelectionChanged()"),self.serverSelected)

###############################################################################

    def displayServerList(self):
        """ Initialize the listview with the serverlist.
        """
        
        self.serverListView.clear()
        self.oldServerItem = None
        self.categoryDictionary = {}
        self.currentServer = None
        
        self.selectAServer(None)
        
        if self.serverListObject.serverList == None:
            return
            
        for x in self.serverListObject.serverList:
            serverItem = QTreeWidgetItem(self.serverListView)
            serverItem.setText(0, x.name)
            self.buildCategories(serverItem)
            
###############################################################################
    def selectAServer(self, serverItem):

        if serverItem == None:
            self.oldServerItem = serverItem
            self.currentServerItem = serverItem
            self.configStack.setCurrentIndex(5)
            self.serverNameStack.setCurrentIndex(0)
            self.serverLabel.setText(self.trUtf8("<b>No server selected</b>"))
            self.renameButton.hide()
        else:
            self.oldServerItem = serverItem
            self.currentServerItem = serverItem
            self.serverLabel.setText(QtCore.QString("<b>%1</b>").arg(serverItem.text(0)))
            self.configStack.setCurrentIndex(0)
            self.serverNameStack.setCurrentIndex(0)
            self.renameButton.show()

            selectedServerString = unicode(serverItem.text(0))
            x = self.serverListObject.getServerObject(selectedServerString)
            self.currentServer = x
            
            self.initializeFields()

            # Activate/deactivate certificate fields
            if self.currentServer.encryptionMethod == u"None":
                for key, value in self.categoryDictionary.items():
                    if value == 3:
                        listItem = key
                        break
                    
                listItem.setHidden(True)
            else:
                for key, value in self.categoryDictionary.items():
                    if value == 3:
                        listItem = key
                        break
                    
                listItem.setHidden(False)
        
###############################################################################

    def serverTmpSelected(self, current, previous):
        import sys
        sys.stdout.write("serverTmpSelected(): ")
        try:
            sys.stdout.write("(%s, " % (current.text(0)))
        except:
            sys.stdout.write("(None, ")
        try:
            sys.stdout.write("%s)" % (previous.text(0)))
        except:
            sys.stdout.write("None)")
        print ""

        if current == None:
            print "Should this ever happen?"
            self.selectAServer(current)
            return

        serverItem = current
        if current.parent():
            serverItem = current.parent()
        prevServerItem = previous
        if previous and previous.parent():
            prevServerItem = previous.parent()

        if serverItem != prevServerItem:
            if prevServerItem:
                #prevServerItem.setExpanded(False)
                print "collapseOld"
            self.selectAServer(serverItem)
            #self.serverListView.emit(QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem *,int)"), current, 0)
            serverItem.setExpanded(True)

        if current.parent(): # Subitem selected, show appropriate widget
            self.serverNameStack.setCurrentIndex(0)
            self.currentCategoryItem = current
            widgetId = self.categoryDictionary[current]
            self.configStack.setCurrentIndex(widgetId)
        else:
            self.selectAServer(serverItem)

###############################################################################

    def serverSelected(self):
        # FIXME: is there another way of finding selected item?
        serverItems = self.serverListView.selectedItems()
        if len(serverItems) < 1:
            serverItem = None
        else:
            serverItem = serverItems[0]

        import sys
        sys.stdout.write("serverSelected: (serverItem, oldServerItem)")
        try:
            sys.stdout.write("(%s, " % (serverItem.text(0)))
        except:
            sys.stdout.write("(None, ")
        try:
            sys.stdout.write("%s)" % (self.oldServerItem.text(0)))
        except:
            sys.stdout.write("None)")
        sys.stdout.write(", selectedItems(): %s" % ([x.text(0).__str__() for x in self.serverListView.selectedItems()]))
        print ""

        ## Nothing selected
        if serverItem == None:
            print "Nothing selected. Should not happen?"
            if not (self.oldServerItem == None):
                self.oldServerItem.setExpanded(False)
                while self.oldServerItem.takeChild(0):
                    print "takeChild"
            self.oldServerItem = None
            self.serverLabel.setText(self.trUtf8("<b>No server selected</b>"))
            self.configStack.setCurrentIndex(5)
            self.renameButton.hide()
            return
    
        # Server selected
        if serverItem.parent() == None:
            if not (self.oldServerItem == None):
                self.categoryDictionary = {}
                self.oldServerItem.setExpanded(False)
                while self.oldServerItem.takeChild(0):
                    print "takeChild"
                self.oldServerItem = None
                        
                
            self.oldServerItem = serverItem
            self.currentServerItem = serverItem
            
            self.serverLabel.setText(QtCore.QString("<b>%1</b>").arg(serverItem.text(0)))
            self.configStack.setCurrentIndex(0)
            self.serverNameStack.setCurrentIndex(0)
            self.renameButton.show()
            
            
            selectedServerString = unicode(serverItem.text(0))
            x = self.serverListObject.getServerObject(selectedServerString)
            self.currentServer = x
            
            #self.initializeFields()
            #self.buildCategories(serverItem)
            
            # Activate/deactivate certificate fields
            if self.currentServer.encryptionMethod == u"None":
                for key, value in self.categoryDictionary.items():
                    if value == 3:
                        listItem = key
                        break
                    
                listItem.setHidden(True)
            else:
                for key, value in self.categoryDictionary.items():
                    if value == 3:
                        listItem = key
                        break
                    
                listItem.setHidden(False)
            
            serverItem.setExpanded(True)
            
        # Subcategory from server selected
        if serverItem in self.categoryDictionary.keys():
            self.serverNameStack.setCurrentIndex(0)
            self.currentCategoryItem = serverItem
            widgetId = self.categoryDictionary[serverItem]
            self.configStack.setCurrentIndex(widgetId)

###############################################################################
        
    def initializeFields(self):
        self.networkLabel.blockSignals(True)
        self.credentialLabel.blockSignals(True)
        self.encryptionLabel.blockSignals(True)
        self.authLabel.blockSignals(True)
        self.ldapOptLabel.blockSignals(True)
        self.hostnameEdit.blockSignals(True)
        self.portBox.blockSignals(True)
        self.anonBindBox.blockSignals(True)
        self.bindAsEdit.blockSignals(True)
        self.bindPasswordEdit.blockSignals(True)
        self.encryptionBox.blockSignals(True)
        self.authentificationBox.blockSignals(True)
        self.serverCertBox.blockSignals(True)
        self.clientCertBox.blockSignals(True)
        self.certFileEdit.blockSignals(True)
        self.certKeyFileEdit.blockSignals(True)
        self.aliasBox.blockSignals(True)
        self.baseBox.blockSignals(True)
        self.baseDNView.blockSignals(True)
        
        x = self.currentServer
        
        self.networkLabel.setText(x.host + ":" + str(x.port))
        
        if x.bindAnon:
            self.credentialLabel.setText(self.trUtf8("Anonymous"))
        else:
            self.credentialLabel.setText(x.bindDN)
            
        self.encryptionLabel.setText(x.encryptionMethod)
        self.authLabel.setText(x.authMethod)
        
        if x.autoBase:
            self.ldapOptLabel.setText(self.trUtf8("Automatic"))
        else:
            baseString = ""
            for tmpBase in x.baseDN:
                baseString += tmpBase + "\n"
            self.ldapOptLabel.setText(baseString)
            
        self.showBaseWidgets()
            
        
        self.hostnameEdit.setText(x.host)
        self.portBox.setValue(x.port)
        self.anonBindBox.setChecked(x.bindAnon)
        self.bindAsEdit.setText(x.bindDN)
        self.bindPasswordEdit.setText(x.bindPassword)
        
        if x.encryptionMethod == u"None":
            self.encryptionBox.setCurrentIndex(0)
            #self.validateBox.setEnabled(False)
            #self.useClientCertBox.setEnabled(False)
        elif x.encryptionMethod == u"TLS":
            self.encryptionBox.setCurrentIndex(1)
            #self.validateBox.setEnabled(True)
            #self.useClientCertBox.setEnabled(True)
        elif x.encryptionMethod == u"SSL":
            self.encryptionBox.setCurrentIndex(2)
            #self.validateBox.setEnabled(True)
            #self.useClientCertBox.setEnabled(True)
        
        # FIXME: qt4 migration needed
        #self.authentificationBox.setCurrentText(x.authMethod)
        self.showAuthWidgets()
        
        if x.checkServerCertificate == u"never":
            self.serverCertBox.setCurrentIndex(0)
        elif x.checkServerCertificate == u"try":
            self.serverCertBox.setCurrentIndex(1)
        elif x.checkServerCertificate == u"allow":
            self.serverCertBox.setCurrentIndex(2)
        elif x.checkServerCertificate == u"demand":
            self.serverCertBox.setCurrentIndex(3)
        
        self.clientCertBox.setChecked(x.useCertificate)
        self.certFileEdit.setText(x.clientCertFile)
        self.certKeyFileEdit.setText(x.clientCertKeyfile)
        self.displayCertWidgets()
        
        self.aliasBox.setChecked(x.followAliases)
        self.baseBox.setChecked(x.autoBase)
        
        self.displayBaseDnList()
        
        
        self.networkLabel.blockSignals(False)
        self.credentialLabel.blockSignals(False)
        self.encryptionLabel.blockSignals(False)
        self.authLabel.blockSignals(False)
        self.ldapOptLabel.blockSignals(False)
        self.hostnameEdit.blockSignals(False)
        self.portBox.blockSignals(False)
        self.anonBindBox.blockSignals(False)
        self.bindAsEdit.blockSignals(False)
        self.bindPasswordEdit.blockSignals(False)
        self.encryptionBox.blockSignals(False)
        self.authentificationBox.blockSignals(False)
        self.serverCertBox.blockSignals(False)
        self.clientCertBox.blockSignals(False)
        self.certFileEdit.blockSignals(False)
        self.certKeyFileEdit.blockSignals(False)
        self.aliasBox.blockSignals(False)
        self.baseBox.blockSignals(False)
        self.baseDNView.blockSignals(False)
        
###############################################################################

    def buildCategories(self, serverItem):
        subItem = QTreeWidgetItem(serverItem)
        subItem.setText(0, "Network options") 
        self.categoryDictionary[subItem] = 1
        subItem.setIcon(0, self.networkPixmap)

        subItem = QTreeWidgetItem(serverItem)
        subItem.setText(0, "Authentification")
        self.categoryDictionary[subItem] = 2
        subItem.setIcon(0, self.credentialsPixmap)
        
        subItem = QTreeWidgetItem(serverItem)
        subItem.setText(0, "LDAP Options")
        self.categoryDictionary[subItem] = 4
        subItem.setIcon(0, self.ldapOptionsPixmap)
        
        subItem = QTreeWidgetItem(serverItem)
        subItem.setText(0, "Certificates")
        self.categoryDictionary[subItem] = 3
        subItem.setIcon(0, self.certificatePixmap)
        
###############################################################################

    def showSummary(self):
        self.configStack.setCurrentIndex(0)
        self.serverListView.setItemSelected(self.currentCategoryItem, False)
        self.serverListView.setItemSelected(self.currentServerItem, True)
        
###############################################################################

    def renameServer(self):
        self.renameEdit.setText(self.currentServer.name)
        self.renameEdit.selectAll()
        self.renameEdit.setFocus()
        self.serverNameStack.setCurrentIndex(1)
        
###############################################################################

    def cancelRename(self):
        self.serverNameStack.setCurrentIndex(0)
        
###############################################################################

    def hostnameChanged(self, serverString):
        self.currentServer.host = unicode(serverString)
        self.saveButton.setEnabled(True)
        
###############################################################################

    def portChanged(self, portNumber):
        self.currentServer.port = portNumber
        self.saveButton.setEnabled(True)
        
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
        
        if tmpBool:
            self.editCertButton.show()
            listItem = None
            for key, value in self.categoryDictionary.items():
                if value == 3:
                    listItem = key
                    break
                    
            listItem.setVisible(True)
        else:
            self.editCertButton.hide()
            
            listItem = None
            for key, value in self.categoryDictionary.items():
                if value == 3:
                    listItem = key
                    break
                    
            listItem.setVisible(False)
        
        # Set port numbers according to the encryption method
        self.portBox.blockSignals(True)
        
        portValue = 389
        if encryptionMethod == u"SSL":
            portValue = 636
            
        self.portBox.setValue(portValue)
        self.currentServer.port = portValue
        
        self.portBox.blockSignals(False)
        
        self.saveButton.setEnabled(True)
    
        
###############################################################################

    def showCertWidget(self):
        self.configStack.setCurrentIndex(3)
        
        listItem = None
        for key, value in self.categoryDictionary.items():
            if value == 3:
                listItem = key
                break
        self.serverListView.setItemSelected(listItem, True)
        
###############################################################################

    def saveCloseDialog(self):
        """ Save server settings and close the dialog.
        """
        
        self.saveSettings()
        self.accept()
        
###############################################################################

    def saveSettings(self):
        self.serverListObject.saveSettings(self.serverListObject.serverList)
        
        #self.displayServerList()
        self.saveButton.setEnabled(False)
        self.SAVED = True

###############################################################################

    def displayBaseDnList(self):
        self.baseDNView.clear()
        
        if self.currentServer.autoBase:
            self.baseDNView.hide()
            self.manageBaseButton.hide()
        else:
            self.baseDNView.show()
            self.manageBaseButton.show()
            
        if self.disableBaseLookup:
            return
            
        if self.currentServer.autoBase:
            item = QListWidgetItem(self.trUtf8("Automatic retrieval"), self.baseDNView)
            #success, result = self.searchBaseDn()
            
            #if success:
            #    for x in result:
            #        item = QListWidgetItem(self.baseDNView, x)
            #else:
            #    item = QListWidgetItem(self.baseDNView, result)
        else:
            for x in self.currentServer.baseDN:
                item = QListWidgetItem(x, self.baseDNView)
                
###############################################################################
                
    def searchBaseDn(self):
        """ Retrieve the baseDN for a given LDAP server.
        
            Currently OpenLDAP, Novell and UMich are supported.
        """

        connection = LumaConnection(self.currentServer)
        success, baseList, exceptionObject = connection.getBaseDNList()
        
        if success:
            return True, baseList
        else:
            errorMsg = self.trUtf8("Could not retrieve baseDN for LDAP server at host/ip:")
            errorMsg.append("<br><b>" + unicode(self.currentServer.host) + "</b><br><br>")
            errorMsg.append("Reason: ")
            errorMsg.append(str(exceptionObject))
            return False, errorMsg
            
###############################################################################

    def anonBindChanged(self, activated):
        if activated == 1:
            self.currentServer.bindAnon = True
        else:
            self.currentServer.bindAnon = False
            
        self.showAuthWidgets()
        self.saveButton.setEnabled(True)
            
###############################################################################

    def showAuthWidgets(self):
        if self.currentServer.bindAnon:
            self.authMechanismLabel.hide()
            self.authentificationBox.hide()
            self.bindAsLabel.hide()
            self.bindAsEdit.hide()
            self.bindPasswordLabel.hide()
            self.bindPasswordEdit.hide()
        else:
            self.authMechanismLabel.show()
            self.authentificationBox.show()
            
            authMethod = self.currentServer.authMethod
            if (authMethod == u"SASL GSSAPI") or (u"SASL EXTERNAL" == authMethod):
                self.bindAsLabel.hide()
                self.bindAsEdit.hide()
                self.bindPasswordLabel.hide()
                self.bindPasswordEdit.hide()
            else:
                self.bindAsLabel.show()
                self.bindAsEdit.show()
                self.bindPasswordLabel.show()
                self.bindPasswordEdit.show()
        
###############################################################################

    def authMethodChanged(self, methodString):
        self.currentServer.authMethod = unicode(self.authentificationBox.currentText())
        
        self.bindAsEdit.blockSignals(True)
        self.bindPasswordEdit.blockSignals(True)
        
        authMethod = self.currentServer.authMethod
        if (u"SASL GSSAPI" == authMethod) or (u"SASL EXTERNAL" == authMethod):
            self.bindAsEdit.clear()
            self.bindPasswordEdit.clear()
        else:
            self.bindAsEdit.setText(self.currentServer.bindDN)
            self.bindPasswordEdit.setText(self.currentServer.bindPassword)
        
        self.bindAsEdit.blockSignals(False)
        self.bindPasswordEdit.blockSignals(False)
        
        self.showAuthWidgets()
        
        self.saveButton.setEnabled(True)
        
###############################################################################

    def aliasChanged(self, activated):
        if activated == 1:
            self.currentServer.followAliases = True
        else:
            self.currentServer.followAliases = False
            
        self.saveButton.setEnabled(True)
        
###############################################################################

    def autoBaseChanged(self, activated):
        if activated == 1:
            self.currentServer.autoBase = True
        else:
            self.currentServer.autoBase = False
            
        self.displayBaseDnList()
        self.showBaseWidgets()
        self.saveButton.setEnabled(True)
        
###############################################################################

    def showBaseWidgets(self):
        if self.currentServer.autoBase:
            self.baseDNView.hide()
            self.manageBaseButton.hide()
        else:
            self.baseDNView.show()
            self.manageBaseButton.show()
            
###############################################################################

    def showBaseDialog(self):
        connection = LumaConnection(self.currentServer)
        dialog = BaseSelector()
        
        tmpText = dialog.baseLabel.text().arg(self.currentServer.name)
        dialog.baseLabel.setText(tmpText)
        
        dialog.connection = connection
        dialog.baseList = copy.deepcopy(self.currentServer.baseDN)
        dialog.displayBase()
        dialog.exec_loop()
        if dialog.result() == QDialog.Accepted:
            self.saveButton.setEnabled(True)
            self.currentServer.baseDN = copy.deepcopy(dialog.baseList)
            self.displayBaseDnList()
    
###############################################################################

    def serverCertCheckChanged(self, methodNumber):
        validityType = u"demand"
        
        if methodNumber == 0:
            validityType = u"never"
        elif methodNumber == 1:
            validityType = u"try"
        elif methodNumber == 2:
            validityType = u"allow"
        elif methodNumber == 3:
            validityType = u"demand"
            
        self.currentServer.checkServerCertificate = validityType
        self.saveButton.setEnabled(True)
        
###############################################################################

    def clientCertsChanged(self, activated):
        if activated == 1:
            self.currentServer.useCertificate = True
        else:
            self.currentServer.useCertificate = False
            
        self.displayCertWidgets()
        self.saveButton.setEnabled(True)
        
###############################################################################

    def displayCertWidgets(self):
        if self.currentServer.useCertificate:
            self.certKeyLabel.show()
            self.certLabel.show()
            self.certFileEdit.show()
            self.certKeyFileEdit.show()
            self.certFileButton.show()
            self.certKeyFileButton.show()
        else:
            self.certKeyLabel.hide()
            self.certLabel.hide()
            self.certFileEdit.hide()
            self.certKeyFileEdit.hide()
            self.certFileButton.hide()
            self.certKeyFileButton.hide()
            
###############################################################################

    def certFileChanged(self, tmpText):
        tmpFileName = unicode(tmpText)
        
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
            self.certFileEdit.setPaletteBackgroundColor(QtCore.Qt.red)
        else:
            self.certFileEdit.unsetPalette()
        
        # Now do internal stuff like updating the ServerObject 
        # and activate apply button
        self.currentServer.clientCertFile = tmpFileName
        self.saveButton.setEnabled(True)
        
###############################################################################

    def certKeyFileChanged(self, tmpText):
        tmpFileName = unicode(tmpText)
        
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
            self.certKeyFileEdit.setPaletteBackgroundColor(QtCore.Qt.red)
        else:
            self.certKeyFileEdit.unsetPalette()
        
        # Now do internal stuff like updating the ServerObject 
        # and activate apply button
        self.currentServer.clientCertKeyfile = tmpFileName
        self.saveButton.setEnabled(True)
    
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
            
        self.certKeyFileEdit.setText(unicode(filename))
        
###############################################################################

    def saveRename(self):
        tmpName = unicode(self.renameEdit.text())
        
        if tmpName == "":
            self.serverNameStack.setCurrentIndex(0)
            return
            
        checkName = self.serverListObject.getServerObject(tmpName)
        if checkName == None:
            self.currentServer.name = tmpName
            self.serverLabel.setText("<b>" + tmpName + "</b>")
            self.currentServerItem.setText(0, tmpName)
            self.serverNameStack.setCurrentIndex(0)
            self.saveButton.setEnabled(True)
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("A server with the name <b>%1</b> already exists.").arg(tmpName)
            errorMsg.append("<br><br>")
            errorMsg.append(self.trUtf8("Please choose another name."))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
    
###############################################################################

    def bindAsChanged(self, tmpString):
        self.currentServer.bindDN = unicode(tmpString)
        self.saveButton.setEnabled(True)
    
###############################################################################

    def bindPasswordChanged(self, tmpString):
        self.currentServer.bindPassword = unicode(tmpString)
        self.saveButton.setEnabled(True)
        
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

        serverObject = ServerObject()
        serverObject.name = unicode(result[0])
        
        if self.serverListObject.serverList == None:
            self.serverListObject.serverList = [serverObject]
        else:
            self.serverListObject.serverList.append(serverObject)
        
        self.saveButton.setEnabled(True)
        self.displayServerList()
        
###############################################################################
        
    def deleteServer(self):
        """ Delete the currently selected server.
        """
        
        if self.currentServer == None:
            return
        selectedServerString = self.currentServer.name
        tmpDialog = QMessageBox(self.trUtf8("Delete Server?"),
                self.trUtf8("Do you really want to delete server <b>%1</b>?").arg(selectedServerString),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.Cancel,
                QMessageBox.NoButton,
                self)
        tmpDialog.setIcon(QIcon(os.path.join(self.iconPath, "warning_big.png")))
        tmpDialog.exec_loop()
        if (tmpDialog.result() == 1):
            self.serverListObject.deleteServer(selectedServerString)
            
            self.displayServerList()
            self.saveButton.setEnabled(1)
            
###############################################################################

    def selectServer(self, serverName):
        tmpItem = self.serverListView.firstChild()
        if tmpItem == 0:
            return
            
        while not (unicode(tmpItem.text(0)) == serverName):
            tmpItem = tmpItem.nextSibling()
            if tmpItem.nextSibling() == 0:
                return
            
                
        if unicode(tmpItem.text(0)) == serverName:
            self.serverListView.setItemSelected(tmpItem, True)
        
