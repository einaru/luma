# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/addressbook/AddressbookSettingsDesign.ui'
#
# Created: Mon Apr 5 21:56:40 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class AddressbookSettingsDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("AddressbookSettingsDesign")


        AddressbookSettingsDesignLayout = QVBoxLayout(self,11,6,"AddressbookSettingsDesignLayout")

        self.tabWidget2 = QTabWidget(self,"tabWidget2")

        self.tab = QWidget(self.tabWidget2,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")

        layout4 = QGridLayout(None,1,1,0,6,"layout4")

        self.attributeView = QListView(self.tab,"attributeView")
        self.attributeView.addColumn(self.__tr("Attributes"))
        self.attributeView.setResizeMode(QListView.AllColumns)

        layout4.addMultiCellWidget(self.attributeView,0,0,0,1)

        self.attributeEdit = QLineEdit(self.tab,"attributeEdit")

        layout4.addWidget(self.attributeEdit,1,0)

        self.addButton = QPushButton(self.tab,"addButton")

        layout4.addWidget(self.addButton,1,1)

        tabLayout.addMultiCellLayout(layout4,0,1,0,0)

        self.deleteButton = QPushButton(self.tab,"deleteButton")

        tabLayout.addWidget(self.deleteButton,0,2)
        spacer6 = QSpacerItem(41,260,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer6,1,2)
        self.tabWidget2.insertTab(self.tab,QString(""))
        AddressbookSettingsDesignLayout.addWidget(self.tabWidget2)

        layout2 = QHBoxLayout(None,0,6,"layout2")
        Horizontal_Spacing2 = QSpacerItem(300,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(Horizontal_Spacing2)

        self.saveButton = QPushButton(self,"saveButton")
        self.saveButton.setFocusPolicy(QPushButton.ClickFocus)
        layout2.addWidget(self.saveButton)
        AddressbookSettingsDesignLayout.addLayout(layout2)

        self.languageChange()

        self.resize(QSize(344,299).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.saveButton,SIGNAL("clicked()"),self.saveValues)
        self.connect(self.addButton,SIGNAL("clicked()"),self.addAttribute)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteAttribute)

        self.setTabOrder(self.tabWidget2,self.attributeView)
        self.setTabOrder(self.attributeView,self.attributeEdit)
        self.setTabOrder(self.attributeEdit,self.addButton)
        self.setTabOrder(self.addButton,self.deleteButton)
        self.setTabOrder(self.deleteButton,self.saveButton)


    def languageChange(self):
        self.setCaption(self.__tr("Addressbook Settings"))
        self.attributeView.header().setLabel(0,self.__tr("Attributes"))
        self.addButton.setText(self.__tr("&Add"))
        self.addButton.setAccel(self.__tr("Alt+A"))
        self.deleteButton.setText(self.__tr("&Delete"))
        self.deleteButton.setAccel(self.__tr("Alt+D"))
        self.tabWidget2.changeTab(self.tab,self.__tr("Search Criteria"))
        self.saveButton.setText(self.__tr("&Save"))
        self.saveButton.setAccel(self.__tr("Alt+S"))


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
