# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/gui/ServerDialogDesign.ui'
#
# Created: Sat Jul 3 23:35:31 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *

image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x10\x00\x00\x00\x10" \
    "\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\x00\x00\x01" \
    "\xd0\x49\x44\x41\x54\x78\x9c\x9d\x93\x4d\x6b\x13" \
    "\x51\x14\x86\x9f\x93\x4c\xd2\xa6\xda\x60\x3f\x54" \
    "\x8c\xc5\x85\x96\x2e\x54\x14\x0d\x52\x93\x8d\x20" \
    "\x2e\x22\x08\x2e\xc5\x45\xd7\xc5\x1f\x20\x5d\xe5" \
    "\x17\xf8\x23\x94\x56\xa4\x50\x15\x17\xe2\x42\xa8" \
    "\x2b\xcd\x60\x55\xc4\x60\x45\x68\xd0\xd2\x86\x2a" \
    "\x06\x33\x26\x19\x27\x61\x32\x99\xe3\x22\x6d\xc9" \
    "\x58\xa7\x8a\x07\xde\xc5\x85\x7b\x9e\xfb\x9e\x8f" \
    "\x2b\x85\x42\x81\xb0\xc8\xe8\x15\x35\xe5\xb1\x84" \
    "\x5e\x00\x22\xa1\xc9\x7d\x59\xe5\xe0\x34\x19\xeb" \
    "\xba\xfe\x17\x00\x67\x02\x8e\xcd\x40\xff\x91\xdd" \
    "\xf2\xc3\x01\x9a\xb8\x04\xe4\xe1\xdc\x0c\x67\x3f" \
    "\x5e\x0e\x75\xf1\x47\xc0\xe4\x6a\x4e\x25\x7d\x0d" \
    "\xd8\x80\x41\x17\x47\x0e\x85\x3a\x10\x6d\x9c\x57" \
    "\xea\x07\xc0\x13\x68\x25\xc0\x1b\xc7\xdd\x77\x81" \
    "\x78\xea\x05\xb0\x02\xf4\xe3\x35\xa6\x69\x2e\x2f" \
    "\xa2\x56\x89\xa4\x61\x83\xd1\x81\x8d\x22\xe6\xd1" \
    "\x3b\x22\xba\x7c\x5c\xf1\x4e\xc0\xa9\x3c\x30\x0b" \
    "\xd4\xbb\xd2\x68\x57\xe2\x83\x78\x9b\x66\x87\x81" \
    "\x11\x3a\xcf\x3f\x50\x7d\x5d\xa4\x34\x79\x5b\x64" \
    "\x6b\x8c\x19\x37\xaf\x64\x2f\x42\xcb\x04\xdf\x00" \
    "\x95\x5e\x9f\x10\x05\xda\x09\xdc\x67\x9f\xf8\x5c" \
    "\x2c\x53\xcd\x2d\x08\x80\xf4\xee\x41\xda\xba\xa9" \
    "\xb1\xd3\xfb\x91\x48\x1d\x7a\xdb\x26\x0a\xcd\x21" \
    "\x6a\x8b\x2b\x2c\xbd\x5d\x67\xef\xd4\x93\x6d\x7a" \
    "\xa0\x89\x6f\x86\x6e\x49\xb3\x54\x01\xa7\x01\x3f" \
    "\xb7\x64\x83\x63\xc3\xf7\x2f\x34\xaa\xf5\x40\x32" \
    "\x80\xd1\x7b\xc8\x38\x53\xea\x0f\xf6\x81\xed\x83" \
    "\x1f\x81\xa8\xdf\x2d\x45\x15\x62\x71\xc6\x52\x7b" \
    "\x58\xff\x6d\x0a\x01\x00\xf1\x01\x22\x5a\x81\x5a" \
    "\x14\x6a\x06\xce\xd7\x36\x03\x87\x05\x46\x37\x41" \
    "\x24\x77\x8c\x31\xb8\x07\x1a\x81\x6f\x3f\x60\xcd" \
    "\x80\x56\x8c\x77\x27\xef\x0b\x95\x18\x8d\x25\xa0" \
    "\x52\xc3\x77\xed\xbf\x00\x56\xcb\xe0\xa6\x98\x7b" \
    "\x5a\xc6\x1c\x9b\x15\x00\x73\xe2\x9e\xbc\x4f\x3f" \
    "\x10\x6f\x6d\x84\x8e\x55\x65\xf4\x61\x2e\xb0\x95" \
    "\xdb\x25\x64\xac\xac\xfa\xed\x61\x5e\xa6\xee\xca" \
    "\xf8\x8d\x1d\x0f\xf1\xea\xcc\xbc\x00\x24\x1f\x5d" \
    "\x0d\x00\x64\xb7\xef\xfc\x2f\xf1\x0b\xb3\x71\xb6" \
    "\x14\xbc\x93\x8f\x17\x00\x00\x00\x00\x49\x45\x4e" \
    "\x44\xae\x42\x60\x82"

class ServerDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("ServerDialogDesign")


        ServerDialogDesignLayout = QVBoxLayout(self,11,6,"ServerDialogDesignLayout")

        self.splitter2 = QSplitter(self,"splitter2")
        self.splitter2.setOrientation(QSplitter.Horizontal)

        LayoutWidget = QWidget(self.splitter2,"layout3")
        layout3 = QGridLayout(LayoutWidget,1,1,11,6,"layout3")

        self.addButton = QPushButton(LayoutWidget,"addButton")

        layout3.addWidget(self.addButton,1,1)

        self.serverListView = QListView(LayoutWidget,"serverListView")
        self.serverListView.addColumn(self.__tr("Server"))
        self.serverListView.setResizeMode(QListView.AllColumns)

        layout3.addMultiCellWidget(self.serverListView,0,0,0,2)
        spacer5 = QSpacerItem(32,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout3.addItem(spacer5,1,0)

        self.deleteButton = QPushButton(LayoutWidget,"deleteButton")

        layout3.addWidget(self.deleteButton,1,2)

        self.infoGroupBox = QGroupBox(self.splitter2,"infoGroupBox")
        self.infoGroupBox.setColumnLayout(0,Qt.Vertical)
        self.infoGroupBox.layout().setSpacing(6)
        self.infoGroupBox.layout().setMargin(11)
        infoGroupBoxLayout = QGridLayout(self.infoGroupBox.layout())
        infoGroupBoxLayout.setAlignment(Qt.AlignTop)

        self.tlsCheckBox = QCheckBox(self.infoGroupBox,"tlsCheckBox")
        self.tlsCheckBox.setSizePolicy(QSizePolicy(0,0,0,0,self.tlsCheckBox.sizePolicy().hasHeightForWidth()))

        infoGroupBoxLayout.addMultiCellWidget(self.tlsCheckBox,3,3,1,2)

        self.textLabel8 = QLabel(self.infoGroupBox,"textLabel8")
        self.textLabel8.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel8.sizePolicy().hasHeightForWidth()))

        infoGroupBoxLayout.addWidget(self.textLabel8,1,1)

        self.textLabel9 = QLabel(self.infoGroupBox,"textLabel9")
        self.textLabel9.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel9.sizePolicy().hasHeightForWidth()))

        infoGroupBoxLayout.addWidget(self.textLabel9,2,1)

        self.hostLineEdit = QLineEdit(self.infoGroupBox,"hostLineEdit")

        infoGroupBoxLayout.addMultiCellWidget(self.hostLineEdit,1,1,4,5)

        self.portSpinBox = QSpinBox(self.infoGroupBox,"portSpinBox")
        self.portSpinBox.setSizePolicy(QSizePolicy(7,0,0,0,self.portSpinBox.sizePolicy().hasHeightForWidth()))
        self.portSpinBox.setMaxValue(65535)
        self.portSpinBox.setMinValue(1)
        self.portSpinBox.setValue(389)

        infoGroupBoxLayout.addMultiCellWidget(self.portSpinBox,2,2,4,5)

        self.networkLabel = QLabel(self.infoGroupBox,"networkLabel")
        self.networkLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.networkLabel.sizePolicy().hasHeightForWidth()))
        self.networkLabel.setMinimumSize(QSize(48,48))

        infoGroupBoxLayout.addWidget(self.networkLabel,0,0)

        self.textLabel1_2 = QLabel(self.infoGroupBox,"textLabel1_2")

        infoGroupBoxLayout.addMultiCellWidget(self.textLabel1_2,0,0,1,4)

        self.basednButton = QPushButton(self.infoGroupBox,"basednButton")
        self.basednButton.setEnabled(1)
        self.basednButton.setPixmap(self.image0)

        infoGroupBoxLayout.addWidget(self.basednButton,9,5)

        self.bindLineEdit = QLineEdit(self.infoGroupBox,"bindLineEdit")

        infoGroupBoxLayout.addMultiCellWidget(self.bindLineEdit,7,7,4,5)

        self.authLabel = QLabel(self.infoGroupBox,"authLabel")
        self.authLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.authLabel.sizePolicy().hasHeightForWidth()))
        self.authLabel.setMinimumSize(QSize(48,48))

        infoGroupBoxLayout.addWidget(self.authLabel,5,0)

        self.bindAnonBox = QCheckBox(self.infoGroupBox,"bindAnonBox")

        infoGroupBoxLayout.addMultiCellWidget(self.bindAnonBox,6,6,1,4)
        spacer7 = QSpacerItem(21,30,QSizePolicy.Minimum,QSizePolicy.Expanding)
        infoGroupBoxLayout.addItem(spacer7,10,2)

        self.textLabel10 = QLabel(self.infoGroupBox,"textLabel10")
        self.textLabel10.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        infoGroupBoxLayout.addMultiCellWidget(self.textLabel10,7,7,1,3)

        self.textLabel12 = QLabel(self.infoGroupBox,"textLabel12")
        self.textLabel12.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        infoGroupBoxLayout.addMultiCellWidget(self.textLabel12,8,8,1,3)

        self.passwordLineEdit = QLineEdit(self.infoGroupBox,"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        infoGroupBoxLayout.addMultiCellWidget(self.passwordLineEdit,8,8,4,5)

        self.baseLineEdit = QLineEdit(self.infoGroupBox,"baseLineEdit")

        infoGroupBoxLayout.addWidget(self.baseLineEdit,9,4)

        self.textLabel1 = QLabel(self.infoGroupBox,"textLabel1")

        infoGroupBoxLayout.addMultiCellWidget(self.textLabel1,9,9,1,3)

        self.textLabel4 = QLabel(self.infoGroupBox,"textLabel4")

        infoGroupBoxLayout.addMultiCellWidget(self.textLabel4,5,5,1,4)
        spacer4 = QSpacerItem(41,25,QSizePolicy.Minimum,QSizePolicy.Fixed)
        infoGroupBoxLayout.addMultiCell(spacer4,4,4,3,4)
        ServerDialogDesignLayout.addWidget(self.splitter2)

        self.line3 = QFrame(self,"line3")
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setFrameShadow(QFrame.Sunken)
        self.line3.setFrameShape(QFrame.HLine)
        ServerDialogDesignLayout.addWidget(self.line3)

        layout4 = QHBoxLayout(None,0,6,"layout4")
        spacer6 = QSpacerItem(350,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout4.addItem(spacer6)

        self.okButton = QPushButton(self,"okButton")
        layout4.addWidget(self.okButton)

        self.applyButton = QPushButton(self,"applyButton")
        self.applyButton.setSizePolicy(QSizePolicy(1,0,0,0,self.applyButton.sizePolicy().hasHeightForWidth()))
        layout4.addWidget(self.applyButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        layout4.addWidget(self.cancelButton)
        ServerDialogDesignLayout.addLayout(layout4)

        self.languageChange()

        self.resize(QSize(639,462).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.applyButton,SIGNAL("clicked()"),self.saveServer)
        self.connect(self.basednButton,SIGNAL("clicked()"),self.searchBaseDN)
        self.connect(self.addButton,SIGNAL("clicked()"),self.addServer)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteServer)
        self.connect(self.tlsCheckBox,SIGNAL("toggled(bool)"),self.tlsChanged)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.hostLineEdit,SIGNAL("textChanged(const QString&)"),self.hostChanged)
        self.connect(self.portSpinBox,SIGNAL("valueChanged(int)"),self.portChanged)
        self.connect(self.tlsCheckBox,SIGNAL("toggled(bool)"),self.tlsChanged)
        self.connect(self.bindAnonBox,SIGNAL("toggled(bool)"),self.bindAnonChanged)
        self.connect(self.bindLineEdit,SIGNAL("textChanged(const QString&)"),self.bindDNChanged)
        self.connect(self.passwordLineEdit,SIGNAL("textChanged(const QString&)"),self.bindPasswordChanged)
        self.connect(self.baseLineEdit,SIGNAL("textChanged(const QString&)"),self.baseDNChanged)
        self.connect(self.serverListView,SIGNAL("selectionChanged(QListViewItem*)"),self.serverSelectionChanged)
        self.connect(self.okButton,SIGNAL("clicked()"),self.saveCloseDialog)

        self.setTabOrder(self.addButton,self.deleteButton)
        self.setTabOrder(self.deleteButton,self.hostLineEdit)
        self.setTabOrder(self.hostLineEdit,self.portSpinBox)
        self.setTabOrder(self.portSpinBox,self.baseLineEdit)
        self.setTabOrder(self.baseLineEdit,self.bindLineEdit)
        self.setTabOrder(self.bindLineEdit,self.passwordLineEdit)
        self.setTabOrder(self.passwordLineEdit,self.applyButton)


    def languageChange(self):
        self.setCaption(self.__tr("Manage Server List"))
        self.addButton.setText(self.__tr("&Add"))
        self.addButton.setAccel(self.__tr("Alt+A"))
        self.serverListView.header().setLabel(0,self.__tr("Server"))
        self.deleteButton.setText(self.__tr("&Delete"))
        self.deleteButton.setAccel(self.__tr("Alt+D"))
        self.infoGroupBox.setTitle(self.__tr("Server Information"))
        self.tlsCheckBox.setText(self.__tr("Use TLS"))
        QToolTip.add(self.tlsCheckBox,self.__tr("User Transport Layer Security"))
        self.textLabel8.setText(self.__tr("Host:"))
        self.textLabel9.setText(self.__tr("Port:"))
        self.networkLabel.setText(self.__tr("NO"))
        self.textLabel1_2.setText(self.__tr("<b>Network options</b>"))
        self.basednButton.setText(QString.null)
        self.authLabel.setText(self.__tr("AO"))
        self.bindAnonBox.setText(self.__tr("Bind anonymously"))
        self.textLabel10.setText(self.__tr("Bind DN:"))
        self.textLabel12.setText(self.__tr("Bind Password:"))
        self.textLabel1.setText(self.__tr("Base DN:"))
        self.textLabel4.setText(self.__tr("<b>Authentification options</b>"))
        self.okButton.setText(self.__tr("&OK"))
        self.okButton.setAccel(self.__tr("Alt+O"))
        self.applyButton.setText(self.__tr("&Apply"))
        self.applyButton.setAccel(self.__tr("Alt+A"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))


    def serverSelectionChanged(self):
        print "ServerDialogDesign.serverSelectionChanged(): Not implemented yet"

    def deleteServer(self):
        print "ServerDialogDesign.deleteServer(): Not implemented yet"

    def saveServer(self):
        print "ServerDialogDesign.saveServer(): Not implemented yet"

    def addServer(self):
        print "ServerDialogDesign.addServer(): Not implemented yet"

    def searchBaseDN(self):
        print "ServerDialogDesign.searchBaseDN(): Not implemented yet"

    def hostChanged(self):
        print "ServerDialogDesign.hostChanged(): Not implemented yet"

    def portChanged(self):
        print "ServerDialogDesign.portChanged(): Not implemented yet"

    def tlsChanged(self):
        print "ServerDialogDesign.tlsChanged(): Not implemented yet"

    def bindAnonChanged(self):
        print "ServerDialogDesign.bindAnonChanged(): Not implemented yet"

    def bindDNChanged(self):
        print "ServerDialogDesign.bindDNChanged(): Not implemented yet"

    def bindPasswordChanged(self):
        print "ServerDialogDesign.bindPasswordChanged(): Not implemented yet"

    def baseDNChanged(self):
        print "ServerDialogDesign.baseDNChanged(): Not implemented yet"

    def saveCloseDialog(self):
        print "ServerDialogDesign.saveCloseDialog(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ServerDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ServerDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
