# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/einar/Desktop/luma-release-tagging/resources/forms/AboutPluginDesign.ui'
#
# Created: Thu Mar 31 18:10:54 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AboutPlugin(object):
    def setupUi(self, AboutPlugin):
        AboutPlugin.setObjectName("AboutPlugin")
        AboutPlugin.resize(171, 75)
        self.formLayout = QtGui.QFormLayout(AboutPlugin)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(AboutPlugin)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_name = QtGui.QLabel(AboutPlugin)
        self.label_name.setWordWrap(True)
        self.label_name.setObjectName("label_name")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_name)
        self.label_3 = QtGui.QLabel(AboutPlugin)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_version = QtGui.QLabel(AboutPlugin)
        self.label_version.setWordWrap(True)
        self.label_version.setObjectName("label_version")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_version)
        self.label_5 = QtGui.QLabel(AboutPlugin)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_author = QtGui.QLabel(AboutPlugin)
        self.label_author.setWordWrap(True)
        self.label_author.setObjectName("label_author")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.label_author)

        self.retranslateUi(AboutPlugin)
        QtCore.QMetaObject.connectSlotsByName(AboutPlugin)

    def retranslateUi(self, AboutPlugin):
        AboutPlugin.setWindowTitle(QtGui.QApplication.translate("AboutPlugin", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AboutPlugin", "Plugin name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_name.setText(QtGui.QApplication.translate("AboutPlugin", "\"name\"", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("AboutPlugin", "Version:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_version.setText(QtGui.QApplication.translate("AboutPlugin", "\"version\"", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("AboutPlugin", "Author:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_author.setText(QtGui.QApplication.translate("AboutPlugin", "\"author\"", None, QtGui.QApplication.UnicodeUTF8))

