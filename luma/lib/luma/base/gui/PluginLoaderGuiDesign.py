# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/gui/PluginLoaderGuiDesign.ui'
#
# Created: Mon Dec 29 16:56:30 2003
#      by: The PyQt User Interface Compiler (pyuic) 3.8.1
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

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(5,0,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))

        PluginLoaderGuiDesignLayout.addMultiCellWidget(self.textLabel1,0,0,0,1)
        spacer = QSpacerItem(201,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        PluginLoaderGuiDesignLayout.addItem(spacer,6,0)

        self.line2 = QFrame(self,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)

        PluginLoaderGuiDesignLayout.addMultiCellWidget(self.line2,4,5,0,2)

        self.chooserView = QListView(self,"chooserView")
        self.chooserView.addColumn(self.__tr("Load"))
        self.chooserView.setAllColumnsShowFocus(0)
        self.chooserView.setResizeMode(QListView.AllColumns)

        PluginLoaderGuiDesignLayout.addMultiCellWidget(self.chooserView,2,3,0,1)

        self.pushButton3 = QPushButton(self,"pushButton3")

        PluginLoaderGuiDesignLayout.addWidget(self.pushButton3,2,2)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        PluginLoaderGuiDesignLayout.addMultiCellWidget(self.line1,1,1,0,2)
        spacer_2 = QSpacerItem(41,141,QSizePolicy.Minimum,QSizePolicy.Expanding)
        PluginLoaderGuiDesignLayout.addItem(spacer_2,3,2)

        self.pushButton1 = QPushButton(self,"pushButton1")

        PluginLoaderGuiDesignLayout.addMultiCellWidget(self.pushButton1,5,6,1,2)

        self.languageChange()

        self.resize(QSize(462,331).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton1,SIGNAL("clicked()"),self.saveValues)


    def languageChange(self):
        self.setCaption(self.__tr("Configure Plugins"))
        self.textLabel1.setText(self.__tr("Available Plugins:"))
        self.chooserView.header().setLabel(0,self.__tr("Load"))
        self.pushButton3.setText(self.__tr("Modify"))
        self.pushButton1.setText(self.__tr("Close"))


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
