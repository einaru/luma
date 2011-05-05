# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/debris/devel/git/luma/resources/forms/AboutLicenseDesign.ui'
#
# Created: Thu May  5 14:01:57 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AboutLicense(object):
    def setupUi(self, AboutLicense):
        AboutLicense.setObjectName(_fromUtf8("AboutLicense"))
        AboutLicense.setWindowModality(QtCore.Qt.WindowModal)
        AboutLicense.resize(407, 276)
        self.gridLayout = QtGui.QGridLayout(AboutLicense)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textBrowser = QtGui.QTextBrowser(AboutLicense)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setOpenLinks(True)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.actionCloseLicense = QtGui.QPushButton(AboutLicense)
        self.actionCloseLicense.setObjectName(_fromUtf8("actionCloseLicense"))
        self.horizontalLayout.addWidget(self.actionCloseLicense)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(AboutLicense)
        QtCore.QObject.connect(self.actionCloseLicense, QtCore.SIGNAL(_fromUtf8("clicked()")), AboutLicense.close)
        QtCore.QMetaObject.connectSlotsByName(AboutLicense)

    def retranslateUi(self, AboutLicense):
        AboutLicense.setWindowTitle(QtGui.QApplication.translate("AboutLicense", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("AboutLicense", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Luma is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version. </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Luma is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You should have received a copy of the GNU General Public License along with Luma; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA, or visit <a href=\"http://www.gnu.org/licenses/gpl-2.0.html\"><span style=\" text-decoration: underline; color:#0000ff;\">www.gnu.org/licenses/gpl-2.0</span></a>.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCloseLicense.setText(QtGui.QApplication.translate("AboutLicense", "&Close", None, QtGui.QApplication.UnicodeUTF8))

