# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/SearchFormDesign.ui'
#
# Created: Sat Oct 30 00:16:19 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class SearchFormDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("SearchFormDesign")

        self.setSizePolicy(QSizePolicy(5,0,0,0,self.sizePolicy().hasHeightForWidth()))

        SearchFormDesignLayout = QVBoxLayout(self,11,6,"SearchFormDesignLayout")

        self.groupBox2 = QGroupBox(self,"groupBox2")
        self.groupBox2.setSizePolicy(QSizePolicy(5,0,0,0,self.groupBox2.sizePolicy().hasHeightForWidth()))
        self.groupBox2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2.layout().setSpacing(6)
        self.groupBox2.layout().setMargin(11)
        groupBox2Layout = QGridLayout(self.groupBox2.layout())
        groupBox2Layout.setAlignment(Qt.AlignTop)

        self.searchEdit = QComboBox(0,self.groupBox2,"searchEdit")
        self.searchEdit.setSizePolicy(QSizePolicy(7,0,0,0,self.searchEdit.sizePolicy().hasHeightForWidth()))
        self.searchEdit.setEditable(1)

        groupBox2Layout.addMultiCellWidget(self.searchEdit,1,1,1,3)

        self.textLabel6 = QLabel(self.groupBox2,"textLabel6")
        self.textLabel6.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel6.sizePolicy().hasHeightForWidth()))

        groupBox2Layout.addWidget(self.textLabel6,1,0)

        self.serverBox = QComboBox(0,self.groupBox2,"serverBox")

        groupBox2Layout.addWidget(self.serverBox,0,1)

        self.textLabel2 = QLabel(self.groupBox2,"textLabel2")
        self.textLabel2.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel2.sizePolicy().hasHeightForWidth()))

        groupBox2Layout.addWidget(self.textLabel2,0,0)

        self.filterWizardButton = QPushButton(self.groupBox2,"filterWizardButton")
        self.filterWizardButton.setSizePolicy(QSizePolicy(0,0,0,0,self.filterWizardButton.sizePolicy().hasHeightForWidth()))

        groupBox2Layout.addWidget(self.filterWizardButton,0,2)

        self.startButton = QPushButton(self.groupBox2,"startButton")
        self.startButton.setSizePolicy(QSizePolicy(0,0,0,0,self.startButton.sizePolicy().hasHeightForWidth()))

        groupBox2Layout.addWidget(self.startButton,0,3)
        SearchFormDesignLayout.addWidget(self.groupBox2)

        self.languageChange()

        self.resize(QSize(609,118).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.filterWizardButton,SIGNAL("clicked()"),self.startFilterWizard)
        self.connect(self.startButton,SIGNAL("clicked()"),self.startSearch)


    def languageChange(self):
        self.setCaption(self.__tr("SearchFormDesign"))
        self.groupBox2.setTitle(self.__tr("Search"))
        self.textLabel6.setText(self.__tr("Filter:"))
        self.textLabel2.setText(self.__tr("Server:"))
        self.filterWizardButton.setText(self.__tr("&Filter wizard"))
        self.filterWizardButton.setAccel(self.__tr("Alt+F"))
        self.startButton.setText(self.__tr("&Search"))
        self.startButton.setAccel(self.__tr("Alt+S"))


    def startFilterWizard(self):
        print "SearchFormDesign.startFilterWizard(): Not implemented yet"

    def startSearch(self):
        print "SearchFormDesign.startSearch(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("SearchFormDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = SearchFormDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
