# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/debris/devel/git/luma/resources/forms/plugins/browser_plugin/PasswordEditorDesign.ui'
#
# Created: Wed May 11 13:31:19 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PasswordEditorDesign(object):
    def setupUi(self, PasswordEditorDesign):
        PasswordEditorDesign.setObjectName(_fromUtf8("PasswordEditorDesign"))
        PasswordEditorDesign.resize(441, 257)
        PasswordEditorDesign.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(PasswordEditorDesign)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        spacerItem = QtGui.QSpacerItem(20, 70, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 2, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.asciiBox = QtGui.QCheckBox(PasswordEditorDesign)
        self.asciiBox.setChecked(True)
        self.asciiBox.setObjectName(_fromUtf8("asciiBox"))
        self.hboxlayout.addWidget(self.asciiBox)
        self.hiddenBox = QtGui.QCheckBox(PasswordEditorDesign)
        self.hiddenBox.setObjectName(_fromUtf8("hiddenBox"))
        self.hboxlayout.addWidget(self.hiddenBox)
        self.okButton = QtGui.QPushButton(PasswordEditorDesign)
        self.okButton.setShortcut(_fromUtf8(""))
        self.okButton.setDefault(True)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(PasswordEditorDesign)
        self.cancelButton.setShortcut(_fromUtf8(""))
        self.cancelButton.setAutoDefault(True)
        self.cancelButton.setDefault(False)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.hboxlayout.addWidget(self.cancelButton)
        self.gridlayout.addLayout(self.hboxlayout, 5, 0, 1, 2)
        self.line1 = QtGui.QFrame(PasswordEditorDesign)
        self.line1.setFrameShape(QtGui.QFrame.HLine)
        self.line1.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1.setObjectName(_fromUtf8("line1"))
        self.gridlayout.addWidget(self.line1, 4, 0, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(41, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem2, 3, 1, 1, 1)
        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.textLabel1 = QtGui.QLabel(PasswordEditorDesign)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName(_fromUtf8("textLabel1"))
        self.gridlayout1.addWidget(self.textLabel1, 4, 0, 1, 1)
        self.textLabel3 = QtGui.QLabel(PasswordEditorDesign)
        self.textLabel3.setAlignment(QtCore.Qt.AlignVCenter)
        self.textLabel3.setWordWrap(False)
        self.textLabel3.setObjectName(_fromUtf8("textLabel3"))
        self.gridlayout1.addWidget(self.textLabel3, 1, 0, 1, 1)
        self.passwordSaveEdit = QtGui.QLineEdit(PasswordEditorDesign)
        self.passwordSaveEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordSaveEdit.setObjectName(_fromUtf8("passwordSaveEdit"))
        self.gridlayout1.addWidget(self.passwordSaveEdit, 3, 1, 1, 1)
        self.textLabel4 = QtGui.QLabel(PasswordEditorDesign)
        self.textLabel4.setAlignment(QtCore.Qt.AlignVCenter)
        self.textLabel4.setWordWrap(False)
        self.textLabel4.setObjectName(_fromUtf8("textLabel4"))
        self.gridlayout1.addWidget(self.textLabel4, 2, 0, 1, 1)
        self.textLabel5 = QtGui.QLabel(PasswordEditorDesign)
        self.textLabel5.setWordWrap(False)
        self.textLabel5.setObjectName(_fromUtf8("textLabel5"))
        self.gridlayout1.addWidget(self.textLabel5, 3, 0, 1, 1)
        self.passwordLabel = QtGui.QLabel(PasswordEditorDesign)
        self.passwordLabel.setWordWrap(False)
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.gridlayout1.addWidget(self.passwordLabel, 5, 0, 1, 2)
        self.textLabel2 = QtGui.QLabel(PasswordEditorDesign)
        self.textLabel2.setAlignment(QtCore.Qt.AlignVCenter)
        self.textLabel2.setWordWrap(True)
        self.textLabel2.setObjectName(_fromUtf8("textLabel2"))
        self.gridlayout1.addWidget(self.textLabel2, 0, 0, 1, 2)
        self.passwordEdit = QtGui.QLineEdit(PasswordEditorDesign)
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordEdit.setObjectName(_fromUtf8("passwordEdit"))
        self.gridlayout1.addWidget(self.passwordEdit, 2, 1, 1, 1)
        self.methodBox = QtGui.QComboBox(PasswordEditorDesign)
        self.methodBox.setObjectName(_fromUtf8("methodBox"))
        self.gridlayout1.addWidget(self.methodBox, 1, 1, 1, 1)
        self.progressBar = QtGui.QProgressBar(PasswordEditorDesign)
        self.progressBar.setProperty(_fromUtf8("value"), 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout1.addWidget(self.progressBar, 4, 1, 1, 1)
        self.gridlayout.addLayout(self.gridlayout1, 0, 1, 3, 1)
        self.iconLabel = QtGui.QLabel(PasswordEditorDesign)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconLabel.sizePolicy().hasHeightForWidth())
        self.iconLabel.setSizePolicy(sizePolicy)
        self.iconLabel.setMinimumSize(QtCore.QSize(64, 64))
        self.iconLabel.setWordWrap(False)
        self.iconLabel.setObjectName(_fromUtf8("iconLabel"))
        self.gridlayout.addWidget(self.iconLabel, 1, 0, 1, 1)

        self.retranslateUi(PasswordEditorDesign)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PasswordEditorDesign.accept)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PasswordEditorDesign.reject)
        QtCore.QObject.connect(self.passwordEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), PasswordEditorDesign.passwordChanged)
        QtCore.QObject.connect(self.passwordSaveEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), PasswordEditorDesign.passwordChanged)
        QtCore.QMetaObject.connectSlotsByName(PasswordEditorDesign)
        PasswordEditorDesign.setTabOrder(self.methodBox, self.passwordEdit)
        PasswordEditorDesign.setTabOrder(self.passwordEdit, self.passwordSaveEdit)
        PasswordEditorDesign.setTabOrder(self.passwordSaveEdit, self.okButton)
        PasswordEditorDesign.setTabOrder(self.okButton, self.cancelButton)

    def retranslateUi(self, PasswordEditorDesign):
        PasswordEditorDesign.setWindowTitle(QtGui.QApplication.translate("PasswordEditorDesign", "New password", None, QtGui.QApplication.UnicodeUTF8))
        self.asciiBox.setText(QtGui.QApplication.translate("PasswordEditorDesign", "Ascii characters", None, QtGui.QApplication.UnicodeUTF8))
        self.hiddenBox.setText(QtGui.QApplication.translate("PasswordEditorDesign", "Hidden string", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("PasswordEditorDesign", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("PasswordEditorDesign", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setText(QtGui.QApplication.translate("PasswordEditorDesign", "Strength:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel3.setText(QtGui.QApplication.translate("PasswordEditorDesign", "Hash algorithm:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel4.setText(QtGui.QApplication.translate("PasswordEditorDesign", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel5.setText(QtGui.QApplication.translate("PasswordEditorDesign", "Verify:", None, QtGui.QApplication.UnicodeUTF8))
        self.passwordLabel.setText(QtGui.QApplication.translate("PasswordEditorDesign", "Passwords do not match", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel2.setText(QtGui.QApplication.translate("PasswordEditorDesign", "<b>Please enter a new password.</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.iconLabel.setText(QtGui.QApplication.translate("PasswordEditorDesign", "PW", "DO NOT TRANSLATE", QtGui.QApplication.UnicodeUTF8))

