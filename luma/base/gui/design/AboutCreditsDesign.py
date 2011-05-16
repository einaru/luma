# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/einar/Desktop/luma-merging/resources/forms/AboutCreditsDesign.ui'
#
# Created: Mon May 16 02:47:11 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AboutCredits(object):
    def setupUi(self, AboutCredits):
        AboutCredits.setObjectName(_fromUtf8("AboutCredits"))
        AboutCredits.setWindowModality(QtCore.Qt.WindowModal)
        AboutCredits.resize(401, 301)
        self.gridLayout = QtGui.QGridLayout(AboutCredits)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(AboutCredits)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabAuthors = QtGui.QWidget()
        self.tabAuthors.setObjectName(_fromUtf8("tabAuthors"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabAuthors)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.textAuthors = QtGui.QTextBrowser(self.tabAuthors)
        self.textAuthors.setOpenExternalLinks(True)
        self.textAuthors.setObjectName(_fromUtf8("textAuthors"))
        self.gridLayout_3.addWidget(self.textAuthors, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabAuthors, _fromUtf8(""))
        self.tabTranselators = QtGui.QWidget()
        self.tabTranselators.setObjectName(_fromUtf8("tabTranselators"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabTranselators)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.textTranselators = QtGui.QTextBrowser(self.tabTranselators)
        self.textTranselators.setOpenExternalLinks(True)
        self.textTranselators.setObjectName(_fromUtf8("textTranselators"))
        self.gridLayout_2.addWidget(self.textTranselators, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabTranselators, _fromUtf8(""))
        self.tabCredits = QtGui.QWidget()
        self.tabCredits.setObjectName(_fromUtf8("tabCredits"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tabCredits)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.textCredits = QtGui.QTextBrowser(self.tabCredits)
        self.textCredits.setOpenExternalLinks(True)
        self.textCredits.setObjectName(_fromUtf8("textCredits"))
        self.gridLayout_4.addWidget(self.textCredits, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabCredits, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.closeButton = QtGui.QPushButton(AboutCredits)
        self.closeButton.setDefault(True)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.hboxlayout.addWidget(self.closeButton)
        self.gridLayout.addLayout(self.hboxlayout, 1, 0, 1, 1)

        self.retranslateUi(AboutCredits)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), AboutCredits.close)
        QtCore.QMetaObject.connectSlotsByName(AboutCredits)

    def retranslateUi(self, AboutCredits):
        AboutCredits.setWindowTitle(QtGui.QApplication.translate("AboutCredits", "Credits", None, QtGui.QApplication.UnicodeUTF8))
        self.textAuthors.setHtml(QtGui.QApplication.translate("AboutCredits", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Wido Depping &lt;<a href=\"mailto:widod@users.sourceforge.net\"><span style=\" text-decoration: underline; color:#0000ff;\">widod@users.sourceforge.net</span></a>&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Bjørn Ove Grøtan</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Vegar Westerlund</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Johannes Harestad</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Sondre Frisvold</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Christian Forfang</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Per Ove RIngdal</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Einar Uvsløkk &lt;<a href=\"mailto:einaru@stud.ntnu.no\"><span style=\" text-decoration: underline; color:#0000ff;\">einar.uvslokk@gmail.com</span></a>&gt;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Simen Natvig &lt;<a href=\"mailto:simenna@stud.ntnu.no\"><span style=\" text-decoration: underline; color:#0000ff;\">simen.natvig@gmail.com</span></a>&gt;</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAuthors), QtGui.QApplication.translate("AboutCredits", "Developers", None, QtGui.QApplication.UnicodeUTF8))
        self.textTranselators.setHtml(QtGui.QApplication.translate("AboutCredits", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Norwegian translation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Bjørn Ove Grøtan &lt;<a href=\"mailto:bgrotan@grotan.com\"><span style=\" text-decoration: underline; color:#0000ff;\">bgrotan@grotan.com</span></a>&gt;</p>\n"
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
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Florens Daignière &lt;<a href=\"mailto:nextgens@freenetproject.org\"><span style=\" text-decoration: underline; color:#0000ff;\">nextgens@freenetproject.org</span></a>&gt;</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
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
        self.closeButton.setText(QtGui.QApplication.translate("AboutCredits", "&Close", None, QtGui.QApplication.UnicodeUTF8))

