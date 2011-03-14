# -*- coding: utf-8 -*-

<<<<<<< HEAD
# Form implementation generated from reading ui file '/mnt/debris/devel/git/luma/src/lib/luma/resources/forms/AboutDialogDesign.ui'
#
# Created: Fri Feb 25 12:12:02 2011
=======
# Form implementation generated from reading ui file '/mnt/debris/devel/git/luma-playground/resources/forms/AboutDialogDesign.ui'
#
# Created: Mon Mar 14 13:16:09 2011
>>>>>>> S3-installation-v2
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.setWindowModality(QtCore.Qt.WindowModal)
        AboutDialog.setEnabled(True)
        AboutDialog.resize(332, 245)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutDialog.sizePolicy().hasHeightForWidth())
        AboutDialog.setSizePolicy(sizePolicy)
        AboutDialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        AboutDialog.setSizeGripEnabled(False)
        AboutDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(AboutDialog)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout.setObjectName("gridLayout")
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.aboutCredits = QtGui.QPushButton(AboutDialog)
        self.aboutCredits.setAutoDefault(True)
        self.aboutCredits.setObjectName("aboutCredits")
        self.hboxlayout.addWidget(self.aboutCredits)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.aboutLicense = QtGui.QPushButton(AboutDialog)
        self.aboutLicense.setAutoDefault(True)
        self.aboutLicense.setDefault(False)
        self.aboutLicense.setObjectName("aboutLicense")
        self.hboxlayout.addWidget(self.aboutLicense)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.aboutClose = QtGui.QPushButton(AboutDialog)
        self.aboutClose.setAutoDefault(True)
        self.aboutClose.setDefault(True)
        self.aboutClose.setObjectName("aboutClose")
        self.hboxlayout.addWidget(self.aboutClose)
        self.gridLayout.addLayout(self.hboxlayout, 6, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
<<<<<<< HEAD
        self.label = QtGui.QLabel(AboutDialog)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../../../../../../../../../home/einar/devel/workspace/Luma24/share/luma/icons/luma-64.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
=======
        self.labelLogo = QtGui.QLabel(AboutDialog)
        self.labelLogo.setText("None")
        self.labelLogo.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLogo.setObjectName("labelLogo")
        self.verticalLayout_2.addWidget(self.labelLogo)
>>>>>>> S3-installation-v2
        self.labelApplication = QtGui.QLabel(AboutDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelApplication.sizePolicy().hasHeightForWidth())
        self.labelApplication.setSizePolicy(sizePolicy)
        self.labelApplication.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.labelApplication.setObjectName("labelApplication")
        self.verticalLayout_2.addWidget(self.labelApplication)
        self.labelDescription = QtGui.QLabel(AboutDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDescription.sizePolicy().hasHeightForWidth())
        self.labelDescription.setSizePolicy(sizePolicy)
        self.labelDescription.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.labelDescription.setObjectName("labelDescription")
        self.verticalLayout_2.addWidget(self.labelDescription)
        self.labelCopyright = QtGui.QLabel(AboutDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCopyright.sizePolicy().hasHeightForWidth())
        self.labelCopyright.setSizePolicy(sizePolicy)
        self.labelCopyright.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCopyright.setObjectName("labelCopyright")
        self.verticalLayout_2.addWidget(self.labelCopyright)
        self.labelUrl = QtGui.QLabel(AboutDialog)
        self.labelUrl.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.labelUrl.setOpenExternalLinks(True)
        self.labelUrl.setObjectName("labelUrl")
        self.verticalLayout_2.addWidget(self.labelUrl)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 4, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 1)

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.aboutClose, QtCore.SIGNAL("clicked()"), AboutDialog.close)
        QtCore.QObject.connect(self.aboutCredits, QtCore.SIGNAL("clicked()"), AboutDialog.giveCreditWhereCreditIsDue)
        QtCore.QObject.connect(self.aboutLicense, QtCore.SIGNAL("clicked()"), AboutDialog.showLicense)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "About Luma", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutCredits.setText(QtGui.QApplication.translate("AboutDialog", "Credits", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutLicense.setText(QtGui.QApplication.translate("AboutDialog", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutClose.setText(QtGui.QApplication.translate("AboutDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.labelApplication.setText(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">Luma 3.x.x</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDescription.setText(QtGui.QApplication.translate("AboutDialog", "LDAP management made easy", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCopyright.setText(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Copyright © 2003–2005 Wido Depping</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUrl.setText(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://luma.sf.net/\"><span style=\" text-decoration: underline; color:#0000ff;\">Luma Website</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

