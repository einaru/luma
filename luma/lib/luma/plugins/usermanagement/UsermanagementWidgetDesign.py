# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/usermanagement/UsermanagementWidgetDesign.ui'
#
# Created: Thu Sep 30 18:34:12 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class UsermanagementWidgetDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("UsermanagementWidgetDesign")


        UsermanagementWidgetDesignLayout = QGridLayout(self,1,1,6,6,"UsermanagementWidgetDesignLayout")

        self.textLabel15 = QLabel(self,"textLabel15")
        self.textLabel15.setAlignment(QLabel.AlignVCenter)

        UsermanagementWidgetDesignLayout.addWidget(self.textLabel15,3,1)

        self.textLabel3 = QLabel(self,"textLabel3")
        self.textLabel3.setAlignment(QLabel.AlignVCenter)

        UsermanagementWidgetDesignLayout.addWidget(self.textLabel3,1,1)

        self.textLabel18 = QLabel(self,"textLabel18")
        self.textLabel18.setAlignment(QLabel.AlignVCenter)

        UsermanagementWidgetDesignLayout.addWidget(self.textLabel18,2,1)
        spacer1 = QSpacerItem(21,89,QSizePolicy.Minimum,QSizePolicy.Expanding)
        UsermanagementWidgetDesignLayout.addMultiCell(spacer1,1,3,0,0)

        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setAlignment(QLabel.AlignVCenter)

        UsermanagementWidgetDesignLayout.addWidget(self.textLabel2,0,1)

        self.accountLabel = QLabel(self,"accountLabel")
        self.accountLabel.setMinimumSize(QSize(32,32))
        self.accountLabel.setMaximumSize(QSize(32,32))

        UsermanagementWidgetDesignLayout.addWidget(self.accountLabel,0,0)

        self.expireEdit = QDateEdit(self,"expireEdit")

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.expireEdit,3,3,2,5)

        self.nameEdit = QLineEdit(self,"nameEdit")

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.nameEdit,2,2,2,5)

        self.findButton = QPushButton(self,"findButton")

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.findButton,1,1,4,5)

        self.uidBox = QSpinBox(self,"uidBox")
        self.uidBox.setMaxValue(65535)

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.uidBox,1,1,2,3)

        self.uidEdit = QLineEdit(self,"uidEdit")
        self.uidEdit.setReadOnly(1)

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.uidEdit,0,0,2,5)

        self.textLabel12 = QLabel(self,"textLabel12")
        self.textLabel12.setAlignment(QLabel.AlignVCenter)

        UsermanagementWidgetDesignLayout.addWidget(self.textLabel12,10,1)

        self.homeEdit = QLineEdit(self,"homeEdit")

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.homeEdit,10,10,2,5)

        self.textLabel10 = QLabel(self,"textLabel10")
        self.textLabel10.setAlignment(QLabel.AlignVCenter)

        UsermanagementWidgetDesignLayout.addWidget(self.textLabel10,9,1)

        self.groupLabel = QLabel(self,"groupLabel")
        self.groupLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.groupLabel.sizePolicy().hasHeightForWidth()))
        self.groupLabel.setMinimumSize(QSize(32,32))

        UsermanagementWidgetDesignLayout.addWidget(self.groupLabel,5,0)

        self.shellEdit = QLineEdit(self,"shellEdit")

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.shellEdit,9,9,2,5)

        self.textLabel17 = QLabel(self,"textLabel17")
        self.textLabel17.setAlignment(QLabel.AlignVCenter)

        UsermanagementWidgetDesignLayout.addWidget(self.textLabel17,14,1)

        self.passwordLabel = QLabel(self,"passwordLabel")
        self.passwordLabel.setMinimumSize(QSize(32,32))

        UsermanagementWidgetDesignLayout.addWidget(self.passwordLabel,11,0)
        spacer4 = QSpacerItem(112,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        UsermanagementWidgetDesignLayout.addItem(spacer4,12,2)
        spacer8 = QSpacerItem(20,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        UsermanagementWidgetDesignLayout.addItem(spacer8,7,2)

        self.passwordEdit = QLineEdit(self,"passwordEdit")
        self.passwordEdit.setReadOnly(1)

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.passwordEdit,11,11,2,5)
        spacer5 = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        UsermanagementWidgetDesignLayout.addItem(spacer5,16,3)

        self.groupEdit = QLineEdit(self,"groupEdit")
        self.groupEdit.setReadOnly(1)

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.groupEdit,5,5,2,5)

        self.mailLabel = QLabel(self,"mailLabel")
        self.mailLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.mailLabel.sizePolicy().hasHeightForWidth()))
        self.mailLabel.setMinimumSize(QSize(32,32))

        UsermanagementWidgetDesignLayout.addWidget(self.mailLabel,14,0)

        self.textLabel4 = QLabel(self,"textLabel4")
        self.textLabel4.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel4.sizePolicy().hasHeightForWidth()))
        self.textLabel4.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        UsermanagementWidgetDesignLayout.addWidget(self.textLabel4,6,1)
        spacer6 = QSpacerItem(112,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        UsermanagementWidgetDesignLayout.addItem(spacer6,15,2)

        self.shellLabel = QLabel(self,"shellLabel")
        self.shellLabel.setMinimumSize(QSize(32,32))

        UsermanagementWidgetDesignLayout.addWidget(self.shellLabel,9,0)

        self.textLabel5 = QLabel(self,"textLabel5")
        self.textLabel5.setSizePolicy(QSizePolicy(5,5,0,0,self.textLabel5.sizePolicy().hasHeightForWidth()))
        self.textLabel5.setAlignment(QLabel.AlignVCenter)

        UsermanagementWidgetDesignLayout.addWidget(self.textLabel5,5,1)

        self.groupNumberEdit = QLineEdit(self,"groupNumberEdit")
        self.groupNumberEdit.setReadOnly(1)

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.groupNumberEdit,6,6,2,5)
        spacer3 = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        UsermanagementWidgetDesignLayout.addItem(spacer3,6,0)

        self.mailBox = QComboBox(0,self,"mailBox")

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.mailBox,14,14,2,5)

        self.textLabel14 = QLabel(self,"textLabel14")
        self.textLabel14.setAlignment(QLabel.AlignVCenter)

        UsermanagementWidgetDesignLayout.addWidget(self.textLabel14,11,1)

        self.homeLabel = QLabel(self,"homeLabel")
        self.homeLabel.setMinimumSize(QSize(32,32))

        UsermanagementWidgetDesignLayout.addWidget(self.homeLabel,10,0)

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.addMailButton = QPushButton(self,"addMailButton")
        layout3.addWidget(self.addMailButton)

        self.deleteMailButton = QPushButton(self,"deleteMailButton")
        layout3.addWidget(self.deleteMailButton)

        UsermanagementWidgetDesignLayout.addMultiCellLayout(layout3,15,15,3,5)

        self.groupButton = QPushButton(self,"groupButton")
        self.groupButton.setSizePolicy(QSizePolicy(1,0,0,0,self.groupButton.sizePolicy().hasHeightForWidth()))

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.groupButton,7,7,3,5)

        self.passwordButton = QPushButton(self,"passwordButton")

        UsermanagementWidgetDesignLayout.addMultiCellWidget(self.passwordButton,12,12,3,5)

        self.languageChange()

        self.resize(QSize(484,461).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.addMailButton,SIGNAL("clicked()"),self.addMail)
        self.connect(self.deleteMailButton,SIGNAL("clicked()"),self.deleteMail)
        self.connect(self.passwordButton,SIGNAL("clicked()"),self.editPassword)
        self.connect(self.groupButton,SIGNAL("clicked()"),self.editGroups)
        self.connect(self.uidBox,SIGNAL("valueChanged(int)"),self.uidChanged)
        self.connect(self.nameEdit,SIGNAL("textChanged(const QString&)"),self.commonNameChanged)
        self.connect(self.expireEdit,SIGNAL("valueChanged(const QDate&)"),self.expireChanged)
        self.connect(self.shellEdit,SIGNAL("textChanged(const QString&)"),self.shellChanged)
        self.connect(self.homeEdit,SIGNAL("textChanged(const QString&)"),self.homeChanged)
        self.connect(self.uidEdit,SIGNAL("textChanged(const QString&)"),self.uidNameChanged)
        self.connect(self.findButton,SIGNAL("clicked()"),self.nextFreeUserID)

        self.setTabOrder(self.uidEdit,self.uidBox)
        self.setTabOrder(self.uidBox,self.nameEdit)
        self.setTabOrder(self.nameEdit,self.expireEdit)
        self.setTabOrder(self.expireEdit,self.groupEdit)
        self.setTabOrder(self.groupEdit,self.groupNumberEdit)
        self.setTabOrder(self.groupNumberEdit,self.groupButton)
        self.setTabOrder(self.groupButton,self.shellEdit)
        self.setTabOrder(self.shellEdit,self.homeEdit)
        self.setTabOrder(self.homeEdit,self.passwordEdit)
        self.setTabOrder(self.passwordEdit,self.passwordButton)
        self.setTabOrder(self.passwordButton,self.mailBox)
        self.setTabOrder(self.mailBox,self.deleteMailButton)
        self.setTabOrder(self.deleteMailButton,self.addMailButton)


    def languageChange(self):
        self.setCaption(self.__tr("Usermanagement"))
        self.textLabel15.setText(self.__tr("Valid until:"))
        self.textLabel3.setText(self.__tr("User ID number:"))
        self.textLabel18.setText(self.__tr("Common name:"))
        self.textLabel2.setText(self.__tr("User ID:"))
        self.accountLabel.setText(self.__tr("US","DO NOT TRANSLATE"))
        self.findButton.setText(self.__tr("Find next free"))
        self.textLabel12.setText(self.__tr("Home directory:"))
        self.textLabel10.setText(self.__tr("Login shell:"))
        self.groupLabel.setText(self.__tr("GR"))
        self.textLabel17.setText(self.__tr("Mail:"))
        self.passwordLabel.setText(self.__tr("PW","DO NOT TRANSLATE"))
        self.mailLabel.setText(self.__tr("M","DO NOT TRANSLATE"))
        self.textLabel4.setText(self.__tr("Group ID number:"))
        self.shellLabel.setText(self.__tr("SH","DO NOT TRANSLATE"))
        self.textLabel5.setText(self.__tr("Primary group:"))
        self.textLabel14.setText(self.__tr("Password:"))
        self.homeLabel.setText(self.__tr("HO","DO NOT TRANSLATE"))
        self.addMailButton.setText(self.__tr("Add..."))
        self.deleteMailButton.setText(self.__tr("Delete"))
        self.groupButton.setText(self.__tr("Manage group memberships"))
        self.passwordButton.setText(self.__tr("Change password..."))


    def editPassword(self):
        print "UsermanagementWidgetDesign.editPassword(): Not implemented yet"

    def deleteMail(self):
        print "UsermanagementWidgetDesign.deleteMail(): Not implemented yet"

    def addMail(self):
        print "UsermanagementWidgetDesign.addMail(): Not implemented yet"

    def editGroups(self):
        print "UsermanagementWidgetDesign.editGroups(): Not implemented yet"

    def uidChanged(self):
        print "UsermanagementWidgetDesign.uidChanged(): Not implemented yet"

    def commonNameChanged(self):
        print "UsermanagementWidgetDesign.commonNameChanged(): Not implemented yet"

    def expireChanged(self):
        print "UsermanagementWidgetDesign.expireChanged(): Not implemented yet"

    def shellChanged(self):
        print "UsermanagementWidgetDesign.shellChanged(): Not implemented yet"

    def homeChanged(self):
        print "UsermanagementWidgetDesign.homeChanged(): Not implemented yet"

    def saveAccount(self):
        print "UsermanagementWidgetDesign.saveAccount(): Not implemented yet"

    def uidNameChanged(self):
        print "UsermanagementWidgetDesign.uidNameChanged(): Not implemented yet"

    def nextFreeUserID(self):
        print "UsermanagementWidgetDesign.nextFreeUserID(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("UsermanagementWidgetDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = UsermanagementWidgetDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
