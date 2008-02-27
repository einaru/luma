# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/luma/base/gui/UnknownCertDialogDesign.ui'
#
# Created: Sat Feb 23 23:59:24 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class UnknownCertDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("UnknownCertDialogDesign")


        UnknownCertDialogDesignLayout = QGridLayout(self,1,1,11,6,"UnknownCertDialogDesignLayout")

        layout10 = QHBoxLayout(None,0,6,"layout10")
        spacer20 = QSpacerItem(189,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout10.addItem(spacer20)

        self.textLabel2 = QLabel(self,"textLabel2")
        layout10.addWidget(self.textLabel2)

        self.okButton = QPushButton(self,"okButton")
        layout10.addWidget(self.okButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        layout10.addWidget(self.cancelButton)

        UnknownCertDialogDesignLayout.addLayout(layout10,2,0)

        self.certificateFrame = QFrame(self,"certificateFrame")
        self.certificateFrame.setFrameShape(QFrame.StyledPanel)
        self.certificateFrame.setFrameShadow(QFrame.Raised)

        UnknownCertDialogDesignLayout.addWidget(self.certificateFrame,1,0)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setMaximumSize(QSize(32767,21))

        UnknownCertDialogDesignLayout.addWidget(self.textLabel1,0,0)

        self.languageChange()

        self.resize(QSize(522,404).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.okButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self.reject)


    def languageChange(self):
        self.setCaption(self.__tr("Certificate error"))
        self.textLabel2.setText(self.__tr("Continue anyway?"))
        self.okButton.setText(self.__tr("&Yes"))
        self.okButton.setAccel(QKeySequence(self.__tr("Alt+Y")))
        self.cancelButton.setText(self.__tr("&No"))
        self.cancelButton.setAccel(QKeySequence(self.__tr("Alt+N")))
        self.textLabel1.setText(self.__tr("The server certificate can not be verified"))


    def __tr(self,s,c = None):
        return qApp.translate("UnknownCertDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = UnknownCertDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
