# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/debris/devel/git/luma/src/lib/luma/resources/forms/AboutCreditsDesign.ui'
#
# Created: Wed Feb 23 01:42:02 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AboutCredits(object):
    def setupUi(self, AboutCredits):
        AboutCredits.setObjectName("AboutCredits")
        AboutCredits.setWindowModality(QtCore.Qt.WindowModal)
        AboutCredits.resize(401, 301)
        self.gridLayout = QtGui.QGridLayout(AboutCredits)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtGui.QTabWidget(AboutCredits)
        self.tabWidget.setObjectName("tabWidget")
        self.tabAuthors = QtGui.QWidget()
        self.tabAuthors.setObjectName("tabAuthors")
        self.gridLayout_3 = QtGui.QGridLayout(self.tabAuthors)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textAuthors = QtGui.QTextBrowser(self.tabAuthors)
        self.textAuthors.setOpenExternalLinks(True)
        self.textAuthors.setObjectName("textAuthors")
        self.gridLayout_3.addWidget(self.textAuthors, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabAuthors, "")
        self.tabTranselators = QtGui.QWidget()
        self.tabTranselators.setObjectName("tabTranselators")
        self.gridLayout_2 = QtGui.QGridLayout(self.tabTranselators)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textTranselators = QtGui.QTextBrowser(self.tabTranselators)
        self.textTranselators.setOpenExternalLinks(True)
        self.textTranselators.setObjectName("textTranselators")
        self.gridLayout_2.addWidget(self.textTranselators, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabTranselators, "")
        self.tabCredits = QtGui.QWidget()
        self.tabCredits.setObjectName("tabCredits")
        self.gridLayout_4 = QtGui.QGridLayout(self.tabCredits)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textCredits = QtGui.QTextBrowser(self.tabCredits)
        self.textCredits.setOpenExternalLinks(True)
        self.textCredits.setObjectName("textCredits")
        self.gridLayout_4.addWidget(self.textCredits, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabCredits, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.closeButton = QtGui.QPushButton(AboutCredits)
        self.closeButton.setObjectName("closeButton")
        self.hboxlayout.addWidget(self.closeButton)
        self.gridLayout.addLayout(self.hboxlayout, 1, 0, 1, 1)

        self.retranslateUi(AboutCredits)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL("clicked()"), AboutCredits.close)
        QtCore.QMetaObject.connectSlotsByName(AboutCredits)

    def retranslateUi(self, AboutCredits):
        AboutCredits.setWindowTitle(QtGui.QApplication.translate("AboutCredits", "Credits", None, QtGui.QApplication.UnicodeUTF8))
        self.textAuthors.setHtml(QtGui.QApplication.translate("AboutCredits", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Wido Depping &lt;<a href=\"mailto:widod@users.sourceforge.net\"><span style=\" text-decoration: underline; color:#0000ff;\">widod@users.sourceforge.net</span></a>&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Bjørn Ove Grøtan &lt;<a href=\"mailto:bgrotan@grotan.com\"><span style=\" text-decoration: underline; color:#0000ff;\">bgrotan@grotan.com</span></a>&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Vegar Westerlund</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Johannes Harestad &lt;<a href=\"mailto:johannesharestad@gmail.com\"><span style=\" text-decoration: underline; color:#0000ff;\">johannesharestad@gmail.com</span></a>&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Sondre Frisvold &lt;<a href=\"mailto:sondre.frisvold@c2i.net\"><span style=\" text-decoration: underline; color:#0000ff;\">sondre.frisvold@c2i.net</span></a>&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Christian Forfang &lt;<a href=\"mailto:cforfang@gmail.com\"><span style=\" text-decoration: underline; color:#0000ff;\">cforfang@gmail.com</span></a>&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Per Ove RIngdal &lt;<a href=\"mailto:peroveri@stud.ntnu.no\"><span style=\" text-decoration: underline; color:#0000ff;\">peroveri@stud.ntnu.no</span></a>&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Einar Uvsløkk &lt;<a href=\"mailto:einaru@stud.ntnu.no\"><span style=\" text-decoration: underline; color:#0000ff;\">einar.uvslokk@gmail.com</span></a>&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Simen Natvig &lt;<a href=\"mailto:simenna@stud.ntnu.no\"><span style=\" text-decoration: underline; color:#0000ff;\">simen.natvig@gmail.com</span></a>&gt;</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAuthors), QtGui.QApplication.translate("AboutCredits", "Developers", None, QtGui.QApplication.UnicodeUTF8))
        self.textTranselators.setHtml(QtGui.QApplication.translate("AboutCredits", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Norwegian translation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Luma 2.4 : Bjørn Ove Grøtan &lt;<a href=\"mailto:bgrotan@grotan.com\"><span style=\" text-decoration: underline; color:#0000ff;\">bgrotan@grotan.com</span></a>&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Luma 3.0 : Einar Uvsløkk &lt;<a href=\"mailto:einar.uvslokk@linux.com\"><span style=\" text-decoration: underline; color:#0000ff;\">einar.uvslokk@linux.com</span></a>&gt;</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Portuguese translation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Fernando Maciel Souto Maior</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Czech translation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Jirka Jurek &lt;<a href=\"mailto:jiri.jurek@trinet.as\"><span style=\" text-decoration: underline; color:#0000ff;\">jiri.jurek@trinet.as</span></a>&gt;</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Swedish translation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Magnus Määttä</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Russian translation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Alexander Novitsky</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">French translation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Florens Daignière &lt;<a href=\"mailto:nextgens@freenetproject.org\"><span style=\" text-decoration: underline; color:#0000ff;\">nextgens@freenetproject.org</span></a>&gt;</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">h4x0r translation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Einar Uvsløkk &lt;<a href=\"mailto:einar.uvslokk@linux.com\"><span style=\" text-decoration: underline; color:#0000ff;\">einar.uvslokk@linux.com</span></a>&gt;</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTranselators), QtGui.QApplication.translate("AboutCredits", "Translators", None, QtGui.QApplication.UnicodeUTF8))
        self.textCredits.setHtml(QtGui.QApplication.translate("AboutCredits", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Jesse Morgan</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Cleaning up the bugtracker and initiating the qt4-port.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Vegar Westerlund</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">For contributing patches</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                                </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Bjørn Ove Grøtan</span> &lt;<a href=\"mailto:bgrotan@grotan.com\"><span style=\" text-decoration: underline; color:#0000ff;\">bgrotan@grotan.com</span></a>&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Luma Project Admin and Debian Maintainer</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Contributed his mkpasswd module.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Kerstin Isebrecht</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Thanks for the ice and all your patience :) </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Joern Koerner</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Luma-crash-test-dummy. He also had the idea with the plugin support. </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Jan Winhuysen</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">My mentor and UI tester :) </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Eric Cote</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Testing guinea pig for python 2.3</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Rebekka Golombek</span> &lt;<a href=\"mailto:rebekkagolombe@web.de\"><span style=\" text-decoration: underline; color:#0000ff;\">rebekkagolombe@web.de</span></a>&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Luma logo</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCredits), QtGui.QApplication.translate("AboutCredits", "Contributors", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("AboutCredits", "Close", None, QtGui.QApplication.UnicodeUTF8))

