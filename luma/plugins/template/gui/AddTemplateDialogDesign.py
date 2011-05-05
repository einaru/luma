# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Skole\it2901\resources\forms\plugins\template\AddTemplateDialogDesign.ui'
#
# Created: Thu May 05 14:43:18 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AddTemplateDialog(object):
    def setupUi(self, AddTemplateDialog):
        AddTemplateDialog.setObjectName(_fromUtf8("AddTemplateDialog"))
        AddTemplateDialog.resize(500, 300)
        self.gridLayout = QtGui.QGridLayout(AddTemplateDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEditDescription = QtGui.QLineEdit(AddTemplateDialog)
        self.lineEditDescription.setObjectName(_fromUtf8("lineEditDescription"))
        self.gridLayout.addWidget(self.lineEditDescription, 5, 2, 1, 3)
        self.pushButtonOk = QtGui.QPushButton(AddTemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonOk.sizePolicy().hasHeightForWidth())
        self.pushButtonOk.setSizePolicy(sizePolicy)
        self.pushButtonOk.setObjectName(_fromUtf8("pushButtonOk"))
        self.gridLayout.addWidget(self.pushButtonOk, 8, 3, 1, 1)
        self.pushButtonCancel = QtGui.QPushButton(AddTemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonCancel.sizePolicy().hasHeightForWidth())
        self.pushButtonCancel.setSizePolicy(sizePolicy)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.gridLayout.addWidget(self.pushButtonCancel, 8, 4, 1, 1)
        self.lineEditTemplateName = QtGui.QLineEdit(AddTemplateDialog)
        self.lineEditTemplateName.setObjectName(_fromUtf8("lineEditTemplateName"))
        self.gridLayout.addWidget(self.lineEditTemplateName, 2, 2, 1, 3)
        self.labelMain = QtGui.QLabel(AddTemplateDialog)
        self.labelMain.setWordWrap(True)
        self.labelMain.setObjectName(_fromUtf8("labelMain"))
        self.gridLayout.addWidget(self.labelMain, 0, 2, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 1, 1, 4)
        self.line = QtGui.QFrame(AddTemplateDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 1, 1, 4)
        self.line_2 = QtGui.QFrame(AddTemplateDialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 7, 1, 1, 4)
        self.labelMainIcon = QtGui.QLabel(AddTemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMainIcon.sizePolicy().hasHeightForWidth())
        self.labelMainIcon.setSizePolicy(sizePolicy)
        self.labelMainIcon.setMinimumSize(QtCore.QSize(64, 64))
        self.labelMainIcon.setText(_fromUtf8(""))
        self.labelMainIcon.setObjectName(_fromUtf8("labelMainIcon"))
        self.gridLayout.addWidget(self.labelMainIcon, 0, 1, 1, 1)
        self.labelTemplateName = QtGui.QLabel(AddTemplateDialog)
        self.labelTemplateName.setObjectName(_fromUtf8("labelTemplateName"))
        self.gridLayout.addWidget(self.labelTemplateName, 2, 1, 1, 1)
        self.labelServer = QtGui.QLabel(AddTemplateDialog)
        self.labelServer.setObjectName(_fromUtf8("labelServer"))
        self.gridLayout.addWidget(self.labelServer, 4, 1, 1, 1)
        self.labelDescription = QtGui.QLabel(AddTemplateDialog)
        self.labelDescription.setObjectName(_fromUtf8("labelDescription"))
        self.gridLayout.addWidget(self.labelDescription, 5, 1, 1, 1)
        self.comboBoxServer = QtGui.QComboBox(AddTemplateDialog)
        self.comboBoxServer.setObjectName(_fromUtf8("comboBoxServer"))
        self.gridLayout.addWidget(self.comboBoxServer, 4, 2, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 8, 1, 1, 2)

        self.retranslateUi(AddTemplateDialog)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), AddTemplateDialog.reject)
        QtCore.QObject.connect(self.pushButtonOk, QtCore.SIGNAL(_fromUtf8("clicked()")), AddTemplateDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AddTemplateDialog)
        AddTemplateDialog.setTabOrder(self.lineEditTemplateName, self.comboBoxServer)
        AddTemplateDialog.setTabOrder(self.comboBoxServer, self.lineEditDescription)
        AddTemplateDialog.setTabOrder(self.lineEditDescription, self.pushButtonOk)
        AddTemplateDialog.setTabOrder(self.pushButtonOk, self.pushButtonCancel)

    def retranslateUi(self, AddTemplateDialog):
        AddTemplateDialog.setWindowTitle(QtGui.QApplication.translate("AddTemplateDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOk.setText(QtGui.QApplication.translate("AddTemplateDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel.setText(QtGui.QApplication.translate("AddTemplateDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditTemplateName.setToolTip(QtGui.QApplication.translate("AddTemplateDialog", "Name for template", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMain.setText(QtGui.QApplication.translate("AddTemplateDialog", "Please choose a template name, a description and a server with which the template is associated.", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTemplateName.setText(QtGui.QApplication.translate("AddTemplateDialog", "Template name:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelServer.setText(QtGui.QApplication.translate("AddTemplateDialog", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDescription.setText(QtGui.QApplication.translate("AddTemplateDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxServer.setToolTip(QtGui.QApplication.translate("AddTemplateDialog", "Choose a server", None, QtGui.QApplication.UnicodeUTF8))

