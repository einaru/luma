# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/luma/base/gui/ImprovedServerDialogDesign.ui'
#
# Created: Tue Mar 18 23:21:03 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ImprovedServerDialogDesign(object):
    def setupUi(self, ImprovedServerDialogDesign):
        ImprovedServerDialogDesign.setObjectName("ImprovedServerDialogDesign")
        ImprovedServerDialogDesign.resize(QtCore.QSize(QtCore.QRect(0,0,556,375).size()).expandedTo(ImprovedServerDialogDesign.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(ImprovedServerDialogDesign)
        self.vboxlayout.setObjectName("vboxlayout")

        self.splitter2 = QtGui.QSplitter(ImprovedServerDialogDesign)
        self.splitter2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter2.setObjectName("splitter2")

        self.layout20 = QtGui.QWidget(self.splitter2)
        self.layout20.setObjectName("layout20")

        self.gridlayout = QtGui.QGridLayout(self.layout20)
        self.gridlayout.setObjectName("gridlayout")

        self.addServerButton = QtGui.QPushButton(self.layout20)
        self.addServerButton.setAutoDefault(False)
        self.addServerButton.setDefault(False)
        self.addServerButton.setObjectName("addServerButton")
        self.gridlayout.addWidget(self.addServerButton,1,1,1,1)

        self.serverListView = QtGui.QTreeWidget(self.layout20)
        self.serverListView.setRootIsDecorated(False)
        self.serverListView.setObjectName("serverListView")
        self.gridlayout.addWidget(self.serverListView,0,0,1,3)

        self.deleteServerButton = QtGui.QPushButton(self.layout20)
        self.deleteServerButton.setAutoDefault(False)
        self.deleteServerButton.setObjectName("deleteServerButton")
        self.gridlayout.addWidget(self.deleteServerButton,1,2,1,1)

        spacerItem = QtGui.QSpacerItem(68,21,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.layout12 = QtGui.QWidget(self.splitter2)
        self.layout12.setObjectName("layout12")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.layout12)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName("gridlayout1")

        self.line2 = QtGui.QFrame(self.layout12)
        self.line2.setFrameShape(QtGui.QFrame.HLine)
        self.line2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line2.setObjectName("line2")
        self.gridlayout1.addWidget(self.line2,1,0,1,2)

        self.serverNameStack = QtGui.QStackedWidget(self.layout12)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverNameStack.sizePolicy().hasHeightForWidth())
        self.serverNameStack.setSizePolicy(sizePolicy)
        self.serverNameStack.setObjectName("serverNameStack")

        self.namePage = QtGui.QWidget()
        self.namePage.setObjectName("namePage")

        self.hboxlayout = QtGui.QHBoxLayout(self.namePage)
        self.hboxlayout.setObjectName("hboxlayout")

        self.serverLabel = QtGui.QLabel(self.namePage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverLabel.sizePolicy().hasHeightForWidth())
        self.serverLabel.setSizePolicy(sizePolicy)
        self.serverLabel.setAlignment(QtCore.Qt.AlignVCenter)
        self.serverLabel.setWordWrap(False)
        self.serverLabel.setObjectName("serverLabel")
        self.hboxlayout.addWidget(self.serverLabel)

        self.renameButton = QtGui.QPushButton(self.namePage)
        self.renameButton.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.renameButton.sizePolicy().hasHeightForWidth())
        self.renameButton.setSizePolicy(sizePolicy)
        self.renameButton.setAutoDefault(False)
        self.renameButton.setObjectName("renameButton")
        self.hboxlayout.addWidget(self.renameButton)
        self.serverNameStack.addWidget(self.namePage)

        self.editNamePage = QtGui.QWidget()
        self.editNamePage.setObjectName("editNamePage")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.editNamePage)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.renameEdit = QtGui.QLineEdit(self.editNamePage)
        self.renameEdit.setObjectName("renameEdit")
        self.hboxlayout1.addWidget(self.renameEdit)

        self.renameOkButton = QtGui.QPushButton(self.editNamePage)
        self.renameOkButton.setAutoDefault(False)
        self.renameOkButton.setObjectName("renameOkButton")
        self.hboxlayout1.addWidget(self.renameOkButton)

        self.cancelRenameButton = QtGui.QPushButton(self.editNamePage)
        self.cancelRenameButton.setAutoDefault(False)
        self.cancelRenameButton.setObjectName("cancelRenameButton")
        self.hboxlayout1.addWidget(self.cancelRenameButton)
        self.serverNameStack.addWidget(self.editNamePage)
        self.gridlayout1.addWidget(self.serverNameStack,0,1,1,1)

        self.pixmapLabel1 = QtGui.QLabel(self.layout12)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pixmapLabel1.sizePolicy().hasHeightForWidth())
        self.pixmapLabel1.setSizePolicy(sizePolicy)
        self.pixmapLabel1.setScaledContents(False)
        self.pixmapLabel1.setWordWrap(False)
        self.pixmapLabel1.setObjectName("pixmapLabel1")
        self.gridlayout1.addWidget(self.pixmapLabel1,0,0,1,1)
        self.vboxlayout1.addLayout(self.gridlayout1)

        self.configStack = QtGui.QStackedWidget(self.layout12)
        self.configStack.setObjectName("configStack")

        self.WStackPage = QtGui.QWidget()
        self.WStackPage.setObjectName("WStackPage")

        self.gridlayout2 = QtGui.QGridLayout(self.WStackPage)
        self.gridlayout2.setObjectName("gridlayout2")

        self.textLabel5 = QtGui.QLabel(self.WStackPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel5.sizePolicy().hasHeightForWidth())
        self.textLabel5.setSizePolicy(sizePolicy)
        self.textLabel5.setMouseTracking(True)
        self.textLabel5.setWordWrap(False)
        self.textLabel5.setObjectName("textLabel5")
        self.gridlayout2.addWidget(self.textLabel5,0,0,1,1)

        self.networkLabel = QtGui.QLabel(self.WStackPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.networkLabel.sizePolicy().hasHeightForWidth())
        self.networkLabel.setSizePolicy(sizePolicy)
        self.networkLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.networkLabel.setWordWrap(False)
        self.networkLabel.setObjectName("networkLabel")
        self.gridlayout2.addWidget(self.networkLabel,0,1,1,1)

        self.textLabel7 = QtGui.QLabel(self.WStackPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel7.sizePolicy().hasHeightForWidth())
        self.textLabel7.setSizePolicy(sizePolicy)
        self.textLabel7.setWordWrap(False)
        self.textLabel7.setObjectName("textLabel7")
        self.gridlayout2.addWidget(self.textLabel7,1,0,1,1)

        self.credentialLabel = QtGui.QLabel(self.WStackPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.credentialLabel.sizePolicy().hasHeightForWidth())
        self.credentialLabel.setSizePolicy(sizePolicy)
        self.credentialLabel.setWordWrap(False)
        self.credentialLabel.setObjectName("credentialLabel")
        self.gridlayout2.addWidget(self.credentialLabel,1,1,1,1)

        self.encryptionLabel = QtGui.QLabel(self.WStackPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.encryptionLabel.sizePolicy().hasHeightForWidth())
        self.encryptionLabel.setSizePolicy(sizePolicy)
        self.encryptionLabel.setWordWrap(False)
        self.encryptionLabel.setObjectName("encryptionLabel")
        self.gridlayout2.addWidget(self.encryptionLabel,2,1,1,1)

        self.authLabel = QtGui.QLabel(self.WStackPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.authLabel.sizePolicy().hasHeightForWidth())
        self.authLabel.setSizePolicy(sizePolicy)
        self.authLabel.setWordWrap(False)
        self.authLabel.setObjectName("authLabel")
        self.gridlayout2.addWidget(self.authLabel,3,1,1,1)

        self.textLabel10 = QtGui.QLabel(self.WStackPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel10.sizePolicy().hasHeightForWidth())
        self.textLabel10.setSizePolicy(sizePolicy)
        self.textLabel10.setWordWrap(False)
        self.textLabel10.setObjectName("textLabel10")
        self.gridlayout2.addWidget(self.textLabel10,2,0,1,1)

        self.textLabel12 = QtGui.QLabel(self.WStackPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel12.sizePolicy().hasHeightForWidth())
        self.textLabel12.setSizePolicy(sizePolicy)
        self.textLabel12.setWordWrap(False)
        self.textLabel12.setObjectName("textLabel12")
        self.gridlayout2.addWidget(self.textLabel12,3,0,1,1)

        self.textLabel16 = QtGui.QLabel(self.WStackPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel16.sizePolicy().hasHeightForWidth())
        self.textLabel16.setSizePolicy(sizePolicy)
        self.textLabel16.setWordWrap(False)
        self.textLabel16.setObjectName("textLabel16")
        self.gridlayout2.addWidget(self.textLabel16,4,0,1,1)

        self.ldapOptLabel = QtGui.QLabel(self.WStackPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ldapOptLabel.sizePolicy().hasHeightForWidth())
        self.ldapOptLabel.setSizePolicy(sizePolicy)
        self.ldapOptLabel.setAlignment(QtCore.Qt.AlignTop)
        self.ldapOptLabel.setWordWrap(False)
        self.ldapOptLabel.setObjectName("ldapOptLabel")
        self.gridlayout2.addWidget(self.ldapOptLabel,4,1,2,1)

        spacerItem1 = QtGui.QSpacerItem(20,41,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem1,5,0,1,1)
        self.configStack.addWidget(self.WStackPage)

        self.WStackPage1 = QtGui.QWidget()
        self.WStackPage1.setObjectName("WStackPage1")

        self.gridlayout3 = QtGui.QGridLayout(self.WStackPage1)
        self.gridlayout3.setObjectName("gridlayout3")

        self.textLabel3 = QtGui.QLabel(self.WStackPage1)
        self.textLabel3.setWordWrap(False)
        self.textLabel3.setObjectName("textLabel3")
        self.gridlayout3.addWidget(self.textLabel3,2,0,1,1)

        self.portBox = QtGui.QSpinBox(self.WStackPage1)
        self.portBox.setMaximum(32767)
        self.portBox.setProperty("value",QtCore.QVariant(389))
        self.portBox.setObjectName("portBox")
        self.gridlayout3.addWidget(self.portBox,2,1,1,2)

        self.textLabel2 = QtGui.QLabel(self.WStackPage1)
        self.textLabel2.setWordWrap(False)
        self.textLabel2.setObjectName("textLabel2")
        self.gridlayout3.addWidget(self.textLabel2,1,0,1,1)

        self.hostnameEdit = QtGui.QLineEdit(self.WStackPage1)
        self.hostnameEdit.setObjectName("hostnameEdit")
        self.gridlayout3.addWidget(self.hostnameEdit,1,1,1,2)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.pixmapLabel1_2 = QtGui.QLabel(self.WStackPage1)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pixmapLabel1_2.sizePolicy().hasHeightForWidth())
        self.pixmapLabel1_2.setSizePolicy(sizePolicy)
        self.pixmapLabel1_2.setScaledContents(False)
        self.pixmapLabel1_2.setWordWrap(False)
        self.pixmapLabel1_2.setObjectName("pixmapLabel1_2")
        self.hboxlayout2.addWidget(self.pixmapLabel1_2)

        self.textLabel4 = QtGui.QLabel(self.WStackPage1)
        self.textLabel4.setWordWrap(False)
        self.textLabel4.setObjectName("textLabel4")
        self.hboxlayout2.addWidget(self.textLabel4)

        self.pushButton6 = QtGui.QPushButton(self.WStackPage1)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton6.sizePolicy().hasHeightForWidth())
        self.pushButton6.setSizePolicy(sizePolicy)
        self.pushButton6.setAutoDefault(False)
        self.pushButton6.setObjectName("pushButton6")
        self.hboxlayout2.addWidget(self.pushButton6)
        self.gridlayout3.addLayout(self.hboxlayout2,0,0,1,3)

        self.textLabel5_2 = QtGui.QLabel(self.WStackPage1)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel5_2.sizePolicy().hasHeightForWidth())
        self.textLabel5_2.setSizePolicy(sizePolicy)
        self.textLabel5_2.setWordWrap(False)
        self.textLabel5_2.setObjectName("textLabel5_2")
        self.gridlayout3.addWidget(self.textLabel5_2,3,0,1,1)

        self.encryptionBox = QtGui.QComboBox(self.WStackPage1)
        self.encryptionBox.setObjectName("encryptionBox")
        self.gridlayout3.addWidget(self.encryptionBox,3,1,1,2)

        spacerItem2 = QtGui.QSpacerItem(20,30,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout3.addItem(spacerItem2,5,2,1,1)

        spacerItem3 = QtGui.QSpacerItem(111,21,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem3,4,0,1,2)

        self.editCertButton = QtGui.QPushButton(self.WStackPage1)
        self.editCertButton.setAutoDefault(False)
        self.editCertButton.setObjectName("editCertButton")
        self.gridlayout3.addWidget(self.editCertButton,4,2,1,1)
        self.configStack.addWidget(self.WStackPage1)

        self.blankPage = QtGui.QWidget()
        self.blankPage.setObjectName("blankPage")

        self.gridlayout4 = QtGui.QGridLayout(self.blankPage)
        self.gridlayout4.setObjectName("gridlayout4")

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.pixmapLabel2 = QtGui.QLabel(self.blankPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pixmapLabel2.sizePolicy().hasHeightForWidth())
        self.pixmapLabel2.setSizePolicy(sizePolicy)
        self.pixmapLabel2.setScaledContents(False)
        self.pixmapLabel2.setWordWrap(False)
        self.pixmapLabel2.setObjectName("pixmapLabel2")
        self.hboxlayout3.addWidget(self.pixmapLabel2)

        self.textLabel1 = QtGui.QLabel(self.blankPage)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName("textLabel1")
        self.hboxlayout3.addWidget(self.textLabel1)

        self.pushButton7 = QtGui.QPushButton(self.blankPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton7.sizePolicy().hasHeightForWidth())
        self.pushButton7.setSizePolicy(sizePolicy)
        self.pushButton7.setObjectName("pushButton7")
        self.hboxlayout3.addWidget(self.pushButton7)
        self.gridlayout4.addLayout(self.hboxlayout3,0,0,1,2)

        self.anonBindBox = QtGui.QCheckBox(self.blankPage)
        self.anonBindBox.setObjectName("anonBindBox")
        self.gridlayout4.addWidget(self.anonBindBox,1,0,1,2)

        spacerItem4 = QtGui.QSpacerItem(21,50,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout4.addItem(spacerItem4,5,1,1,1)

        self.bindAsLabel = QtGui.QLabel(self.blankPage)
        self.bindAsLabel.setWordWrap(False)
        self.bindAsLabel.setObjectName("bindAsLabel")
        self.gridlayout4.addWidget(self.bindAsLabel,3,0,1,1)

        self.authentificationBox = QtGui.QComboBox(self.blankPage)
        self.authentificationBox.setObjectName("authentificationBox")
        self.gridlayout4.addWidget(self.authentificationBox,2,1,1,1)

        self.bindPasswordLabel = QtGui.QLabel(self.blankPage)
        self.bindPasswordLabel.setWordWrap(False)
        self.bindPasswordLabel.setObjectName("bindPasswordLabel")
        self.gridlayout4.addWidget(self.bindPasswordLabel,4,0,1,1)

        self.authMechanismLabel = QtGui.QLabel(self.blankPage)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.authMechanismLabel.sizePolicy().hasHeightForWidth())
        self.authMechanismLabel.setSizePolicy(sizePolicy)
        self.authMechanismLabel.setWordWrap(False)
        self.authMechanismLabel.setObjectName("authMechanismLabel")
        self.gridlayout4.addWidget(self.authMechanismLabel,2,0,1,1)

        self.bindAsEdit = QtGui.QLineEdit(self.blankPage)
        self.bindAsEdit.setObjectName("bindAsEdit")
        self.gridlayout4.addWidget(self.bindAsEdit,3,1,1,1)

        self.bindPasswordEdit = QtGui.QLineEdit(self.blankPage)
        self.bindPasswordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.bindPasswordEdit.setObjectName("bindPasswordEdit")
        self.gridlayout4.addWidget(self.bindPasswordEdit,4,1,1,1)
        self.configStack.addWidget(self.blankPage)

        self.WStackPage2 = QtGui.QWidget()
        self.WStackPage2.setObjectName("WStackPage2")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.WStackPage2)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.pixmapLabel4 = QtGui.QLabel(self.WStackPage2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pixmapLabel4.sizePolicy().hasHeightForWidth())
        self.pixmapLabel4.setSizePolicy(sizePolicy)
        self.pixmapLabel4.setScaledContents(False)
        self.pixmapLabel4.setWordWrap(False)
        self.pixmapLabel4.setObjectName("pixmapLabel4")
        self.hboxlayout4.addWidget(self.pixmapLabel4)

        self.textLabel7_2 = QtGui.QLabel(self.WStackPage2)
        self.textLabel7_2.setWordWrap(False)
        self.textLabel7_2.setObjectName("textLabel7_2")
        self.hboxlayout4.addWidget(self.textLabel7_2)

        self.pushButton9 = QtGui.QPushButton(self.WStackPage2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton9.sizePolicy().hasHeightForWidth())
        self.pushButton9.setSizePolicy(sizePolicy)
        self.pushButton9.setObjectName("pushButton9")
        self.hboxlayout4.addWidget(self.pushButton9)
        self.vboxlayout2.addLayout(self.hboxlayout4)

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.textLabel8_2 = QtGui.QLabel(self.WStackPage2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel8_2.sizePolicy().hasHeightForWidth())
        self.textLabel8_2.setSizePolicy(sizePolicy)
        self.textLabel8_2.setWordWrap(False)
        self.textLabel8_2.setObjectName("textLabel8_2")
        self.hboxlayout5.addWidget(self.textLabel8_2)

        self.serverCertBox = QtGui.QComboBox(self.WStackPage2)
        self.serverCertBox.setObjectName("serverCertBox")
        self.hboxlayout5.addWidget(self.serverCertBox)
        self.vboxlayout2.addLayout(self.hboxlayout5)

        spacerItem5 = QtGui.QSpacerItem(20,10,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.vboxlayout2.addItem(spacerItem5)

        self.gridlayout5 = QtGui.QGridLayout()
        self.gridlayout5.setObjectName("gridlayout5")

        self.certFileButton = QtGui.QToolButton(self.WStackPage2)
        self.certFileButton.setEnabled(True)
        self.certFileButton.setObjectName("certFileButton")
        self.gridlayout5.addWidget(self.certFileButton,1,2,1,1)

        self.certKeyFileButton = QtGui.QToolButton(self.WStackPage2)
        self.certKeyFileButton.setEnabled(True)
        self.certKeyFileButton.setObjectName("certKeyFileButton")
        self.gridlayout5.addWidget(self.certKeyFileButton,2,2,1,1)

        self.certLabel = QtGui.QLabel(self.WStackPage2)
        self.certLabel.setWordWrap(False)
        self.certLabel.setObjectName("certLabel")
        self.gridlayout5.addWidget(self.certLabel,1,0,1,1)

        self.clientCertBox = QtGui.QCheckBox(self.WStackPage2)
        self.clientCertBox.setObjectName("clientCertBox")
        self.gridlayout5.addWidget(self.clientCertBox,0,0,1,2)

        self.certFileEdit = QtGui.QLineEdit(self.WStackPage2)
        self.certFileEdit.setEnabled(True)
        self.certFileEdit.setObjectName("certFileEdit")
        self.gridlayout5.addWidget(self.certFileEdit,1,1,1,1)

        self.certKeyLabel = QtGui.QLabel(self.WStackPage2)
        self.certKeyLabel.setWordWrap(False)
        self.certKeyLabel.setObjectName("certKeyLabel")
        self.gridlayout5.addWidget(self.certKeyLabel,2,0,1,1)

        self.certKeyFileEdit = QtGui.QLineEdit(self.WStackPage2)
        self.certKeyFileEdit.setEnabled(True)
        self.certKeyFileEdit.setObjectName("certKeyFileEdit")
        self.gridlayout5.addWidget(self.certKeyFileEdit,2,1,1,1)
        self.vboxlayout2.addLayout(self.gridlayout5)

        spacerItem6 = QtGui.QSpacerItem(20,41,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem6)
        self.configStack.addWidget(self.WStackPage2)

        self.WStackPage3 = QtGui.QWidget()
        self.WStackPage3.setObjectName("WStackPage3")

        self.gridlayout6 = QtGui.QGridLayout(self.WStackPage3)
        self.gridlayout6.setObjectName("gridlayout6")

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.pixmapLabel5 = QtGui.QLabel(self.WStackPage3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pixmapLabel5.sizePolicy().hasHeightForWidth())
        self.pixmapLabel5.setSizePolicy(sizePolicy)
        self.pixmapLabel5.setScaledContents(False)
        self.pixmapLabel5.setWordWrap(False)
        self.pixmapLabel5.setObjectName("pixmapLabel5")
        self.hboxlayout6.addWidget(self.pixmapLabel5)

        self.textLabel9 = QtGui.QLabel(self.WStackPage3)
        self.textLabel9.setWordWrap(False)
        self.textLabel9.setObjectName("textLabel9")
        self.hboxlayout6.addWidget(self.textLabel9)

        self.pushButton10_2 = QtGui.QPushButton(self.WStackPage3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton10_2.sizePolicy().hasHeightForWidth())
        self.pushButton10_2.setSizePolicy(sizePolicy)
        self.pushButton10_2.setObjectName("pushButton10_2")
        self.hboxlayout6.addWidget(self.pushButton10_2)
        self.gridlayout6.addLayout(self.hboxlayout6,0,0,1,3)

        self.aliasBox = QtGui.QCheckBox(self.WStackPage3)
        self.aliasBox.setObjectName("aliasBox")
        self.gridlayout6.addWidget(self.aliasBox,1,0,1,3)

        self.baseBox = QtGui.QCheckBox(self.WStackPage3)
        self.baseBox.setObjectName("baseBox")
        self.gridlayout6.addWidget(self.baseBox,2,0,1,3)

        self.baseDNView = QtGui.QListWidget(self.WStackPage3)
        self.baseDNView.setObjectName("baseDNView")
        self.gridlayout6.addWidget(self.baseDNView,3,1,1,2)

        spacerItem7 = QtGui.QSpacerItem(176,21,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem7,4,1,1,1)

        spacerItem8 = QtGui.QSpacerItem(16,21,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem8,3,0,1,1)

        spacerItem9 = QtGui.QSpacerItem(21,51,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout6.addItem(spacerItem9,5,2,1,1)

        self.manageBaseButton = QtGui.QPushButton(self.WStackPage3)
        self.manageBaseButton.setAutoDefault(False)
        self.manageBaseButton.setObjectName("manageBaseButton")
        self.gridlayout6.addWidget(self.manageBaseButton,4,2,1,1)
        self.configStack.addWidget(self.WStackPage3)

        self.WStackPage4 = QtGui.QWidget()
        self.WStackPage4.setObjectName("WStackPage4")
        self.configStack.addWidget(self.WStackPage4)
        self.vboxlayout1.addWidget(self.configStack)
        self.vboxlayout.addWidget(self.splitter2)

        self.line1 = QtGui.QFrame(ImprovedServerDialogDesign)
        self.line1.setFrameShape(QtGui.QFrame.HLine)
        self.line1.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1.setObjectName("line1")
        self.vboxlayout.addWidget(self.line1)

        self.hboxlayout7 = QtGui.QHBoxLayout()
        self.hboxlayout7.setObjectName("hboxlayout7")

        spacerItem10 = QtGui.QSpacerItem(363,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout7.addItem(spacerItem10)

        self.okButton = QtGui.QPushButton(ImprovedServerDialogDesign)
        self.okButton.setAutoDefault(False)
        self.okButton.setObjectName("okButton")
        self.hboxlayout7.addWidget(self.okButton)

        self.saveButton = QtGui.QPushButton(ImprovedServerDialogDesign)
        self.saveButton.setAutoDefault(False)
        self.saveButton.setObjectName("saveButton")
        self.hboxlayout7.addWidget(self.saveButton)

        self.cancelButton = QtGui.QPushButton(ImprovedServerDialogDesign)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout7.addWidget(self.cancelButton)
        self.vboxlayout.addLayout(self.hboxlayout7)

        self.retranslateUi(ImprovedServerDialogDesign)
        self.configStack.setCurrentIndex(3)
        QtCore.QObject.connect(self.pushButton6,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.showSummary)
        QtCore.QObject.connect(self.pushButton7,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.showSummary)
        QtCore.QObject.connect(self.pushButton9,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.showSummary)
        QtCore.QObject.connect(self.pushButton10_2,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.showSummary)
        QtCore.QObject.connect(self.serverListView,QtCore.SIGNAL("itemSelectionChanged()"),ImprovedServerDialogDesign.serverSelected)
        QtCore.QObject.connect(self.renameButton,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.renameServer)
        QtCore.QObject.connect(self.renameOkButton,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.saveRename)
        QtCore.QObject.connect(self.renameEdit,QtCore.SIGNAL("returnPressed()"),ImprovedServerDialogDesign.saveRename)
        QtCore.QObject.connect(self.cancelRenameButton,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.cancelRename)
        QtCore.QObject.connect(self.hostnameEdit,QtCore.SIGNAL("textChanged(QString)"),ImprovedServerDialogDesign.hostnameChanged)
        QtCore.QObject.connect(self.portBox,QtCore.SIGNAL("valueChanged(int)"),ImprovedServerDialogDesign.portChanged)
        QtCore.QObject.connect(self.encryptionBox,QtCore.SIGNAL("activated(int)"),ImprovedServerDialogDesign.encryptionChanged)
        QtCore.QObject.connect(self.editCertButton,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.showCertWidget)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.reject)
        QtCore.QObject.connect(self.saveButton,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.saveSettings)
        QtCore.QObject.connect(self.okButton,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.saveCloseDialog)
        QtCore.QObject.connect(self.anonBindBox,QtCore.SIGNAL("toggled(bool)"),ImprovedServerDialogDesign.anonBindChanged)
        QtCore.QObject.connect(self.authentificationBox,QtCore.SIGNAL("activated(QString)"),ImprovedServerDialogDesign.authMethodChanged)
        QtCore.QObject.connect(self.aliasBox,QtCore.SIGNAL("toggled(bool)"),ImprovedServerDialogDesign.aliasChanged)
        QtCore.QObject.connect(self.baseBox,QtCore.SIGNAL("toggled(bool)"),ImprovedServerDialogDesign.autoBaseChanged)
        QtCore.QObject.connect(self.manageBaseButton,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.showBaseDialog)
        QtCore.QObject.connect(self.serverCertBox,QtCore.SIGNAL("activated(int)"),ImprovedServerDialogDesign.serverCertCheckChanged)
        QtCore.QObject.connect(self.clientCertBox,QtCore.SIGNAL("toggled(bool)"),ImprovedServerDialogDesign.clientCertsChanged)
        QtCore.QObject.connect(self.certFileEdit,QtCore.SIGNAL("textChanged(QString)"),ImprovedServerDialogDesign.certFileChanged)
        QtCore.QObject.connect(self.certKeyFileEdit,QtCore.SIGNAL("textChanged(QString)"),ImprovedServerDialogDesign.certKeyFileChanged)
        QtCore.QObject.connect(self.certFileButton,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.showCertFileDialog)
        QtCore.QObject.connect(self.certKeyFileButton,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.showCertKeyFileDialog)
        QtCore.QObject.connect(self.bindAsEdit,QtCore.SIGNAL("textChanged(QString)"),ImprovedServerDialogDesign.bindAsChanged)
        QtCore.QObject.connect(self.bindPasswordEdit,QtCore.SIGNAL("textChanged(QString)"),ImprovedServerDialogDesign.bindPasswordChanged)
        QtCore.QObject.connect(self.addServerButton,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.addServer)
        QtCore.QObject.connect(self.deleteServerButton,QtCore.SIGNAL("clicked()"),ImprovedServerDialogDesign.deleteServer)
        QtCore.QMetaObject.connectSlotsByName(ImprovedServerDialogDesign)

    def retranslateUi(self, ImprovedServerDialogDesign):
        ImprovedServerDialogDesign.setWindowTitle(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Server settings", None, QtGui.QApplication.UnicodeUTF8))
        self.addServerButton.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Add...", None, QtGui.QApplication.UnicodeUTF8))
        self.serverListView.headerItem().setText(0,QtGui.QApplication.translate("ImprovedServerDialogDesign", "Serverlist", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteServerButton.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.serverLabel.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "<b>No server selected</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.renameButton.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "&Rename", None, QtGui.QApplication.UnicodeUTF8))
        self.renameButton.setShortcut(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Alt+R", None, QtGui.QApplication.UnicodeUTF8))
        self.renameOkButton.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelRenameButton.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel5.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Server address:", None, QtGui.QApplication.UnicodeUTF8))
        self.networkLabel.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Not configured yet", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel7.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Bind as:", None, QtGui.QApplication.UnicodeUTF8))
        self.credentialLabel.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Not configured yet", None, QtGui.QApplication.UnicodeUTF8))
        self.encryptionLabel.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Not configured yet", None, QtGui.QApplication.UnicodeUTF8))
        self.authLabel.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Not configured yet", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel10.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Encryption:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel12.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Authentification:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel16.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "BaseDN:", None, QtGui.QApplication.UnicodeUTF8))
        self.ldapOptLabel.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Not configured yet", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel3.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel2.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Hostname:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel4.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "<b>Network options</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton6.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "&Summary", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton6.setShortcut(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Alt+S", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel5_2.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Encryption:", None, QtGui.QApplication.UnicodeUTF8))
        self.encryptionBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "No encryption", None, QtGui.QApplication.UnicodeUTF8))
        self.encryptionBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "TLS (Transport Layer Security)", None, QtGui.QApplication.UnicodeUTF8))
        self.encryptionBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "SSL (Secure Socket Layer)", None, QtGui.QApplication.UnicodeUTF8))
        self.editCertButton.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Certificate options", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "<b>Authentification</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton7.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "&Summary", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton7.setShortcut(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Alt+S", None, QtGui.QApplication.UnicodeUTF8))
        self.anonBindBox.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Anonymous bind", None, QtGui.QApplication.UnicodeUTF8))
        self.bindAsLabel.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Bind as:", None, QtGui.QApplication.UnicodeUTF8))
        self.authentificationBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Simple", None, QtGui.QApplication.UnicodeUTF8))
        self.authentificationBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "SASL CRAM-MD5", None, QtGui.QApplication.UnicodeUTF8))
        self.authentificationBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "SASL DIGEST-MD5", None, QtGui.QApplication.UnicodeUTF8))
        self.authentificationBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "SASL EXTERNAL", None, QtGui.QApplication.UnicodeUTF8))
        self.authentificationBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "SASL GSSAPI", None, QtGui.QApplication.UnicodeUTF8))
        self.authentificationBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "SASL Login", None, QtGui.QApplication.UnicodeUTF8))
        self.authentificationBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "SASL Plain", None, QtGui.QApplication.UnicodeUTF8))
        self.bindPasswordLabel.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.authMechanismLabel.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Mechanism:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel7_2.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "<b>Certificate options</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton9.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "&Summary", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton9.setShortcut(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Alt+S", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel8_2.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Validate server:", None, QtGui.QApplication.UnicodeUTF8))
        self.serverCertBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "never", None, QtGui.QApplication.UnicodeUTF8))
        self.serverCertBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "try", None, QtGui.QApplication.UnicodeUTF8))
        self.serverCertBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "allow", None, QtGui.QApplication.UnicodeUTF8))
        self.serverCertBox.addItem(QtGui.QApplication.translate("ImprovedServerDialogDesign", "demand", None, QtGui.QApplication.UnicodeUTF8))
        self.certFileButton.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.certKeyFileButton.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.certLabel.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Certificate file:", None, QtGui.QApplication.UnicodeUTF8))
        self.clientCertBox.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Use client certificates", None, QtGui.QApplication.UnicodeUTF8))
        self.certKeyLabel.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Certificate keyfile:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel9.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "<b>LDAP options</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton10_2.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "&Summary", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton10_2.setShortcut(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Alt+S", None, QtGui.QApplication.UnicodeUTF8))
        self.aliasBox.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Follow aliases", None, QtGui.QApplication.UnicodeUTF8))
        self.baseBox.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Use Base DNs provided by the server", None, QtGui.QApplication.UnicodeUTF8))
        self.manageBaseButton.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Edit BaseDN list", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setShortcut(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Alt+O", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "S&ave", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setShortcut(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Alt+A", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("ImprovedServerDialogDesign", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setShortcut(QtGui.QApplication.translate("ImprovedServerDialogDesign", "Alt+C", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ImprovedServerDialogDesign = QtGui.QDialog()
    ui = Ui_ImprovedServerDialogDesign()
    ui.setupUi(ImprovedServerDialogDesign)
    ImprovedServerDialogDesign.show()
    sys.exit(app.exec_())
