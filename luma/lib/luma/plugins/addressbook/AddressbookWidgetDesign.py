# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/addressbook/AddressbookWidgetDesign.ui'
#
# Created: Sun Jan 4 20:52:59 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.8.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class AddressbookWidgetDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("AddressbookWidgetDesign")


        AddressbookWidgetDesignLayout = QGridLayout(self,1,1,0,6,"AddressbookWidgetDesignLayout")

        self.splitter4 = QSplitter(self,"splitter4")
        self.splitter4.setOrientation(QSplitter.Horizontal)

        LayoutWidget = QWidget(self.splitter4,"layout17")
        layout17 = QGridLayout(LayoutWidget,1,1,0,6,"layout17")

        self.textLabel13 = QLabel(LayoutWidget,"textLabel13")

        layout17.addWidget(self.textLabel13,2,0)

        self.resultView = QIconView(LayoutWidget,"resultView")
        self.resultView.setResizePolicy(QIconView.AutoOneFit)
        self.resultView.setGridX(100)
        self.resultView.setGridY(100)
        self.resultView.setResizeMode(QIconView.Adjust)
        self.resultView.setItemsMovable(0)

        layout17.addMultiCellWidget(self.resultView,1,1,0,1)

        self.searchEdit = QLineEdit(LayoutWidget,"searchEdit")

        layout17.addWidget(self.searchEdit,2,1)

        self.textLabel12 = QLabel(LayoutWidget,"textLabel12")

        layout17.addWidget(self.textLabel12,0,0)

        self.serverBox = QComboBox(0,LayoutWidget,"serverBox")

        layout17.addWidget(self.serverBox,0,1)

        self.frame3 = QFrame(self.splitter4,"frame3")
        self.frame3.setFrameShape(QFrame.StyledPanel)
        self.frame3.setFrameShadow(QFrame.Raised)
        frame3Layout = QGridLayout(self.frame3,1,1,0,6,"frame3Layout")

        self.tabWidget2 = QTabWidget(self.frame3,"tabWidget2")

        self.tab = QWidget(self.tabWidget2,"tab")
        tabLayout = QVBoxLayout(self.tab,0,6,"tabLayout")

        layout11 = QGridLayout(None,1,1,0,6,"layout11")

        layout9 = QGridLayout(None,1,1,0,6,"layout9")

        self.organisationEdit = QLineEdit(self.tab,"organisationEdit")

        layout9.addWidget(self.organisationEdit,5,1)

        self.textLabel1 = QLabel(self.tab,"textLabel1")

        layout9.addWidget(self.textLabel1,4,0)

        self.textLabel3_2 = QLabel(self.tab,"textLabel3_2")

        layout9.addWidget(self.textLabel3_2,1,0)

        self.line3 = QFrame(self.tab,"line3")
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setFrameShadow(QFrame.Sunken)
        self.line3.setFrameShape(QFrame.HLine)

        layout9.addMultiCellWidget(self.line3,3,3,0,1)

        self.textLabel2_2 = QLabel(self.tab,"textLabel2_2")

        layout9.addWidget(self.textLabel2_2,2,0)

        self.givenNameEdit = QLineEdit(self.tab,"givenNameEdit")

        layout9.addWidget(self.givenNameEdit,1,1)

        self.textLabel1_2 = QLabel(self.tab,"textLabel1_2")

        layout9.addWidget(self.textLabel1_2,0,0)

        self.textLabel2 = QLabel(self.tab,"textLabel2")

        layout9.addWidget(self.textLabel2,5,0)

        self.commonNameEdit = QLineEdit(self.tab,"commonNameEdit")

        layout9.addWidget(self.commonNameEdit,0,1)

        self.textLabel3 = QLabel(self.tab,"textLabel3")

        layout9.addWidget(self.textLabel3,6,0)

        self.departementEdit = QLineEdit(self.tab,"departementEdit")

        layout9.addWidget(self.departementEdit,6,1)

        self.surenameEdit = QLineEdit(self.tab,"surenameEdit")

        layout9.addWidget(self.surenameEdit,2,1)

        self.roleEdit = QLineEdit(self.tab,"roleEdit")

        layout9.addWidget(self.roleEdit,4,1)

        layout11.addMultiCellLayout(layout9,0,1,1,1)
        spacer = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout11.addItem(spacer,2,1)

        self.personLabel = QLabel(self.tab,"personLabel")
        self.personLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.personLabel.sizePolicy().hasHeightForWidth()))
        self.personLabel.setMinimumSize(QSize(32,32))

        layout11.addWidget(self.personLabel,0,0)
        spacer_2 = QSpacerItem(21,192,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout11.addMultiCell(spacer_2,1,2,0,0)
        tabLayout.addLayout(layout11)

        self.line2 = QFrame(self.tab,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)
        tabLayout.addWidget(self.line2)

        layout12 = QGridLayout(None,1,1,0,6,"layout12")

        self.workPhoneEdit = QLineEdit(self.tab,"workPhoneEdit")

        layout12.addWidget(self.workPhoneEdit,1,2)
        spacer_3 = QSpacerItem(21,31,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout12.addItem(spacer_3,3,2)

        self.textLabel8 = QLabel(self.tab,"textLabel8")

        layout12.addWidget(self.textLabel8,1,1)

        self.homePhoneEdit = QLineEdit(self.tab,"homePhoneEdit")

        layout12.addWidget(self.homePhoneEdit,0,2)

        self.textLabel9 = QLabel(self.tab,"textLabel9")

        layout12.addWidget(self.textLabel9,2,1)

        self.mobilePhoneEdit = QLineEdit(self.tab,"mobilePhoneEdit")

        layout12.addWidget(self.mobilePhoneEdit,2,2)

        self.phoneLabel = QLabel(self.tab,"phoneLabel")
        self.phoneLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.phoneLabel.sizePolicy().hasHeightForWidth()))
        self.phoneLabel.setMinimumSize(QSize(32,32))

        layout12.addWidget(self.phoneLabel,0,0)

        self.textLabel7 = QLabel(self.tab,"textLabel7")

        layout12.addWidget(self.textLabel7,0,1)
        tabLayout.addLayout(layout12)

        self.line1 = QFrame(self.tab,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)
        tabLayout.addWidget(self.line1)

        layout8 = QHBoxLayout(None,0,6,"layout8")

        self.mailLabel = QLabel(self.tab,"mailLabel")
        self.mailLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.mailLabel.sizePolicy().hasHeightForWidth()))
        self.mailLabel.setMinimumSize(QSize(32,32))
        layout8.addWidget(self.mailLabel)

        self.textLabel10 = QLabel(self.tab,"textLabel10")
        self.textLabel10.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel10.sizePolicy().hasHeightForWidth()))
        layout8.addWidget(self.textLabel10)

        self.mailBox = QComboBox(0,self.tab,"mailBox")
        self.mailBox.setEditable(1)
        layout8.addWidget(self.mailBox)
        tabLayout.addLayout(layout8)
        spacer_4 = QSpacerItem(31,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer_4)
        self.tabWidget2.insertTab(self.tab,QString(""))

        self.tab_2 = QWidget(self.tabWidget2,"tab_2")
        self.tabWidget2.insertTab(self.tab_2,QString(""))

        frame3Layout.addWidget(self.tabWidget2,0,0)

        AddressbookWidgetDesignLayout.addWidget(self.splitter4,0,0)

        self.languageChange()

        self.resize(QSize(519,427).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.serverBox,SIGNAL("activated(const QString&)"),self.serverChanged)
        self.connect(self.searchEdit,SIGNAL("returnPressed()"),self.search)
        self.connect(self.resultView,SIGNAL("selectionChanged(QIconViewItem*)"),self.iconClicked)


    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.textLabel13.setText(self.__tr("Search:"))
        self.textLabel12.setText(self.__tr("Server:"))
        self.textLabel1.setText(self.__tr("Role:"))
        self.textLabel3_2.setText(self.__tr("Given Name:"))
        self.textLabel2_2.setText(self.__tr("Surename:"))
        self.textLabel1_2.setText(self.__tr("Common Name:"))
        self.textLabel2.setText(self.__tr("Organisation:"))
        self.textLabel3.setText(self.__tr("Departement:"))
        self.personLabel.setText(self.__tr("P"))
        self.textLabel8.setText(self.__tr("Work:"))
        self.textLabel9.setText(self.__tr("Mobile:"))
        self.phoneLabel.setText(self.__tr("Ph"))
        self.textLabel7.setText(self.__tr("Home:"))
        self.mailLabel.setText(self.__tr("Ma"))
        self.textLabel10.setText(self.__tr("Email:"))
        self.tabWidget2.changeTab(self.tab,self.__tr("General"))
        self.tabWidget2.changeTab(self.tab_2,self.__tr("Tab 2"))


    def serverChanged(self):
        print "AddressbookWidgetDesign.serverChanged(): Not implemented yet"

    def search(self):
        print "AddressbookWidgetDesign.search(): Not implemented yet"

    def iconClicked(self):
        print "AddressbookWidgetDesign.iconClicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("AddressbookWidgetDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = AddressbookWidgetDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
