# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/addressbook/AddressbookWidgetDesign.ui'
#
# Created: Thu Apr 29 16:49:01 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class AddressbookWidgetDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("AddressbookWidgetDesign")


        AddressbookWidgetDesignLayout = QGridLayout(self,1,1,0,6,"AddressbookWidgetDesignLayout")

        self.tabWidget2 = QTabWidget(self,"tabWidget2")
        self.tabWidget2.setMinimumSize(QSize(300,0))

        self.tab = QWidget(self.tabWidget2,"tab")
        tabLayout = QGridLayout(self.tab,1,1,0,6,"tabLayout")

        self.personLabel = QLabel(self.tab,"personLabel")
        self.personLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.personLabel.sizePolicy().hasHeightForWidth()))
        self.personLabel.setMinimumSize(QSize(32,32))

        tabLayout.addWidget(self.personLabel,0,0)

        self.nameButton = QPushButton(self.tab,"nameButton")

        tabLayout.addMultiCellWidget(self.nameButton,0,0,1,2)

        self.line3 = QFrame(self.tab,"line3")
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setFrameShadow(QFrame.Sunken)
        self.line3.setFrameShape(QFrame.HLine)

        tabLayout.addMultiCellWidget(self.line3,3,3,0,5)
        spacer4_2 = QSpacerItem(21,130,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer4_2,10,4)

        self.categoryButton = QPushButton(self.tab,"categoryButton")
        self.categoryButton.setSizePolicy(QSizePolicy(0,0,0,0,self.categoryButton.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.categoryButton,9,2)

        self.categoryLabel = QLabel(self.tab,"categoryLabel")
        self.categoryLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.categoryLabel.sizePolicy().hasHeightForWidth()))
        self.categoryLabel.setMinimumSize(QSize(32,32))
        self.categoryLabel.setMaximumSize(QSize(32,32))

        tabLayout.addMultiCellWidget(self.categoryLabel,9,9,0,1)

        self.line1 = QFrame(self.tab,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        tabLayout.addMultiCellWidget(self.line1,8,8,0,5)

        self.webPageLabel = QLabel(self.tab,"webPageLabel")
        self.webPageLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.webPageLabel.sizePolicy().hasHeightForWidth()))
        self.webPageLabel.setMinimumSize(QSize(32,32))

        tabLayout.addMultiCellWidget(self.webPageLabel,7,7,0,1)

        self.line2 = QFrame(self.tab,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)

        tabLayout.addMultiCellWidget(self.line2,6,6,0,5)

        self.deleteMailButton = QPushButton(self.tab,"deleteMailButton")

        tabLayout.addWidget(self.deleteMailButton,5,5)

        self.addMailButton = QPushButton(self.tab,"addMailButton")

        tabLayout.addWidget(self.addMailButton,5,4)
        spacer8 = QSpacerItem(120,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        tabLayout.addItem(spacer8,5,3)

        self.mailLabel = QLabel(self.tab,"mailLabel")
        self.mailLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.mailLabel.sizePolicy().hasHeightForWidth()))
        self.mailLabel.setMinimumSize(QSize(32,32))

        tabLayout.addMultiCellWidget(self.mailLabel,4,4,0,1)

        self.categoryEdit = QLineEdit(self.tab,"categoryEdit")

        tabLayout.addMultiCellWidget(self.categoryEdit,9,9,3,5)

        self.labeledURIEdit = QLineEdit(self.tab,"labeledURIEdit")

        tabLayout.addMultiCellWidget(self.labeledURIEdit,7,7,3,5)

        self.textLabel10 = QLabel(self.tab,"textLabel10")
        self.textLabel10.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel10.sizePolicy().hasHeightForWidth()))
        self.textLabel10.setAlignment(QLabel.AlignVCenter)

        tabLayout.addWidget(self.textLabel10,4,2)

        self.textLabel1 = QLabel(self.tab,"textLabel1")
        self.textLabel1.setAlignment(QLabel.AlignVCenter)

        tabLayout.addWidget(self.textLabel1,7,2)

        self.textLabel2_2 = QLabel(self.tab,"textLabel2_2")
        self.textLabel2_2.setAlignment(QLabel.AlignVCenter)

        tabLayout.addWidget(self.textLabel2_2,2,2)

        self.textLabel3_2 = QLabel(self.tab,"textLabel3_2")
        self.textLabel3_2.setAlignment(QLabel.AlignVCenter)

        tabLayout.addWidget(self.textLabel3_2,1,2)

        self.cnEdit = QLineEdit(self.tab,"cnEdit")
        self.cnEdit.setReadOnly(1)

        tabLayout.addMultiCellWidget(self.cnEdit,0,0,3,5)

        self.titleEdit = QLineEdit(self.tab,"titleEdit")

        tabLayout.addMultiCellWidget(self.titleEdit,1,1,3,5)

        self.organisationEdit = QLineEdit(self.tab,"organisationEdit")

        tabLayout.addMultiCellWidget(self.organisationEdit,2,2,3,5)

        self.mailBox = QComboBox(0,self.tab,"mailBox")
        self.mailBox.setEditable(1)

        tabLayout.addMultiCellWidget(self.mailBox,4,4,3,5)
        self.tabWidget2.insertTab(self.tab,QString(""))

        self.tab_2 = QWidget(self.tabWidget2,"tab_2")
        tabLayout_2 = QGridLayout(self.tab_2,1,1,0,6,"tabLayout_2")

        self.homePhoneEdit = QLineEdit(self.tab_2,"homePhoneEdit")
        self.homePhoneEdit.setMinimumSize(QSize(100,0))

        tabLayout_2.addWidget(self.homePhoneEdit,0,2)

        self.textLabel9 = QLabel(self.tab_2,"textLabel9")
        self.textLabel9.setAlignment(QLabel.AlignVCenter)

        tabLayout_2.addWidget(self.textLabel9,2,1)

        self.textLabel3 = QLabel(self.tab_2,"textLabel3")
        self.textLabel3.setAlignment(QLabel.AlignVCenter)

        tabLayout_2.addWidget(self.textLabel3,3,1)

        self.telephoneNumberEdit = QLineEdit(self.tab_2,"telephoneNumberEdit")

        tabLayout_2.addWidget(self.telephoneNumberEdit,1,2)

        self.mobileEdit = QLineEdit(self.tab_2,"mobileEdit")

        tabLayout_2.addWidget(self.mobileEdit,2,2)

        self.phoneLabel = QLabel(self.tab_2,"phoneLabel")
        self.phoneLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.phoneLabel.sizePolicy().hasHeightForWidth()))
        self.phoneLabel.setMinimumSize(QSize(32,32))

        tabLayout_2.addWidget(self.phoneLabel,0,0)

        self.facsimileTelephoneNumberEdit = QLineEdit(self.tab_2,"facsimileTelephoneNumberEdit")

        tabLayout_2.addWidget(self.facsimileTelephoneNumberEdit,3,2)

        self.textLabel8 = QLabel(self.tab_2,"textLabel8")
        self.textLabel8.setAlignment(QLabel.AlignVCenter)

        tabLayout_2.addWidget(self.textLabel8,1,1)

        self.textLabel7 = QLabel(self.tab_2,"textLabel7")
        self.textLabel7.setAlignment(QLabel.AlignVCenter)

        tabLayout_2.addWidget(self.textLabel7,0,1)

        self.line4 = QFrame(self.tab_2,"line4")
        self.line4.setFrameShape(QFrame.HLine)
        self.line4.setFrameShadow(QFrame.Sunken)
        self.line4.setFrameShape(QFrame.HLine)

        tabLayout_2.addMultiCellWidget(self.line4,4,4,0,2)

        layout2 = QGridLayout(None,1,1,0,6,"layout2")
        spacer5 = QSpacerItem(21,30,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout2.addItem(spacer5,2,1)

        self.addressBox = QComboBox(0,self.tab_2,"addressBox")

        layout2.addWidget(self.addressBox,0,1)

        self.homeLabel = QLabel(self.tab_2,"homeLabel")
        self.homeLabel.setMaximumSize(QSize(32,32))

        layout2.addWidget(self.homeLabel,0,0)

        tabLayout_2.addMultiCellLayout(layout2,5,6,0,1)

        self.addressEdit = QTextEdit(self.tab_2,"addressEdit")

        tabLayout_2.addWidget(self.addressEdit,6,2)
        self.tabWidget2.insertTab(self.tab_2,QString(""))

        self.TabPage = QWidget(self.tabWidget2,"TabPage")
        TabPageLayout = QGridLayout(self.TabPage,1,1,0,6,"TabPageLayout")

        self.personalLabel = QLabel(self.TabPage,"personalLabel")
        self.personalLabel.setMaximumSize(QSize(32,32))

        TabPageLayout.addWidget(self.personalLabel,5,0)

        self.ouEdit = QLineEdit(self.TabPage,"ouEdit")

        TabPageLayout.addWidget(self.ouEdit,0,2)

        self.textLabel5 = QLabel(self.TabPage,"textLabel5")
        self.textLabel5.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel5,2,1)

        self.roomNumberEdit = QLineEdit(self.TabPage,"roomNumberEdit")

        TabPageLayout.addWidget(self.roomNumberEdit,1,2)

        self.textLabel4 = QLabel(self.TabPage,"textLabel4")
        self.textLabel4.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel4,1,1)

        self.businessRoleEdit = QLineEdit(self.TabPage,"businessRoleEdit")

        TabPageLayout.addWidget(self.businessRoleEdit,2,2)

        self.workLabel = QLabel(self.TabPage,"workLabel")
        self.workLabel.setMaximumSize(QSize(32,32))

        TabPageLayout.addWidget(self.workLabel,0,0)

        self.textLabel3_3 = QLabel(self.TabPage,"textLabel3_3")
        self.textLabel3_3.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel3_3,0,1)

        self.line5 = QFrame(self.TabPage,"line5")
        self.line5.setFrameShape(QFrame.HLine)
        self.line5.setFrameShadow(QFrame.Sunken)
        self.line5.setFrameShape(QFrame.HLine)

        TabPageLayout.addMultiCellWidget(self.line5,3,4,0,5)

        self.managerNameEdit = QLineEdit(self.TabPage,"managerNameEdit")

        TabPageLayout.addWidget(self.managerNameEdit,0,5)

        self.assistantNameEdit = QLineEdit(self.TabPage,"assistantNameEdit")

        TabPageLayout.addWidget(self.assistantNameEdit,1,5)

        self.textLabel6 = QLabel(self.TabPage,"textLabel6")
        self.textLabel6.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel6,0,4)

        self.textLabel7_2 = QLabel(self.TabPage,"textLabel7_2")
        self.textLabel7_2.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel7_2,1,4)

        self.line7 = QFrame(self.TabPage,"line7")
        self.line7.setFrameShape(QFrame.VLine)
        self.line7.setFrameShadow(QFrame.Sunken)
        self.line7.setFrameShape(QFrame.VLine)

        TabPageLayout.addMultiCellWidget(self.line7,0,2,3,3)

        self.noteEdit = QTextEdit(self.TabPage,"noteEdit")

        TabPageLayout.addMultiCellWidget(self.noteEdit,10,11,1,5)

        self.textLabel14 = QLabel(self.TabPage,"textLabel14")
        self.textLabel14.setAlignment(QLabel.AlignVCenter | QLabel.AlignLeft)

        TabPageLayout.addWidget(self.textLabel14,9,1)

        self.line6 = QFrame(self.TabPage,"line6")
        self.line6.setFrameShape(QFrame.HLine)
        self.line6.setFrameShadow(QFrame.Sunken)
        self.line6.setFrameShape(QFrame.HLine)

        TabPageLayout.addMultiCellWidget(self.line6,7,7,0,5)

        self.anniversaryEdit = QDateEdit(self.TabPage,"anniversaryEdit")

        TabPageLayout.addWidget(self.anniversaryEdit,6,5)

        self.textLabel12 = QLabel(self.TabPage,"textLabel12")
        self.textLabel12.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel12,6,4)

        self.birthDateEdit = QDateEdit(self.TabPage,"birthDateEdit")

        TabPageLayout.addWidget(self.birthDateEdit,5,5)

        self.textLabel11 = QLabel(self.TabPage,"textLabel11")
        self.textLabel11.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel11,5,4)

        self.line8 = QFrame(self.TabPage,"line8")
        self.line8.setFrameShape(QFrame.VLine)
        self.line8.setFrameShadow(QFrame.Sunken)
        self.line8.setFrameShape(QFrame.VLine)

        TabPageLayout.addMultiCellWidget(self.line8,4,6,3,3)

        self.spouseNameEdit = QLineEdit(self.TabPage,"spouseNameEdit")

        TabPageLayout.addWidget(self.spouseNameEdit,6,2)

        self.displayNameEdit = QLineEdit(self.TabPage,"displayNameEdit")

        TabPageLayout.addWidget(self.displayNameEdit,5,2)

        self.textLabel9_2 = QLabel(self.TabPage,"textLabel9_2")
        self.textLabel9_2.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel9_2,5,1)

        self.textLabel10_2 = QLabel(self.TabPage,"textLabel10_2")
        self.textLabel10_2.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel10_2,6,1)

        self.notesLabel = QLabel(self.TabPage,"notesLabel")
        self.notesLabel.setMaximumSize(QSize(32,32))

        TabPageLayout.addMultiCellWidget(self.notesLabel,8,10,0,0)
        spacer7 = QSpacerItem(20,201,QSizePolicy.Minimum,QSizePolicy.Expanding)
        TabPageLayout.addItem(spacer7,11,0)
        self.tabWidget2.insertTab(self.TabPage,QString(""))

        AddressbookWidgetDesignLayout.addMultiCellWidget(self.tabWidget2,0,0,0,1)

        self.languageChange()

        self.resize(QSize(710,517).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.nameButton,SIGNAL("clicked()"),self.showNameDialog)
        self.connect(self.deleteMailButton,SIGNAL("clicked()"),self.deleteMail)
        self.connect(self.addMailButton,SIGNAL("clicked()"),self.addMail)
        self.connect(self.categoryButton,SIGNAL("clicked()"),self.editCategories)
        self.connect(self.addressBox,SIGNAL("activated(int)"),self.initAddress)

        self.setTabOrder(self.tabWidget2,self.nameButton)
        self.setTabOrder(self.nameButton,self.cnEdit)
        self.setTabOrder(self.cnEdit,self.titleEdit)
        self.setTabOrder(self.titleEdit,self.organisationEdit)
        self.setTabOrder(self.organisationEdit,self.mailBox)
        self.setTabOrder(self.mailBox,self.deleteMailButton)
        self.setTabOrder(self.deleteMailButton,self.addMailButton)
        self.setTabOrder(self.addMailButton,self.labeledURIEdit)
        self.setTabOrder(self.labeledURIEdit,self.categoryButton)
        self.setTabOrder(self.categoryButton,self.categoryEdit)
        self.setTabOrder(self.categoryEdit,self.homePhoneEdit)
        self.setTabOrder(self.homePhoneEdit,self.telephoneNumberEdit)
        self.setTabOrder(self.telephoneNumberEdit,self.mobileEdit)
        self.setTabOrder(self.mobileEdit,self.facsimileTelephoneNumberEdit)
        self.setTabOrder(self.facsimileTelephoneNumberEdit,self.addressBox)
        self.setTabOrder(self.addressBox,self.addressEdit)
        self.setTabOrder(self.addressEdit,self.ouEdit)
        self.setTabOrder(self.ouEdit,self.managerNameEdit)
        self.setTabOrder(self.managerNameEdit,self.roomNumberEdit)
        self.setTabOrder(self.roomNumberEdit,self.assistantNameEdit)
        self.setTabOrder(self.assistantNameEdit,self.businessRoleEdit)
        self.setTabOrder(self.businessRoleEdit,self.displayNameEdit)
        self.setTabOrder(self.displayNameEdit,self.birthDateEdit)
        self.setTabOrder(self.birthDateEdit,self.spouseNameEdit)
        self.setTabOrder(self.spouseNameEdit,self.anniversaryEdit)
        self.setTabOrder(self.anniversaryEdit,self.noteEdit)


    def languageChange(self):
        self.setCaption(self.__tr("AddressbookWidgetDesign"))
        self.personLabel.setText(self.__tr("P","DO NOT TRANSLATE"))
        self.nameButton.setText(self.__tr("&Full Name..."))
        self.nameButton.setAccel(self.__tr("Alt+F"))
        self.categoryButton.setText(self.__tr("&Categories..."))
        self.categoryButton.setAccel(self.__tr("Alt+C"))
        self.categoryLabel.setText(self.__tr("CL","DO NOT TRANSLATE"))
        self.webPageLabel.setText(self.__tr("WP","DO NOT TRANSLATE"))
        self.deleteMailButton.setText(self.__tr("&Delete"))
        self.deleteMailButton.setAccel(self.__tr("Alt+D"))
        self.addMailButton.setText(self.__tr("&Add..."))
        self.addMailButton.setAccel(self.__tr("Alt+A"))
        self.mailLabel.setText(self.__tr("Ma","DO NOT TRANSLATE"))
        self.textLabel10.setText(self.__tr("Email:"))
        self.textLabel1.setText(self.__tr("Web page address:"))
        self.textLabel2_2.setText(self.__tr("Organisation:"))
        self.textLabel3_2.setText(self.__tr("Job title:"))
        self.tabWidget2.changeTab(self.tab,self.__tr("General"))
        self.textLabel9.setText(self.__tr("Mobile:"))
        self.textLabel3.setText(self.__tr("Business Fax:"))
        self.phoneLabel.setText(self.__tr("Ph","DO NOT TRANSLATE"))
        self.textLabel8.setText(self.__tr("Work:"))
        self.textLabel7.setText(self.__tr("Home:"))
        self.addressBox.clear()
        self.addressBox.insertItem(self.__tr("Business"))
        self.addressBox.insertItem(self.__tr("Home"))
        self.addressBox.insertItem(self.__tr("Other"))
        self.homeLabel.setText(self.__tr("HI","DO NOT TRANSLATE"))
        self.tabWidget2.changeTab(self.tab_2,self.__tr("Phone/Address"))
        self.personalLabel.setText(self.__tr("ME","DO NOT TRANSLATE"))
        self.textLabel5.setText(self.__tr("Profession:"))
        self.textLabel4.setText(self.__tr("Office:"))
        self.workLabel.setText(self.__tr("WO","DO NOT TRANSLATE"))
        self.textLabel3_3.setText(self.__tr("Departement:"))
        self.textLabel6.setText(self.__tr("Manager's name:"))
        self.textLabel7_2.setText(self.__tr("Assistant's name:"))
        self.textLabel14.setText(self.__tr("Notes:"))
        self.textLabel12.setText(self.__tr("Anniversary:"))
        self.textLabel11.setText(self.__tr("Birthday:"))
        self.textLabel9_2.setText(self.__tr("Nickname:"))
        self.textLabel10_2.setText(self.__tr("Spouse:"))
        self.notesLabel.setText(self.__tr("NO","DO NOT TRANSLATE"))
        self.tabWidget2.changeTab(self.TabPage,self.__tr("Details"))


    def serverChanged(self):
        print "AddressbookWidgetDesign.serverChanged(): Not implemented yet"

    def search(self):
        print "AddressbookWidgetDesign.search(): Not implemented yet"

    def iconClicked(self):
        print "AddressbookWidgetDesign.iconClicked(): Not implemented yet"

    def addEntry(self):
        print "AddressbookWidgetDesign.addEntry(): Not implemented yet"

    def deleteEntry(self):
        print "AddressbookWidgetDesign.deleteEntry(): Not implemented yet"

    def saveEntry(self):
        print "AddressbookWidgetDesign.saveEntry(): Not implemented yet"

    def showNameDialog(self):
        print "AddressbookWidgetDesign.showNameDialog(): Not implemented yet"

    def deleteMail(self):
        print "AddressbookWidgetDesign.deleteMail(): Not implemented yet"

    def addMail(self):
        print "AddressbookWidgetDesign.addMail(): Not implemented yet"

    def editCategories(self):
        print "AddressbookWidgetDesign.editCategories(): Not implemented yet"

    def initAddress(self):
        print "AddressbookWidgetDesign.initAddress(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("AddressbookWidgetDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = AddressbookWidgetDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
