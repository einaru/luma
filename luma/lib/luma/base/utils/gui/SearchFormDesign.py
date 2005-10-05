# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/SearchFormDesign.ui'
#
# Created: Wed Aug 17 15:23:41 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class SearchFormDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("SearchFormDesign")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.sizePolicy().hasHeightForWidth()))

        SearchFormDesignLayout = QVBoxLayout(self,11,6,"SearchFormDesignLayout")

        self.groupFrame = QFrame(self,"groupFrame")
        self.groupFrame.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed,0,0,self.groupFrame.sizePolicy().hasHeightForWidth()))
        self.groupFrame.setFrameShape(QFrame.StyledPanel)
        self.groupFrame.setFrameShadow(QFrame.Sunken)
        groupFrameLayout = QGridLayout(self.groupFrame,1,1,11,6,"groupFrameLayout")

        self.filterWizardButton = QPushButton(self.groupFrame,"filterWizardButton")
        self.filterWizardButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.filterWizardButton.sizePolicy().hasHeightForWidth()))

        groupFrameLayout.addWidget(self.filterWizardButton,0,4)

        self.baseBox = QComboBox(0,self.groupFrame,"baseBox")

        groupFrameLayout.addWidget(self.baseBox,0,3)

        self.searchEdit = QComboBox(0,self.groupFrame,"searchEdit")
        self.searchEdit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.searchEdit.sizePolicy().hasHeightForWidth()))
        self.searchEdit.setEditable(1)

        groupFrameLayout.addMultiCellWidget(self.searchEdit,1,1,1,4)

        self.textLabel1 = QLabel(self.groupFrame,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))

        groupFrameLayout.addWidget(self.textLabel1,0,2)

        self.serverBox = QComboBox(0,self.groupFrame,"serverBox")

        groupFrameLayout.addWidget(self.serverBox,0,1)

        self.textLabel6 = QLabel(self.groupFrame,"textLabel6")
        self.textLabel6.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel6.sizePolicy().hasHeightForWidth()))

        groupFrameLayout.addWidget(self.textLabel6,1,0)

        self.textLabel2 = QLabel(self.groupFrame,"textLabel2")
        self.textLabel2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel2.sizePolicy().hasHeightForWidth()))

        groupFrameLayout.addWidget(self.textLabel2,0,0)

        self.startButton = QPushButton(self.groupFrame,"startButton")
        self.startButton.setEnabled(0)
        self.startButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.startButton.sizePolicy().hasHeightForWidth()))
        self.startButton.setDefault(1)

        groupFrameLayout.addWidget(self.startButton,0,5)
        SearchFormDesignLayout.addWidget(self.groupFrame)

        self.languageChange()

        self.resize(QSize(641,102).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.filterWizardButton,SIGNAL("clicked()"),self.startFilterWizard)
        self.connect(self.startButton,SIGNAL("clicked()"),self.startSearch)
        self.connect(self.serverBox,SIGNAL("activated(const QString&)"),self.serverChanged)

        self.setTabOrder(self.serverBox,self.baseBox)
        self.setTabOrder(self.baseBox,self.searchEdit)
        self.setTabOrder(self.searchEdit,self.filterWizardButton)
        self.setTabOrder(self.filterWizardButton,self.startButton)


    def languageChange(self):
        self.setCaption(self.__tr("SearchFormDesign"))
        self.filterWizardButton.setText(self.__tr("&Filter wizard"))
        self.filterWizardButton.setAccel(self.__tr("Alt+F"))
        self.textLabel1.setText(self.__tr("Base DN:"))
        self.textLabel6.setText(self.__tr("Filter:"))
        self.textLabel2.setText(self.__tr("Server:"))
        self.startButton.setText(self.__tr("&Search"))
        self.startButton.setAccel(self.__tr("Alt+S"))


    def startFilterWizard(self):
        print "SearchFormDesign.startFilterWizard(): Not implemented yet"

    def startSearch(self):
        print "SearchFormDesign.startSearch(): Not implemented yet"

    def serverChanged(self):
        print "SearchFormDesign.serverChanged(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("SearchFormDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = SearchFormDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
