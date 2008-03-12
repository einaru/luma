import sys
from PyQt4.QtGui import *

from base.gui.UnknownCertDialogDesign import UnknownCertDialogDesign
from base.gui.CertificateDialogDesign import CertificateDialogDesign

# SSL
from base.backend.LumaSSLConnection import *

class UnknownCertDialog(UnknownCertDialogDesign):

    def __init__(self, serverMeta,parent = None,name = None,fl = 0):
        UnknownCertDialogDesign.__init__(self,parent,name,fl)

        self.serverMeta = serverMeta
        self.cert = None

        self.fetchCertificate()
        self.showCert()
        
###############################################################################

    def fetchCertificate(self):
        # Return is no server is selected
        if self.serverMeta == None:
            return
    
        # Connect to server
        try:
            conn = LumaSSLConnection(self.serverMeta)
            bindSuccess, exceptionObject = conn.connect()
            if bindSuccess:
                self.cert = conn.getCertDetails()
                conn.close()
        except LumaSSLConnectionException, e:
            exceptionObject = e
            bindSuccess = 0

        # Error handling
        # Silently ignore errors?
        #if not bindSuccess:
        #    a = QMessageBox.critical(self, "Unable to connect to server",
        #            "An error occured when connecting to %s. (%s)"
        #            % (self.SERVERMETA.name, str(exceptionObject)), "Ok")
        #    a.exec_loop()
        #    return

###############################################################################

    def showCert(self):
        if self.cert == None:
            return

        certificateFrameLayout = QHBoxLayout(self.certificateFrame,11,6,"certificateFrameLayout")
        self.certificateDialog = CertificateDialogDesign(self.certificateFrame)
        certificateFrameLayout.addWidget(self.certificateDialog)

        # To
        self.certificateDialog.cnToLabel.setText(     self.cert["cnTo"]   )
        self.certificateDialog.oToLabel.setText(      self.cert["oTo"]    )
        self.certificateDialog.ouToLabel.setText(     self.cert["ouTo"]   )
        self.certificateDialog.serialToLabel.setText( self.cert["serial"] )

        # By
        self.certificateDialog.cnByLabel.setText(     self.cert["cnBy"]   )
        self.certificateDialog.oByLabel.setText(      self.cert["oBy"]    )
        self.certificateDialog.ouByLabel.setText(     self.cert["ouBy"]   )
        
        # Validity
        if (self.cert["valid"]):
            self.certificateDialog.issuedOnLabel.setText("Yes")
        else:
            self.certificateDialog.issuedOnLabel.setText("No")

        # Fingerprints
        self.certificateDialog.sha1Label.setText(     self.cert["sha1"]   )
        self.certificateDialog.md5Label.setText(      self.cert["md5"]    )
