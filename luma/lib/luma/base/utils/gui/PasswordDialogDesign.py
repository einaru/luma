# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/PasswordDialogDesign.ui'
#
# Created: Mon Apr 26 16:08:40 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class PasswordDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("PasswordDialogDesign")

        self.setSizeGripEnabled(1)

        PasswordDialogDesignLayout = QGridLayout(self,1,1,11,6,"PasswordDialogDesignLayout")

        self.iconLabel = QLabel(self,"iconLabel")
        self.iconLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.iconLabel.sizePolicy().hasHeightForWidth()))
        self.iconLabel.setMinimumSize(QSize(64,64))

        PasswordDialogDesignLayout.addWidget(self.iconLabel,0,0)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        PasswordDialogDesignLayout.addMultiCellWidget(self.line1,1,1,0,1)

        self.textLabel2 = QLabel(self,"textLabel2")

        PasswordDialogDesignLayout.addWidget(self.textLabel2,0,1)

        Layout1 = QHBoxLayout(None,0,6,"Layout1")
        Horizontal_Spacing2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Layout1.addItem(Horizontal_Spacing2)

        self.okButton = QPushButton(self,"okButton")
        self.okButton.setAutoDefault(1)
        self.okButton.setDefault(1)
        Layout1.addWidget(self.okButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        self.cancelButton.setAutoDefault(1)
        Layout1.addWidget(self.cancelButton)

        PasswordDialogDesignLayout.addMultiCellLayout(Layout1,5,5,0,1)

        self.line2 = QFrame(self,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)

        PasswordDialogDesignLayout.addMultiCellWidget(self.line2,4,4,0,1)

        layout2 = QGridLayout(None,1,1,0,6,"layout2")

        self.textLabel5 = QLabel(self,"textLabel5")

        layout2.addWidget(self.textLabel5,2,0)

        self.methodBox = QComboBox(0,self,"methodBox")

        layout2.addWidget(self.methodBox,0,1)

        self.passwordEdit = QLineEdit(self,"passwordEdit")
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        layout2.addWidget(self.passwordEdit,1,1)

        self.passwordSaveEdit = QLineEdit(self,"passwordSaveEdit")
        self.passwordSaveEdit.setEchoMode(QLineEdit.Password)

        layout2.addWidget(self.passwordSaveEdit,2,1)

        self.textLabel4 = QLabel(self,"textLabel4")
        self.textLabel4.setAlignment(QLabel.AlignVCenter)

        layout2.addWidget(self.textLabel4,1,0)

        self.textLabel3 = QLabel(self,"textLabel3")
        self.textLabel3.setAlignment(QLabel.AlignVCenter)

        layout2.addWidget(self.textLabel3,0,0)

        PasswordDialogDesignLayout.addMultiCellLayout(layout2,2,2,0,1)
        spacer2 = QSpacerItem(41,141,QSizePolicy.Minimum,QSizePolicy.Expanding)
        PasswordDialogDesignLayout.addItem(spacer2,3,1)

        self.languageChange()

        self.resize(QSize(409,253).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.okButton,SIGNAL("clicked()"),self.checkPassword)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.passwordEdit,SIGNAL("textChanged(const QString&)"),self.passwordChanged)
        self.connect(self.passwordSaveEdit,SIGNAL("textChanged(const QString&)"),self.passwordChanged)


    def languageChange(self):
        self.setCaption(self.__tr("New password"))
        self.iconLabel.setText(self.__tr("PW","DO NOT TRANSLATE"))
        self.textLabel2.setText(self.__tr("Please enter a new password."))
        self.okButton.setText(self.__tr("&OK"))
        self.okButton.setAccel(QString.null)
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(QString.null)
        self.textLabel5.setText(self.__tr("Retype new password:"))
        self.textLabel4.setText(self.__tr("New password:"))
        self.textLabel3.setText(self.__tr("Method:"))


    def checkPassword(self):
        print "PasswordDialogDesign.checkPassword(): Not implemented yet"

    def passwordChanged(self):
        print "PasswordDialogDesign.passwordChanged(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("PasswordDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = PasswordDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
