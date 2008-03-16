# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lib/luma/base/gui/PluginLoaderGuiDesign.ui'
#
# Created: Sat Mar 15 19:22:47 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PluginLoaderGuiDesign(object):
    def setupUi(self, PluginLoaderGuiDesign):
        PluginLoaderGuiDesign.setObjectName("PluginLoaderGuiDesign")
        PluginLoaderGuiDesign.resize(QtCore.QSize(QtCore.QRect(0,0,600,496).size()).expandedTo(PluginLoaderGuiDesign.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PluginLoaderGuiDesign)
        self.vboxlayout.setObjectName("vboxlayout")

        self.textLabel1 = QtGui.QLabel(PluginLoaderGuiDesign)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel1.sizePolicy().hasHeightForWidth())
        self.textLabel1.setSizePolicy(sizePolicy)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName("textLabel1")
        self.vboxlayout.addWidget(self.textLabel1)

        self.line1 = QtGui.QFrame(PluginLoaderGuiDesign)
        self.line1.setFrameShape(QtGui.QFrame.HLine)
        self.line1.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1.setObjectName("line1")
        self.vboxlayout.addWidget(self.line1)

        self.splitter2 = QtGui.QSplitter(PluginLoaderGuiDesign)
        self.splitter2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter2.setObjectName("splitter2")

        self.chooserView = QtGui.QListWidget(self.splitter2)
        self.chooserView.setMaximumSize(QtCore.QSize(200,32767))
        self.chooserView.setObjectName("chooserView")

        self.settingsBox = QtGui.QGroupBox(self.splitter2)
        self.settingsBox.setObjectName("settingsBox")

        self.gridlayout = QtGui.QGridLayout(self.settingsBox)
        self.gridlayout.setObjectName("gridlayout")

        self.settingsStack = QtGui.QStackedWidget(self.settingsBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsStack.sizePolicy().hasHeightForWidth())
        self.settingsStack.setSizePolicy(sizePolicy)
        self.settingsStack.setObjectName("settingsStack")

        self.WStackPage = QtGui.QWidget()
        self.WStackPage.setGeometry(QtCore.QRect(0,0,358,364))
        self.WStackPage.setObjectName("WStackPage")
        self.settingsStack.addWidget(self.WStackPage)
        self.gridlayout.addWidget(self.settingsStack,0,0,1,1)
        self.vboxlayout.addWidget(self.splitter2)

        self.line2 = QtGui.QFrame(PluginLoaderGuiDesign)
        self.line2.setFrameShape(QtGui.QFrame.HLine)
        self.line2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line2.setObjectName("line2")
        self.vboxlayout.addWidget(self.line2)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(458,21,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.closeButton = QtGui.QPushButton(PluginLoaderGuiDesign)
        self.closeButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.closeButton.setAutoDefault(False)
        self.closeButton.setObjectName("closeButton")
        self.hboxlayout.addWidget(self.closeButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(PluginLoaderGuiDesign)
        QtCore.QObject.connect(self.closeButton,QtCore.SIGNAL("clicked()"),PluginLoaderGuiDesign.saveValues)
        QtCore.QObject.connect(self.chooserView,QtCore.SIGNAL("selectionChanged(Q3ListViewItem*)"),PluginLoaderGuiDesign.pluginSelected)
        QtCore.QMetaObject.connectSlotsByName(PluginLoaderGuiDesign)
        PluginLoaderGuiDesign.setTabOrder(self.chooserView,self.closeButton)

    def retranslateUi(self, PluginLoaderGuiDesign):
        PluginLoaderGuiDesign.setWindowTitle(QtGui.QApplication.translate("PluginLoaderGuiDesign", "Plugin Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setText(QtGui.QApplication.translate("PluginLoaderGuiDesign", "Available Plugins:", None, QtGui.QApplication.UnicodeUTF8))
        self.settingsBox.setTitle(QtGui.QApplication.translate("PluginLoaderGuiDesign", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("PluginLoaderGuiDesign", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setShortcut(QtGui.QApplication.translate("PluginLoaderGuiDesign", "Alt+C", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PluginLoaderGuiDesign = QtGui.QDialog()
    ui = Ui_PluginLoaderGuiDesign()
    ui.setupUi(PluginLoaderGuiDesign)
    PluginLoaderGuiDesign.show()
    sys.exit(app.exec_())
