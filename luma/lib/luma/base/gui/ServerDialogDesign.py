# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/gui/ServerDialogDesign.ui'
#
# Created: Tue Feb 8 22:53:37 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class ServerDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ServerDialogDesign")


        ServerDialogDesignLayout = QGridLayout(self,1,1,11,6,"ServerDialogDesignLayout")

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        ServerDialogDesignLayout.addWidget(self.line1,1,0)

        layout4 = QHBoxLayout(None,0,6,"layout4")
        spacer6 = QSpacerItem(350,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout4.addItem(spacer6)

        self.okButton = QPushButton(self,"okButton")
        self.okButton.setDefault(1)
        layout4.addWidget(self.okButton)

        self.applyButton = QPushButton(self,"applyButton")
        self.applyButton.setSizePolicy(QSizePolicy(1,0,0,0,self.applyButton.sizePolicy().hasHeightForWidth()))
        layout4.addWidget(self.applyButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        layout4.addWidget(self.cancelButton)

        ServerDialogDesignLayout.addLayout(layout4,2,0)

        self.splitter2 = QSplitter(self,"splitter2")
        self.splitter2.setOrientation(QSplitter.Horizontal)

        LayoutWidget = QWidget(self.splitter2,"layout3")
        layout3 = QGridLayout(LayoutWidget,1,1,0,6,"layout3")

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

        self.serverWidget = QTabWidget(self.splitter2,"serverWidget")

        self.tab = QWidget(self.serverWidget,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")
        spacer7_2 = QSpacerItem(21,263,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addMultiCell(spacer7_2,2,8,0,0)

        self.networkLabel = QLabel(self.tab,"networkLabel")
        self.networkLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.networkLabel.sizePolicy().hasHeightForWidth()))
        self.networkLabel.setMinimumSize(QSize(48,48))

        tabLayout.addMultiCellWidget(self.networkLabel,0,1,0,0)

        self.textLabel1_2 = QLabel(self.tab,"textLabel1_2")
        self.textLabel1_2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        tabLayout.addMultiCellWidget(self.textLabel1_2,0,0,1,4)

        self.portSpinBox = QSpinBox(self.tab,"portSpinBox")
        self.portSpinBox.setSizePolicy(QSizePolicy(1,0,0,0,self.portSpinBox.sizePolicy().hasHeightForWidth()))
        self.portSpinBox.setMaxValue(65535)
        self.portSpinBox.setMinValue(1)
        self.portSpinBox.setValue(389)

        tabLayout.addMultiCellWidget(self.portSpinBox,3,3,3,4)

        self.hostLineEdit = QLineEdit(self.tab,"hostLineEdit")

        tabLayout.addMultiCellWidget(self.hostLineEdit,1,2,3,4)

        self.textLabel9 = QLabel(self.tab,"textLabel9")
        self.textLabel9.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel9.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.textLabel9,3,2)
        spacer8_2 = QSpacerItem(12,10,QSizePolicy.Fixed,QSizePolicy.Minimum)
        tabLayout.addItem(spacer8_2,1,1)

        self.textLabel8 = QLabel(self.tab,"textLabel8")
        self.textLabel8.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel8.sizePolicy().hasHeightForWidth()))

        tabLayout.addMultiCellWidget(self.textLabel8,1,2,2,2)
        spacer8 = QSpacerItem(41,81,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer8,10,4)

        self.aliasBox = QCheckBox(self.tab,"aliasBox")

        tabLayout.addMultiCellWidget(self.aliasBox,6,6,2,4)

        self.baseDNView = QListView(self.tab,"baseDNView")
        self.baseDNView.addColumn(self.__tr("Base DNs"))
        self.baseDNView.setResizeMode(QListView.AllColumns)

        tabLayout.addMultiCellWidget(self.baseDNView,8,8,2,4)

        self.baseBox = QCheckBox(self.tab,"baseBox")

        tabLayout.addMultiCellWidget(self.baseBox,7,7,2,4)

        self.manageBaseBaseButton = QPushButton(self.tab,"manageBaseBaseButton")

        tabLayout.addWidget(self.manageBaseBaseButton,9,4)

        self.textLabel1 = QLabel(self.tab,"textLabel1")
        self.textLabel1.setAlignment(QLabel.AlignVCenter)

        tabLayout.addMultiCellWidget(self.textLabel1,5,5,1,3)
        spacer9_2 = QSpacerItem(12,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        tabLayout.addItem(spacer9_2,6,1)
        spacer10 = QSpacerItem(124,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        tabLayout.addMultiCell(spacer10,9,9,2,3)
        spacer10_2 = QSpacerItem(20,10,QSizePolicy.Minimum,QSizePolicy.Fixed)
        tabLayout.addItem(spacer10_2,4,2)
        self.serverWidget.insertTab(self.tab,QString(""))

        self.tab_2 = QWidget(self.serverWidget,"tab_2")
        tabLayout_2 = QGridLayout(self.tab_2,1,1,11,6,"tabLayout_2")

        self.authLabel = QLabel(self.tab_2,"authLabel")
        self.authLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.authLabel.sizePolicy().hasHeightForWidth()))
        self.authLabel.setMinimumSize(QSize(48,48))

        tabLayout_2.addWidget(self.authLabel,0,0)
        spacer6_2 = QSpacerItem(21,178,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout_2.addMultiCell(spacer6_2,1,5,0,0)
        spacer14 = QSpacerItem(21,10,QSizePolicy.Minimum,QSizePolicy.Fixed)
        tabLayout_2.addItem(spacer14,2,1)
        spacer9 = QSpacerItem(21,70,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout_2.addItem(spacer9,6,3)

        layout5 = QGridLayout(None,1,1,0,6,"layout5")

        self.tlsCheckBox = QCheckBox(self.tab_2,"tlsCheckBox")

        layout5.addWidget(self.tlsCheckBox,1,1)

        self.textLabel2 = QLabel(self.tab_2,"textLabel2")
        self.textLabel2.setAlignment(QLabel.AlignVCenter)

        layout5.addMultiCellWidget(self.textLabel2,0,0,0,1)

        self.bindAnonBox = QCheckBox(self.tab_2,"bindAnonBox")

        layout5.addWidget(self.bindAnonBox,2,1)
        spacer11 = QSpacerItem(12,16,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout5.addItem(spacer11,1,0)

        tabLayout_2.addMultiCellLayout(layout5,0,1,1,3)

        layout7 = QGridLayout(None,1,1,0,6,"layout7")

        self.methodBox = QComboBox(0,self.tab_2,"methodBox")

        layout7.addWidget(self.methodBox,1,1)
        spacer13 = QSpacerItem(16,16,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout7.addItem(spacer13,1,0)

        self.textLabel4 = QLabel(self.tab_2,"textLabel4")
        self.textLabel4.setAlignment(QLabel.AlignVCenter)

        layout7.addMultiCellWidget(self.textLabel4,0,0,0,1)

        tabLayout_2.addMultiCellLayout(layout7,3,3,1,3)
        spacer12 = QSpacerItem(20,10,QSizePolicy.Minimum,QSizePolicy.Fixed)
        tabLayout_2.addItem(spacer12,4,2)

        layout8 = QGridLayout(None,1,1,0,6,"layout8")

        self.textLabel5 = QLabel(self.tab_2,"textLabel5")
        self.textLabel5.setAlignment(QLabel.AlignVCenter)

        layout8.addMultiCellWidget(self.textLabel5,0,0,0,2)

        self.textLabel12 = QLabel(self.tab_2,"textLabel12")
        self.textLabel12.setAlignment(QLabel.AlignVCenter)

        layout8.addWidget(self.textLabel12,2,1)

        self.passwordLineEdit = QLineEdit(self.tab_2,"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        layout8.addWidget(self.passwordLineEdit,2,2)

        self.textLabel10 = QLabel(self.tab_2,"textLabel10")
        self.textLabel10.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        layout8.addWidget(self.textLabel10,1,1)
        spacer15 = QSpacerItem(12,10,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout8.addItem(spacer15,1,0)

        self.bindLineEdit = QLineEdit(self.tab_2,"bindLineEdit")

        layout8.addWidget(self.bindLineEdit,1,2)

        tabLayout_2.addMultiCellLayout(layout8,5,5,1,3)
        self.serverWidget.insertTab(self.tab_2,QString(""))

        ServerDialogDesignLayout.addWidget(self.splitter2,0,0)

        self.languageChange()

        self.resize(QSize(621,444).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.applyButton,SIGNAL("clicked()"),self.saveServer)
        self.connect(self.addButton,SIGNAL("clicked()"),self.addServer)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteServer)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.hostLineEdit,SIGNAL("textChanged(const QString&)"),self.hostChanged)
        self.connect(self.portSpinBox,SIGNAL("valueChanged(int)"),self.portChanged)
        self.connect(self.bindLineEdit,SIGNAL("textChanged(const QString&)"),self.bindDNChanged)
        self.connect(self.passwordLineEdit,SIGNAL("textChanged(const QString&)"),self.bindPasswordChanged)
        self.connect(self.serverListView,SIGNAL("selectionChanged(QListViewItem*)"),self.serverSelectionChanged)
        self.connect(self.okButton,SIGNAL("clicked()"),self.saveCloseDialog)
        self.connect(self.tlsCheckBox,SIGNAL("toggled(bool)"),self.tlsChanged)
        self.connect(self.bindAnonBox,SIGNAL("toggled(bool)"),self.bindAnonChanged)
        self.connect(self.methodBox,SIGNAL("activated(int)"),self.methodChanged)
        self.connect(self.manageBaseBaseButton,SIGNAL("clicked()"),self.manageBaseDN)
        self.connect(self.baseBox,SIGNAL("clicked()"),self.useServerBase)
        self.connect(self.aliasBox,SIGNAL("clicked()"),self.aliasesChanged)

        self.setTabOrder(self.serverListView,self.addButton)
        self.setTabOrder(self.addButton,self.deleteButton)
        self.setTabOrder(self.deleteButton,self.serverWidget)
        self.setTabOrder(self.serverWidget,self.hostLineEdit)
        self.setTabOrder(self.hostLineEdit,self.portSpinBox)
        self.setTabOrder(self.portSpinBox,self.aliasBox)
        self.setTabOrder(self.aliasBox,self.baseBox)
        self.setTabOrder(self.baseBox,self.baseDNView)
        self.setTabOrder(self.baseDNView,self.manageBaseBaseButton)
        self.setTabOrder(self.manageBaseBaseButton,self.tlsCheckBox)
        self.setTabOrder(self.tlsCheckBox,self.bindAnonBox)
        self.setTabOrder(self.bindAnonBox,self.methodBox)
        self.setTabOrder(self.methodBox,self.bindLineEdit)
        self.setTabOrder(self.bindLineEdit,self.passwordLineEdit)
        self.setTabOrder(self.passwordLineEdit,self.okButton)
        self.setTabOrder(self.okButton,self.applyButton)
        self.setTabOrder(self.applyButton,self.cancelButton)


    def languageChange(self):
        self.setCaption(self.__tr("Manage Server List"))
        self.okButton.setText(self.__tr("&OK"))
        self.okButton.setAccel(self.__tr("Alt+O"))
        self.applyButton.setText(self.__tr("&Apply"))
        self.applyButton.setAccel(self.__tr("Alt+A"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))
        self.addButton.setText(self.__tr("&Add..."))
        self.addButton.setAccel(self.__tr("Alt+A"))
        self.serverListView.header().setLabel(0,self.__tr("Server"))
        self.deleteButton.setText(self.__tr("&Delete"))
        self.deleteButton.setAccel(self.__tr("Alt+D"))
        self.networkLabel.setText(self.__tr("NO"))
        self.textLabel1_2.setText(self.__tr("<b>Network options</b>"))
        self.textLabel9.setText(self.__tr("Port:"))
        self.textLabel8.setText(self.__tr("Host:"))
        self.aliasBox.setText(self.__tr("Follow aliases"))
        self.baseDNView.header().setLabel(0,self.__tr("Base DNs"))
        self.baseBox.setText(self.__tr("Use Base DNs provided by the server"))
        self.manageBaseBaseButton.setText(self.__tr("Manage Base DN list"))
        self.textLabel1.setText(self.__tr("<b>LDAP options</b>"))
        self.serverWidget.changeTab(self.tab,self.__tr("Network"))
        self.authLabel.setText(self.__tr("SO"))
        self.tlsCheckBox.setText(self.__tr("Use secure connection (SSL)"))
        self.textLabel2.setText(self.__tr("<b>Security options</b>"))
        self.bindAnonBox.setText(self.__tr("Anonymous bind"))
        self.methodBox.clear()
        self.methodBox.insertItem(self.__tr("Simple"))
        self.methodBox.insertItem(self.__tr("SASL CRAM-MD5"))
        self.methodBox.insertItem(self.__tr("SASL DIGEST-MD5"))
        self.methodBox.insertItem(self.__tr("SASL EXTERNAL"))
        self.methodBox.insertItem(self.__tr("SASL GSSAPI"))
        self.methodBox.insertItem(self.__tr("SASL Login"))
        self.methodBox.insertItem(self.__tr("SASL Plain"))
        self.textLabel4.setText(self.__tr("<b>Authentification mechanism</b>"))
        self.textLabel5.setText(self.__tr("<b>Credentials</b>"))
        self.textLabel12.setText(self.__tr("Password:"))
        self.textLabel10.setText(self.__tr("Bind as:"))
        self.serverWidget.changeTab(self.tab_2,self.__tr("Security"))


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

    def useServerBase(self):
        print "ServerDialogDesign.useServerBase(): Not implemented yet"

    def manageBaseDN(self):
        print "ServerDialogDesign.manageBaseDN(): Not implemented yet"

    def aliasesChanged(self):
        print "ServerDialogDesign.aliasesChanged(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ServerDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ServerDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
