import os

from qt import *

from base.gui.ServerDialogDesign import ServerDialogDesign
from base.backend.ServerObject import ServerObject
from base.backend.ServerList import ServerList
from base.backend.DirUtils import DirUtils

class ServerDialog(ServerDialogDesign):

    def __init__(self, parent= None):
        ServerDialogDesign.__init__(self, parent)

        self._PREFIX = DirUtils().PREFIX

        self.guiParent = parent

        self.saveButton.setEnabled(0)

        self.serverListObject = ServerList()
        self.serverList = self.serverListObject.SERVERLIST

        self.serverListIconView = []

        self.reloadServer()

        self.setInputEnabled(0)
        
###############################################################################

    def serverSelectionChanged(self):
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
        
###############################################################################

    def modifyServer(self):
        self.setInputEnabled(1)
        self.nameLineEdit.setEnabled(0)

###############################################################################

    def addServer(self):
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
        self.serverIconView.clear()
        self.serverListObject.readServerList()
        if self.serverListObject.SERVERLIST == None:
            self.serverList = []
        else:
            self.serverList = self.serverListObject.SERVERLIST
        self.serverListIconView = []
        for x in self.serverList:
            self.serverListIconView.append(QIconViewItem(
                    self.serverIconView, x.name, QPixmap(
                    self._PREFIX + "/share/luma/icons/server.png")))
        self.serverIconView.setCurrentItem(self.serverIconView.firstItem())
        self.setInputEnabled(0)
        
###############################################################################

    def saveServer(self):
        if len(self.serverList) > 0:
            self.serverListObject.deleteServer(str(self.nameLineEdit.text()))
        self.serverListObject.addServer(str(self.nameLineEdit.text()),
                str(self.hostLineEdit.text()),
                str(self.portSpinBox.value()),
                str(self.bindAnonBox.isChecked()),
                str(self.baseLineEdit.text()),
                str(self.bindLineEdit.text()),
                str(self.passwordLineEdit.text()),
                str(self.tlsCheckBox.isChecked()))
        self.reloadServer()
        
###############################################################################

    def deleteServer(self):
        selectedServerString = self.serverIconView.currentItem().text()
        reallyDelete = QMessageBox(self.trUtf8("Delete Server?"),
                self.trUtf8("Do your really want to delete the Server?"),
                QMessageBox.Critical,
                QMessageBox.Ok,
                QMessageBox.Cancel,
                QMessageBox.NoButton,
                self)
        reallyDelete.setIconPixmap(QPixmap(
                self._PREFIX + "/share/luma/icons/error.png"))
        reallyDelete.exec_loop()
        if (reallyDelete.result() == 1):
            self.serverListObject.deleteServer(str(selectedServerString))
            self.reloadServer()

###############################################################################

    def bind_anon(self):
        if self.bindAnonBox.isChecked():
            self.passwordLineEdit.setEnabled(0)
            self.bindLineEdit.setEnabled(0)
        else:
            self.passwordLineEdit.setEnabled(1)
            self.bindLineEdit.setEnabled(1)






