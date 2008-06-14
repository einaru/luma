# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/luma/base/gui/ServerDialogDesign.ui'
#
# Created: Sat Jun 14 21:43:57 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ServerDialogDesign(object):
    def setupUi(self, ServerDialogDesign):
        ServerDialogDesign.setObjectName("ServerDialogDesign")
        ServerDialogDesign.resize(QtCore.QSize(QtCore.QRect(0,0,757,504).size()).expandedTo(ServerDialogDesign.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(ServerDialogDesign)
        self.vboxlayout.setObjectName("vboxlayout")

        self.splitter2 = QtGui.QSplitter(ServerDialogDesign)
        self.splitter2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter2.setObjectName("splitter2")

        self.layout3 = QtGui.QWidget(self.splitter2)
        self.layout3.setObjectName("layout3")

        self.gridlayout = QtGui.QGridLayout(self.layout3)
        self.gridlayout.setMargin(0)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(48,25,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.addButton = QtGui.QPushButton(self.layout3)
        self.addButton.setObjectName("addButton")
        self.gridlayout.addWidget(self.addButton,1,1,1,1)

        self.deleteButton = QtGui.QPushButton(self.layout3)
        self.deleteButton.setObjectName("deleteButton")
        self.gridlayout.addWidget(self.deleteButton,1,2,1,1)

        self.serverListView = QtGui.QListWidget(self.layout3)
        self.serverListView.setObjectName("serverListView")
        self.gridlayout.addWidget(self.serverListView,0,0,1,3)

        self.serverWidget = QtGui.QTabWidget(self.splitter2)
        self.serverWidget.setObjectName("serverWidget")

        self.tab = QtGui.QWidget()
        self.tab.setGeometry(QtCore.QRect(0,0,428,413))
        self.tab.setObjectName("tab")

        self.gridlayout1 = QtGui.QGridLayout(self.tab)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem1 = QtGui.QSpacerItem(21,263,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem1,2,0,7,1)

        self.networkLabel = QtGui.QLabel(self.tab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.networkLabel.sizePolicy().hasHeightForWidth())
        self.networkLabel.setSizePolicy(sizePolicy)
        self.networkLabel.setMinimumSize(QtCore.QSize(48,48))
        self.networkLabel.setWordWrap(False)
        self.networkLabel.setObjectName("networkLabel")
        self.gridlayout1.addWidget(self.networkLabel,0,0,2,1)

        self.textLabel1_2 = QtGui.QLabel(self.tab)
        self.textLabel1_2.setAlignment(QtCore.Qt.AlignVCenter)
        self.textLabel1_2.setWordWrap(True)
        self.textLabel1_2.setObjectName("textLabel1_2")
        self.gridlayout1.addWidget(self.textLabel1_2,0,1,1,4)

        self.portSpinBox = QtGui.QSpinBox(self.tab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portSpinBox.sizePolicy().hasHeightForWidth())
        self.portSpinBox.setSizePolicy(sizePolicy)
        self.portSpinBox.setMinimum(1)
        self.portSpinBox.setMaximum(65535)
        self.portSpinBox.setProperty("value",QtCore.QVariant(389))
        self.portSpinBox.setObjectName("portSpinBox")
        self.gridlayout1.addWidget(self.portSpinBox,3,3,1,2)

        self.hostLineEdit = QtGui.QLineEdit(self.tab)
        self.hostLineEdit.setObjectName("hostLineEdit")
        self.gridlayout1.addWidget(self.hostLineEdit,1,3,2,2)

        self.textLabel9 = QtGui.QLabel(self.tab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel9.sizePolicy().hasHeightForWidth())
        self.textLabel9.setSizePolicy(sizePolicy)
        self.textLabel9.setWordWrap(False)
        self.textLabel9.setObjectName("textLabel9")
        self.gridlayout1.addWidget(self.textLabel9,3,2,1,1)

        spacerItem2 = QtGui.QSpacerItem(12,10,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem2,1,1,1,1)

        self.textLabel8 = QtGui.QLabel(self.tab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel8.sizePolicy().hasHeightForWidth())
        self.textLabel8.setSizePolicy(sizePolicy)
        self.textLabel8.setWordWrap(False)
        self.textLabel8.setObjectName("textLabel8")
        self.gridlayout1.addWidget(self.textLabel8,1,2,2,1)

        self.aliasBox = QtGui.QCheckBox(self.tab)
        self.aliasBox.setObjectName("aliasBox")
        self.gridlayout1.addWidget(self.aliasBox,6,2,1,3)

        self.baseDNView = QtGui.QListWidget(self.tab)
        self.baseDNView.setObjectName("baseDNView")
        self.gridlayout1.addWidget(self.baseDNView,8,2,1,3)

        self.baseBox = QtGui.QCheckBox(self.tab)
        self.baseBox.setObjectName("baseBox")
        self.gridlayout1.addWidget(self.baseBox,7,2,1,3)

        self.manageBaseButton = QtGui.QPushButton(self.tab)
        self.manageBaseButton.setObjectName("manageBaseButton")
        self.gridlayout1.addWidget(self.manageBaseButton,9,4,1,1)

        self.textLabel1 = QtGui.QLabel(self.tab)
        self.textLabel1.setAlignment(QtCore.Qt.AlignVCenter)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName("textLabel1")
        self.gridlayout1.addWidget(self.textLabel1,5,1,1,3)

        spacerItem3 = QtGui.QSpacerItem(12,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem3,6,1,1,1)

        spacerItem4 = QtGui.QSpacerItem(124,21,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem4,9,2,1,2)

        spacerItem5 = QtGui.QSpacerItem(20,6,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.gridlayout1.addItem(spacerItem5,4,2,1,1)
        self.serverWidget.addTab(self.tab,"")

        self.tab1 = QtGui.QWidget()
        self.tab1.setGeometry(QtCore.QRect(0,0,428,413))
        self.tab1.setObjectName("tab1")

        self.gridlayout2 = QtGui.QGridLayout(self.tab1)
        self.gridlayout2.setObjectName("gridlayout2")

        self.authLabel = QtGui.QLabel(self.tab1)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.authLabel.sizePolicy().hasHeightForWidth())
        self.authLabel.setSizePolicy(sizePolicy)
        self.authLabel.setMinimumSize(QtCore.QSize(48,48))
        self.authLabel.setWordWrap(False)
        self.authLabel.setObjectName("authLabel")
        self.gridlayout2.addWidget(self.authLabel,0,0,1,1)

        self.gridlayout3 = QtGui.QGridLayout()
        self.gridlayout3.setObjectName("gridlayout3")

        self.textLabel1_4 = QtGui.QLabel(self.tab1)
        self.textLabel1_4.setWordWrap(False)
        self.textLabel1_4.setObjectName("textLabel1_4")
        self.gridlayout3.addWidget(self.textLabel1_4,0,0,1,3)

        spacerItem6 = QtGui.QSpacerItem(13,18,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem6,1,0,1,1)

        self.bindAnonBox = QtGui.QCheckBox(self.tab1)
        self.bindAnonBox.setObjectName("bindAnonBox")
        self.gridlayout3.addWidget(self.bindAnonBox,1,1,1,2)

        self.textLabel4 = QtGui.QLabel(self.tab1)
        self.textLabel4.setAlignment(QtCore.Qt.AlignVCenter)
        self.textLabel4.setWordWrap(False)
        self.textLabel4.setObjectName("textLabel4")
        self.gridlayout3.addWidget(self.textLabel4,2,1,1,1)

        self.methodBox = QtGui.QComboBox(self.tab1)
        self.methodBox.setObjectName("methodBox")
        self.gridlayout3.addWidget(self.methodBox,2,2,1,1)

        self.textLabel10 = QtGui.QLabel(self.tab1)
        self.textLabel10.setAlignment(QtCore.Qt.AlignVCenter)
        self.textLabel10.setWordWrap(True)
        self.textLabel10.setObjectName("textLabel10")
        self.gridlayout3.addWidget(self.textLabel10,3,1,1,1)

        self.bindLineEdit = QtGui.QLineEdit(self.tab1)
        self.bindLineEdit.setObjectName("bindLineEdit")
        self.gridlayout3.addWidget(self.bindLineEdit,3,2,1,1)

        self.textLabel12 = QtGui.QLabel(self.tab1)
        self.textLabel12.setAlignment(QtCore.Qt.AlignVCenter)
        self.textLabel12.setWordWrap(False)
        self.textLabel12.setObjectName("textLabel12")
        self.gridlayout3.addWidget(self.textLabel12,4,1,1,1)

        self.passwordLineEdit = QtGui.QLineEdit(self.tab1)
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.gridlayout3.addWidget(self.passwordLineEdit,4,2,1,1)
        self.gridlayout2.addLayout(self.gridlayout3,0,1,2,1)

        spacerItem7 = QtGui.QSpacerItem(45,445,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem7,1,0,2,1)

        spacerItem8 = QtGui.QSpacerItem(114,21,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem8,2,1,1,1)
        self.serverWidget.addTab(self.tab1,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setGeometry(QtCore.QRect(0,0,428,413))
        self.tab_2.setObjectName("tab_2")

        self.gridlayout4 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout4.setObjectName("gridlayout4")

        self.securityLabel = QtGui.QLabel(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.securityLabel.sizePolicy().hasHeightForWidth())
        self.securityLabel.setSizePolicy(sizePolicy)
        self.securityLabel.setMinimumSize(QtCore.QSize(48,48))
        self.securityLabel.setWordWrap(False)
        self.securityLabel.setObjectName("securityLabel")
        self.gridlayout4.addWidget(self.securityLabel,0,0,1,1)

        self.gridlayout5 = QtGui.QGridLayout()
        self.gridlayout5.setObjectName("gridlayout5")

        self.textLabel1_10 = QtGui.QLabel(self.tab_2)
        self.textLabel1_10.setWordWrap(False)
        self.textLabel1_10.setObjectName("textLabel1_10")
        self.gridlayout5.addWidget(self.textLabel1_10,0,0,1,2)

        self.encryptionBox = QtGui.QComboBox(self.tab_2)
        self.encryptionBox.setObjectName("encryptionBox")
        self.gridlayout5.addWidget(self.encryptionBox,1,1,1,1)

        spacerItem9 = QtGui.QSpacerItem(16,16,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem9,1,0,1,1)
        self.gridlayout4.addLayout(self.gridlayout5,0,1,1,2)

        spacerItem10 = QtGui.QSpacerItem(45,200,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout4.addItem(spacerItem10,1,0,5,1)

        spacerItem11 = QtGui.QSpacerItem(21,18,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.gridlayout4.addItem(spacerItem11,1,1,1,1)

        self.gridlayout6 = QtGui.QGridLayout()
        self.gridlayout6.setObjectName("gridlayout6")

        spacerItem12 = QtGui.QSpacerItem(16,16,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem12,1,0,1,1)

        self.textLabel1_9 = QtGui.QLabel(self.tab_2)
        self.textLabel1_9.setAlignment(QtCore.Qt.AlignVCenter)
        self.textLabel1_9.setWordWrap(False)
        self.textLabel1_9.setObjectName("textLabel1_9")
        self.gridlayout6.addWidget(self.textLabel1_9,0,0,1,2)

        self.validateBox = QtGui.QComboBox(self.tab_2)
        self.validateBox.setObjectName("validateBox")
        self.gridlayout6.addWidget(self.validateBox,1,1,1,1)
        self.gridlayout4.addLayout(self.gridlayout6,2,1,1,2)

        spacerItem13 = QtGui.QSpacerItem(21,18,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.gridlayout4.addItem(spacerItem13,3,1,1,1)

        self.gridlayout7 = QtGui.QGridLayout()
        self.gridlayout7.setObjectName("gridlayout7")

        self.textLabel3 = QtGui.QLabel(self.tab_2)
        self.textLabel3.setWordWrap(False)
        self.textLabel3.setObjectName("textLabel3")
        self.gridlayout7.addWidget(self.textLabel3,3,1,1,1)

        self.certKeyFileButton = QtGui.QToolButton(self.tab_2)
        self.certKeyFileButton.setEnabled(False)
        self.certKeyFileButton.setObjectName("certKeyFileButton")
        self.gridlayout7.addWidget(self.certKeyFileButton,3,3,1,1)

        self.certFileButton = QtGui.QToolButton(self.tab_2)
        self.certFileButton.setEnabled(False)
        self.certFileButton.setObjectName("certFileButton")
        self.gridlayout7.addWidget(self.certFileButton,2,3,1,1)

        spacerItem14 = QtGui.QSpacerItem(16,16,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout7.addItem(spacerItem14,1,0,1,1)

        self.certFileEdit = QtGui.QLineEdit(self.tab_2)
        self.certFileEdit.setEnabled(False)
        self.certFileEdit.setObjectName("certFileEdit")
        self.gridlayout7.addWidget(self.certFileEdit,2,2,1,1)

        self.useClientCertBox = QtGui.QCheckBox(self.tab_2)
        self.useClientCertBox.setEnabled(False)
        self.useClientCertBox.setObjectName("useClientCertBox")
        self.gridlayout7.addWidget(self.useClientCertBox,1,1,1,3)

        self.certKeyfileEdit = QtGui.QLineEdit(self.tab_2)
        self.certKeyfileEdit.setEnabled(False)
        self.certKeyfileEdit.setObjectName("certKeyfileEdit")
        self.gridlayout7.addWidget(self.certKeyfileEdit,3,2,1,1)

        self.textLabel2_2 = QtGui.QLabel(self.tab_2)
        self.textLabel2_2.setWordWrap(False)
        self.textLabel2_2.setObjectName("textLabel2_2")
        self.gridlayout7.addWidget(self.textLabel2_2,2,1,1,1)

        self.textLabel1_3 = QtGui.QLabel(self.tab_2)
        self.textLabel1_3.setWordWrap(False)
        self.textLabel1_3.setObjectName("textLabel1_3")
        self.gridlayout7.addWidget(self.textLabel1_3,0,0,1,4)
        self.gridlayout4.addLayout(self.gridlayout7,4,1,1,2)

        spacerItem15 = QtGui.QSpacerItem(175,100,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.gridlayout4.addItem(spacerItem15,5,2,1,1)
        self.serverWidget.addTab(self.tab_2,"")
        self.vboxlayout.addWidget(self.splitter2)

        self.line1 = QtGui.QFrame(ServerDialogDesign)
        self.line1.setFrameShape(QtGui.QFrame.HLine)
        self.line1.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1.setObjectName("line1")
        self.vboxlayout.addWidget(self.line1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem16 = QtGui.QSpacerItem(383,25,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem16)

        self.okButton = QtGui.QPushButton(ServerDialogDesign)
        self.okButton.setDefault(True)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)

        self.applyButton = QtGui.QPushButton(ServerDialogDesign)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.applyButton.sizePolicy().hasHeightForWidth())
        self.applyButton.setSizePolicy(sizePolicy)
        self.applyButton.setObjectName("applyButton")
        self.hboxlayout.addWidget(self.applyButton)

        self.cancelButton = QtGui.QPushButton(ServerDialogDesign)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(ServerDialogDesign)
        self.serverWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.addButton,QtCore.SIGNAL("clicked()"),ServerDialogDesign.addServer)
        QtCore.QObject.connect(self.applyButton,QtCore.SIGNAL("clicked()"),ServerDialogDesign.saveServer)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),ServerDialogDesign.reject)
        QtCore.QObject.connect(self.deleteButton,QtCore.SIGNAL("clicked()"),ServerDialogDesign.deleteServer)
        QtCore.QObject.connect(self.okButton,QtCore.SIGNAL("clicked()"),ServerDialogDesign.saveCloseDialog)
        QtCore.QObject.connect(self.serverListView,QtCore.SIGNAL("currentItemChanged(QListWidgetItem*, QListWidgetItem*)"),ServerDialogDesign.serverSelectionChanged)
        QtCore.QObject.connect(self.aliasBox,QtCore.SIGNAL("clicked()"),ServerDialogDesign.aliasesChanged)
        QtCore.QObject.connect(self.baseBox,QtCore.SIGNAL("clicked()"),ServerDialogDesign.useServerBase)
        QtCore.QObject.connect(self.bindAnonBox,QtCore.SIGNAL("toggled(bool)"),ServerDialogDesign.bindAnonChanged)
        QtCore.QObject.connect(self.bindLineEdit,QtCore.SIGNAL("textChanged(QString)"),ServerDialogDesign.bindDNChanged)
        QtCore.QObject.connect(self.methodBox,QtCore.SIGNAL("activated(int)"),ServerDialogDesign.methodChanged)
        QtCore.QObject.connect(self.manageBaseButton,QtCore.SIGNAL("clicked()"),ServerDialogDesign.manageBaseDN)
        QtCore.QObject.connect(self.portSpinBox,QtCore.SIGNAL("valueChanged(int)"),ServerDialogDesign.portChanged)
        QtCore.QObject.connect(self.passwordLineEdit,QtCore.SIGNAL("textChanged(QString)"),ServerDialogDesign.bindPasswordChanged)
        QtCore.QObject.connect(self.hostLineEdit,QtCore.SIGNAL("textChanged(QString)"),ServerDialogDesign.hostChanged)
        QtCore.QMetaObject.connectSlotsByName(ServerDialogDesign)
        ServerDialogDesign.setTabOrder(self.serverListView,self.addButton)
        ServerDialogDesign.setTabOrder(self.addButton,self.deleteButton)
        ServerDialogDesign.setTabOrder(self.deleteButton,self.serverWidget)
        ServerDialogDesign.setTabOrder(self.serverWidget,self.hostLineEdit)
        ServerDialogDesign.setTabOrder(self.hostLineEdit,self.portSpinBox)
        ServerDialogDesign.setTabOrder(self.portSpinBox,self.aliasBox)
        ServerDialogDesign.setTabOrder(self.aliasBox,self.baseBox)
        ServerDialogDesign.setTabOrder(self.baseBox,self.baseDNView)
        ServerDialogDesign.setTabOrder(self.baseDNView,self.manageBaseButton)
        ServerDialogDesign.setTabOrder(self.manageBaseButton,self.bindAnonBox)
        ServerDialogDesign.setTabOrder(self.bindAnonBox,self.methodBox)
        ServerDialogDesign.setTabOrder(self.methodBox,self.bindLineEdit)
        ServerDialogDesign.setTabOrder(self.bindLineEdit,self.passwordLineEdit)
        ServerDialogDesign.setTabOrder(self.passwordLineEdit,self.okButton)
        ServerDialogDesign.setTabOrder(self.okButton,self.applyButton)
        ServerDialogDesign.setTabOrder(self.applyButton,self.cancelButton)

    def retranslateUi(self, ServerDialogDesign):
        ServerDialogDesign.setWindowTitle(QtGui.QApplication.translate("ServerDialogDesign", "Manage Server List", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("ServerDialogDesign", "&Add...", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setShortcut(QtGui.QApplication.translate("ServerDialogDesign", "Alt+A", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("ServerDialogDesign", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setShortcut(QtGui.QApplication.translate("ServerDialogDesign", "Alt+D", None, QtGui.QApplication.UnicodeUTF8))
        self.networkLabel.setText(QtGui.QApplication.translate("ServerDialogDesign", "NO", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_2.setText(QtGui.QApplication.translate("ServerDialogDesign", "<b>Network options</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel9.setText(QtGui.QApplication.translate("ServerDialogDesign", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel8.setText(QtGui.QApplication.translate("ServerDialogDesign", "Host:", None, QtGui.QApplication.UnicodeUTF8))
        self.aliasBox.setText(QtGui.QApplication.translate("ServerDialogDesign", "Follow aliases", None, QtGui.QApplication.UnicodeUTF8))
        self.baseBox.setText(QtGui.QApplication.translate("ServerDialogDesign", "Use Base DNs provided by the server", None, QtGui.QApplication.UnicodeUTF8))
        self.manageBaseButton.setText(QtGui.QApplication.translate("ServerDialogDesign", "Manage Base DN list", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setText(QtGui.QApplication.translate("ServerDialogDesign", "<b>LDAP options</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.serverWidget.setTabText(self.serverWidget.indexOf(self.tab), QtGui.QApplication.translate("ServerDialogDesign", "Network", None, QtGui.QApplication.UnicodeUTF8))
        self.authLabel.setText(QtGui.QApplication.translate("ServerDialogDesign", "SO", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_4.setText(QtGui.QApplication.translate("ServerDialogDesign", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Bind options</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.bindAnonBox.setText(QtGui.QApplication.translate("ServerDialogDesign", "Anonymous bind", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel4.setText(QtGui.QApplication.translate("ServerDialogDesign", "Mechanism:", None, QtGui.QApplication.UnicodeUTF8))
        self.methodBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "Simple", None, QtGui.QApplication.UnicodeUTF8))
        self.methodBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "SASL CRAM-MD5", None, QtGui.QApplication.UnicodeUTF8))
        self.methodBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "SASL DIGEST-MD5", None, QtGui.QApplication.UnicodeUTF8))
        self.methodBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "SASL EXTERNAL", None, QtGui.QApplication.UnicodeUTF8))
        self.methodBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "SASL GSSAPI", None, QtGui.QApplication.UnicodeUTF8))
        self.methodBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "SASL Login", None, QtGui.QApplication.UnicodeUTF8))
        self.methodBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "SASL Plain", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel10.setText(QtGui.QApplication.translate("ServerDialogDesign", "Bind as:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel12.setText(QtGui.QApplication.translate("ServerDialogDesign", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.serverWidget.setTabText(self.serverWidget.indexOf(self.tab1), QtGui.QApplication.translate("ServerDialogDesign", "Authentification", None, QtGui.QApplication.UnicodeUTF8))
        self.securityLabel.setText(QtGui.QApplication.translate("ServerDialogDesign", "SO", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_10.setText(QtGui.QApplication.translate("ServerDialogDesign", "<b>Security options</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.encryptionBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "Unencrypted connection", None, QtGui.QApplication.UnicodeUTF8))
        self.encryptionBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "Transport Layer Security (TLS)", None, QtGui.QApplication.UnicodeUTF8))
        self.encryptionBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "Secure Socket Layer (SSL)", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_9.setText(QtGui.QApplication.translate("ServerDialogDesign", "<b>Validate server certificate</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.validateBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "Never", None, QtGui.QApplication.UnicodeUTF8))
        self.validateBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "Allow", None, QtGui.QApplication.UnicodeUTF8))
        self.validateBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "Try", None, QtGui.QApplication.UnicodeUTF8))
        self.validateBox.addItem(QtGui.QApplication.translate("ServerDialogDesign", "Demand", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel3.setText(QtGui.QApplication.translate("ServerDialogDesign", "Certificate keyfile:", None, QtGui.QApplication.UnicodeUTF8))
        self.certKeyFileButton.setText(QtGui.QApplication.translate("ServerDialogDesign", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.certFileButton.setText(QtGui.QApplication.translate("ServerDialogDesign", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.useClientCertBox.setText(QtGui.QApplication.translate("ServerDialogDesign", "Use client certificates", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel2_2.setText(QtGui.QApplication.translate("ServerDialogDesign", "Certificate file:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_3.setText(QtGui.QApplication.translate("ServerDialogDesign", "<b>Client certificate options</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.serverWidget.setTabText(self.serverWidget.indexOf(self.tab_2), QtGui.QApplication.translate("ServerDialogDesign", "Security", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("ServerDialogDesign", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setShortcut(QtGui.QApplication.translate("ServerDialogDesign", "Alt+O", None, QtGui.QApplication.UnicodeUTF8))
        self.applyButton.setText(QtGui.QApplication.translate("ServerDialogDesign", "&Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.applyButton.setShortcut(QtGui.QApplication.translate("ServerDialogDesign", "Alt+A", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("ServerDialogDesign", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setShortcut(QtGui.QApplication.translate("ServerDialogDesign", "Alt+C", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ServerDialogDesign = QtGui.QDialog()
    ui = Ui_ServerDialogDesign()
    ui.setupUi(ServerDialogDesign)
    ServerDialogDesign.show()
    sys.exit(app.exec_())
