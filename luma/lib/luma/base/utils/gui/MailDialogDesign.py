# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/MailDialogDesign.ui'
#
# Created: Mon Apr 26 16:00:32 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class MailDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("MailDialogDesign")


        MailDialogDesignLayout = QGridLayout(self,1,1,11,6,"MailDialogDesignLayout")

        self.line7 = QFrame(self,"line7")
        self.line7.setFrameShape(QFrame.HLine)
        self.line7.setFrameShadow(QFrame.Sunken)
        self.line7.setFrameShape(QFrame.HLine)

        MailDialogDesignLayout.addWidget(self.line7,2,0)
        spacer10 = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        MailDialogDesignLayout.addItem(spacer10,1,0)

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.mailIconLabel = QLabel(self,"mailIconLabel")
        self.mailIconLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.mailIconLabel.sizePolicy().hasHeightForWidth()))
        self.mailIconLabel.setMinimumSize(QSize(32,32))
        layout2.addWidget(self.mailIconLabel)

        self.textLabel2 = QLabel(self,"textLabel2")
        layout2.addWidget(self.textLabel2)

        self.mailEdit = QLineEdit(self,"mailEdit")
        layout2.addWidget(self.mailEdit)

        MailDialogDesignLayout.addLayout(layout2,0,0)

        layout2_2 = QHBoxLayout(None,0,6,"layout2_2")
        spacer9 = QSpacerItem(311,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2_2.addItem(spacer9)

        self.okButton = QPushButton(self,"okButton")
        self.okButton.setDefault(1)
        layout2_2.addWidget(self.okButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        self.cancelButton.setAutoDefault(0)
        layout2_2.addWidget(self.cancelButton)

        MailDialogDesignLayout.addLayout(layout2_2,3,0)

        self.languageChange()

        self.resize(QSize(412,116).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.okButton,SIGNAL("clicked()"),self,SLOT("accept()"))

        self.setTabOrder(self.mailEdit,self.cancelButton)
        self.setTabOrder(self.cancelButton,self.okButton)


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
