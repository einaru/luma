# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/usermanagement/UsermanagementWidgetDesign.ui'
#
# Created: Mon Jun 28 18:17:47 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class UsermanagementWidgetDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("UsermanagementWidgetDesign")


        UsermanagementWidgetDesignLayout = QVBoxLayout(self,6,6,"UsermanagementWidgetDesignLayout")

        layout5 = QHBoxLayout(None,0,6,"layout5")

        self.saveButton = QToolButton(self,"saveButton")
        self.saveButton.setSizePolicy(QSizePolicy(0,0,0,0,self.saveButton.sizePolicy().hasHeightForWidth()))
        self.saveButton.setMinimumSize(QSize(24,24))
        self.saveButton.setAutoRaise(1)
        layout5.addWidget(self.saveButton)

        self.optionLine1 = QFrame(self,"optionLine1")
        self.optionLine1.setFrameShape(QFrame.VLine)
        self.optionLine1.setFrameShadow(QFrame.Sunken)
        self.optionLine1.setFrameShape(QFrame.VLine)
        layout5.addWidget(self.optionLine1)

        self.deleteButton = QToolButton(self,"deleteButton")
        self.deleteButton.setSizePolicy(QSizePolicy(0,0,0,0,self.deleteButton.sizePolicy().hasHeightForWidth()))
        self.deleteButton.setMinimumSize(QSize(24,24))
        self.deleteButton.setAutoRaise(1)
        layout5.addWidget(self.deleteButton)
        spacer8 = QSpacerItem(411,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout5.addItem(spacer8)
        UsermanagementWidgetDesignLayout.addLayout(layout5)

        self.optionLine3 = QFrame(self,"optionLine3")
        self.optionLine3.setFrameShape(QFrame.HLine)
        self.optionLine3.setFrameShadow(QFrame.Sunken)
        self.optionLine3.setFrameShape(QFrame.HLine)
        UsermanagementWidgetDesignLayout.addWidget(self.optionLine3)

        layout5_2 = QGridLayout(None,1,1,0,6,"layout5_2")
        spacer10 = QSpacerItem(21,22,QSizePolicy.Minimum,QSizePolicy.Fixed)
        layout5_2.addItem(spacer10,10,3)

        self.textLabel17 = QLabel(self,"textLabel17")
        self.textLabel17.setAlignment(QLabel.AlignVCenter)

        layout5_2.addWidget(self.textLabel17,14,1)

        self.passwordButton = QPushButton(self,"passwordButton")

        layout5_2.addMultiCellWidget(self.passwordButton,12,12,3,4)

        self.mailLabel = QLabel(self,"mailLabel")
        self.mailLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.mailLabel.sizePolicy().hasHeightForWidth()))
        self.mailLabel.setMinimumSize(QSize(32,32))

        layout5_2.addWidget(self.mailLabel,14,0)

        self.groupButton = QPushButton(self,"groupButton")
        self.groupButton.setSizePolicy(QSizePolicy(1,0,0,0,self.groupButton.sizePolicy().hasHeightForWidth()))

        layout5_2.addMultiCellWidget(self.groupButton,6,6,3,4)

        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setAlignment(QLabel.AlignVCenter)

        layout5_2.addWidget(self.textLabel2,0,1)

        self.findButton = QPushButton(self,"findButton")

        layout5_2.addWidget(self.findButton,1,4)

        self.passwordEdit = QLineEdit(self,"passwordEdit")
        self.passwordEdit.setReadOnly(1)

        layout5_2.addMultiCellWidget(self.passwordEdit,11,11,2,4)

        self.groupLabel = QLabel(self,"groupLabel")
        self.groupLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.groupLabel.sizePolicy().hasHeightForWidth()))
        self.groupLabel.setMinimumSize(QSize(32,32))

        layout5_2.addWidget(self.groupLabel,5,0)

        self.textLabel4 = QLabel(self,"textLabel4")
        self.textLabel4.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel4.sizePolicy().hasHeightForWidth()))
        self.textLabel4.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout5_2.addWidget(self.textLabel4,5,3)

        self.uidEdit = QLineEdit(self,"uidEdit")
        self.uidEdit.setReadOnly(1)

        layout5_2.addMultiCellWidget(self.uidEdit,0,0,2,4)

        self.accountLabel = QLabel(self,"accountLabel")
        self.accountLabel.setMinimumSize(QSize(32,32))
        self.accountLabel.setMaximumSize(QSize(32,32))

        layout5_2.addWidget(self.accountLabel,0,0)

        layout38 = QHBoxLayout(None,0,6,"layout38")

        self.deleteMailButton = QPushButton(self,"deleteMailButton")
        layout38.addWidget(self.deleteMailButton)

        self.addMailButton = QPushButton(self,"addMailButton")
        layout38.addWidget(self.addMailButton)

        layout5_2.addMultiCellLayout(layout38,15,15,3,4)

        self.textLabel5 = QLabel(self,"textLabel5")
        self.textLabel5.setSizePolicy(QSizePolicy(5,5,0,0,self.textLabel5.sizePolicy().hasHeightForWidth()))
        self.textLabel5.setAlignment(QLabel.AlignVCenter)

        layout5_2.addWidget(self.textLabel5,5,1)

        self.mailBox = QComboBox(0,self,"mailBox")

        layout5_2.addMultiCellWidget(self.mailBox,14,14,2,4)
        spacer2 = QSpacerItem(248,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout5_2.addMultiCell(spacer2,6,6,1,2)
        spacer4 = QSpacerItem(110,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout5_2.addItem(spacer4,12,2)
        spacer8_2 = QSpacerItem(16,22,QSizePolicy.Minimum,QSizePolicy.Fixed)
        layout5_2.addItem(spacer8_2,13,3)

        self.shellLabel = QLabel(self,"shellLabel")
        self.shellLabel.setMinimumSize(QSize(32,32))

        layout5_2.addWidget(self.shellLabel,8,0)

        self.homeLabel = QLabel(self,"homeLabel")
        self.homeLabel.setMinimumSize(QSize(32,32))

        layout5_2.addWidget(self.homeLabel,9,0)

        self.nameEdit = QLineEdit(self,"nameEdit")

        layout5_2.addMultiCellWidget(self.nameEdit,2,2,2,4)

        self.textLabel18 = QLabel(self,"textLabel18")
        self.textLabel18.setAlignment(QLabel.AlignVCenter)

        layout5_2.addWidget(self.textLabel18,2,1)

        self.textLabel14 = QLabel(self,"textLabel14")
        self.textLabel14.setAlignment(QLabel.AlignVCenter)

        layout5_2.addWidget(self.textLabel14,11,1)

        self.groupNumberEdit = QLineEdit(self,"groupNumberEdit")
        self.groupNumberEdit.setSizePolicy(QSizePolicy(1,0,0,0,self.groupNumberEdit.sizePolicy().hasHeightForWidth()))
        self.groupNumberEdit.setMaximumSize(QSize(100,32767))
        self.groupNumberEdit.setReadOnly(1)

        layout5_2.addWidget(self.groupNumberEdit,5,4)

        self.homeEdit = QLineEdit(self,"homeEdit")

        layout5_2.addMultiCellWidget(self.homeEdit,9,9,2,4)
        spacer6 = QSpacerItem(110,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout5_2.addItem(spacer6,15,2)

        self.textLabel12 = QLabel(self,"textLabel12")
        self.textLabel12.setAlignment(QLabel.AlignVCenter)

        layout5_2.addWidget(self.textLabel12,9,1)

        self.textLabel15 = QLabel(self,"textLabel15")
        self.textLabel15.setAlignment(QLabel.AlignVCenter)

        layout5_2.addWidget(self.textLabel15,3,1)

        self.textLabel10 = QLabel(self,"textLabel10")
        self.textLabel10.setAlignment(QLabel.AlignVCenter)

        layout5_2.addWidget(self.textLabel10,8,1)

        self.shellEdit = QLineEdit(self,"shellEdit")

        layout5_2.addMultiCellWidget(self.shellEdit,8,8,2,4)

        self.expireEdit = QDateEdit(self,"expireEdit")

        layout5_2.addMultiCellWidget(self.expireEdit,3,3,2,4)
        spacer13 = QSpacerItem(21,22,QSizePolicy.Minimum,QSizePolicy.Fixed)
        layout5_2.addItem(spacer13,7,3)

        self.uidBox = QSpinBox(self,"uidBox")
        self.uidBox.setMaxValue(65535)

        layout5_2.addMultiCellWidget(self.uidBox,1,1,2,3)

        self.textLabel3 = QLabel(self,"textLabel3")
        self.textLabel3.setAlignment(QLabel.AlignVCenter)

        layout5_2.addWidget(self.textLabel3,1,1)
        spacer3 = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        layout5_2.addItem(spacer3,6,0)

        self.groupEdit = QLineEdit(self,"groupEdit")
        self.groupEdit.setMinimumSize(QSize(100,0))
        self.groupEdit.setReadOnly(1)

        layout5_2.addWidget(self.groupEdit,5,2)

        self.passwordLabel = QLabel(self,"passwordLabel")
        self.passwordLabel.setMinimumSize(QSize(32,32))

        layout5_2.addWidget(self.passwordLabel,11,0)
        spacer11 = QSpacerItem(21,22,QSizePolicy.Minimum,QSizePolicy.Fixed)
        layout5_2.addItem(spacer11,4,3)
        spacer1 = QSpacerItem(21,92,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout5_2.addMultiCell(spacer1,1,3,0,0)
        UsermanagementWidgetDesignLayout.addLayout(layout5_2)
        spacer5 = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        UsermanagementWidgetDesignLayout.addItem(spacer5)

        self.languageChange()

        self.resize(QSize(585,602).expandedTo(self.minimumSizeHint()))
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
        self.connect(self.saveButton,SIGNAL("clicked()"),self.saveAccount)
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
        self.saveButton.setText(self.__tr("...","DO NOT TRANSLATE"))
        self.deleteButton.setText(self.__tr("...","DO NOT TRANSLATE"))
        self.textLabel17.setText(self.__tr("Mail:"))
        self.passwordButton.setText(self.__tr("Change password..."))
        self.mailLabel.setText(self.__tr("M","DO NOT TRANSLATE"))
        self.groupButton.setText(self.__tr("Manage group memberships"))
        self.textLabel2.setText(self.__tr("User ID:"))
        self.findButton.setText(self.__tr("Find next free"))
        self.groupLabel.setText(self.__tr("GR"))
        self.textLabel4.setText(self.__tr("Group ID number:"))
        self.accountLabel.setText(self.__tr("US","DO NOT TRANSLATE"))
        self.deleteMailButton.setText(self.__tr("Delete"))
        self.addMailButton.setText(self.__tr("Add..."))
        self.textLabel5.setText(self.__tr("Primary group:"))
        self.shellLabel.setText(self.__tr("SH","DO NOT TRANSLATE"))
        self.homeLabel.setText(self.__tr("HO","DO NOT TRANSLATE"))
        self.textLabel18.setText(self.__tr("Common name:"))
        self.textLabel14.setText(self.__tr("Password:"))
        self.textLabel12.setText(self.__tr("Home directory:"))
        self.textLabel15.setText(self.__tr("Valid until:"))
        self.textLabel10.setText(self.__tr("Login shell:"))
        self.textLabel3.setText(self.__tr("User ID number:"))
        self.passwordLabel.setText(self.__tr("PW","DO NOT TRANSLATE"))


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
