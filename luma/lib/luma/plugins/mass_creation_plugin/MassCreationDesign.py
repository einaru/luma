# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/mass_creation_plugin/MassCreationDesign.ui'
#
# Created: Wed Aug 17 15:23:42 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *

image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x10\x00\x00\x00\x10" \
    "\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\x00\x00\x01" \
    "\x8e\x49\x44\x41\x54\x38\x8d\x95\x93\x3f\x4b\x1c" \
    "\x51\x14\xc5\x7f\x77\x33\x96\xe2\x07\x90\x94\x62" \
    "\x67\xd4\xc2\xef\x20\x49\x13\x05\x0b\x0b\x21\x85" \
    "\x88\x85\xa8\x20\x82\xb0\x04\x02\x2a\x04\x44\x12" \
    "\x2c\x6c\xfc\x0a\x82\x5b\xd9\xa4\xb1\x14\x82\xa2" \
    "\xec\x6e\x63\x67\x48\x61\xa1\x2b\x2e\xb3\x6f\xfe" \
    "\xbd\xbd\x16\x6f\x66\x67\x75\xd8\x15\x0f\x0c\x97" \
    "\xfb\xee\xdc\x73\xcf\x3d\x33\x4f\x48\x31\xb9\x71" \
    "\xa3\x28\x08\xa0\x22\x80\x02\x70\xb1\x37\x22\xbc" \
    "\x85\x89\xb5\xba\xfa\xb1\x55\x3f\xb4\x79\x4c\x9f" \
    "\x89\xb5\xba\xf6\xeb\xf5\xc6\x57\xae\xf5\x74\x67" \
    "\x94\x66\x94\x9e\xa4\xc3\x33\x0d\x63\x83\x37\xb0" \
    "\x72\xa5\x2a\x20\x08\x8a\x76\xea\x97\x07\x9f\xc4" \
    "\xc3\x46\x34\xe3\x22\xb3\xb6\x41\x4a\x50\x5e\xff" \
    "\xe2\x72\x5c\x4e\x1b\x28\xb9\x7c\xce\xfe\x55\x4f" \
    "\x93\x88\xc7\xa0\x8f\x46\x81\xf9\xcd\x6a\x8f\xe2" \
    "\x00\x9e\xda\x88\x87\x54\xfe\x07\xc0\x66\x51\x5d" \
    "\x5c\xfe\x5e\x65\x6b\xe9\x23\x0b\x53\x43\x2f\x5a" \
    "\x4f\x6a\xb0\xb5\x5f\xc5\xd3\xb6\x75\x0a\x04\xca" \
    "\xdb\xc5\x49\xdf\xe6\x87\x59\x98\x1a\xe2\xd7\x19" \
    "\xd8\xec\x7b\x74\xd9\xea\xa9\x8d\x79\x0c\xe1\xe7" \
    "\xee\x05\xd3\x5f\x27\xf9\x3d\x53\x14\xba\x7a\x4c" \
    "\xee\x6a\x17\x6c\x14\xe3\x69\x12\xd2\x08\xc0\x86" \
    "\x11\xff\x1f\x60\xf6\x28\x9f\x22\x52\xe8\xc9\x79" \
    "\x14\x92\x30\x74\x2b\x3c\x85\x60\x4d\xc0\x5d\x23" \
    "\x7d\x23\x93\xd9\x3d\xb5\xfb\x77\x4a\x6b\xd6\x04" \
    "\xce\xc4\x66\x04\x89\x09\x68\xf8\x3d\x9a\x5f\x1d" \
    "\x65\x5c\xb6\x15\x38\x0f\xfc\x10\x62\xe3\x53\xfb" \
    "\x51\xdc\xbf\x17\x2a\x95\x73\x16\xff\x18\x4a\xb4" \
    "\x93\x0e\xdb\x7b\x61\x5b\x2d\x3c\xb5\x09\xf7\x06" \
    "\xe2\xc0\x50\xa9\x9c\xbf\x8b\x20\x09\x8c\x5b\x67" \
    "\xf4\xf3\xa1\xde\x5e\x47\x79\x45\xe0\xc5\xd6\x2a" \
    "\x20\xaf\xdc\x54\x30\xff\x56\x45\x54\xfb\x5e\xb6" \
    "\x37\xf1\x0c\xc3\x88\xd2\x50\xff\x19\x2d\xeb\x00" \
    "\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"

class MassCreationDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("MassCreationDesign")


        MassCreationDesignLayout = QGridLayout(self,1,1,11,6,"MassCreationDesignLayout")
        spacer4_2 = QSpacerItem(130,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        MassCreationDesignLayout.addItem(spacer4_2,1,0)

        self.createButton = QPushButton(self,"createButton")

        MassCreationDesignLayout.addWidget(self.createButton,1,1)

        self.tabWidget2 = QTabWidget(self,"tabWidget2")

        self.tab = QWidget(self.tabWidget2,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")

        self.textLabel2_3 = QLabel(self.tab,"textLabel2_3")

        tabLayout.addMultiCellWidget(self.textLabel2_3,0,0,0,3)
        spacer5 = QSpacerItem(16,21,QSizePolicy.Fixed,QSizePolicy.Minimum)
        tabLayout.addItem(spacer5,1,0)

        self.textLabel5_2 = QLabel(self.tab,"textLabel5_2")

        tabLayout.addMultiCellWidget(self.textLabel5_2,3,3,0,3)
        spacer9 = QSpacerItem(16,21,QSizePolicy.Fixed,QSizePolicy.Minimum)
        tabLayout.addItem(spacer9,4,0)
        spacer8 = QSpacerItem(16,21,QSizePolicy.Fixed,QSizePolicy.Minimum)
        tabLayout.addItem(spacer8,6,0)

        self.textLabel4_2 = QLabel(self.tab,"textLabel4_2")

        tabLayout.addMultiCellWidget(self.textLabel4_2,5,5,0,5)

        self.textLabel7 = QLabel(self.tab,"textLabel7")
        self.textLabel7.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.textLabel7.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.textLabel7,8,1)

        self.textLabel6 = QLabel(self.tab,"textLabel6")
        self.textLabel6.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.textLabel6.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.textLabel6,7,1)

        self.homeEdit = QLineEdit(self.tab,"homeEdit")

        tabLayout.addMultiCellWidget(self.homeEdit,6,6,2,6)

        self.gidBox = QSpinBox(self.tab,"gidBox")
        self.gidBox.setMaxValue(65535)
        self.gidBox.setValue(100)

        tabLayout.addMultiCellWidget(self.gidBox,7,7,2,5)

        self.shellEdit = QLineEdit(self.tab,"shellEdit")

        tabLayout.addMultiCellWidget(self.shellEdit,8,8,2,6)

        self.browseGroupButton = QPushButton(self.tab,"browseGroupButton")
        self.browseGroupButton.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.browseGroupButton.sizePolicy().hasHeightForWidth()))
        self.browseGroupButton.setPixmap(self.image0)

        tabLayout.addWidget(self.browseGroupButton,7,6)

        self.textLabel5 = QLabel(self.tab,"textLabel5")
        self.textLabel5.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.textLabel5.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.textLabel5,6,1)

        self.textLabel2 = QLabel(self.tab,"textLabel2")
        self.textLabel2.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.textLabel2.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.textLabel2,2,1)

        self.textLabel1 = QLabel(self.tab,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.textLabel1,1,1)

        self.textLabel2_2 = QLabel(self.tab,"textLabel2_2")
        self.textLabel2_2.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.textLabel2_2.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.textLabel2_2,4,1)

        self.uidNumMaxBox = QSpinBox(self.tab,"uidNumMaxBox")
        self.uidNumMaxBox.setMaxValue(65535)
        self.uidNumMaxBox.setValue(65535)

        tabLayout.addMultiCellWidget(self.uidNumMaxBox,4,4,5,6)

        self.prefixMaxBox = QSpinBox(self.tab,"prefixMaxBox")
        self.prefixMaxBox.setMaxValue(65535)

        tabLayout.addMultiCellWidget(self.prefixMaxBox,2,2,5,6)

        self.dateButton = QRadioButton(self.tab,"dateButton")
        self.dateButton.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Fixed,0,0,self.dateButton.sizePolicy().hasHeightForWidth()))
        self.dateButton.setChecked(0)

        tabLayout.addWidget(self.dateButton,10,1)

        self.daysButton = QRadioButton(self.tab,"daysButton")
        self.daysButton.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Fixed,0,0,self.daysButton.sizePolicy().hasHeightForWidth()))
        self.daysButton.setChecked(1)

        tabLayout.addMultiCellWidget(self.daysButton,11,11,1,2)
        spacer7 = QSpacerItem(16,21,QSizePolicy.Fixed,QSizePolicy.Minimum)
        tabLayout.addItem(spacer7,10,0)

        self.textLabel3_3 = QLabel(self.tab,"textLabel3_3")

        tabLayout.addMultiCellWidget(self.textLabel3_3,9,9,0,6)

        self.dateEdit = QDateEdit(self.tab,"dateEdit")
        self.dateEdit.setEnabled(0)

        tabLayout.addMultiCellWidget(self.dateEdit,10,10,2,6)

        self.textLabel1_3 = QLabel(self.tab,"textLabel1_3")

        tabLayout.addMultiCellWidget(self.textLabel1_3,12,12,0,5)
        spacer6 = QSpacerItem(16,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        tabLayout.addItem(spacer6,13,0)

        self.browseButton = QPushButton(self.tab,"browseButton")
        self.browseButton.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.browseButton.sizePolicy().hasHeightForWidth()))
        self.browseButton.setPixmap(self.image0)

        tabLayout.addWidget(self.browseButton,13,6)

        self.nodeEdit = QLineEdit(self.tab,"nodeEdit")
        self.nodeEdit.setReadOnly(1)

        tabLayout.addMultiCellWidget(self.nodeEdit,13,13,2,5)

        self.textLabel4 = QLabel(self.tab,"textLabel4")

        tabLayout.addWidget(self.textLabel4,13,1)
        spacer2 = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer2,14,3)

        self.prefixEdit = QLineEdit(self.tab,"prefixEdit")

        tabLayout.addMultiCellWidget(self.prefixEdit,1,1,2,6)

        self.uidNumMinBox = QSpinBox(self.tab,"uidNumMinBox")
        self.uidNumMinBox.setMaxValue(65535)
        self.uidNumMinBox.setValue(1000)

        tabLayout.addMultiCellWidget(self.uidNumMinBox,4,4,2,3)

        self.prefixMinBox = QSpinBox(self.tab,"prefixMinBox")
        self.prefixMinBox.setMaxValue(65535)

        tabLayout.addMultiCellWidget(self.prefixMinBox,2,2,2,3)

        self.dayBox = QSpinBox(self.tab,"dayBox")
        self.dayBox.setEnabled(1)
        self.dayBox.setMaxValue(65535)
        self.dayBox.setValue(120)

        tabLayout.addMultiCellWidget(self.dayBox,11,11,3,6)

        self.textLabel3_2 = QLabel(self.tab,"textLabel3_2")
        self.textLabel3_2.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.textLabel3_2.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.textLabel3_2,4,4)

        self.textLabel3 = QLabel(self.tab,"textLabel3")
        self.textLabel3.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.textLabel3.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.textLabel3,2,4)
        self.tabWidget2.insertTab(self.tab,QString.fromLatin1(""))

        self.TabPage = QWidget(self.tabWidget2,"TabPage")
        TabPageLayout = QGridLayout(self.TabPage,1,1,11,6,"TabPageLayout")

        self.enableNFSBox = QCheckBox(self.TabPage,"enableNFSBox")

        TabPageLayout.addMultiCellWidget(self.enableNFSBox,0,0,0,2)

        self.automountLabel = QLabel(self.TabPage,"automountLabel")

        TabPageLayout.addMultiCellWidget(self.automountLabel,1,1,0,2)
        spacer8_2 = QSpacerItem(16,21,QSizePolicy.Fixed,QSizePolicy.Minimum)
        TabPageLayout.addItem(spacer8_2,2,0)

        self.serverLabel = QLabel(self.TabPage,"serverLabel")

        TabPageLayout.addWidget(self.serverLabel,2,1)

        self.argLabel = QLabel(self.TabPage,"argLabel")

        TabPageLayout.addWidget(self.argLabel,3,1)

        self.locationLabel = QLabel(self.TabPage,"locationLabel")

        TabPageLayout.addWidget(self.locationLabel,5,1)

        self.automountLocationEdit = QLineEdit(self.TabPage,"automountLocationEdit")
        self.automountLocationEdit.setReadOnly(1)

        TabPageLayout.addWidget(self.automountLocationEdit,5,2)

        self.browseAutomountButton = QPushButton(self.TabPage,"browseAutomountButton")
        self.browseAutomountButton.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.browseAutomountButton.sizePolicy().hasHeightForWidth()))
        self.browseAutomountButton.setPixmap(self.image0)

        TabPageLayout.addWidget(self.browseAutomountButton,5,3)

        self.nfsArgumentsEdit = QLineEdit(self.TabPage,"nfsArgumentsEdit")

        TabPageLayout.addMultiCellWidget(self.nfsArgumentsEdit,3,3,2,3)

        self.nfsServerEdit = QLineEdit(self.TabPage,"nfsServerEdit")

        TabPageLayout.addMultiCellWidget(self.nfsServerEdit,2,2,2,3)
        spacer10 = QSpacerItem(41,111,QSizePolicy.Minimum,QSizePolicy.Expanding)
        TabPageLayout.addItem(spacer10,6,2)
        self.tabWidget2.insertTab(self.TabPage,QString.fromLatin1(""))

        self.tab_2 = QWidget(self.tabWidget2,"tab_2")
        tabLayout_2 = QVBoxLayout(self.tab_2,11,6,"tabLayout_2")

        self.textLabel1_2 = QLabel(self.tab_2,"textLabel1_2")
        tabLayout_2.addWidget(self.textLabel1_2)

        self.passwordEdit = QTextEdit(self.tab_2,"passwordEdit")
        tabLayout_2.addWidget(self.passwordEdit)
        self.tabWidget2.insertTab(self.tab_2,QString.fromLatin1(""))

        MassCreationDesignLayout.addMultiCellWidget(self.tabWidget2,0,0,0,1)

        self.languageChange()

        self.resize(QSize(494,547).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.createButton,SIGNAL("clicked()"),self.createUsers)
        self.connect(self.browseButton,SIGNAL("clicked()"),self.browseServer)
        self.connect(self.browseGroupButton,SIGNAL("clicked()"),self.browseGroups)
        self.connect(self.enableNFSBox,SIGNAL("clicked()"),self.enableAutomount)
        self.connect(self.browseAutomountButton,SIGNAL("clicked()"),self.browseAutomount)

        self.setTabOrder(self.tabWidget2,self.prefixEdit)
        self.setTabOrder(self.prefixEdit,self.prefixMinBox)
        self.setTabOrder(self.prefixMinBox,self.prefixMaxBox)
        self.setTabOrder(self.prefixMaxBox,self.uidNumMinBox)
        self.setTabOrder(self.uidNumMinBox,self.uidNumMaxBox)
        self.setTabOrder(self.uidNumMaxBox,self.homeEdit)
        self.setTabOrder(self.homeEdit,self.gidBox)
        self.setTabOrder(self.gidBox,self.browseGroupButton)
        self.setTabOrder(self.browseGroupButton,self.shellEdit)
        self.setTabOrder(self.shellEdit,self.dateButton)
        self.setTabOrder(self.dateButton,self.dateEdit)
        self.setTabOrder(self.dateEdit,self.daysButton)
        self.setTabOrder(self.daysButton,self.dayBox)
        self.setTabOrder(self.dayBox,self.nodeEdit)
        self.setTabOrder(self.nodeEdit,self.browseButton)
        self.setTabOrder(self.browseButton,self.createButton)
        self.setTabOrder(self.createButton,self.enableNFSBox)
        self.setTabOrder(self.enableNFSBox,self.nfsServerEdit)
        self.setTabOrder(self.nfsServerEdit,self.nfsArgumentsEdit)
        self.setTabOrder(self.nfsArgumentsEdit,self.automountLocationEdit)
        self.setTabOrder(self.automountLocationEdit,self.browseAutomountButton)
        self.setTabOrder(self.browseAutomountButton,self.passwordEdit)


    def languageChange(self):
        self.setCaption(self.__tr("MassCreationDesign"))
        self.createButton.setText(self.__tr("&Create"))
        self.createButton.setAccel(self.__tr("Alt+C"))
        self.textLabel2_3.setText(self.__tr("<b>Usernames</b>"))
        self.textLabel5_2.setText(self.__tr("<b>UID number range</b>"))
        self.textLabel4_2.setText(self.__tr("<b>Account settings</b>"))
        self.textLabel7.setText(self.__tr("Login shell:"))
        self.textLabel6.setText(self.__tr("Group Id:"))
        self.homeEdit.setText(self.__tr("/home"))
        self.shellEdit.setText(self.__tr("/bin/bash"))
        self.browseGroupButton.setText(QString.null)
        QToolTip.add(self.browseGroupButton,self.__tr("Select group from LDAP"))
        self.textLabel5.setText(self.__tr("Home prefix:"))
        self.textLabel2.setText(self.__tr("Minimum:"))
        self.textLabel1.setText(self.__tr("Prefix:"))
        self.textLabel2_2.setText(self.__tr("Minimum:"))
        self.dateButton.setText(self.__tr("Date"))
        self.daysButton.setText(self.__tr("Days from now"))
        self.textLabel3_3.setText(self.__tr("<b>Expiration date</b>"))
        self.textLabel1_3.setText(self.__tr("<b>Directory location</b>"))
        self.browseButton.setText(QString.null)
        self.textLabel4.setText(self.__tr("Base node:"))
        self.textLabel3_2.setText(self.__tr("Maximum:"))
        self.textLabel3.setText(self.__tr("Maximum:"))
        self.tabWidget2.changeTab(self.tab,self.__tr("Account"))
        self.enableNFSBox.setText(self.__tr("Enable automount support"))
        self.automountLabel.setText(self.__tr("<b>Automount options</b>"))
        self.serverLabel.setText(self.__tr("Server:"))
        self.argLabel.setText(self.__tr("Arguments:"))
        self.locationLabel.setText(self.__tr("Location:"))
        self.browseAutomountButton.setText(QString.null)
        self.nfsArgumentsEdit.setText(self.__tr("-fstype=nfs,rw,quota,soft,intr"))
        self.tabWidget2.changeTab(self.TabPage,self.__tr("Automount"))
        self.textLabel1_2.setText(self.__tr("<b>Account Passwords</b>"))
        self.tabWidget2.changeTab(self.tab_2,self.__tr("Passwords"))


    def createUsers(self):
        print "MassCreationDesign.createUsers(): Not implemented yet"

    def browseServer(self):
        print "MassCreationDesign.browseServer(): Not implemented yet"

    def browseGroups(self):
        print "MassCreationDesign.browseGroups(): Not implemented yet"

    def showHelp(self):
        print "MassCreationDesign.showHelp(): Not implemented yet"

    def browseAutomount(self):
        print "MassCreationDesign.browseAutomount(): Not implemented yet"

    def enableAutomount(self):
        print "MassCreationDesign.enableAutomount(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("MassCreationDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = MassCreationDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
