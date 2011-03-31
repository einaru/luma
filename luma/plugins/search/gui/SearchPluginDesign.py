# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Dropbox\Git\it2901\resources\forms\plugins\search\SearchPluginDesign.ui'
#
# Created: Fri Apr 01 18:24:08 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SearchPlugin(object):
    def setupUi(self, SearchPlugin):
        SearchPlugin.setObjectName(_fromUtf8("SearchPlugin"))
        SearchPlugin.resize(377, 305)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SearchPlugin.sizePolicy().hasHeightForWidth())
        SearchPlugin.setSizePolicy(sizePolicy)
        SearchPlugin.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontalLayout = QtGui.QHBoxLayout(SearchPlugin)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(SearchPlugin)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.left = QtGui.QTabWidget(self.splitter)
        self.left.setMinimumSize(QtCore.QSize(0, 0))
        self.left.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.left.setTabPosition(QtGui.QTabWidget.South)
        self.left.setObjectName(_fromUtf8("left"))
        self.right = QtGui.QTabWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.right.sizePolicy().hasHeightForWidth())
        self.right.setSizePolicy(sizePolicy)
        self.right.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.right.setTabsClosable(True)
        self.right.setMovable(True)
        self.right.setObjectName(_fromUtf8("right"))
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi(SearchPlugin)
        self.left.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(SearchPlugin)

    def retranslateUi(self, SearchPlugin):
        SearchPlugin.setWindowTitle(QtGui.QApplication.translate("SearchPlugin", "Search", None, QtGui.QApplication.UnicodeUTF8))

