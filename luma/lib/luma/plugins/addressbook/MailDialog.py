# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/addressbook/MailDialog.ui'
#
# Created: Tue Feb 3 23:58:07 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.10
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class MailDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("MailDialog")


        MailDialogLayout = QGridLayout(self,1,1,11,6,"MailDialogLayout")

        self.okButton = QPushButton(self,"okButton")
        self.okButton.setDefault(1)

        MailDialogLayout.addWidget(self.okButton,3,2)

        self.cancelButton = QPushButton(self,"cancelButton")
        self.cancelButton.setAutoDefault(0)

        MailDialogLayout.addWidget(self.cancelButton,3,1)
        spacer = QSpacerItem(311,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        MailDialogLayout.addItem(spacer,3,0)

        self.line7 = QFrame(self,"line7")
        self.line7.setFrameShape(QFrame.HLine)
        self.line7.setFrameShadow(QFrame.Sunken)
        self.line7.setFrameShape(QFrame.HLine)

        MailDialogLayout.addMultiCellWidget(self.line7,2,2,0,2)
        spacer_2 = QSpacerItem(21,231,QSizePolicy.Minimum,QSizePolicy.Expanding)
        MailDialogLayout.addItem(spacer_2,1,1)

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.mailIconLabel = QLabel(self,"mailIconLabel")
        self.mailIconLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.mailIconLabel.sizePolicy().hasHeightForWidth()))
        self.mailIconLabel.setMinimumSize(QSize(32,32))
        layout2.addWidget(self.mailIconLabel)

        self.textLabel2 = QLabel(self,"textLabel2")
        layout2.addWidget(self.textLabel2)

        self.mailEdit = QLineEdit(self,"mailEdit")
        layout2.addWidget(self.mailEdit)

        MailDialogLayout.addMultiCellLayout(layout2,0,0,0,2)

        self.languageChange()

        self.resize(QSize(411,112).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.okButton,SIGNAL("clicked()"),self,SLOT("accept()"))

        self.setTabOrder(self.mailEdit,self.cancelButton)
        self.setTabOrder(self.cancelButton,self.okButton)


    def languageChange(self):
        self.setCaption(self.__tr("New mail"))
        self.okButton.setText(self.__tr("&Ok"))
        self.okButton.setAccel(self.__tr("Alt+O"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))
        self.mailIconLabel.setText(self.__tr("ML"))
        self.textLabel2.setText(self.__tr("New mail:"))


    def __tr(self,s,c = None):
        return qApp.translate("MailDialog",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = MailDialog()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
