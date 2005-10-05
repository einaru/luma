# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/admin_utils/AdminPanelDesign.ui'
#
# Created: Wed Aug 17 15:23:42 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class AdminPanelDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("AdminPanelDesign")


        AdminPanelDesignLayout = QVBoxLayout(self,11,6,"AdminPanelDesignLayout")

        self.tabWidget2 = QTabWidget(self,"tabWidget2")

        self.tab = QWidget(self.tabWidget2,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")
        spacer2 = QSpacerItem(41,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer2,3,2)

        self.secureLabel = QLabel(self.tab,"secureLabel")
        self.secureLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.secureLabel.sizePolicy().hasHeightForWidth()))
        self.secureLabel.setMinimumSize(QSize(64,64))
        self.secureLabel.setScaledContents(0)

        tabLayout.addWidget(self.secureLabel,0,0)

        self.textLabel1_2 = QLabel(self.tab,"textLabel1_2")
        self.textLabel1_2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel1_2.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.textLabel1_2,0,1)

        self.methodBox = QComboBox(0,self.tab,"methodBox")

        tabLayout.addWidget(self.methodBox,0,2)

        layout5 = QGridLayout(None,1,1,0,6,"layout5")
        spacer5 = QSpacerItem(490,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout5.addMultiCell(spacer5,3,3,1,2)

        self.textLabel3 = QLabel(self.tab,"textLabel3")
        self.textLabel3.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel3.sizePolicy().hasHeightForWidth()))
        self.textLabel3.setAlignment(QLabel.AlignVCenter)

        layout5.addWidget(self.textLabel3,1,1)

        self.textLabel2_2 = QLabel(self.tab,"textLabel2_2")

        layout5.addMultiCellWidget(self.textLabel2_2,0,0,0,2)

        self.pwEdit = QLineEdit(self.tab,"pwEdit")

        layout5.addMultiCellWidget(self.pwEdit,1,1,2,3)

        self.textLabel4 = QLabel(self.tab,"textLabel4")
        self.textLabel4.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel4.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.textLabel4,2,1)

        self.cryptEdit = QLineEdit(self.tab,"cryptEdit")

        layout5.addMultiCellWidget(self.cryptEdit,2,2,2,3)
        spacer11 = QSpacerItem(10,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout5.addItem(spacer11,1,0)

        self.cryptButton = QPushButton(self.tab,"cryptButton")

        layout5.addWidget(self.cryptButton,3,3)

        tabLayout.addMultiCellLayout(layout5,2,2,0,2)

        layout6 = QGridLayout(None,1,1,0,6,"layout6")

        self.textLabel1_3 = QLabel(self.tab,"textLabel1_3")
        self.textLabel1_3.setAlignment(QLabel.AlignVCenter)

        layout6.addMultiCellWidget(self.textLabel1_3,0,0,0,2)

        self.randomPwEdit = QLineEdit(self.tab,"randomPwEdit")

        layout6.addMultiCellWidget(self.randomPwEdit,1,1,2,3)

        self.randomCryptEdit = QLineEdit(self.tab,"randomCryptEdit")

        layout6.addMultiCellWidget(self.randomCryptEdit,2,2,2,3)

        self.textLabel2 = QLabel(self.tab,"textLabel2")
        self.textLabel2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel2.sizePolicy().hasHeightForWidth()))

        layout6.addWidget(self.textLabel2,2,1)

        self.createButton = QPushButton(self.tab,"createButton")

        layout6.addWidget(self.createButton,3,3)
        spacer10 = QSpacerItem(16,21,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout6.addItem(spacer10,1,0)

        self.textLabel1 = QLabel(self.tab,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))
        self.textLabel1.setAlignment(QLabel.AlignVCenter)

        layout6.addWidget(self.textLabel1,1,1)
        spacer1 = QSpacerItem(480,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout6.addMultiCell(spacer1,3,3,1,2)

        tabLayout.addMultiCellLayout(layout6,1,1,0,2)
        self.tabWidget2.insertTab(self.tab,QString.fromLatin1(""))

        self.tab_2 = QWidget(self.tabWidget2,"tab_2")
        tabLayout_2 = QGridLayout(self.tab_2,1,1,11,6,"tabLayout_2")

        self.dateLabel = QLabel(self.tab_2,"dateLabel")
        self.dateLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.dateLabel.sizePolicy().hasHeightForWidth()))
        self.dateLabel.setMinimumSize(QSize(64,64))
        self.dateLabel.setScaledContents(0)

        tabLayout_2.addMultiCellWidget(self.dateLabel,0,0,0,1)

        self.dateButton = QPushButton(self.tab_2,"dateButton")
        self.dateButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.dateButton.sizePolicy().hasHeightForWidth()))

        tabLayout_2.addWidget(self.dateButton,2,4)

        self.textLabel6 = QLabel(self.tab_2,"textLabel6")
        self.textLabel6.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel6.sizePolicy().hasHeightForWidth()))

        tabLayout_2.addWidget(self.textLabel6,3,1)

        self.textLabel5 = QLabel(self.tab_2,"textLabel5")
        self.textLabel5.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5.sizePolicy().hasHeightForWidth()))
        self.textLabel5.setAlignment(QLabel.AlignVCenter)

        tabLayout_2.addWidget(self.textLabel5,2,1)

        self.textLabel4_2 = QLabel(self.tab_2,"textLabel4_2")

        tabLayout_2.addMultiCellWidget(self.textLabel4_2,1,1,0,2)
        spacer7 = QSpacerItem(16,21,QSizePolicy.Fixed,QSizePolicy.Minimum)
        tabLayout_2.addItem(spacer7,2,0)

        self.convDateEdit = QLineEdit(self.tab_2,"convDateEdit")

        tabLayout_2.addMultiCellWidget(self.convDateEdit,3,3,2,4)

        self.dateEdit = QDateEdit(self.tab_2,"dateEdit")
        self.dateEdit.setDate(QDate(2000,1,1))

        tabLayout_2.addMultiCellWidget(self.dateEdit,2,2,2,3)
        spacer3 = QSpacerItem(21,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout_2.addItem(spacer3,8,3)

        self.durationButton = QPushButton(self.tab_2,"durationButton")
        self.durationButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.durationButton.sizePolicy().hasHeightForWidth()))

        tabLayout_2.addWidget(self.durationButton,6,4)

        self.convDurationEdit = QLineEdit(self.tab_2,"convDurationEdit")

        tabLayout_2.addMultiCellWidget(self.convDurationEdit,7,7,2,4)

        self.textLabel6_2 = QLabel(self.tab_2,"textLabel6_2")
        self.textLabel6_2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel6_2.sizePolicy().hasHeightForWidth()))
        self.textLabel6_2.setAlignment(QLabel.AlignVCenter)

        tabLayout_2.addWidget(self.textLabel6_2,7,1)

        self.durationBox = QSpinBox(self.tab_2,"durationBox")
        self.durationBox.setButtonSymbols(QSpinBox.UpDownArrows)
        self.durationBox.setMaxValue(65000)
        self.durationBox.setMinValue(-65000)
        self.durationBox.setValue(365)

        tabLayout_2.addMultiCellWidget(self.durationBox,6,6,2,3)

        self.textLabel7 = QLabel(self.tab_2,"textLabel7")
        self.textLabel7.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel7.sizePolicy().hasHeightForWidth()))
        self.textLabel7.setAlignment(QLabel.AlignVCenter)

        tabLayout_2.addWidget(self.textLabel7,6,1)
        spacer8 = QSpacerItem(16,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        tabLayout_2.addItem(spacer8,6,0)

        self.textLabel5_2 = QLabel(self.tab_2,"textLabel5_2")

        tabLayout_2.addMultiCellWidget(self.textLabel5_2,5,5,0,4)
        spacer9 = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        tabLayout_2.addItem(spacer9,4,3)
        self.tabWidget2.insertTab(self.tab_2,QString.fromLatin1(""))
        AdminPanelDesignLayout.addWidget(self.tabWidget2)

        self.languageChange()

        self.resize(QSize(419,408).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.createButton,SIGNAL("clicked()"),self.createRandom)
        self.connect(self.cryptButton,SIGNAL("clicked()"),self.cryptPassword)
        self.connect(self.pwEdit,SIGNAL("returnPressed()"),self.cryptPassword)
        self.connect(self.dateButton,SIGNAL("clicked()"),self.convertDate)
        self.connect(self.durationButton,SIGNAL("clicked()"),self.convertDuration)
        self.connect(self.durationBox,SIGNAL("valueChanged(int)"),self.convertDuration)
        self.connect(self.dateEdit,SIGNAL("valueChanged(const QDate&)"),self.convertDate)

        self.setTabOrder(self.tabWidget2,self.methodBox)
        self.setTabOrder(self.methodBox,self.randomPwEdit)
        self.setTabOrder(self.randomPwEdit,self.randomCryptEdit)
        self.setTabOrder(self.randomCryptEdit,self.createButton)
        self.setTabOrder(self.createButton,self.pwEdit)
        self.setTabOrder(self.pwEdit,self.cryptEdit)
        self.setTabOrder(self.cryptEdit,self.cryptButton)
        self.setTabOrder(self.cryptButton,self.dateEdit)
        self.setTabOrder(self.dateEdit,self.dateButton)
        self.setTabOrder(self.dateButton,self.convDateEdit)
        self.setTabOrder(self.convDateEdit,self.durationBox)
        self.setTabOrder(self.durationBox,self.durationButton)
        self.setTabOrder(self.durationButton,self.convDurationEdit)


    def languageChange(self):
        self.setCaption(self.__tr("AdminPanelDesign"))
        self.secureLabel.setText(self.__tr("Secure","DO NOT TRANSLATE"))
        self.textLabel1_2.setText(self.__tr("<b>Hash method:</b>"))
        self.textLabel3.setText(self.__tr("Password:"))
        self.textLabel2_2.setText(self.__tr("<b>Encrypt password</b>"))
        self.textLabel4.setText(self.__tr("Encrypted Password:"))
        self.cryptButton.setText(self.__tr("&Encrypt"))
        self.cryptButton.setAccel(self.__tr("Alt+E"))
        self.textLabel1_3.setText(self.__tr("<b>Create random password</b>"))
        self.textLabel2.setText(self.__tr("Encrypted password:"))
        self.createButton.setText(self.__tr("&Create"))
        self.createButton.setAccel(self.__tr("Alt+C"))
        self.textLabel1.setText(self.__tr("Password:"))
        self.tabWidget2.changeTab(self.tab,self.__tr("Passwords"))
        self.dateLabel.setText(self.__tr("Date","DO NOT TRANSLATE"))
        self.dateButton.setText(self.__tr("&Convert"))
        self.dateButton.setAccel(self.__tr("Alt+C"))
        self.textLabel6.setText(self.__tr("Unix Date:"))
        self.textLabel5.setText(self.__tr("Date:"))
        self.textLabel4_2.setText(self.__tr("<b>Date to Unix date</b>"))
        self.durationButton.setText(self.__tr("C&onvert"))
        self.durationButton.setAccel(self.__tr("Alt+O"))
        self.textLabel6_2.setText(self.__tr("Unix Date:"))
        self.textLabel7.setText(self.__tr("Days from now:"))
        self.textLabel5_2.setText(self.__tr("<b>Duration to Unix date</b>"))
        self.tabWidget2.changeTab(self.tab_2,self.__tr("Date/Time"))


    def createRandom(self):
        print "AdminPanelDesign.createRandom(): Not implemented yet"

    def cryptPassword(self):
        print "AdminPanelDesign.cryptPassword(): Not implemented yet"

    def convertDate(self):
        print "AdminPanelDesign.convertDate(): Not implemented yet"

    def convertDuration(self):
        print "AdminPanelDesign.convertDuration(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("AdminPanelDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = AdminPanelDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
