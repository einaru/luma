# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from PyQt4.QtGui import *
import os.path
import os
from sets import Set

import environment
from plugins.admin_utils.AdminPanelDesign import AdminPanelDesign
from base.utils.backend.CryptPwGenerator import CryptPwGenerator
from base.utils.backend.DateHelper import DateHelper
from base.utils.backend.mkpasswd import mkpasswd

# For the certificate tab
from ConfigParser import *
from base.backend.ServerList import ServerList
from base.backend.LumaSSLConnection import *
from base.gui.CertificateDialogDesign import CertificateDialogDesign


class AdminPanel(AdminPanelDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        global hasSSLlibrary
        AdminPanelDesign.__init__(self,parent,name,fl)
        
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons", "plugins", "admin_utils")
        secureIcon = QPixmap (os.path.join (iconDir, "secure.png"))
        dateIcon = QPixmap (os.path.join (iconDir, "date.png"))
        
        self.secureLabel.setPixmap (secureIcon)
        self.dateLabel.setPixmap (dateIcon)
        
        self.supportedAlgorithms = environment.getAvailableHashMethods()
        map(self.methodBox.insertItem, self.supportedAlgorithms)
        
        self.pwHandler = CryptPwGenerator()
        self.dateHandler = DateHelper()

        # Holding objects for the certificate tab
        self.SERVERMETA = None
        self.sslConnection = None

        if hasSSLlibrary:
            certificateFrameLayout = QHBoxLayout(self.certificateFrame,11,6,"certificateFrameLayout")
            self.certificateDialog = CertificateDialogDesign(self.certificateFrame)
            certificateFrameLayout.addWidget(self.certificateDialog)

            # Setting up serverBox for the certificate tab
            self.iconPath = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons")
            tmpFile  = os.path.join(self.iconPath, "secure.png")
            securePixmap = QPixmap(tmpFile)

            serverListObject = ServerList()
            serverListObject.readServerList()
            self.serverList = serverListObject.serverList

            self.serverBox.insertItem("")
            if not (self.serverList == None):
                for x in self.serverList:
                    if x.encryptionMethod == u"SSL":
                        self.serverBox.insertItem(securePixmap, x.name)
        else:
            self.certificateTab.setDisabled(1)
            certificateWarning = QLabel(self.certificateFrame)
            certificateWarning.setText(\
                    "Sorry, but there doesn't seem to be any appropriate\n" \
                    "SSL library on this system.\n\n" \
                    "Please refer to the luma documentaion for supported \nSSL libraries"\
                    )
            certificateFrameLayout = QVBoxLayout(self.certificateFrame,11,6,"certificateFrameLayout")
            certificateFrameLayout.addWidget(certificateWarning)
            warningSpacer = QSpacerItem(41,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
            certificateFrameLayout.addItem(warningSpacer)
        
###############################################################################

    def createRandom(self):
        tmpPassword = self.pwHandler.createRandomString(10)
        self.randomPwEdit.setText(tmpPassword)
        method = str(self.methodBox.currentText())
        
        if method == "cleartext":
            password = tmpPassword
        else:
            password = mkpasswd(tmpPassword, 3, method)

        self.randomCryptEdit.setText(password)
        
###############################################################################

    def cryptPassword(self):
        tmpPassword = str(self.pwEdit.text())
        method = str(self.methodBox.currentText())
        
        if method == "cleartext":
            password = tmpPassword
        else:
            password = mkpasswd(tmpPassword, 3, method)
            
        self.cryptEdit.setText(password)
        
###############################################################################

    def convertDate(self):
        tmpDate = self.dateEdit.date()
        year = tmpDate.year()
        month = tmpDate.month()
        day = tmpDate.day()
        tmpDays = self.dateHandler.dateToUnix(year, month, day)
        self.convDateEdit.setText(str(tmpDays))
        
###############################################################################

    def convertDuration(self):
        tmpValue = self.durationBox.value()
        tmpDays = self.dateHandler.datedurationToUnix(tmpValue)
        self.convDurationEdit.setText(str(tmpDays))
        
        
###############################################################################

    def serverChanged(self,serverName):
        if serverName == "":
            self.SERVERMETA = None
            return

        if self.serverList == None:
            return
        
        for x in self.serverList:
            if x.name == str(serverName):
                self.SERVERMETA = x
                break

###############################################################################

    def saveCertificate(self):
        # Abort if no certificate has been fetched (this shouldn't happen)
        if self.sslConnection == None:
            self.saveButton.setEnabled(0)
            return

        # Fetch filename from user
        qfilename = QFileDialog.getSaveFileName(\
            "%s.pem" % self.SERVERMETA.name,
            "Certificates (*.pem)",
            self, "save certificate dialog",
            "Choose a filename to save certificate under",
            None, 1)

        # Return on 'cancel'
        if qfilename.isEmpty():
            return

        filename = unicode(qfilename)

        # Warn if exists
        if os.path.exists(filename):
            a = QMessageBox.information(self, "Overwrite file?",
                    "A file called %s already exists. Do you want to overwrite it?" % filename,
                    "&Yes", "&No")
            if a.exec_loop() == QMessageBox.Rejected:
                return

        # Check that directorystructure exists
        if not os.path.isdir(os.path.dirname(filename)):
            if os.path.exists(os.path.dirname(filename)):
                a = QMessageBox.critical(self, "Unable to create directory",
                        "%s already exists, but is not a directory. Unable to create file %s" 
                        % (os.path.dirname(filename), filename), "Ok")
                a.exec_loop()
                return
            else:
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError, e:
                    a = QMessageBox.critical(self, "Unable to create directory",
                            "An error occured when creating directory %s. (%s)"
                            % (os.path.dirname(filename), e.strerror), "Ok")
                    a.exec_loop()
                    return

        # Save to file
        try:
            fileHandler = open(unicode(filename), "w")
            fileHandler.write(self.sslConnection.getPemDump())
            fileHandler.close()
        except IOError, e:
            a = QMessageBox.critical(self, "Unable to save to file",
                    "An error occured when saveing file %s. (%s)"
                    % (filename, e.strerror), "Ok")
            a.exec_loop()
            return

###############################################################################

    def fetchCertificate(self):
        # Return is no server is selected
        if self.SERVERMETA == None:
            return

        # Connect to server
        try:
            conn = LumaSSLConnection(self.SERVERMETA)
            bindSuccess, exceptionObject = conn.connect()
            if bindSuccess:
                cert = conn.getCertDetails()
                conn.close()
        except LumaSSLConnectionException, e:
            self.saveButton.setEnabled(0)
            exceptionObject = e
            bindSuccess = 0

        # Errorhandling
        if not bindSuccess:
            a = QMessageBox.critical(self, "Unable to connect to server",
                    "An error occured when connecting to %s. (%s)"
                    % (self.SERVERMETA.name, str(exceptionObject)), "Ok")
            a.exec_loop()
            return

        self.sslConnection = conn
        self.saveButton.setEnabled(1)

        # To
        self.certificateDialog.cnToLabel.setText( cert["cnTo"] )
        self.certificateDialog.oToLabel.setText(  cert["oTo"]  )
        self.certificateDialog.ouToLabel.setText( cert["ouTo"] )
        self.certificateDialog.serialToLabel.setText( cert["serial"] )

        # By
        self.certificateDialog.cnByLabel.setText( cert["cnBy"] )
        self.certificateDialog.oByLabel.setText(  cert["oBy"]  )
        self.certificateDialog.ouByLabel.setText( cert["ouBy"] )
        
        # Validity
        if (cert["valid"]):
            self.certificateDialog.issuedOnLabel.setText("Yes")
        else:
            self.certificateDialog.issuedOnLabel.setText("No")

        # Fingerprints
        self.certificateDialog.sha1Label.setText( cert["sha1"] )
        self.certificateDialog.md5Label.setText(  cert["md5"]  )
