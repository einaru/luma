# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/addressbook/AddressbookWidgetDesign.ui'
#
# Created: Wed Aug 17 15:23:43 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
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
        self.tabWidget2.setFocusPolicy(QTabWidget.TabFocus)

        self.tab = QWidget(self.tabWidget2,"tab")
        tabLayout = QGridLayout(self.tab,1,1,0,6,"tabLayout")

        self.personLabel = QLabel(self.tab,"personLabel")
        self.personLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.personLabel.sizePolicy().hasHeightForWidth()))
        self.personLabel.setMinimumSize(QSize(32,32))

        tabLayout.addWidget(self.personLabel,0,0)

        self.nameButton = QPushButton(self.tab,"nameButton")

        tabLayout.addWidget(self.nameButton,0,1)

        self.textLabel2_2 = QLabel(self.tab,"textLabel2_2")
        self.textLabel2_2.setAlignment(QLabel.AlignVCenter)

        tabLayout.addWidget(self.textLabel2_2,2,1)

        self.textLabel3_2 = QLabel(self.tab,"textLabel3_2")
        self.textLabel3_2.setAlignment(QLabel.AlignVCenter)

        tabLayout.addWidget(self.textLabel3_2,1,1)

        self.cnEdit = QLineEdit(self.tab,"cnEdit")
        self.cnEdit.setReadOnly(1)

        tabLayout.addMultiCellWidget(self.cnEdit,0,0,2,5)

        self.titleEdit = QLineEdit(self.tab,"titleEdit")

        tabLayout.addMultiCellWidget(self.titleEdit,1,1,2,5)

        self.organisationEdit = QLineEdit(self.tab,"organisationEdit")

        tabLayout.addMultiCellWidget(self.organisationEdit,2,2,2,5)
        spacer4_2 = QSpacerItem(21,130,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addMultiCell(spacer4_2,8,8,2,3)

        self.addMailButton = QPushButton(self.tab,"addMailButton")

        tabLayout.addMultiCellWidget(self.addMailButton,5,5,3,4)

        self.deleteMailButton = QPushButton(self.tab,"deleteMailButton")

        tabLayout.addWidget(self.deleteMailButton,5,5)
        spacer8 = QSpacerItem(120,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        tabLayout.addItem(spacer8,5,2)
        spacer5_2 = QSpacerItem(21,20,QSizePolicy.Minimum,QSizePolicy.Fixed)
        tabLayout.addItem(spacer5_2,3,4)

        self.mailLabel = QLabel(self.tab,"mailLabel")
        self.mailLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.mailLabel.sizePolicy().hasHeightForWidth()))
        self.mailLabel.setMinimumSize(QSize(32,32))

        tabLayout.addWidget(self.mailLabel,4,0)

        self.webPageLabel = QLabel(self.tab,"webPageLabel")
        self.webPageLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.webPageLabel.sizePolicy().hasHeightForWidth()))
        self.webPageLabel.setMinimumSize(QSize(32,32))

        tabLayout.addWidget(self.webPageLabel,6,0)

        self.categoryLabel = QLabel(self.tab,"categoryLabel")
        self.categoryLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.categoryLabel.sizePolicy().hasHeightForWidth()))
        self.categoryLabel.setMinimumSize(QSize(32,32))
        self.categoryLabel.setMaximumSize(QSize(32,32))

        tabLayout.addWidget(self.categoryLabel,7,0)

        self.textLabel10 = QLabel(self.tab,"textLabel10")
        self.textLabel10.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel10.sizePolicy().hasHeightForWidth()))
        self.textLabel10.setAlignment(QLabel.AlignVCenter)

        tabLayout.addWidget(self.textLabel10,4,1)

        self.textLabel1 = QLabel(self.tab,"textLabel1")
        self.textLabel1.setAlignment(QLabel.AlignVCenter)

        tabLayout.addWidget(self.textLabel1,6,1)

        self.categoryButton = QPushButton(self.tab,"categoryButton")
        self.categoryButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.categoryButton.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.categoryButton,7,1)

        self.mailBox = QComboBox(0,self.tab,"mailBox")
        self.mailBox.setEditable(1)

        tabLayout.addMultiCellWidget(self.mailBox,4,4,2,5)

        self.labeledURIEdit = QLineEdit(self.tab,"labeledURIEdit")

        tabLayout.addMultiCellWidget(self.labeledURIEdit,6,6,2,5)

        self.categoryEdit = QLineEdit(self.tab,"categoryEdit")

        tabLayout.addMultiCellWidget(self.categoryEdit,7,7,2,5)
        self.tabWidget2.insertTab(self.tab,QString.fromLatin1(""))

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
        self.phoneLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.phoneLabel.sizePolicy().hasHeightForWidth()))
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
        spacer6 = QSpacerItem(21,25,QSizePolicy.Minimum,QSizePolicy.Fixed)
        tabLayout_2.addItem(spacer6,4,2)

        self.addressEdit = QTextEdit(self.tab_2,"addressEdit")

        tabLayout_2.addWidget(self.addressEdit,5,2)

        layout2 = QGridLayout(None,1,1,0,6,"layout2")
        spacer5 = QSpacerItem(21,30,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout2.addItem(spacer5,2,1)

        self.addressBox = QComboBox(0,self.tab_2,"addressBox")

        layout2.addWidget(self.addressBox,0,1)

        self.homeLabel = QLabel(self.tab_2,"homeLabel")
        self.homeLabel.setMaximumSize(QSize(32,32))

        layout2.addWidget(self.homeLabel,0,0)

        tabLayout_2.addMultiCellLayout(layout2,5,5,0,1)
        self.tabWidget2.insertTab(self.tab_2,QString.fromLatin1(""))

        self.TabPage = QWidget(self.tabWidget2,"TabPage")
        TabPageLayout = QGridLayout(self.TabPage,1,1,0,6,"TabPageLayout")

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
        spacer7_2 = QSpacerItem(21,25,QSizePolicy.Minimum,QSizePolicy.Fixed)
        TabPageLayout.addItem(spacer7_2,3,1)
        spacer8_2 = QSpacerItem(20,25,QSizePolicy.Minimum,QSizePolicy.Fixed)
        TabPageLayout.addItem(spacer8_2,6,1)

        self.personalLabel = QLabel(self.TabPage,"personalLabel")
        self.personalLabel.setMaximumSize(QSize(32,32))

        TabPageLayout.addWidget(self.personalLabel,4,0)

        self.textLabel9_2 = QLabel(self.TabPage,"textLabel9_2")
        self.textLabel9_2.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel9_2,4,1)

        self.displayNameEdit = QLineEdit(self.TabPage,"displayNameEdit")

        TabPageLayout.addWidget(self.displayNameEdit,4,2)

        self.spouseNameEdit = QLineEdit(self.TabPage,"spouseNameEdit")

        TabPageLayout.addWidget(self.spouseNameEdit,5,2)

        self.textLabel10_2 = QLabel(self.TabPage,"textLabel10_2")
        self.textLabel10_2.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel10_2,5,1)

        self.line8 = QFrame(self.TabPage,"line8")
        self.line8.setFrameShape(QFrame.VLine)
        self.line8.setFrameShadow(QFrame.Sunken)
        self.line8.setFrameShape(QFrame.VLine)

        TabPageLayout.addMultiCellWidget(self.line8,4,5,3,3)

        self.anniversaryEdit = QDateEdit(self.TabPage,"anniversaryEdit")

        TabPageLayout.addWidget(self.anniversaryEdit,5,5)

        self.birthDateEdit = QDateEdit(self.TabPage,"birthDateEdit")

        TabPageLayout.addWidget(self.birthDateEdit,4,5)

        self.textLabel12 = QLabel(self.TabPage,"textLabel12")
        self.textLabel12.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel12,5,4)

        self.textLabel11 = QLabel(self.TabPage,"textLabel11")
        self.textLabel11.setAlignment(QLabel.AlignVCenter)

        TabPageLayout.addWidget(self.textLabel11,4,4)
        spacer7 = QSpacerItem(20,201,QSizePolicy.Minimum,QSizePolicy.Expanding)
        TabPageLayout.addItem(spacer7,8,0)

        self.notesLabel = QLabel(self.TabPage,"notesLabel")
        self.notesLabel.setMaximumSize(QSize(32,32))

        TabPageLayout.addWidget(self.notesLabel,7,0)

        self.noteEdit = QTextEdit(self.TabPage,"noteEdit")

        TabPageLayout.addMultiCellWidget(self.noteEdit,8,8,1,5)

        self.textLabel14 = QLabel(self.TabPage,"textLabel14")
        self.textLabel14.setAlignment(QLabel.AlignVCenter | QLabel.AlignLeft)

        TabPageLayout.addWidget(self.textLabel14,7,1)
        self.tabWidget2.insertTab(self.TabPage,QString.fromLatin1(""))

        AddressbookWidgetDesignLayout.addMultiCellWidget(self.tabWidget2,0,0,0,1)

        self.languageChange()

        self.resize(QSize(608,454).expandedTo(self.minimumSizeHint()))
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
        self.textLabel2_2.setText(self.__tr("Organisation:"))
        self.textLabel3_2.setText(self.__tr("Job title:"))
        self.addMailButton.setText(self.__tr("&Add..."))
        self.addMailButton.setAccel(self.__tr("Alt+A"))
        self.deleteMailButton.setText(self.__tr("&Delete"))
        self.deleteMailButton.setAccel(self.__tr("Alt+D"))
        self.mailLabel.setText(self.__tr("Ma","DO NOT TRANSLATE"))
        self.webPageLabel.setText(self.__tr("WP","DO NOT TRANSLATE"))
        self.categoryLabel.setText(self.__tr("CL","DO NOT TRANSLATE"))
        self.textLabel10.setText(self.__tr("Email:"))
        self.textLabel1.setText(self.__tr("Web page address:"))
        self.categoryButton.setText(self.__tr("&Categories..."))
        self.categoryButton.setAccel(self.__tr("Alt+C"))
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
        self.textLabel5.setText(self.__tr("Profession:"))
        self.textLabel4.setText(self.__tr("Office:"))
        self.workLabel.setText(self.__tr("WO","DO NOT TRANSLATE"))
        self.textLabel3_3.setText(self.__tr("Departement:"))
        self.textLabel6.setText(self.__tr("Manager's name:"))
        self.textLabel7_2.setText(self.__tr("Assistant's name:"))
        self.personalLabel.setText(self.__tr("ME","DO NOT TRANSLATE"))
        self.textLabel9_2.setText(self.__tr("Nickname:"))
        self.textLabel10_2.setText(self.__tr("Spouse:"))
        self.textLabel12.setText(self.__tr("Anniversary:"))
        self.textLabel11.setText(self.__tr("Birthday:"))
        self.notesLabel.setText(self.__tr("NO","DO NOT TRANSLATE"))
        self.textLabel14.setText(self.__tr("Notes:"))
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
