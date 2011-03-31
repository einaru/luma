# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/einar/Desktop/luma-release-tagging/resources/forms/plugins/browser_plugin/DeleteDialogDesign.ui'
#
# Created: Thu Mar 31 18:10:56 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DeleteDialog(object):
    def setupUi(self, DeleteDialog):
        DeleteDialog.setObjectName("DeleteDialog")
        DeleteDialog.resize(499, 469)
        self.gridLayout_2 = QtGui.QGridLayout(DeleteDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.hLayout3 = QtGui.QHBoxLayout()
        self.hLayout3.setObjectName("hLayout3")
        self.iconLabel = QtGui.QLabel(DeleteDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconLabel.sizePolicy().hasHeightForWidth())
        self.iconLabel.setSizePolicy(sizePolicy)
        self.iconLabel.setMinimumSize(QtCore.QSize(64, 64))
        self.iconLabel.setText("")
        self.iconLabel.setPixmap(QtGui.QPixmap(":/icons/delete"))
        self.iconLabel.setObjectName("iconLabel")
        self.hLayout3.addWidget(self.iconLabel)
        self.infoLabel = QtGui.QLabel(DeleteDialog)
        self.infoLabel.setTextFormat(QtCore.Qt.AutoText)
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setObjectName("infoLabel")
        self.hLayout3.addWidget(self.infoLabel)
        self.gridLayout_2.addLayout(self.hLayout3, 0, 0, 1, 1)
        self.hLayout1 = QtGui.QHBoxLayout()
        self.hLayout1.setObjectName("hLayout1")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayout1.addItem(spacerItem)
        self.deleteButton = QtGui.QPushButton(DeleteDialog)
        self.deleteButton.setObjectName("deleteButton")
        self.hLayout1.addWidget(self.deleteButton)
        self.cancelButton = QtGui.QPushButton(DeleteDialog)
        self.cancelButton.setDefault(True)
        self.cancelButton.setObjectName("cancelButton")
        self.hLayout1.addWidget(self.cancelButton)
        self.gridLayout_2.addLayout(self.hLayout1, 3, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(DeleteDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 479, 337))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 1, 1, 1)
        self.messageLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.messageLabel.setText("")
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setObjectName("messageLabel")
        self.gridLayout_3.addWidget(self.messageLabel, 1, 0, 1, 1)
        self.deleteItemView = QtGui.QTreeView(self.scrollAreaWidgetContents)
        self.deleteItemView.setObjectName("deleteItemView")
        self.gridLayout_3.addWidget(self.deleteItemView, 0, 0, 1, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 1, 1)
        self.line = QtGui.QFrame(DeleteDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 2, 0, 1, 1)

        self.retranslateUi(DeleteDialog)
        QtCore.QObject.connect(self.deleteButton, QtCore.SIGNAL("clicked()"), DeleteDialog.delete)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), DeleteDialog.cancel)
        QtCore.QMetaObject.connectSlotsByName(DeleteDialog)
        DeleteDialog.setTabOrder(self.scrollArea, self.cancelButton)
        DeleteDialog.setTabOrder(self.cancelButton, self.deleteButton)

    def retranslateUi(self, DeleteDialog):
        DeleteDialog.setWindowTitle(QtGui.QApplication.translate("DeleteDialog", "Delete items", None, QtGui.QApplication.UnicodeUTF8))
        self.infoLabel.setText(QtGui.QApplication.translate("DeleteDialog", "The following entries will be deleted from the server. You can remove items from the list if you don\'t want them to be deleted. Press start to begin with deletion.", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("DeleteDialog", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("DeleteDialog", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))

