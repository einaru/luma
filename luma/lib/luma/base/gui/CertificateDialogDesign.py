# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/luma/base/gui/CertificateDialogDesign.ui'
#
# Created: Sun Feb 24 15:00:32 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt4.QtGui import *


class CertificateDialogDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("CertificateDialogDesign")


        CertificateDialogDesignLayout = QGridLayout(self,1,1,11,6,"CertificateDialogDesignLayout")

        layout70 = QGridLayout(None,1,1,0,6,"layout70")

        layout47 = QGridLayout(None,1,1,0,6,"layout47")
        spacer28 = QSpacerItem(16,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout47.addItem(spacer28,0,0)

        layout46 = QHBoxLayout(None,0,6,"layout46")

        self.textLabel23 = QLabel(self,"textLabel23")
        layout46.addWidget(self.textLabel23)

        self.issuedOnLabel = QLabel(self,"issuedOnLabel")
        layout46.addWidget(self.issuedOnLabel)

        layout47.addLayout(layout46,0,1)

        layout70.addLayout(layout47,5,0)
        spacer50 = QSpacerItem(160,260,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout70.addMultiCell(spacer50,1,6,1,1)

        layout23 = QHBoxLayout(None,0,6,"layout23")

        self.textLabel1_5 = QLabel(self,"textLabel1_5")
        layout23.addWidget(self.textLabel1_5)
        spacer40 = QSpacerItem(80,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        layout23.addItem(spacer40)

        layout70.addLayout(layout23,0,0)

        layout44 = QGridLayout(None,1,1,0,6,"layout44")

        layout29 = QHBoxLayout(None,0,6,"layout29")

        self.textLabel20 = QLabel(self,"textLabel20")
        layout29.addWidget(self.textLabel20)

        self.cnByLabel = QLabel(self,"cnByLabel")
        layout29.addWidget(self.cnByLabel)

        layout44.addLayout(layout29,0,1)

        layout30 = QHBoxLayout(None,0,6,"layout30")

        self.textLabel21 = QLabel(self,"textLabel21")
        layout30.addWidget(self.textLabel21)

        self.oByLabel = QLabel(self,"oByLabel")
        layout30.addWidget(self.oByLabel)

        layout44.addLayout(layout30,1,1)
        spacer22_2 = QSpacerItem(16,50,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout44.addMultiCell(spacer22_2,0,2,0,0)

        layout31 = QHBoxLayout(None,0,6,"layout31")

        self.textLabel22 = QLabel(self,"textLabel22")
        layout31.addWidget(self.textLabel22)

        self.ouByLabel = QLabel(self,"ouByLabel")
        layout31.addWidget(self.ouByLabel)

        layout44.addLayout(layout31,2,1)

        layout70.addLayout(layout44,3,0)

        layout39 = QGridLayout(None,1,1,0,6,"layout39")
        spacer22 = QSpacerItem(16,70,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout39.addMultiCell(spacer22,0,3,0,0)

        layout25 = QHBoxLayout(None,0,6,"layout25")

        self.textLabel17 = QLabel(self,"textLabel17")
        layout25.addWidget(self.textLabel17)

        self.oToLabel = QLabel(self,"oToLabel")
        layout25.addWidget(self.oToLabel)

        layout39.addLayout(layout25,1,1)

        layout24 = QHBoxLayout(None,0,6,"layout24")

        self.textLabel16 = QLabel(self,"textLabel16")
        self.textLabel16.setFrameShape(QLabel.NoFrame)
        self.textLabel16.setFrameShadow(QLabel.Plain)
        layout24.addWidget(self.textLabel16)

        self.cnToLabel = QLabel(self,"cnToLabel")
        layout24.addWidget(self.cnToLabel)

        layout39.addLayout(layout24,0,1)

        layout26 = QHBoxLayout(None,0,6,"layout26")

        self.textLabel18 = QLabel(self,"textLabel18")
        layout26.addWidget(self.textLabel18)

        self.ouToLabel = QLabel(self,"ouToLabel")
        layout26.addWidget(self.ouToLabel)

        layout39.addLayout(layout26,2,1)

        layout27 = QHBoxLayout(None,0,6,"layout27")

        self.textLabel19 = QLabel(self,"textLabel19")
        layout27.addWidget(self.textLabel19)

        self.serialToLabel = QLabel(self,"serialToLabel")
        layout27.addWidget(self.serialToLabel)

        layout39.addLayout(layout27,3,1)

        layout70.addLayout(layout39,1,0)

        layout32 = QHBoxLayout(None,0,6,"layout32")

        self.textLabel10 = QLabel(self,"textLabel10")
        layout32.addWidget(self.textLabel10)
        spacer36_3 = QSpacerItem(100,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout32.addItem(spacer36_3)

        layout70.addLayout(layout32,4,0)

        layout28 = QHBoxLayout(None,0,6,"layout28")

        self.textLabel5_3 = QLabel(self,"textLabel5_3")
        layout28.addWidget(self.textLabel5_3)
        spacer36_2 = QSpacerItem(100,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout28.addItem(spacer36_2)

        layout70.addLayout(layout28,2,0)

        layout34 = QHBoxLayout(None,0,6,"layout34")

        self.textLabel13 = QLabel(self,"textLabel13")
        layout34.addWidget(self.textLabel13)
        spacer36 = QSpacerItem(100,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout34.addItem(spacer36)

        layout70.addLayout(layout34,6,0)

        CertificateDialogDesignLayout.addLayout(layout70,0,0)

        layout42 = QGridLayout(None,1,1,0,6,"layout42")
        spacer22_2_2 = QSpacerItem(16,30,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout42.addMultiCell(spacer22_2_2,0,1,0,0)

        layout36 = QHBoxLayout(None,0,6,"layout36")

        self.textLabel26 = QLabel(self,"textLabel26")
        layout36.addWidget(self.textLabel26)

        self.md5Label = QLabel(self,"md5Label")
        layout36.addWidget(self.md5Label)

        layout42.addLayout(layout36,1,1)

        layout35 = QHBoxLayout(None,0,6,"layout35")

        self.textLabel25 = QLabel(self,"textLabel25")
        layout35.addWidget(self.textLabel25)

        self.sha1Label = QLabel(self,"sha1Label")
        layout35.addWidget(self.sha1Label)

        layout42.addLayout(layout35,0,1)

        CertificateDialogDesignLayout.addLayout(layout42,1,0)

        self.languageChange()

        self.resize(QSize(566,365).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("CertificateDialogDesign"))
        self.textLabel23.setText(self.__tr("Has expired"))
        self.issuedOnLabel.setText(QString.null)
        self.textLabel1_5.setText(self.__tr("Issued To"))
        self.textLabel20.setText(self.__tr("Common Name (cn)"))
        self.cnByLabel.setText(QString.null)
        self.textLabel21.setText(self.__tr("Organization (o)"))
        self.oByLabel.setText(QString.null)
        self.textLabel22.setText(self.__tr("Organizational Unit (ou)"))
        self.ouByLabel.setText(QString.null)
        self.textLabel17.setText(self.__tr("Organization (o)"))
        self.oToLabel.setText(QString.null)
        self.textLabel16.setText(self.__tr("Common Name (cn)"))
        self.cnToLabel.setText(QString.null)
        self.textLabel18.setText(self.__tr("Organizational Unit (ou)"))
        self.ouToLabel.setText(QString.null)
        self.textLabel19.setText(self.__tr("Serial Number"))
        self.serialToLabel.setText(QString.null)
        self.textLabel10.setText(self.__tr("Validity"))
        self.textLabel5_3.setText(self.__tr("Issued By"))
        self.textLabel13.setText(self.__tr("Fingerprints"))
        self.textLabel26.setText(self.__tr("MD5 Fingerprint"))
        self.md5Label.setText(QString.null)
        self.textLabel25.setText(self.__tr("SHA1 Fingerprint"))
        self.sha1Label.setText(QString.null)


    def __tr(self,s,c = None):
        return qApp.translate("CertificateDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = CertificateDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
