# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/gui/ServerDialogDesign.ui'
#
# Created: Sun Aug 29 00:49:06 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.12
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class ServerDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

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
        self.infoGroupBox.setFrameShape(QGroupBox.NoFrame)
        self.infoGroupBox.setColumnLayout(0,Qt.Vertical)
        self.infoGroupBox.layout().setSpacing(6)
        self.infoGroupBox.layout().setMargin(11)
        infoGroupBoxLayout = QVBoxLayout(self.infoGroupBox.layout())
        infoGroupBoxLayout.setAlignment(Qt.AlignTop)

        layout8 = QGridLayout(None,1,1,0,6,"layout8")

        self.textLabel1 = QLabel(self.infoGroupBox,"textLabel1")

        layout8.addWidget(self.textLabel1,3,1)

        self.portSpinBox = QSpinBox(self.infoGroupBox,"portSpinBox")
        self.portSpinBox.setSizePolicy(QSizePolicy(1,0,0,0,self.portSpinBox.sizePolicy().hasHeightForWidth()))
        self.portSpinBox.setMaxValue(65535)
        self.portSpinBox.setMinValue(1)
        self.portSpinBox.setValue(389)

        layout8.addMultiCellWidget(self.portSpinBox,2,2,2,3)

        self.textLabel8 = QLabel(self.infoGroupBox,"textLabel8")
        self.textLabel8.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel8.sizePolicy().hasHeightForWidth()))

        layout8.addWidget(self.textLabel8,1,1)
        spacer7_2 = QSpacerItem(21,91,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout8.addMultiCell(spacer7_2,2,4,0,0)

        self.basednButton = QPushButton(self.infoGroupBox,"basednButton")
        self.basednButton.setEnabled(1)

        layout8.addWidget(self.basednButton,4,3)

        self.networkLabel = QLabel(self.infoGroupBox,"networkLabel")
        self.networkLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.networkLabel.sizePolicy().hasHeightForWidth()))
        self.networkLabel.setMinimumSize(QSize(48,48))

        layout8.addMultiCellWidget(self.networkLabel,0,1,0,0)

        self.baseLineEdit = QLineEdit(self.infoGroupBox,"baseLineEdit")

        layout8.addMultiCellWidget(self.baseLineEdit,3,3,2,3)
        spacer12 = QSpacerItem(215,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout8.addMultiCell(spacer12,4,4,1,2)

        self.textLabel1_2 = QLabel(self.infoGroupBox,"textLabel1_2")

        layout8.addMultiCellWidget(self.textLabel1_2,0,0,1,3)

        self.textLabel9 = QLabel(self.infoGroupBox,"textLabel9")
        self.textLabel9.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel9.sizePolicy().hasHeightForWidth()))

        layout8.addWidget(self.textLabel9,2,1)

        self.hostLineEdit = QLineEdit(self.infoGroupBox,"hostLineEdit")

        layout8.addMultiCellWidget(self.hostLineEdit,1,1,2,3)
        infoGroupBoxLayout.addLayout(layout8)
        spacer4 = QSpacerItem(41,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        infoGroupBoxLayout.addItem(spacer4)

        layout7 = QGridLayout(None,1,1,0,6,"layout7")

        self.textLabel10 = QLabel(self.infoGroupBox,"textLabel10")
        self.textLabel10.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        layout7.addWidget(self.textLabel10,6,1)

        self.authLabel = QLabel(self.infoGroupBox,"authLabel")
        self.authLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.authLabel.sizePolicy().hasHeightForWidth()))
        self.authLabel.setMinimumSize(QSize(48,48))

        layout7.addMultiCellWidget(self.authLabel,0,1,0,0)

        self.bindLineEdit = QLineEdit(self.infoGroupBox,"bindLineEdit")

        layout7.addWidget(self.bindLineEdit,6,2)

        self.textLabel5 = QLabel(self.infoGroupBox,"textLabel5")

        layout7.addMultiCellWidget(self.textLabel5,5,5,1,2)

        self.textLabel4 = QLabel(self.infoGroupBox,"textLabel4")

        layout7.addMultiCellWidget(self.textLabel4,3,3,1,2)
        spacer6_2 = QSpacerItem(21,170,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout7.addMultiCell(spacer6_2,2,7,0,0)

        self.passwordLineEdit = QLineEdit(self.infoGroupBox,"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        layout7.addWidget(self.passwordLineEdit,7,2)

        self.methodBox = QComboBox(0,self.infoGroupBox,"methodBox")

        layout7.addMultiCellWidget(self.methodBox,4,4,1,2)

        self.bindAnonBox = QCheckBox(self.infoGroupBox,"bindAnonBox")

        layout7.addMultiCellWidget(self.bindAnonBox,2,2,1,2)

        self.textLabel2 = QLabel(self.infoGroupBox,"textLabel2")

        layout7.addMultiCellWidget(self.textLabel2,0,0,1,2)

        self.textLabel12 = QLabel(self.infoGroupBox,"textLabel12")
        self.textLabel12.setAlignment(QLabel.AlignVCenter)

        layout7.addWidget(self.textLabel12,7,1)

        self.tlsCheckBox = QCheckBox(self.infoGroupBox,"tlsCheckBox")

        layout7.addMultiCellWidget(self.tlsCheckBox,1,1,1,2)
        infoGroupBoxLayout.addLayout(layout7)
        spacer7 = QSpacerItem(21,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        infoGroupBoxLayout.addItem(spacer7)
        ServerDialogDesignLayout.addWidget(self.splitter2)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)
        ServerDialogDesignLayout.addWidget(self.line1)

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

        self.resize(QSize(546,521).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.applyButton,SIGNAL("clicked()"),self.saveServer)
        self.connect(self.basednButton,SIGNAL("clicked()"),self.searchBaseDN)
        self.connect(self.addButton,SIGNAL("clicked()"),self.addServer)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteServer)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.hostLineEdit,SIGNAL("textChanged(const QString&)"),self.hostChanged)
        self.connect(self.portSpinBox,SIGNAL("valueChanged(int)"),self.portChanged)
        self.connect(self.bindLineEdit,SIGNAL("textChanged(const QString&)"),self.bindDNChanged)
        self.connect(self.passwordLineEdit,SIGNAL("textChanged(const QString&)"),self.bindPasswordChanged)
        self.connect(self.baseLineEdit,SIGNAL("textChanged(const QString&)"),self.baseDNChanged)
        self.connect(self.serverListView,SIGNAL("selectionChanged(QListViewItem*)"),self.serverSelectionChanged)
        self.connect(self.okButton,SIGNAL("clicked()"),self.saveCloseDialog)
        self.connect(self.tlsCheckBox,SIGNAL("toggled(bool)"),self.tlsChanged)
        self.connect(self.bindAnonBox,SIGNAL("toggled(bool)"),self.bindAnonChanged)
        self.connect(self.methodBox,SIGNAL("activated(int)"),self.methodChanged)

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
        self.textLabel1.setText(self.__tr("Base DN:"))
        self.textLabel8.setText(self.__tr("Host:"))
        self.basednButton.setText(self.__tr("Fetch Base DNs"))
        self.networkLabel.setText(self.__tr("NO"))
        self.textLabel1_2.setText(self.__tr("<b>Network options</b>"))
        self.textLabel9.setText(self.__tr("Port:"))
        self.textLabel10.setText(self.__tr("Bind as:"))
        self.authLabel.setText(self.__tr("SO"))
        self.textLabel5.setText(self.__tr("<b>Credentials</b>"))
        self.textLabel4.setText(self.__tr("<b>Authentification mechanism</b>"))
        self.methodBox.clear()
        self.methodBox.insertItem(self.__tr("Simple"))
        self.methodBox.insertItem(self.__tr("SASL Plain"))
        self.methodBox.insertItem(self.__tr("SASL CRAM-MD5"))
        self.methodBox.insertItem(self.__tr("SASL DIGEST-MD5"))
        self.methodBox.insertItem(self.__tr("SASL Login"))
        self.methodBox.insertItem(self.__tr("SASL GSSAPI"))
        self.bindAnonBox.setText(self.__tr("Anonymous bind"))
        self.textLabel2.setText(self.__tr("<b>Security options</b>"))
        self.textLabel12.setText(self.__tr("Password:"))
        self.tlsCheckBox.setText(self.__tr("Use secure connection (SSL)"))
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

    def methodChanged(self):
        print "ServerDialogDesign.methodChanged(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ServerDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ServerDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
