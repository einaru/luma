# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/editors/PasswordEditorDesign.ui'
#
# Created: Tue Jan 4 00:19:46 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class PasswordEditorDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("PasswordEditorDesign")

        self.setSizeGripEnabled(1)

        PasswordEditorDesignLayout = QGridLayout(self,1,1,11,6,"PasswordEditorDesignLayout")

        self.iconLabel = QLabel(self,"iconLabel")
        self.iconLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.iconLabel.sizePolicy().hasHeightForWidth()))
        self.iconLabel.setMinimumSize(QSize(64,64))

        PasswordEditorDesignLayout.addWidget(self.iconLabel,0,0)
        spacer3 = QSpacerItem(20,70,QSizePolicy.Minimum,QSizePolicy.Expanding)
        PasswordEditorDesignLayout.addItem(spacer3,1,0)

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

        PasswordEditorDesignLayout.addMultiCellLayout(Layout1,4,4,0,1)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        PasswordEditorDesignLayout.addMultiCellWidget(self.line1,3,3,0,1)
        spacer2 = QSpacerItem(41,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        PasswordEditorDesignLayout.addItem(spacer2,2,1)

        layout3 = QGridLayout(None,1,1,0,6,"layout3")

        self.textLabel1 = QLabel(self,"textLabel1")

        layout3.addWidget(self.textLabel1,4,0)

        self.textLabel3 = QLabel(self,"textLabel3")
        self.textLabel3.setAlignment(QLabel.AlignVCenter)

        layout3.addWidget(self.textLabel3,1,0)

        self.passwordSaveEdit = QLineEdit(self,"passwordSaveEdit")
        self.passwordSaveEdit.setEchoMode(QLineEdit.Password)

        layout3.addWidget(self.passwordSaveEdit,3,1)

        self.textLabel4 = QLabel(self,"textLabel4")
        self.textLabel4.setAlignment(QLabel.AlignVCenter)

        layout3.addWidget(self.textLabel4,2,0)

        self.textLabel5 = QLabel(self,"textLabel5")

        layout3.addWidget(self.textLabel5,3,0)

        self.passwordLabel = QLabel(self,"passwordLabel")

        layout3.addMultiCellWidget(self.passwordLabel,5,5,0,1)

        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        layout3.addMultiCellWidget(self.textLabel2,0,0,0,1)

        self.passwordEdit = QLineEdit(self,"passwordEdit")
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        layout3.addWidget(self.passwordEdit,2,1)

        self.strengthBar = QProgressBar(self,"strengthBar")

        layout3.addWidget(self.strengthBar,4,1)

        self.methodBox = QComboBox(0,self,"methodBox")

        layout3.addWidget(self.methodBox,1,1)

        PasswordEditorDesignLayout.addMultiCellLayout(layout3,0,1,1,1)

        self.languageChange()

        self.resize(QSize(441,253).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.okButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.passwordEdit,SIGNAL("textChanged(const QString&)"),self.passwordChanged)
        self.connect(self.passwordSaveEdit,SIGNAL("textChanged(const QString&)"),self.passwordChanged)

        self.setTabOrder(self.methodBox,self.passwordEdit)
        self.setTabOrder(self.passwordEdit,self.passwordSaveEdit)
        self.setTabOrder(self.passwordSaveEdit,self.okButton)
        self.setTabOrder(self.okButton,self.cancelButton)


    def languageChange(self):
        self.setCaption(self.__tr("New password"))
        self.iconLabel.setText(self.__tr("PW","DO NOT TRANSLATE"))
        self.okButton.setText(self.__tr("&OK"))
        self.okButton.setAccel(QString.null)
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(QString.null)
        self.textLabel1.setText(self.__tr("Strength:"))
        self.textLabel3.setText(self.__tr("Hash algorithm:"))
        self.textLabel4.setText(self.__tr("Password:"))
        self.textLabel5.setText(self.__tr("Verify:"))
        self.passwordLabel.setText(self.__tr("Passwords do not match"))
        self.textLabel2.setText(self.__tr("<b>Please enter a new password.</b>"))


    def checkPassword(self):
        print "PasswordEditorDesign.checkPassword(): Not implemented yet"

    def passwordChanged(self):
        print "PasswordEditorDesign.passwordChanged(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("PasswordEditorDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = PasswordEditorDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
