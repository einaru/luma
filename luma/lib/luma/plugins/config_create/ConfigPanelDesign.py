# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/config_create/ConfigPanelDesign.ui'
#
# Created: Mon Apr 26 16:00:27 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *

image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x16\x00\x00\x00\x16" \
    "\x08\x06\x00\x00\x00\xc4\xb4\x6c\x3b\x00\x00\x03" \
    "\xc5\x49\x44\x41\x54\x78\x9c\xb5\x95\x4b\x68\x9c" \
    "\x55\x14\xc7\x7f\xdf\x37\xdf\x34\x93\x36\xaf\x46" \
    "\xd3\xb4\xd6\x36\xd1\x62\x15\x69\x2b\x05\x4b\x4b" \
    "\x35\x45\x24\x5d\xf8\x40\x6b\x11\xa4\xae\x14\x17" \
    "\xe2\x03\x97\x5d\xf8\x5c\x08\xee\x54\x2a\x08\x6e" \
    "\x94\x2e\x44\x41\xc4\x17\x48\x91\xa6\xd6\x5a\x99" \
    "\xda\x60\xa9\x8f\x56\x65\x8c\xa5\xd3\x34\x69\x92" \
    "\x79\x64\x26\x33\xf3\x3d\xee\xe3\x5c\x17\x13\x9b" \
    "\x0e\x11\x45\x25\x17\x2e\xf7\xc0\xe5\xfc\xee\xb9" \
    "\xe7\xfe\xcf\xb9\x5e\x36\x9b\x65\x29\x86\xbf\x24" \
    "\x54\x20\xf8\xb7\x0e\x9f\x1e\x4e\x39\x31\x8e\xf4" \
    "\x32\x9f\x5a\x4d\xb3\x6f\x8f\xe7\xfd\x6f\xf0\x67" \
    "\x23\x29\xd7\xdb\x9d\xe1\xbe\xbb\x37\x90\x4e\xfb" \
    "\xbc\xf6\xe6\x29\x20\xf5\xdf\x23\x3e\x74\x34\x70" \
    "\x56\x60\xf7\xae\xf5\xec\xd8\xd6\x4f\xa3\x61\x48" \
    "\xa7\x7d\x36\xdf\xdc\xcf\xdb\xef\x4f\xb9\xc7\xf6" \
    "\x05\x8b\xa2\xf6\x06\x1e\xfd\xc5\xed\xb9\x63\x15" \
    "\x22\xa0\x2c\x68\x23\x28\x03\x1f\x1e\x9a\xe0\xcb" \
    "\xe7\x42\xef\x8b\xaf\xd3\x6e\xf0\xda\x1e\x76\xdf" \
    "\x39\x40\x77\x67\x1a\x63\x1c\x5a\x5b\x8c\x71\x64" \
    "\x32\x29\x9e\x7f\xe5\x24\xd5\xb9\x84\xa7\x1e\x69" \
    "\x6b\x81\x7b\x43\xfb\xcf\xb9\xd7\x5f\xba\x0e\x65" \
    "\x20\xb6\xa0\x0c\x24\x1a\x26\xc6\x22\xf2\x27\x72" \
    "\xec\x1d\x5e\xc7\xad\x5b\x7b\xd1\x1a\x94\x02\x6b" \
    "\x17\xc0\xce\x39\x7e\x1f\xaf\xf3\xf2\x1b\x3f\x72" \
    "\xf8\x8c\x47\xf6\xad\x65\x97\xe1\x81\x73\xae\xe5" \
    "\x0a\x46\xc1\xe4\xe8\x04\x9d\x26\xe6\xc5\x67\x6e" \
    "\x61\x79\x3b\x58\xfb\xd7\x29\x12\x71\x6c\xda\xd8" \
    "\xc3\xd0\xd6\x5e\x44\x4a\xad\x39\xb6\xb2\x00\xae" \
    "\x5c\x88\x98\x38\x75\x9e\x7b\x87\x07\x19\x5c\xdf" \
    "\xfe\xb7\x79\x9f\xad\x1b\x0e\x7c\x32\x0d\xce\xa1" \
    "\xf5\x0a\x72\xe5\x59\x76\x3e\xa1\x1d\x22\xe0\x1c" \
    "\xc1\x95\xd1\xcc\x4d\xcd\xb1\x73\xdb\x9a\x7f\x84" \
    "\x56\x1a\xc2\x3d\x2f\xe4\x18\xbe\xfd\x1a\xae\x5f" \
    "\xd7\x81\x08\x0c\xde\xb8\x9a\x5a\xc3\xa2\x0d\x1c" \
    "\x78\xf5\x3b\x02\x2b\x0b\x0e\xfe\xda\x55\x3c\xfb" \
    "\xce\x19\xb6\x6f\x13\x9c\x05\x2b\x16\x6b\x05\x31" \
    "\x0e\xb1\x0e\x33\x6f\x7f\xfe\x6d\x99\x07\xef\x1a" \
    "\x60\x59\x5f\x0f\xc7\xf2\x20\x02\x6d\x19\xf8\xe1" \
    "\x74\x95\xf1\x23\x63\x8b\x53\xf1\xf1\x48\x81\xc1" \
    "\x1b\xfa\xd8\xb2\x36\x60\xe5\xd5\xcb\x09\xc5\x11" \
    "\x29\x47\xa4\x20\x8c\x1d\xa1\x16\xe2\x18\x1e\xdf" \
    "\xb8\x9a\x24\x1d\x30\x7a\xae\x09\xf5\x7c\x28\xe5" \
    "\x23\x66\x4e\x9c\x07\xa9\x83\xe7\x5a\xc1\x23\xc7" \
    "\x67\xc8\xbd\xbb\x89\xd2\x8c\xa6\xfb\xaa\x00\xe9" \
    "\x80\x42\x0d\x8a\x35\xc8\x5f\x82\xfa\x2c\x14\x13" \
    "\x28\xce\x40\xb9\x62\x29\x16\x12\xc2\x52\x9d\x4b" \
    "\x67\x67\xa8\x4c\x36\x20\xf6\xa0\xd3\x82\xef\x08" \
    "\x8c\x69\x42\x8f\x8e\x46\x0c\x6d\xee\xa2\x3d\x03" \
    "\xe9\x55\x69\x4e\xe7\xe6\xe8\x5b\xdf\x45\xee\x22" \
    "\x8c\xe5\x61\xaa\x60\x28\x14\x2d\xd3\x45\x43\xa1" \
    "\x68\x08\x2b\x11\x51\xa5\x41\x65\x72\x16\xa7\x1c" \
    "\x84\x40\x60\x01\x4b\xf6\x60\x87\x17\xc8\xbc\xdc" \
    "\x8e\x9d\x2c\xb3\xf7\xb6\x5e\x1a\x02\xd3\x09\xcc" \
    "\xf8\x5d\xfc\xfa\xbd\x45\x5c\x8a\x30\x76\x28\x05" \
    "\xb1\x12\x12\xe5\x88\x13\xa1\x58\x08\xd1\xa1\x86" \
    "\x15\x2b\xc0\x26\x40\x02\x29\x05\xae\xf9\x68\xbe" \
    "\x58\x61\xae\x01\x3f\xfd\x5c\xe1\xa1\xe1\x0e\x72" \
    "\x65\xb8\x58\x86\x18\x28\xd7\x84\x6a\x5d\x48\xb4" \
    "\x23\x56\x0e\xa5\xa1\x52\xd5\x4c\x4d\x85\xd8\xa0" \
    "\x0d\x3f\xd3\xd6\x2a\x97\x94\x01\x7b\x59\xc7\x30" \
    "\x72\xa2\xc6\xae\x2d\xdd\x4c\xd5\xa1\x23\x80\x35" \
    "\x19\xe8\xb0\xd0\xb5\x26\xa0\x5a\x56\x98\xc0\xa3" \
    "\x57\x0c\x5d\x3a\xa6\xb3\x5f\xb1\xa1\x27\x85\x24" \
    "\x09\x12\x26\x98\x44\x13\x85\x86\x42\x49\xc8\x8f" \
    "\x6b\xb2\xef\x75\x7b\x00\x81\xb1\x8e\xaf\xb2\x25" \
    "\xf6\x3f\xd0\xcf\x4d\x9d\xf3\x27\xaf\x04\xad\x21" \
    "\x8e\x1d\x5a\xfb\x24\x89\x21\x49\x2c\x4a\xf9\x28" \
    "\x15\x10\xc7\x06\xad\x03\xe2\xb8\x1d\xa5\xd2\x28" \
    "\x95\xe1\xa3\xe3\x55\x0e\x5e\x58\x10\x82\xdf\x08" \
    "\x0d\xe7\xf3\x35\xee\xdf\xde\x5a\x14\xbe\x0f\x41" \
    "\xe0\x93\x4a\x79\xf8\xbe\x3f\x6f\xfb\x97\x6d\xdf" \
    "\x6f\xee\xfd\x69\x7f\x73\x36\x82\x2b\x14\x16\x94" \
    "\x26\x1b\x3c\xf9\xf0\xc0\xa2\xea\x4a\xa5\x9a\xd3" \
    "\xe1\x10\x31\x24\x4a\x13\xc5\x09\x51\xa4\x09\x43" \
    "\x45\x9c\x24\xc4\x91\x46\x6b\x21\xd1\x86\xb1\xdf" \
    "\x42\xb2\x1f\xac\x5c\x68\x42\xf8\x1e\x47\x4e\x95" \
    "\xd9\xf1\x74\x15\x27\xcd\x52\x47\x1c\x22\x82\xb5" \
    "\x82\xd5\x82\x31\x06\x6b\x04\x6b\x0c\xc6\x58\x8c" \
    "\xb6\x88\x91\xe6\x2a\x96\x46\xe8\x20\x6c\x6d\x66" \
    "\xde\x52\x7d\xa6\x7f\x00\xba\xf7\x3c\x74\xbf\xb0" \
    "\xe0\xa8\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42" \
    "\x60\x82"

class ConfigPanelDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("ConfigPanelDesign")


        ConfigPanelDesignLayout = QVBoxLayout(self,11,6,"ConfigPanelDesignLayout")

        self.groupBox4 = QGroupBox(self,"groupBox4")
        self.groupBox4.setFrameShape(QGroupBox.GroupBoxPanel)
        self.groupBox4.setFrameShadow(QGroupBox.Sunken)
        self.groupBox4.setColumnLayout(0,Qt.Vertical)
        self.groupBox4.layout().setSpacing(6)
        self.groupBox4.layout().setMargin(11)
        groupBox4Layout = QHBoxLayout(self.groupBox4.layout())
        groupBox4Layout.setAlignment(Qt.AlignTop)

        layout4 = QVBoxLayout(None,0,6,"layout4")

        self.textLabel1 = QLabel(self.groupBox4,"textLabel1")
        layout4.addWidget(self.textLabel1)

        self.textLabel2 = QLabel(self.groupBox4,"textLabel2")
        layout4.addWidget(self.textLabel2)

        self.textLabel3 = QLabel(self.groupBox4,"textLabel3")
        layout4.addWidget(self.textLabel3)

        self.textLabel4 = QLabel(self.groupBox4,"textLabel4")
        layout4.addWidget(self.textLabel4)

        self.textLabel2_2 = QLabel(self.groupBox4,"textLabel2_2")
        layout4.addWidget(self.textLabel2_2)
        groupBox4Layout.addLayout(layout4)

        layout5 = QGridLayout(None,1,1,0,6,"layout5")

        self.helpDistribution = QPushButton(self.groupBox4,"helpDistribution")

        layout5.addWidget(self.helpDistribution,4,1)

        self.helpSuffix = QPushButton(self.groupBox4,"helpSuffix")

        layout5.addWidget(self.helpSuffix,0,1)

        self.suffix = QLineEdit(self.groupBox4,"suffix")

        layout5.addWidget(self.suffix,0,0)

        self.adminName = QLineEdit(self.groupBox4,"adminName")

        layout5.addWidget(self.adminName,1,0)

        self.distributionBox = QComboBox(0,self.groupBox4,"distributionBox")

        layout5.addWidget(self.distributionBox,4,0)

        self.adminPassword = QLineEdit(self.groupBox4,"adminPassword")
        self.adminPassword.setEchoMode(QLineEdit.Password)

        layout5.addWidget(self.adminPassword,2,0)

        self.helpAdminName = QPushButton(self.groupBox4,"helpAdminName")

        layout5.addWidget(self.helpAdminName,1,1)
        spacer4 = QSpacerItem(58,20,QSizePolicy.Minimum,QSizePolicy.Minimum)
        layout5.addItem(spacer4,3,1)

        self.helpPassword = QPushButton(self.groupBox4,"helpPassword")

        layout5.addWidget(self.helpPassword,2,1)

        self.adminPasswordVerify = QLineEdit(self.groupBox4,"adminPasswordVerify")
        self.adminPasswordVerify.setEchoMode(QLineEdit.Password)

        layout5.addWidget(self.adminPasswordVerify,3,0)
        groupBox4Layout.addLayout(layout5)
        ConfigPanelDesignLayout.addWidget(self.groupBox4)

        self.groupBox5 = QGroupBox(self,"groupBox5")
        self.groupBox5.setColumnLayout(0,Qt.Vertical)
        self.groupBox5.layout().setSpacing(6)
        self.groupBox5.layout().setMargin(11)
        groupBox5Layout = QVBoxLayout(self.groupBox5.layout())
        groupBox5Layout.setAlignment(Qt.AlignTop)

        layout10 = QHBoxLayout(None,0,6,"layout10")

        self.textLabel5 = QLabel(self.groupBox5,"textLabel5")
        layout10.addWidget(self.textLabel5)

        self.saveFile = QLineEdit(self.groupBox5,"saveFile")
        layout10.addWidget(self.saveFile)

        self.fileChooserButton = QPushButton(self.groupBox5,"fileChooserButton")
        self.fileChooserButton.setPixmap(self.image0)
        layout10.addWidget(self.fileChooserButton)
        groupBox5Layout.addLayout(layout10)
        ConfigPanelDesignLayout.addWidget(self.groupBox5)
        spacer1 = QSpacerItem(21,191,QSizePolicy.Minimum,QSizePolicy.Expanding)
        ConfigPanelDesignLayout.addItem(spacer1)

        self.finishConfig = QPushButton(self,"finishConfig")
        ConfigPanelDesignLayout.addWidget(self.finishConfig)

        self.languageChange()

        self.resize(QSize(452,339).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.helpAdminName,SIGNAL("clicked()"),self.displayAdminNameHelp)
        self.connect(self.helpPassword,SIGNAL("clicked()"),self.displayPasswordHelp)
        self.connect(self.helpSuffix,SIGNAL("clicked()"),self.displaySuffixHelp)
        self.connect(self.finishConfig,SIGNAL("clicked()"),self.createConfig)
        self.connect(self.helpDistribution,SIGNAL("clicked()"),self.displayDistributionHelp)
        self.connect(self.fileChooserButton,SIGNAL("clicked()"),self.displayFileChooser)

        self.setTabOrder(self.suffix,self.adminName)
        self.setTabOrder(self.adminName,self.adminPassword)
        self.setTabOrder(self.adminPassword,self.adminPasswordVerify)
        self.setTabOrder(self.adminPasswordVerify,self.distributionBox)
        self.setTabOrder(self.distributionBox,self.saveFile)
        self.setTabOrder(self.saveFile,self.fileChooserButton)
        self.setTabOrder(self.fileChooserButton,self.finishConfig)
        self.setTabOrder(self.finishConfig,self.helpSuffix)
        self.setTabOrder(self.helpSuffix,self.helpAdminName)
        self.setTabOrder(self.helpAdminName,self.helpPassword)
        self.setTabOrder(self.helpPassword,self.helpDistribution)

        self.textLabel1.setBuddy(self.suffix)
        self.textLabel2.setBuddy(self.adminName)
        self.textLabel3.setBuddy(self.adminPassword)


    def languageChange(self):
        self.setCaption(self.__tr("ConfigPanelDesign"))
        self.groupBox4.setTitle(self.__tr("Server Options"))
        self.textLabel1.setText(self.__tr("Base DN:","DO NOT TRANSLATE"))
        self.textLabel2.setText(self.__tr("Admin Name:","DO NOT TRANSLATE"))
        self.textLabel3.setText(self.__tr("Admin Password:","DO NOT TRANSLATE"))
        self.textLabel4.setText(self.__tr("Admin Password (Re-Type):","DO NOT TRANSLATE"))
        self.textLabel2_2.setText(self.__tr("Distribution:","DO NOT TRANSLATE"))
        self.helpDistribution.setText(self.__tr("Help","DO NOT TRANSLATE"))
        self.helpSuffix.setText(self.__tr("Help","DO NOT TRANSLATE"))
        self.helpAdminName.setText(self.__tr("Help","DO NOT TRANSLATE"))
        self.helpPassword.setText(self.__tr("Help","DO NOT TRANSLATE"))
        self.groupBox5.setTitle(self.__tr("Save Options","DO NOT TRANSLATE"))
        self.textLabel5.setText(self.__tr("Save to file:","DO NOT TRANSLATE"))
        self.fileChooserButton.setText(QString.null)
        self.finishConfig.setText(self.__tr("&Finish","DO NOT TRANSLATE"))
        self.finishConfig.setAccel(self.__tr("Alt+F"))


    def displaySuffixHelp(self):
        print "ConfigPanelDesign.displaySuffixHelp(): Not implemented yet"

    def displayAdminNameHelp(self):
        print "ConfigPanelDesign.displayAdminNameHelp(): Not implemented yet"

    def displayPasswordHelp(self):
        print "ConfigPanelDesign.displayPasswordHelp(): Not implemented yet"

    def createConfig(self):
        print "ConfigPanelDesign.createConfig(): Not implemented yet"

    def displayDistributionHelp(self):
        print "ConfigPanelDesign.displayDistributionHelp(): Not implemented yet"

    def displayFileChooser(self):
        print "ConfigPanelDesign.displayFileChooser(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ConfigPanelDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ConfigPanelDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
