# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/LumaIconViewDesign.ui'
#
# Created: Mon Jan 19 00:13:30 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.8.1
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

        layout15 = QGridLayout(None,1,1,0,6,"layout15")

        self.deleteButton = QPushButton(self,"deleteButton")

        layout15.addMultiCellWidget(self.deleteButton,3,3,0,1)

        self.addButton = QPushButton(self,"addButton")

        layout15.addWidget(self.addButton,3,3)

        self.resultView = QIconView(self,"resultView")
        self.resultView.setResizePolicy(QIconView.AutoOneFit)
        self.resultView.setGridX(100)
        self.resultView.setGridY(100)
        self.resultView.setResizeMode(QIconView.Adjust)
        self.resultView.setItemsMovable(0)

        layout15.addMultiCellWidget(self.resultView,2,2,0,3)

        self.goButton = QPushButton(self,"goButton")

        layout15.addWidget(self.goButton,1,3)

        self.searchEdit = QLineEdit(self,"searchEdit")

        layout15.addMultiCellWidget(self.searchEdit,1,1,1,2)

        self.textLabel13 = QLabel(self,"textLabel13")
        self.textLabel13.setFrameShape(QLabel.NoFrame)
        self.textLabel13.setFrameShadow(QLabel.Plain)

        layout15.addWidget(self.textLabel13,1,0)

        self.serverBox = QComboBox(0,self,"serverBox")

        layout15.addMultiCellWidget(self.serverBox,0,0,1,3)

        self.textLabel12 = QLabel(self,"textLabel12")

        layout15.addWidget(self.textLabel12,0,0)
        spacer = QSpacerItem(61,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout15.addItem(spacer,3,2)

        LumaIconViewDesignLayout.addLayout(layout15,0,0)

        self.languageChange()

        self.resize(QSize(238,368).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.serverBox,SIGNAL("activated(const QString&)"),self.serverChanged)
        self.connect(self.searchEdit,SIGNAL("returnPressed()"),self.search)
        self.connect(self.goButton,SIGNAL("clicked()"),self.search)
        self.connect(self.resultView,SIGNAL("selectionChanged(QIconViewItem*)"),self.iconClicked)


    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.deleteButton.setText(self.__tr("Delete"))
        self.addButton.setText(self.__tr("Add"))
        self.goButton.setText(self.__tr("Go"))
        self.textLabel13.setText(self.__tr("Search:"))
        self.textLabel12.setText(self.__tr("Server:"))


    def serverChanged(self):
        print "LumaIconViewDesign.serverChanged(): Not implemented yet"

    def search(self):
        print "LumaIconViewDesign.search(): Not implemented yet"

    def iconClicked(self):
        print "LumaIconViewDesign.iconClicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("LumaIconViewDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = LumaIconViewDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
