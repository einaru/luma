# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'base/utils/gui/PromptPasswordDialog.ui'
#
# Created: Wed Jul 4 19:54:16 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.16
#
# WARNING! All changes made in this file will be lost!


from qt import *


class PromptPasswordDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("PromptPasswordDialog")


        PromptPasswordDialogLayout = QGridLayout(self,1,1,11,6,"PromptPasswordDialogLayout")

        layout1 = QGridLayout(None,1,1,0,6,"layout1")

        self.passwordEdit = QLineEdit(self,"passwordEdit")
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        layout1.addWidget(self.passwordEdit,1,1)

        self.textLabel4 = QLabel(self,"textLabel4")
        self.textLabel4.setAlignment(QLabel.AlignVCenter)

        layout1.addWidget(self.textLabel4,1,0)

        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        layout1.addMultiCellWidget(self.textLabel2,0,0,0,1)

        PromptPasswordDialogLayout.addLayout(layout1,0,0)

        layout2 = QGridLayout(None,1,1,0,6,"layout2")

        self.okButton = QPushButton(self,"okButton")
        self.okButton.setDefault(1)

        layout2.addWidget(self.okButton,0,1)

        self.cancelButton = QPushButton(self,"cancelButton")

        layout2.addWidget(self.cancelButton,0,2)
        spacer5 = QSpacerItem(281,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer5,0,0)

        PromptPasswordDialogLayout.addLayout(layout2,1,0)

        self.languageChange()

        self.resize(QSize(371,131).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.okButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self.reject)


    def languageChange(self):
        self.setCaption(self.__tr("Enter bind password"))
        self.textLabel4.setText(self.__tr("Password:"))
        self.textLabel2.setText(self.__tr("<b>Please enter a password to bind with.</b>"))
        self.okButton.setText(self.__tr("&OK"))
        self.okButton.setAccel(QKeySequence(self.__tr("Alt+O")))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(QKeySequence(self.__tr("Alt+C")))


    def __tr(self,s,c = None):
        return qApp.translate("PromptPasswordDialog",s,c)
