# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/addressbook/AddressbookWidgetDesign.ui'
#
# Created: Fri Jan 30 21:15:54 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.8.1
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

        self.saveButton = QPushButton(self,"saveButton")

        AddressbookWidgetDesignLayout.addWidget(self.saveButton,1,1)
        spacer = QSpacerItem(320,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        AddressbookWidgetDesignLayout.addItem(spacer,1,0)

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

        self.textLabel3_2 = QLabel(self.tab,"textLabel3_2")
        self.textLabel3_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        tabLayout.addMultiCellWidget(self.textLabel3_2,1,1,1,2)
        spacer_2 = QSpacerItem(21,58,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addMultiCell(spacer_2,1,2,0,0)

        self.textLabel2_2 = QLabel(self.tab,"textLabel2_2")
        self.textLabel2_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        tabLayout.addMultiCellWidget(self.textLabel2_2,2,2,1,2)

        self.line3 = QFrame(self.tab,"line3")
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setFrameShadow(QFrame.Sunken)
        self.line3.setFrameShape(QFrame.HLine)

        tabLayout.addMultiCellWidget(self.line3,3,3,0,3)
        spacer_3 = QSpacerItem(21,290,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer_3,11,3)

        self.pushButton2 = QPushButton(self.tab,"pushButton2")
        self.pushButton2.setSizePolicy(QSizePolicy(0,0,0,0,self.pushButton2.sizePolicy().hasHeightForWidth()))

        tabLayout.addMultiCellWidget(self.pushButton2,10,10,1,2)

        self.categoryLabel = QLabel(self.tab,"categoryLabel")
        self.categoryLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.categoryLabel.sizePolicy().hasHeightForWidth()))
        self.categoryLabel.setMinimumSize(QSize(32,32))
        self.categoryLabel.setMaximumSize(QSize(32,32))

        tabLayout.addWidget(self.categoryLabel,10,0)

        self.line1 = QFrame(self.tab,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        tabLayout.addMultiCellWidget(self.line1,8,9,0,3)

        self.labeledURIEdit = QLineEdit(self.tab,"labeledURIEdit")

        tabLayout.addWidget(self.labeledURIEdit,7,3)

        self.webPageLabel = QLabel(self.tab,"webPageLabel")
        self.webPageLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.webPageLabel.sizePolicy().hasHeightForWidth()))
        self.webPageLabel.setMinimumSize(QSize(32,32))

        tabLayout.addWidget(self.webPageLabel,7,0)

        self.mailLabel = QLabel(self.tab,"mailLabel")
        self.mailLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.mailLabel.sizePolicy().hasHeightForWidth()))
        self.mailLabel.setMinimumSize(QSize(32,32))

        tabLayout.addMultiCellWidget(self.mailLabel,4,5,0,0)

        self.textLabel1 = QLabel(self.tab,"textLabel1")
        self.textLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        tabLayout.addMultiCellWidget(self.textLabel1,7,7,1,2)

        self.mailBox = QComboBox(0,self.tab,"mailBox")
        self.mailBox.setEditable(1)

        tabLayout.addWidget(self.mailBox,5,3)

        self.organisationEdit = QLineEdit(self.tab,"organisationEdit")

        tabLayout.addWidget(self.organisationEdit,2,3)

        self.titleEdit = QLineEdit(self.tab,"titleEdit")

        tabLayout.addWidget(self.titleEdit,1,3)

        self.cnEdit = QLineEdit(self.tab,"cnEdit")
        self.cnEdit.setReadOnly(1)

        tabLayout.addWidget(self.cnEdit,0,3)

        self.line2 = QFrame(self.tab,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)

        tabLayout.addMultiCellWidget(self.line2,6,6,0,3)

        self.categoryEdit = QLineEdit(self.tab,"categoryEdit")

        tabLayout.addMultiCellWidget(self.categoryEdit,9,10,3,3)

        self.textLabel10 = QLabel(self.tab,"textLabel10")
        self.textLabel10.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel10.sizePolicy().hasHeightForWidth()))
        self.textLabel10.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        tabLayout.addWidget(self.textLabel10,5,2)
        spacer_4 = QSpacerItem(51,21,QSizePolicy.Minimum,QSizePolicy.Minimum)
        tabLayout.addItem(spacer_4,5,1)
        self.tabWidget2.insertTab(self.tab,QString(""))

        self.tab_2 = QWidget(self.tabWidget2,"tab_2")
        tabLayout_2 = QGridLayout(self.tab_2,1,1,0,6,"tabLayout_2")

        self.homePhoneEdit = QLineEdit(self.tab_2,"homePhoneEdit")
        self.homePhoneEdit.setMinimumSize(QSize(100,0))

        tabLayout_2.addWidget(self.homePhoneEdit,0,2)

        self.textLabel9 = QLabel(self.tab_2,"textLabel9")
        self.textLabel9.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        tabLayout_2.addWidget(self.textLabel9,2,1)

        self.textLabel3 = QLabel(self.tab_2,"textLabel3")
        self.textLabel3.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

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
        self.textLabel8.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        tabLayout_2.addWidget(self.textLabel8,1,1)

        self.textLabel7 = QLabel(self.tab_2,"textLabel7")
        self.textLabel7.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        tabLayout_2.addWidget(self.textLabel7,0,1)
        spacer_5 = QSpacerItem(21,130,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout_2.addItem(spacer_5,7,2)

        self.line4 = QFrame(self.tab_2,"line4")
        self.line4.setFrameShape(QFrame.HLine)
        self.line4.setFrameShadow(QFrame.Sunken)
        self.line4.setFrameShape(QFrame.HLine)

        tabLayout_2.addMultiCellWidget(self.line4,4,4,0,2)

        layout2 = QGridLayout(None,1,1,0,6,"layout2")
        spacer_6 = QSpacerItem(21,30,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout2.addItem(spacer_6,2,1)

        self.pushButton4 = QPushButton(self.tab_2,"pushButton4")

        layout2.addWidget(self.pushButton4,1,1)

        self.addressBox = QComboBox(0,self.tab_2,"addressBox")

        layout2.addWidget(self.addressBox,0,1)

        self.homeLabel = QLabel(self.tab_2,"homeLabel")
        self.homeLabel.setMaximumSize(QSize(32,32))

        layout2.addWidget(self.homeLabel,0,0)

        tabLayout_2.addMultiCellLayout(layout2,5,6,0,1)

        self.textBrowser1 = QTextBrowser(self.tab_2,"textBrowser1")

        tabLayout_2.addWidget(self.textBrowser1,6,2)
        self.tabWidget2.insertTab(self.tab_2,QString(""))

        self.TabPage = QWidget(self.tabWidget2,"TabPage")
        TabPageLayout = QGridLayout(self.TabPage,1,1,0,6,"TabPageLayout")

        self.personalLabel = QLabel(self.TabPage,"personalLabel")
        self.personalLabel.setMaximumSize(QSize(32,32))

        TabPageLayout.addWidget(self.personalLabel,4,0)

        self.ouEdit = QLineEdit(self.TabPage,"ouEdit")

        TabPageLayout.addWidget(self.ouEdit,0,2)

        self.textLabel5 = QLabel(self.TabPage,"textLabel5")
        self.textLabel5.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        TabPageLayout.addWidget(self.textLabel5,2,1)

        self.roomNumberEdit = QLineEdit(self.TabPage,"roomNumberEdit")

        TabPageLayout.addWidget(self.roomNumberEdit,1,2)

        self.textLabel4 = QLabel(self.TabPage,"textLabel4")
        self.textLabel4.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        TabPageLayout.addWidget(self.textLabel4,1,1)

        self.textLabel7_2 = QLabel(self.TabPage,"textLabel7_2")
        self.textLabel7_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        TabPageLayout.addWidget(self.textLabel7_2,1,3)

        self.businessRoleEdit = QLineEdit(self.TabPage,"businessRoleEdit")

        TabPageLayout.addWidget(self.businessRoleEdit,2,2)

        self.textLabel6 = QLabel(self.TabPage,"textLabel6")
        self.textLabel6.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        TabPageLayout.addWidget(self.textLabel6,0,3)

        self.workLabel = QLabel(self.TabPage,"workLabel")
        self.workLabel.setMaximumSize(QSize(32,32))

        TabPageLayout.addWidget(self.workLabel,0,0)

        self.assistantNameEdit = QLineEdit(self.TabPage,"assistantNameEdit")

        TabPageLayout.addWidget(self.assistantNameEdit,1,4)

        self.managerNameEdit = QLineEdit(self.TabPage,"managerNameEdit")

        TabPageLayout.addWidget(self.managerNameEdit,0,4)

        self.textLabel3_3 = QLabel(self.TabPage,"textLabel3_3")
        self.textLabel3_3.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        TabPageLayout.addWidget(self.textLabel3_3,0,1)

        self.displayNameEdit = QLineEdit(self.TabPage,"displayNameEdit")

        TabPageLayout.addWidget(self.displayNameEdit,4,2)

        self.textLabel10_2 = QLabel(self.TabPage,"textLabel10_2")
        self.textLabel10_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        TabPageLayout.addWidget(self.textLabel10_2,5,1)

        self.textLabel9_2 = QLabel(self.TabPage,"textLabel9_2")
        self.textLabel9_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        TabPageLayout.addWidget(self.textLabel9_2,4,1)

        self.textLabel11 = QLabel(self.TabPage,"textLabel11")
        self.textLabel11.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        TabPageLayout.addWidget(self.textLabel11,4,3)

        self.textLabel12 = QLabel(self.TabPage,"textLabel12")
        self.textLabel12.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        TabPageLayout.addWidget(self.textLabel12,5,3)

        self.anniversaryEdit = QDateEdit(self.TabPage,"anniversaryEdit")

        TabPageLayout.addWidget(self.anniversaryEdit,5,4)

        self.birthDateEdit = QDateEdit(self.TabPage,"birthDateEdit")

        TabPageLayout.addWidget(self.birthDateEdit,4,4)

        self.notesLabel = QLabel(self.TabPage,"notesLabel")
        self.notesLabel.setMaximumSize(QSize(32,32))

        TabPageLayout.addWidget(self.notesLabel,7,0)
        spacer_7 = QSpacerItem(21,110,QSizePolicy.Minimum,QSizePolicy.Expanding)
        TabPageLayout.addItem(spacer_7,8,0)

        self.line6 = QFrame(self.TabPage,"line6")
        self.line6.setFrameShape(QFrame.HLine)
        self.line6.setFrameShadow(QFrame.Sunken)
        self.line6.setFrameShape(QFrame.HLine)

        TabPageLayout.addMultiCellWidget(self.line6,6,6,0,4)

        self.spouseNameEdit = QLineEdit(self.TabPage,"spouseNameEdit")

        TabPageLayout.addWidget(self.spouseNameEdit,5,2)

        self.line5 = QFrame(self.TabPage,"line5")
        self.line5.setFrameShape(QFrame.HLine)
        self.line5.setFrameShadow(QFrame.Sunken)
        self.line5.setFrameShape(QFrame.HLine)

        TabPageLayout.addMultiCellWidget(self.line5,3,3,0,4)

        self.textLabel14 = QLabel(self.TabPage,"textLabel14")
        self.textLabel14.setAlignment(QLabel.AlignVCenter | QLabel.AlignLeft)

        TabPageLayout.addWidget(self.textLabel14,7,1)

        self.noteEdit = QTextEdit(self.TabPage,"noteEdit")

        TabPageLayout.addMultiCellWidget(self.noteEdit,8,8,1,4)
        self.tabWidget2.insertTab(self.TabPage,QString(""))

        AddressbookWidgetDesignLayout.addMultiCellWidget(self.tabWidget2,0,0,0,1)

        self.languageChange()

        self.resize(QSize(589,459).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.saveButton,SIGNAL("clicked()"),self.saveEntry)
        self.connect(self.nameButton,SIGNAL("clicked()"),self.showNameDialog)


    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.saveButton.setText(self.__tr("Save"))
        self.personLabel.setText(self.__tr("P"))
        self.nameButton.setText(self.__tr("Full Name ..."))
        self.textLabel3_2.setText(self.__tr("Job title:"))
        self.textLabel2_2.setText(self.__tr("Organisation:"))
        self.pushButton2.setText(self.__tr("Categories ..."))
        self.categoryLabel.setText(self.__tr("CL"))
        self.webPageLabel.setText(self.__tr("WP"))
        self.mailLabel.setText(self.__tr("Ma"))
        self.textLabel1.setText(self.__tr("Web page address:"))
        self.textLabel10.setText(self.__tr("Email:"))
        self.tabWidget2.changeTab(self.tab,self.__tr("General"))
        self.textLabel9.setText(self.__tr("Mobile:"))
        self.textLabel3.setText(self.__tr("Business Fax:"))
        self.phoneLabel.setText(self.__tr("Ph"))
        self.textLabel8.setText(self.__tr("Work:"))
        self.textLabel7.setText(self.__tr("Home:"))
        self.pushButton4.setText(self.__tr("Address ..."))
        self.addressBox.clear()
        self.addressBox.insertItem(self.__tr("Business"))
        self.addressBox.insertItem(self.__tr("Home"))
        self.addressBox.insertItem(self.__tr("Other"))
        self.homeLabel.setText(self.__tr("HI"))
        self.tabWidget2.changeTab(self.tab_2,self.__tr("Phone/Address"))
        self.personalLabel.setText(self.__tr("ME"))
        self.textLabel5.setText(self.__tr("Profession:"))
        self.textLabel4.setText(self.__tr("Office:"))
        self.textLabel7_2.setText(self.__tr("Assistant's name:"))
        self.textLabel6.setText(self.__tr("Manager's name:"))
        self.workLabel.setText(self.__tr("WO"))
        self.textLabel3_3.setText(self.__tr("Departement:"))
        self.textLabel10_2.setText(self.__tr("Spouse:"))
        self.textLabel9_2.setText(self.__tr("Nickname:"))
        self.textLabel11.setText(self.__tr("Birthday:"))
        self.textLabel12.setText(self.__tr("Anniversary:"))
        self.notesLabel.setText(self.__tr("NO"))
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

    def __tr(self,s,c = None):
        return qApp.translate("AddressbookWidgetDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = AddressbookWidgetDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
