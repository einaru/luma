# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PluginLoaderDesign.ui'
#
# Created: Wed Feb  9 17:17:40 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PluginLoader(object):
    def setupUi(self, PluginLoader):
        PluginLoader.setObjectName(_fromUtf8("PluginLoader"))
        PluginLoader.resize(628, 531)
        self.gridLayout = QtGui.QGridLayout(PluginLoader)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(PluginLoader)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.line = QtGui.QFrame(PluginLoader)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 3, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(PluginLoader)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(12)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.listView = QtGui.QListView(self.splitter)
        self.listView.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listView.setAutoScroll(True)
        self.listView.setAlternatingRowColors(True)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.Settingsbox = QtGui.QGroupBox(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Settingsbox.sizePolicy().hasHeightForWidth())
        self.Settingsbox.setSizePolicy(sizePolicy)
        self.Settingsbox.setSizeIncrement(QtCore.QSize(0, 0))
        self.Settingsbox.setBaseSize(QtCore.QSize(0, 0))
        self.Settingsbox.setObjectName(_fromUtf8("Settingsbox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.Settingsbox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.stackedWidget = QtGui.QStackedWidget(self.Settingsbox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QtCore.QSize(100, 0))
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.page = QtGui.QWidget(self.stackedWidget)
        self.page.setObjectName(_fromUtf8("page"))
        self.stackedWidget.addWidget(self.page)
        self.gridLayout_2.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.splitter)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        self.line_2 = QtGui.QFrame(PluginLoader)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 5, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(PluginLoader)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 0, 1, 1)

        self.retranslateUi(PluginLoader)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("released()")), PluginLoader.closeButton)
        QtCore.QObject.connect(self.listView, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), PluginLoader.pluginSelected)
        QtCore.QObject.connect(PluginLoader, QtCore.SIGNAL(_fromUtf8("finished(int)")), PluginLoader.close)
        QtCore.QMetaObject.connectSlotsByName(PluginLoader)

    def retranslateUi(self, PluginLoader):
        PluginLoader.setWindowTitle(QtGui.QApplication.translate("PluginLoader", "PluginLoader", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PluginLoader", "Available plugins:", None, QtGui.QApplication.UnicodeUTF8))
        self.Settingsbox.setTitle(QtGui.QApplication.translate("PluginLoader", "Settings:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("PluginLoader", "Close", None, QtGui.QApplication.UnicodeUTF8))

