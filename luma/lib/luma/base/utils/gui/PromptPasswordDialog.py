# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PromptPasswordDialog.ui'
#
# Created: Thu Jun 1 23:07:47 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.15
#
# WARNING! All changes made in this file will be lost!


from qt import *


class PromptPasswordDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("PromptPasswordDialog")



        LayoutWidget = QWidget(self,"layout1")
        LayoutWidget.setGeometry(QRect(60,10,300,60))
        layout1 = QGridLayout(LayoutWidget,1,1,11,6,"layout1")

        self.passwordEdit = QLineEdit(LayoutWidget,"passwordEdit")
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        layout1.addWidget(self.passwordEdit,1,1)

        self.textLabel4 = QLabel(LayoutWidget,"textLabel4")
        self.textLabel4.setAlignment(QLabel.AlignVCenter)

        layout1.addWidget(self.textLabel4,1,0)

        self.textLabel2 = QLabel(LayoutWidget,"textLabel2")
        self.textLabel2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        layout1.addMultiCellWidget(self.textLabel2,0,0,0,1)

        LayoutWidget_2 = QWidget(self,"layout2")
        LayoutWidget_2.setGeometry(QRect(10,100,350,40))
        layout2 = QGridLayout(LayoutWidget_2,1,1,11,6,"layout2")

        self.okButton = QPushButton(LayoutWidget_2,"okButton")
        self.okButton.setDefault(1)

        layout2.addWidget(self.okButton,0,1)

        self.cancelButton = QPushButton(LayoutWidget_2,"cancelButton")

        layout2.addWidget(self.cancelButton,0,2)
        spacer5 = QSpacerItem(281,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer5,0,0)

        self.languageChange()

        self.resize(QSize(371,153).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.okButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self.reject)


    def languageChange(self):
        self.setCaption(self.__tr("Enter bind password"))
        self.textLabel4.setText(self.__tr("Password:"))
        self.textLabel2.setText(self.__tr("<b>Please enter a password to bind with.</b>"))
        self.okButton.setText(self.__tr("&OK"))
        self.okButton.setAccel(self.__tr("Alt+O"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))


    def __tr(self,s,c = None):
        return qApp.translate("PromptPasswordDialog",s,c)
