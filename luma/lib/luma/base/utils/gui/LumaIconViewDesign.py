# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/LumaIconViewDesign.ui'
#
# Created: Wed Feb 4 23:47:11 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.10
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class LumaIconViewDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("LumaIconViewDesign")


        LumaIconViewDesignLayout = QGridLayout(self,1,1,11,6,"LumaIconViewDesignLayout")

        self.addButton = QPushButton(self,"addButton")

        LumaIconViewDesignLayout.addWidget(self.addButton,3,3)

        self.resultView = QIconView(self,"resultView")
        self.resultView.setResizePolicy(QIconView.AutoOneFit)
        self.resultView.setGridX(100)
        self.resultView.setGridY(100)
        self.resultView.setResizeMode(QIconView.Adjust)
        self.resultView.setItemsMovable(0)

        LumaIconViewDesignLayout.addMultiCellWidget(self.resultView,2,2,0,3)

        self.goButton = QPushButton(self,"goButton")

        LumaIconViewDesignLayout.addWidget(self.goButton,1,3)

        self.searchEdit = QLineEdit(self,"searchEdit")

        LumaIconViewDesignLayout.addMultiCellWidget(self.searchEdit,1,1,1,2)

        self.textLabel13 = QLabel(self,"textLabel13")
        self.textLabel13.setFrameShape(QLabel.NoFrame)
        self.textLabel13.setFrameShadow(QLabel.Plain)

        LumaIconViewDesignLayout.addWidget(self.textLabel13,1,0)

        self.serverBox = QComboBox(0,self,"serverBox")

        LumaIconViewDesignLayout.addMultiCellWidget(self.serverBox,0,0,1,3)

        self.textLabel12 = QLabel(self,"textLabel12")

        LumaIconViewDesignLayout.addWidget(self.textLabel12,0,0)

        self.deleteButton = QPushButton(self,"deleteButton")

        LumaIconViewDesignLayout.addWidget(self.deleteButton,3,2)
        spacer = QSpacerItem(80,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        LumaIconViewDesignLayout.addMultiCell(spacer,3,3,0,1)

        self.languageChange()

        self.resize(QSize(238,376).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.serverBox,SIGNAL("activated(const QString&)"),self.serverChanged)
        self.connect(self.searchEdit,SIGNAL("returnPressed()"),self.search)
        self.connect(self.goButton,SIGNAL("clicked()"),self.search)
        self.connect(self.resultView,SIGNAL("selectionChanged(QIconViewItem*)"),self.iconClicked)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteItem)
        self.connect(self.addButton,SIGNAL("clicked()"),self.addItem)


    def languageChange(self):
        self.setCaption(self.__tr("LumaIconViewDesign"))
        self.addButton.setText(self.__tr("&Add..."))
        self.addButton.setAccel(self.__tr("Alt+A"))
        self.goButton.setText(self.__tr("&Go"))
        self.goButton.setAccel(self.__tr("Alt+G"))
        self.textLabel13.setText(self.__tr("Filter:"))
        self.textLabel12.setText(self.__tr("Server:"))
        self.deleteButton.setText(self.__tr("&Delete"))
        self.deleteButton.setAccel(self.__tr("Alt+D"))


    def serverChanged(self):
        print "LumaIconViewDesign.serverChanged(): Not implemented yet"

    def search(self):
        print "LumaIconViewDesign.search(): Not implemented yet"

    def iconClicked(self):
        print "LumaIconViewDesign.iconClicked(): Not implemented yet"

    def deleteItem(self):
        print "LumaIconViewDesign.deleteItem(): Not implemented yet"

    def addItem(self):
        print "LumaIconViewDesign.addItem(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("LumaIconViewDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = LumaIconViewDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
