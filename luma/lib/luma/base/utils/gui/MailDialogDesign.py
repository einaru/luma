# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/MailDialogDesign.ui'
#
# Created: Wed Aug 17 15:23:46 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt4.QtGui import *


class MailDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("MailDialogDesign")


        MailDialogDesignLayout = QVBoxLayout(self,11,6,"MailDialogDesignLayout")

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.mailIconLabel = QLabel(self,"mailIconLabel")
        self.mailIconLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.mailIconLabel.sizePolicy().hasHeightForWidth()))
        self.mailIconLabel.setMinimumSize(QSize(32,32))
        layout2.addWidget(self.mailIconLabel)

        self.textLabel2 = QLabel(self,"textLabel2")
        layout2.addWidget(self.textLabel2)

        self.mailEdit = QLineEdit(self,"mailEdit")
        layout2.addWidget(self.mailEdit)
        MailDialogDesignLayout.addLayout(layout2)
        spacer2 = QSpacerItem(41,50,QSizePolicy.Minimum,QSizePolicy.Expanding)
        MailDialogDesignLayout.addItem(spacer2)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)
        MailDialogDesignLayout.addWidget(self.line1)

        layout2_2 = QHBoxLayout(None,0,6,"layout2_2")
        spacer9 = QSpacerItem(311,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2_2.addItem(spacer9)

        self.okButton = QPushButton(self,"okButton")
        self.okButton.setDefault(1)
        layout2_2.addWidget(self.okButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        self.cancelButton.setAutoDefault(0)
        layout2_2.addWidget(self.cancelButton)
        MailDialogDesignLayout.addLayout(layout2_2)

        self.languageChange()

        self.resize(QSize(439,105).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.okButton,SIGNAL("clicked()"),self.accept)

        self.setTabOrder(self.mailEdit,self.okButton)
        self.setTabOrder(self.okButton,self.cancelButton)


    def languageChange(self):
        self.setCaption(self.__tr("New mail"))
        self.mailIconLabel.setText(self.__tr("ML","DO NOT TRANSLATE"))
        self.textLabel2.setText(self.__tr("New mail:"))
        self.okButton.setText(self.__tr("&Ok"))
        self.okButton.setAccel(self.__tr("Alt+O"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))


    def __tr(self,s,c = None):
        return qApp.translate("MailDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = MailDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
