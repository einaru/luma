# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/admin_utils/AdminPanelDesign.ui'
#
# Created: Tue Feb 3 23:58:04 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.10
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class AdminPanelDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("AdminPanelDesign")


        AdminPanelDesignLayout = QGridLayout(self,1,1,11,6,"AdminPanelDesignLayout")

        self.tabWidget2 = QTabWidget(self,"tabWidget2")

        self.tab = QWidget(self.tabWidget2,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")
        spacer = QSpacerItem(41,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer,3,2)

        self.groupBox2 = QGroupBox(self.tab,"groupBox2")
        self.groupBox2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2.layout().setSpacing(6)
        self.groupBox2.layout().setMargin(11)
        groupBox2Layout = QGridLayout(self.groupBox2.layout())
        groupBox2Layout.setAlignment(Qt.AlignTop)

        self.textLabel4 = QLabel(self.groupBox2,"textLabel4")

        groupBox2Layout.addWidget(self.textLabel4,1,0)

        self.cryptButton = QPushButton(self.groupBox2,"cryptButton")

        groupBox2Layout.addWidget(self.cryptButton,0,2)

        self.pwEdit = QLineEdit(self.groupBox2,"pwEdit")

        groupBox2Layout.addWidget(self.pwEdit,0,1)

        self.textLabel3 = QLabel(self.groupBox2,"textLabel3")
        self.textLabel3.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        groupBox2Layout.addWidget(self.textLabel3,0,0)

        self.cryptEdit = QLineEdit(self.groupBox2,"cryptEdit")

        groupBox2Layout.addWidget(self.cryptEdit,1,1)

        tabLayout.addMultiCellWidget(self.groupBox2,2,2,0,2)

        self.groupBox1 = QGroupBox(self.tab,"groupBox1")
        self.groupBox1.setColumnLayout(0,Qt.Vertical)
        self.groupBox1.layout().setSpacing(6)
        self.groupBox1.layout().setMargin(11)
        groupBox1Layout = QGridLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(Qt.AlignTop)

        self.textLabel1 = QLabel(self.groupBox1,"textLabel1")
        self.textLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        groupBox1Layout.addWidget(self.textLabel1,0,0)

        self.textLabel2 = QLabel(self.groupBox1,"textLabel2")

        groupBox1Layout.addWidget(self.textLabel2,1,0)

        self.randomPwEdit = QLineEdit(self.groupBox1,"randomPwEdit")

        groupBox1Layout.addMultiCellWidget(self.randomPwEdit,0,0,1,2)

        self.randomCryptEdit = QLineEdit(self.groupBox1,"randomCryptEdit")

        groupBox1Layout.addMultiCellWidget(self.randomCryptEdit,1,1,1,2)

        self.createButton = QPushButton(self.groupBox1,"createButton")

        groupBox1Layout.addWidget(self.createButton,2,2)
        spacer_2 = QSpacerItem(191,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox1Layout.addItem(spacer_2,2,1)

        tabLayout.addMultiCellWidget(self.groupBox1,1,1,0,2)

        self.methodBox = QComboBox(0,self.tab,"methodBox")

        tabLayout.addWidget(self.methodBox,0,2)

        self.textLabel1_2 = QLabel(self.tab,"textLabel1_2")
        self.textLabel1_2.setSizePolicy(QSizePolicy(4,5,0,0,self.textLabel1_2.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.textLabel1_2,0,1)

        self.secureLabel = QLabel(self.tab,"secureLabel")
        self.secureLabel.setSizePolicy(QSizePolicy(0,5,0,0,self.secureLabel.sizePolicy().hasHeightForWidth()))
        self.secureLabel.setScaledContents(0)

        tabLayout.addWidget(self.secureLabel,0,0)
        self.tabWidget2.insertTab(self.tab,QString(""))

        self.tab_2 = QWidget(self.tabWidget2,"tab_2")
        tabLayout_2 = QGridLayout(self.tab_2,1,1,11,6,"tabLayout_2")

        self.dateLabel = QLabel(self.tab_2,"dateLabel")
        self.dateLabel.setScaledContents(0)

        tabLayout_2.addWidget(self.dateLabel,0,0)

        self.groupBox3 = QGroupBox(self.tab_2,"groupBox3")
        self.groupBox3.setColumnLayout(0,Qt.Vertical)
        self.groupBox3.layout().setSpacing(6)
        self.groupBox3.layout().setMargin(11)
        groupBox3Layout = QGridLayout(self.groupBox3.layout())
        groupBox3Layout.setAlignment(Qt.AlignTop)

        self.convDateEdit = QLineEdit(self.groupBox3,"convDateEdit")

        groupBox3Layout.addMultiCellWidget(self.convDateEdit,1,1,1,2)

        self.dateEdit = QDateEdit(self.groupBox3,"dateEdit")
        self.dateEdit.setDate(QDate(2000,1,1))

        groupBox3Layout.addWidget(self.dateEdit,0,1)

        self.dateButton = QPushButton(self.groupBox3,"dateButton")
        self.dateButton.setSizePolicy(QSizePolicy(0,0,0,0,self.dateButton.sizePolicy().hasHeightForWidth()))

        groupBox3Layout.addWidget(self.dateButton,0,2)

        self.textLabel5 = QLabel(self.groupBox3,"textLabel5")
        self.textLabel5.setSizePolicy(QSizePolicy(1,5,0,0,self.textLabel5.sizePolicy().hasHeightForWidth()))
        self.textLabel5.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        groupBox3Layout.addWidget(self.textLabel5,0,0)

        self.textLabel6 = QLabel(self.groupBox3,"textLabel6")
        self.textLabel6.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel6.sizePolicy().hasHeightForWidth()))

        groupBox3Layout.addWidget(self.textLabel6,1,0)

        tabLayout_2.addWidget(self.groupBox3,1,0)
        spacer_3 = QSpacerItem(21,141,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout_2.addItem(spacer_3,3,0)

        self.groupBox4 = QGroupBox(self.tab_2,"groupBox4")
        self.groupBox4.setColumnLayout(0,Qt.Vertical)
        self.groupBox4.layout().setSpacing(6)
        self.groupBox4.layout().setMargin(11)
        groupBox4Layout = QGridLayout(self.groupBox4.layout())
        groupBox4Layout.setAlignment(Qt.AlignTop)

        self.durationButton = QPushButton(self.groupBox4,"durationButton")
        self.durationButton.setSizePolicy(QSizePolicy(0,0,0,0,self.durationButton.sizePolicy().hasHeightForWidth()))

        groupBox4Layout.addWidget(self.durationButton,0,2)

        self.convDurationEdit = QLineEdit(self.groupBox4,"convDurationEdit")

        groupBox4Layout.addMultiCellWidget(self.convDurationEdit,1,1,1,2)

        self.durationBox = QSpinBox(self.groupBox4,"durationBox")
        self.durationBox.setButtonSymbols(QSpinBox.UpDownArrows)
        self.durationBox.setMaxValue(65000)
        self.durationBox.setMinValue(-65000)
        self.durationBox.setValue(365)

        groupBox4Layout.addWidget(self.durationBox,0,1)

        self.textLabel7 = QLabel(self.groupBox4,"textLabel7")
        self.textLabel7.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel7.sizePolicy().hasHeightForWidth()))
        self.textLabel7.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        groupBox4Layout.addWidget(self.textLabel7,0,0)

        self.textLabel6_2 = QLabel(self.groupBox4,"textLabel6_2")
        self.textLabel6_2.setSizePolicy(QSizePolicy(1,5,0,0,self.textLabel6_2.sizePolicy().hasHeightForWidth()))
        self.textLabel6_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        groupBox4Layout.addWidget(self.textLabel6_2,1,0)

        tabLayout_2.addWidget(self.groupBox4,2,0)
        self.tabWidget2.insertTab(self.tab_2,QString(""))

        AdminPanelDesignLayout.addWidget(self.tabWidget2,0,0)

        self.languageChange()

        self.resize(QSize(380,364).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.createButton,SIGNAL("clicked()"),self.create_random)
        self.connect(self.cryptButton,SIGNAL("clicked()"),self.crypt_password)
        self.connect(self.pwEdit,SIGNAL("returnPressed()"),self.crypt_password)
        self.connect(self.dateButton,SIGNAL("clicked()"),self.convert_date)
        self.connect(self.durationButton,SIGNAL("clicked()"),self.convert_duration)
        self.connect(self.durationBox,SIGNAL("valueChanged(int)"),self.convert_duration)
        self.connect(self.dateEdit,SIGNAL("valueChanged(const QDate&)"),self.convert_date)


    def languageChange(self):
        self.setCaption(QString.null)
        self.groupBox2.setTitle(self.__tr("Encrypt Password"))
        self.textLabel4.setText(self.__tr("Encrypted Password:"))
        self.cryptButton.setText(self.__tr("&Encrypt"))
        self.cryptButton.setAccel(self.__tr("Alt+E"))
        self.textLabel3.setText(self.__tr("Password:"))
        self.groupBox1.setTitle(self.__tr("Create Random Password"))
        self.textLabel1.setText(self.__tr("Password:"))
        self.textLabel2.setText(self.__tr("Encrypted password:"))
        self.createButton.setText(self.__tr("&Create"))
        self.createButton.setAccel(self.__tr("Alt+C"))
        self.methodBox.clear()
        self.methodBox.insertItem(self.__tr("crypt"))
        self.methodBox.insertItem(self.__tr("md5"))
        self.methodBox.insertItem(self.__tr("sha"))
        self.methodBox.insertItem(self.__tr("ssha"))
        self.textLabel1_2.setText(self.__tr("Method:"))
        self.secureLabel.setText(self.__tr("Secure","DO NOT TRANSLATE"))
        self.tabWidget2.changeTab(self.tab,self.__tr("Passwords"))
        self.dateLabel.setText(self.__tr("Date","DO NOT TRANSLATE"))
        self.groupBox3.setTitle(self.__tr("Date to Unix Date"))
        self.dateButton.setText(self.__tr("&Convert"))
        self.dateButton.setAccel(self.__tr("Alt+C"))
        self.textLabel5.setText(self.__tr("Date:"))
        self.textLabel6.setText(self.__tr("Unix Date:"))
        self.groupBox4.setTitle(self.__tr("Duration to Unix Date"))
        self.durationButton.setText(self.__tr("C&onvert"))
        self.durationButton.setAccel(self.__tr("Alt+O"))
        self.textLabel7.setText(self.__tr("Days from now:"))
        self.textLabel6_2.setText(self.__tr("Unix Date:"))
        self.tabWidget2.changeTab(self.tab_2,self.__tr("Date/Time"))


    def create_random(self):
        print "AdminPanelDesign.create_random(): Not implemented yet"

    def crypt_password(self):
        print "AdminPanelDesign.crypt_password(): Not implemented yet"

    def convert_date(self):
        print "AdminPanelDesign.convert_date(): Not implemented yet"

    def convert_duration(self):
        print "AdminPanelDesign.convert_duration(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("AdminPanelDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = AdminPanelDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
