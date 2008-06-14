# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/luma/base/gui/BaseSelectorDesign.ui'
#
# Created: Sat Jun 14 20:54:19 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_BaseSelectorDesign(object):
    def setupUi(self, BaseSelectorDesign):
        BaseSelectorDesign.setObjectName("BaseSelectorDesign")
        BaseSelectorDesign.resize(QtCore.QSize(QtCore.QRect(0,0,502,456).size()).expandedTo(BaseSelectorDesign.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(BaseSelectorDesign)
        self.vboxlayout.setObjectName("vboxlayout")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")

        self.baseLabel = QtGui.QLabel(BaseSelectorDesign)
        self.baseLabel.setAlignment(QtCore.Qt.AlignVCenter)
        self.baseLabel.setWordWrap(True)
        self.baseLabel.setObjectName("baseLabel")
        self.gridlayout.addWidget(self.baseLabel,0,1,1,1)

        self.pixmapLabel1 = QtGui.QLabel(BaseSelectorDesign)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pixmapLabel1.sizePolicy().hasHeightForWidth())
        self.pixmapLabel1.setSizePolicy(sizePolicy)
        self.pixmapLabel1.setScaledContents(True)
        self.pixmapLabel1.setWordWrap(False)
        self.pixmapLabel1.setObjectName("pixmapLabel1")
        self.gridlayout.addWidget(self.pixmapLabel1,0,0,1,1)

        self.line2 = QtGui.QFrame(BaseSelectorDesign)
        self.line2.setFrameShape(QtGui.QFrame.HLine)
        self.line2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line2.setObjectName("line2")
        self.gridlayout.addWidget(self.line2,1,0,1,2)
        self.vboxlayout.addLayout(self.gridlayout)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(21,150,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem,3,2,1,1)

        self.textLabel2 = QtGui.QLabel(BaseSelectorDesign)
        self.textLabel2.setWordWrap(False)
        self.textLabel2.setObjectName("textLabel2")
        self.gridlayout1.addWidget(self.textLabel2,0,0,1,1)

        self.deleteButton = QtGui.QPushButton(BaseSelectorDesign)
        self.deleteButton.setObjectName("deleteButton")
        self.gridlayout1.addWidget(self.deleteButton,1,2,1,1)

        self.baseView = QtGui.QListWidget(BaseSelectorDesign)
        self.baseView.setObjectName("baseView")
        self.gridlayout1.addWidget(self.baseView,1,0,3,2)

        self.baseEdit = QtGui.QLineEdit(BaseSelectorDesign)
        self.baseEdit.setObjectName("baseEdit")
        self.gridlayout1.addWidget(self.baseEdit,0,1,1,1)

        self.addButton = QtGui.QPushButton(BaseSelectorDesign)
        self.addButton.setObjectName("addButton")
        self.gridlayout1.addWidget(self.addButton,0,2,1,1)

        self.updateButton = QtGui.QPushButton(BaseSelectorDesign)
        self.updateButton.setObjectName("updateButton")
        self.gridlayout1.addWidget(self.updateButton,2,2,1,1)
        self.vboxlayout.addLayout(self.gridlayout1)

        self.gridlayout2 = QtGui.QGridLayout()
        self.gridlayout2.setObjectName("gridlayout2")

        self.line3 = QtGui.QFrame(BaseSelectorDesign)
        self.line3.setFrameShape(QtGui.QFrame.HLine)
        self.line3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line3.setObjectName("line3")
        self.gridlayout2.addWidget(self.line3,0,0,1,3)

        spacerItem1 = QtGui.QSpacerItem(391,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem1,1,0,1,1)

        self.cancelButton = QtGui.QPushButton(BaseSelectorDesign)
        self.cancelButton.setDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.gridlayout2.addWidget(self.cancelButton,1,2,1,1)

        self.okButton = QtGui.QPushButton(BaseSelectorDesign)
        self.okButton.setDefault(True)
        self.okButton.setObjectName("okButton")
        self.gridlayout2.addWidget(self.okButton,1,1,1,1)
        self.vboxlayout.addLayout(self.gridlayout2)

        self.retranslateUi(BaseSelectorDesign)
        QtCore.QObject.connect(self.okButton,QtCore.SIGNAL("clicked()"),BaseSelectorDesign.accept)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),BaseSelectorDesign.reject)
        QtCore.QObject.connect(self.addButton,QtCore.SIGNAL("clicked()"),BaseSelectorDesign.addBase)
        QtCore.QObject.connect(self.deleteButton,QtCore.SIGNAL("clicked()"),BaseSelectorDesign.deleteBase)
        QtCore.QObject.connect(self.updateButton,QtCore.SIGNAL("clicked()"),BaseSelectorDesign.addServerBase)
        QtCore.QMetaObject.connectSlotsByName(BaseSelectorDesign)
        BaseSelectorDesign.setTabOrder(self.baseEdit,self.addButton)
        BaseSelectorDesign.setTabOrder(self.addButton,self.baseView)
        BaseSelectorDesign.setTabOrder(self.baseView,self.deleteButton)
        BaseSelectorDesign.setTabOrder(self.deleteButton,self.updateButton)
        BaseSelectorDesign.setTabOrder(self.updateButton,self.okButton)
        BaseSelectorDesign.setTabOrder(self.okButton,self.cancelButton)

    def retranslateUi(self, BaseSelectorDesign):
        BaseSelectorDesign.setWindowTitle(QtGui.QApplication.translate("BaseSelectorDesign", "Select Base DNs", None, QtGui.QApplication.UnicodeUTF8))
        self.baseLabel.setText(QtGui.QApplication.translate("BaseSelectorDesign", "Manage the base distinguished names you want to use with server <b>%1</b>.", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel2.setText(QtGui.QApplication.translate("BaseSelectorDesign", "Custom:", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("BaseSelectorDesign", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setShortcut(QtGui.QApplication.translate("BaseSelectorDesign", "Alt+D", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("BaseSelectorDesign", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setShortcut(QtGui.QApplication.translate("BaseSelectorDesign", "Alt+A", None, QtGui.QApplication.UnicodeUTF8))
        self.updateButton.setText(QtGui.QApplication.translate("BaseSelectorDesign", "&Update from server", None, QtGui.QApplication.UnicodeUTF8))
        self.updateButton.setShortcut(QtGui.QApplication.translate("BaseSelectorDesign", "Alt+U", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("BaseSelectorDesign", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setShortcut(QtGui.QApplication.translate("BaseSelectorDesign", "Alt+C", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("BaseSelectorDesign", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setShortcut(QtGui.QApplication.translate("BaseSelectorDesign", "Alt+O", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    BaseSelectorDesign = QtGui.QDialog()
    ui = Ui_BaseSelectorDesign()
    ui.setupUi(BaseSelectorDesign)
    BaseSelectorDesign.show()
    sys.exit(app.exec_())
