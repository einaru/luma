# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/daten/src/cvs/luma/lib/luma/base/gui/PluginLoaderGuiDesign.ui'
#
# Created: Mon Sep 1 00:18:34 2003
#      by: The PyQt User Interface Compiler (pyuic) 3.7
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class PluginLoaderGuiDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("PluginLoaderGuiDesign")


        PluginLoaderGuiDesignLayout = QGridLayout(self,1,1,11,6,"PluginLoaderGuiDesignLayout")

        self.pushButton1 = QPushButton(self,"pushButton1")

        PluginLoaderGuiDesignLayout.addWidget(self.pushButton1,3,1)

        self.pushButton2 = QPushButton(self,"pushButton2")

        PluginLoaderGuiDesignLayout.addWidget(self.pushButton2,3,2)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(5,0,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))

        PluginLoaderGuiDesignLayout.addMultiCellWidget(self.textLabel1,0,0,0,2)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        PluginLoaderGuiDesignLayout.addMultiCellWidget(self.line1,1,1,0,2)
        spacer = QSpacerItem(201,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        PluginLoaderGuiDesignLayout.addItem(spacer,3,0)

        self.chooserView = QListView(self,"chooserView")
        self.chooserView.addColumn(self.__tr("Plugins"))
        self.chooserView.setAllColumnsShowFocus(0)
        self.chooserView.setResizeMode(QListView.NoColumn)

        PluginLoaderGuiDesignLayout.addMultiCellWidget(self.chooserView,2,2,0,2)

        self.languageChange()

        self.resize(QSize(412,346).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton2,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(self.pushButton1,SIGNAL("clicked()"),self.saveValues)


    def languageChange(self):
        self.setCaption(self.__tr("Configure Plugins"))
        self.pushButton1.setText(self.__tr("Ok"))
        self.pushButton2.setText(self.__tr("Cancel"))
        self.textLabel1.setText(self.__tr("Available Plugins:"))
        self.chooserView.header().setLabel(0,self.__tr("Plugins"))


    def saveValues(self):
        print "PluginLoaderGuiDesign.saveValues(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("PluginLoaderGuiDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = PluginLoaderGuiDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
