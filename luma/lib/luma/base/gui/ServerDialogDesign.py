# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/gui/ServerDialogDesign.ui'
#
# Created: Tue Nov 30 22:42:49 2004
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
        layout4.addWidget(self.okButton)

        self.applyButton = QPushButton(self,"applyButton")
        self.applyButton.setSizePolicy(QSizePolicy(1,0,0,0,self.applyButton.sizePolicy().hasHeightForWidth()))
        layout4.addWidget(self.applyButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        layout4.addWidget(self.cancelButton)

        ServerDialogDesignLayout.addLayout(layout4,2,0)

        self.splitter3 = QSplitter(self,"splitter3")
        self.splitter3.setOrientation(QSplitter.Horizontal)

        LayoutWidget = QWidget(self.splitter3,"layout3")
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

        self.serverWidget = QTabWidget(self.splitter3,"serverWidget")

        self.tab = QWidget(self.serverWidget,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")
        spacer8 = QSpacerItem(41,81,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer8,1,0)

        layout8 = QGridLayout(None,1,1,0,6,"layout8")
        spacer7_2 = QSpacerItem(21,232,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout8.addMultiCell(spacer7_2,2,4,0,0)

        self.manageBaseBaseButton = QPushButton(self.tab,"manageBaseBaseButton")

        layout8.addWidget(self.manageBaseBaseButton,5,3)

        self.networkLabel = QLabel(self.tab,"networkLabel")
        self.networkLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.networkLabel.sizePolicy().hasHeightForWidth()))
        self.networkLabel.setMinimumSize(QSize(48,48))

        layout8.addMultiCellWidget(self.networkLabel,0,1,0,0)

        self.textLabel9 = QLabel(self.tab,"textLabel9")
        self.textLabel9.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel9.sizePolicy().hasHeightForWidth()))

        layout8.addWidget(self.textLabel9,2,1)

        self.portSpinBox = QSpinBox(self.tab,"portSpinBox")
        self.portSpinBox.setSizePolicy(QSizePolicy(1,0,0,0,self.portSpinBox.sizePolicy().hasHeightForWidth()))
        self.portSpinBox.setMaxValue(65535)
        self.portSpinBox.setMinValue(1)
        self.portSpinBox.setValue(389)

        layout8.addMultiCellWidget(self.portSpinBox,2,2,2,3)

        self.baseBox = QCheckBox(self.tab,"baseBox")

        layout8.addMultiCellWidget(self.baseBox,3,3,1,3)

        self.hostLineEdit = QLineEdit(self.tab,"hostLineEdit")

        layout8.addMultiCellWidget(self.hostLineEdit,1,1,2,3)

        self.baseDNView = QListView(self.tab,"baseDNView")
        self.baseDNView.addColumn(self.__tr("Base DNs"))
        self.baseDNView.setResizeMode(QListView.AllColumns)

        layout8.addMultiCellWidget(self.baseDNView,4,4,1,3)

        self.textLabel1_2 = QLabel(self.tab,"textLabel1_2")
        self.textLabel1_2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        layout8.addMultiCellWidget(self.textLabel1_2,0,0,1,3)

        self.textLabel8 = QLabel(self.tab,"textLabel8")
        self.textLabel8.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel8.sizePolicy().hasHeightForWidth()))

        layout8.addWidget(self.textLabel8,1,1)
        spacer10 = QSpacerItem(81,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout8.addMultiCell(spacer10,5,5,1,2)

        tabLayout.addLayout(layout8,0,0)
        self.serverWidget.insertTab(self.tab,QString(""))

        self.tab_2 = QWidget(self.serverWidget,"tab_2")
        tabLayout_2 = QVBoxLayout(self.tab_2,11,6,"tabLayout_2")

        layout7 = QGridLayout(None,1,1,0,6,"layout7")

        self.textLabel10 = QLabel(self.tab_2,"textLabel10")
        self.textLabel10.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        layout7.addWidget(self.textLabel10,6,1)

        self.authLabel = QLabel(self.tab_2,"authLabel")
        self.authLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.authLabel.sizePolicy().hasHeightForWidth()))
        self.authLabel.setMinimumSize(QSize(48,48))

        layout7.addMultiCellWidget(self.authLabel,0,1,0,0)

        self.bindLineEdit = QLineEdit(self.tab_2,"bindLineEdit")

        layout7.addWidget(self.bindLineEdit,6,2)

        self.textLabel5 = QLabel(self.tab_2,"textLabel5")

        layout7.addMultiCellWidget(self.textLabel5,5,5,1,2)

        self.textLabel4 = QLabel(self.tab_2,"textLabel4")

        layout7.addMultiCellWidget(self.textLabel4,3,3,1,2)
        spacer6_2 = QSpacerItem(21,170,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout7.addMultiCell(spacer6_2,2,7,0,0)

        self.passwordLineEdit = QLineEdit(self.tab_2,"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        layout7.addWidget(self.passwordLineEdit,7,2)

        self.methodBox = QComboBox(0,self.tab_2,"methodBox")

        layout7.addMultiCellWidget(self.methodBox,4,4,1,2)

        self.bindAnonBox = QCheckBox(self.tab_2,"bindAnonBox")

        layout7.addMultiCellWidget(self.bindAnonBox,2,2,1,2)

        self.textLabel2 = QLabel(self.tab_2,"textLabel2")
        self.textLabel2.setAlignment(QLabel.AlignVCenter)

        layout7.addMultiCellWidget(self.textLabel2,0,0,1,2)

        self.textLabel12 = QLabel(self.tab_2,"textLabel12")
        self.textLabel12.setAlignment(QLabel.AlignVCenter)

        layout7.addWidget(self.textLabel12,7,1)

        self.tlsCheckBox = QCheckBox(self.tab_2,"tlsCheckBox")

        layout7.addMultiCellWidget(self.tlsCheckBox,1,1,1,2)
        tabLayout_2.addLayout(layout7)
        spacer9 = QSpacerItem(21,101,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout_2.addItem(spacer9)
        self.serverWidget.insertTab(self.tab_2,QString(""))

        ServerDialogDesignLayout.addWidget(self.splitter3,0,0)

        self.languageChange()

        self.resize(QSize(616,561).expandedTo(self.minimumSizeHint()))
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

        self.setTabOrder(self.addButton,self.deleteButton)
        self.setTabOrder(self.deleteButton,self.hostLineEdit)
        self.setTabOrder(self.hostLineEdit,self.portSpinBox)
        self.setTabOrder(self.portSpinBox,self.bindLineEdit)
        self.setTabOrder(self.bindLineEdit,self.passwordLineEdit)
        self.setTabOrder(self.passwordLineEdit,self.applyButton)


    def languageChange(self):
        self.setCaption(self.__tr("Manage Server List"))
        self.okButton.setText(self.__tr("&OK"))
        self.okButton.setAccel(self.__tr("Alt+O"))
        self.applyButton.setText(self.__tr("&Apply"))
        self.applyButton.setAccel(self.__tr("Alt+A"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))
        self.addButton.setText(self.__tr("&Add"))
        self.addButton.setAccel(self.__tr("Alt+A"))
        self.serverListView.header().setLabel(0,self.__tr("Server"))
        self.deleteButton.setText(self.__tr("&Delete"))
        self.deleteButton.setAccel(self.__tr("Alt+D"))
        self.manageBaseBaseButton.setText(self.__tr("Manage Base DN list"))
        self.networkLabel.setText(self.__tr("NO"))
        self.textLabel9.setText(self.__tr("Port:"))
        self.baseBox.setText(self.__tr("Use Base DNs provided by the server"))
        self.baseDNView.header().setLabel(0,self.__tr("Base DNs"))
        self.textLabel1_2.setText(self.__tr("<b>Network options</b>"))
        self.textLabel8.setText(self.__tr("Host:"))
        self.serverWidget.changeTab(self.tab,self.__tr("Network"))
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

    def __tr(self,s,c = None):
        return qApp.translate("ServerDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ServerDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
