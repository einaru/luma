# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/gui/PluginLoaderGuiDesign.ui'
#
# Created: Sun Aug 29 00:49:05 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.12
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class PluginLoaderGuiDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("PluginLoaderGuiDesign")


        PluginLoaderGuiDesignLayout = QVBoxLayout(self,11,6,"PluginLoaderGuiDesignLayout")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(5,0,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))
        PluginLoaderGuiDesignLayout.addWidget(self.textLabel1)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)
        PluginLoaderGuiDesignLayout.addWidget(self.line1)

        self.splitter2 = QSplitter(self,"splitter2")
        self.splitter2.setOrientation(QSplitter.Horizontal)

        self.chooserView = QListView(self.splitter2,"chooserView")
        self.chooserView.addColumn(self.__tr("Load"))
        self.chooserView.setMaximumSize(QSize(200,32767))
        self.chooserView.setAllColumnsShowFocus(0)
        self.chooserView.setResizeMode(QListView.AllColumns)

        self.settingsBox = QGroupBox(self.splitter2,"settingsBox")
        self.settingsBox.setColumnLayout(0,Qt.Vertical)
        self.settingsBox.layout().setSpacing(6)
        self.settingsBox.layout().setMargin(11)
        settingsBoxLayout = QGridLayout(self.settingsBox.layout())
        settingsBoxLayout.setAlignment(Qt.AlignTop)

        self.settingsStack = QWidgetStack(self.settingsBox,"settingsStack")
        self.settingsStack.setSizePolicy(QSizePolicy(5,7,0,0,self.settingsStack.sizePolicy().hasHeightForWidth()))

        self.WStackPage = QWidget(self.settingsStack,"WStackPage")
        self.settingsStack.addWidget(self.WStackPage,0)

        settingsBoxLayout.addWidget(self.settingsStack,0,0)
        PluginLoaderGuiDesignLayout.addWidget(self.splitter2)

        self.line2 = QFrame(self,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)
        PluginLoaderGuiDesignLayout.addWidget(self.line2)

        layout1 = QHBoxLayout(None,0,6,"layout1")
        spacer1 = QSpacerItem(458,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout1.addItem(spacer1)

        self.closeButton = QPushButton(self,"closeButton")
        self.closeButton.setFocusPolicy(QPushButton.ClickFocus)
        self.closeButton.setAutoDefault(0)
        layout1.addWidget(self.closeButton)
        PluginLoaderGuiDesignLayout.addLayout(layout1)

        self.languageChange()

        self.resize(QSize(600,496).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.closeButton,SIGNAL("clicked()"),self.saveValues)
        self.connect(self.chooserView,SIGNAL("selectionChanged(QListViewItem*)"),self.pluginSelected)

        self.setTabOrder(self.chooserView,self.closeButton)


    def languageChange(self):
        self.setCaption(self.__tr("Plugin Settings"))
        self.textLabel1.setText(self.__tr("Available Plugins:"))
        self.chooserView.header().setLabel(0,self.__tr("Load"))
        self.settingsBox.setTitle(self.__tr("Settings"))
        self.closeButton.setText(self.__tr("&Close"))
        self.closeButton.setAccel(self.__tr("Alt+C"))


    def saveValues(self):
        print "PluginLoaderGuiDesign.saveValues(): Not implemented yet"

    def pluginSelected(self):
        print "PluginLoaderGuiDesign.pluginSelected(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("PluginLoaderGuiDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = PluginLoaderGuiDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
