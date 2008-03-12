# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/addressbook/AddressbookSettingsDesign.ui'
#
# Created: Wed Aug 17 15:23:44 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt4.QtGui import *


class AddressbookSettingsDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("AddressbookSettingsDesign")


        AddressbookSettingsDesignLayout = QGridLayout(self,1,1,11,6,"AddressbookSettingsDesignLayout")

        layout2 = QHBoxLayout(None,0,6,"layout2")

        AddressbookSettingsDesignLayout.addMultiCellLayout(layout2,2,2,0,1)

        self.textLabel1 = QLabel(self,"textLabel1")

        AddressbookSettingsDesignLayout.addMultiCellWidget(self.textLabel1,0,0,0,1)

        layout3 = QGridLayout(None,1,1,0,6,"layout3")

        self.attributeView = QListView(self,"attributeView")
        self.attributeView.addColumn(self.__tr("Attributes"))
        self.attributeView.setResizeMode(QListView.AllColumns)

        layout3.addMultiCellWidget(self.attributeView,0,2,0,0)

        self.deleteButton = QPushButton(self,"deleteButton")

        layout3.addWidget(self.deleteButton,1,1)

        self.addButton = QPushButton(self,"addButton")

        layout3.addWidget(self.addButton,0,1)
        spacer6 = QSpacerItem(41,50,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout3.addItem(spacer6,2,1)

        AddressbookSettingsDesignLayout.addLayout(layout3,1,1)
        spacer3 = QSpacerItem(10,21,QSizePolicy.Fixed,QSizePolicy.Minimum)
        AddressbookSettingsDesignLayout.addItem(spacer3,1,0)

        self.languageChange()

        self.resize(QSize(431,335).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.addButton,SIGNAL("clicked()"),self.addAttribute)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteAttribute)

        self.setTabOrder(self.attributeView,self.addButton)
        self.setTabOrder(self.addButton,self.deleteButton)


    def languageChange(self):
        self.setCaption(self.__tr("Addressbook Settings"))
        self.textLabel1.setText(self.__tr("<b>Search criteria</b>"))
        self.attributeView.header().setLabel(0,self.__tr("Attributes"))
        self.deleteButton.setText(self.__tr("&Delete"))
        self.deleteButton.setAccel(self.__tr("Alt+D"))
        self.addButton.setText(self.__tr("&Add..."))
        self.addButton.setAccel(self.__tr("Alt+A"))


    def saveValues(self):
        print "AddressbookSettingsDesign.saveValues(): Not implemented yet"

    def addAttribute(self):
        print "AddressbookSettingsDesign.addAttribute(): Not implemented yet"

    def deleteAttribute(self):
        print "AddressbookSettingsDesign.deleteAttribute(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("AddressbookSettingsDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = AddressbookSettingsDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
