# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/FilterWizardDesign.ui'
#
# Created: Wed Aug 17 15:23:41 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class FilterWizardDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("FilterWizardDesign")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.sizePolicy().hasHeightForWidth()))

        FilterWizardDesignLayout = QVBoxLayout(self,11,6,"FilterWizardDesignLayout")

        layout7 = QGridLayout(None,1,1,0,6,"layout7")

        self.delBookmarkButton = QPushButton(self,"delBookmarkButton")
        self.delBookmarkButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.delBookmarkButton.sizePolicy().hasHeightForWidth()))

        layout7.addWidget(self.delBookmarkButton,2,4)
        spacer6 = QSpacerItem(128,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout7.addMultiCell(spacer6,2,2,1,2)

        self.bookmarkBox = QComboBox(0,self,"bookmarkBox")
        self.bookmarkBox.setSizeLimit(200)

        layout7.addMultiCellWidget(self.bookmarkBox,1,1,2,4)
        spacer5 = QSpacerItem(16,16,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout7.addItem(spacer5,1,0)

        self.addBookmarkButton = QPushButton(self,"addBookmarkButton")
        self.addBookmarkButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.addBookmarkButton.sizePolicy().hasHeightForWidth()))

        layout7.addWidget(self.addBookmarkButton,2,3)

        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setAlignment(QLabel.AlignVCenter)

        layout7.addMultiCellWidget(self.textLabel2,0,0,0,4)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))

        layout7.addWidget(self.textLabel1,1,1)
        FilterWizardDesignLayout.addLayout(layout7)
        spacer7 = QSpacerItem(31,10,QSizePolicy.Minimum,QSizePolicy.Fixed)
        FilterWizardDesignLayout.addItem(spacer7)

        layout6 = QGridLayout(None,1,1,0,6,"layout6")

        self.expressionEdit = QLineEdit(self,"expressionEdit")

        layout6.addMultiCellWidget(self.expressionEdit,2,2,2,3)

        self.attributeButton = QRadioButton(self,"attributeButton")
        self.attributeButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.attributeButton.sizePolicy().hasHeightForWidth()))

        layout6.addWidget(self.attributeButton,1,2)

        self.filterTypeBox = QComboBox(0,self,"filterTypeBox")
        self.filterTypeBox.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.filterTypeBox.sizePolicy().hasHeightForWidth()))

        layout6.addWidget(self.filterTypeBox,2,1)

        self.textLabel1_2 = QLabel(self,"textLabel1_2")
        self.textLabel1_2.setAlignment(QLabel.AlignVCenter)

        layout6.addMultiCellWidget(self.textLabel1_2,0,0,0,4)

        self.addObjectButton = QPushButton(self,"addObjectButton")
        self.addObjectButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.addObjectButton.sizePolicy().hasHeightForWidth()))

        layout6.addWidget(self.addObjectButton,2,4)

        self.classButton = QRadioButton(self,"classButton")
        self.classButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.classButton.sizePolicy().hasHeightForWidth()))
        self.classButton.setChecked(0)

        layout6.addWidget(self.classButton,1,1)

        self.objectBox = QComboBox(0,self,"objectBox")

        layout6.addMultiCellWidget(self.objectBox,1,1,3,4)
        spacer4 = QSpacerItem(16,21,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout6.addItem(spacer4,1,0)
        FilterWizardDesignLayout.addLayout(layout6)
        spacer13 = QSpacerItem(21,10,QSizePolicy.Minimum,QSizePolicy.Fixed)
        FilterWizardDesignLayout.addItem(spacer13)

        layout3 = QGridLayout(None,1,1,0,6,"layout3")
        spacer12 = QSpacerItem(16,16,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout3.addItem(spacer12,1,0)

        self.concatBox = QComboBox(0,self,"concatBox")

        layout3.addWidget(self.concatBox,1,1)

        self.concatButton = QPushButton(self,"concatButton")
        self.concatButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.concatButton.sizePolicy().hasHeightForWidth()))

        layout3.addWidget(self.concatButton,1,2)

        self.textLabel4 = QLabel(self,"textLabel4")
        self.textLabel4.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel4.sizePolicy().hasHeightForWidth()))
        self.textLabel4.setAlignment(QLabel.AlignVCenter)

        layout3.addMultiCellWidget(self.textLabel4,0,0,0,1)
        FilterWizardDesignLayout.addLayout(layout3)
        spacer8 = QSpacerItem(31,10,QSizePolicy.Minimum,QSizePolicy.Fixed)
        FilterWizardDesignLayout.addItem(spacer8)

        self.textLabel3_2 = QLabel(self,"textLabel3_2")
        self.textLabel3_2.setAlignment(QLabel.AlignVCenter)
        FilterWizardDesignLayout.addWidget(self.textLabel3_2)

        self.searchFilterEdit = QLineEdit(self,"searchFilterEdit")
        FilterWizardDesignLayout.addWidget(self.searchFilterEdit)
        spacer11 = QSpacerItem(31,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        FilterWizardDesignLayout.addItem(spacer11)

        self.line2 = QFrame(self,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)
        FilterWizardDesignLayout.addWidget(self.line2)

        layout27 = QHBoxLayout(None,0,6,"layout27")
        spacer3 = QSpacerItem(470,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout27.addItem(spacer3)

        self.pushButton11 = QPushButton(self,"pushButton11")
        self.pushButton11.setDefault(1)
        layout27.addWidget(self.pushButton11)

        self.pushButton6 = QPushButton(self,"pushButton6")
        layout27.addWidget(self.pushButton6)
        FilterWizardDesignLayout.addLayout(layout27)

        self.languageChange()

        self.resize(QSize(423,451).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton11,SIGNAL("clicked()"),self.accept)
        self.connect(self.addObjectButton,SIGNAL("clicked()"),self.addCriteria)
        self.connect(self.concatButton,SIGNAL("clicked()"),self.addConcat)
        self.connect(self.attributeButton,SIGNAL("clicked()"),self.attributeChoiceChanged)
        self.connect(self.classButton,SIGNAL("clicked()"),self.classChoiceChanged)
        self.connect(self.bookmarkBox,SIGNAL("activated(const QString&)"),self.bookmarkSelected)
        self.connect(self.delBookmarkButton,SIGNAL("clicked()"),self.deleteBookmark)
        self.connect(self.addBookmarkButton,SIGNAL("clicked()"),self.addBookmark)
        self.connect(self.pushButton6,SIGNAL("clicked()"),self.reject)

        self.setTabOrder(self.bookmarkBox,self.addBookmarkButton)
        self.setTabOrder(self.addBookmarkButton,self.delBookmarkButton)
        self.setTabOrder(self.delBookmarkButton,self.classButton)
        self.setTabOrder(self.classButton,self.attributeButton)
        self.setTabOrder(self.attributeButton,self.objectBox)
        self.setTabOrder(self.objectBox,self.filterTypeBox)
        self.setTabOrder(self.filterTypeBox,self.expressionEdit)
        self.setTabOrder(self.expressionEdit,self.addObjectButton)
        self.setTabOrder(self.addObjectButton,self.concatBox)
        self.setTabOrder(self.concatBox,self.concatButton)
        self.setTabOrder(self.concatButton,self.searchFilterEdit)
        self.setTabOrder(self.searchFilterEdit,self.pushButton11)
        self.setTabOrder(self.pushButton11,self.pushButton6)


    def languageChange(self):
        self.setCaption(self.__tr("Search Filter Wizard"))
        self.delBookmarkButton.setText(self.__tr("&Delete"))
        self.delBookmarkButton.setAccel(self.__tr("Alt+D"))
        self.addBookmarkButton.setText(self.__tr("&Add current filter"))
        self.addBookmarkButton.setAccel(self.__tr("Alt+A"))
        self.textLabel2.setText(self.__tr("<b>Filter bookmarks</b>"))
        self.textLabel1.setText(self.__tr("Filter:"))
        self.attributeButton.setText(self.__tr("Attribute"))
        self.filterTypeBox.clear()
        self.filterTypeBox.insertItem(self.__tr("=  (equal)"))
        self.filterTypeBox.insertItem(self.__tr("-=  (approx)"))
        self.filterTypeBox.insertItem(self.__tr(">=  (greater)"))
        self.filterTypeBox.insertItem(self.__tr("<=  (less)"))
        self.textLabel1_2.setText(self.__tr("<b>Search Criteria</b>"))
        self.addObjectButton.setText(self.__tr("Add"))
        self.classButton.setText(self.__tr("ObjectClass"))
        self.concatBox.clear()
        self.concatBox.insertItem(self.__tr("and"))
        self.concatBox.insertItem(self.__tr("or"))
        self.concatBox.insertItem(self.__tr("not"))
        self.concatButton.setText(self.__tr("Add"))
        self.textLabel4.setText(self.__tr("<b>Concatenation</b>"))
        self.textLabel3_2.setText(self.__tr("<b>Current filter</b>"))
        self.pushButton11.setText(self.__tr("&Ok"))
        self.pushButton11.setAccel(self.__tr("Alt+O"))
        self.pushButton6.setText(self.__tr("&Cancel"))
        self.pushButton6.setAccel(self.__tr("Alt+C"))


    def classChoiceChanged(self):
        print "FilterWizardDesign.classChoiceChanged(): Not implemented yet"

    def addCriteria(self):
        print "FilterWizardDesign.addCriteria(): Not implemented yet"

    def addConcat(self):
        print "FilterWizardDesign.addConcat(): Not implemented yet"

    def attributeChoiceChanged(self):
        print "FilterWizardDesign.attributeChoiceChanged(): Not implemented yet"

    def bookmarkSelected(self):
        print "FilterWizardDesign.bookmarkSelected(): Not implemented yet"

    def deleteBookmark(self):
        print "FilterWizardDesign.deleteBookmark(): Not implemented yet"

    def addBookmark(self):
        print "FilterWizardDesign.addBookmark(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("FilterWizardDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = FilterWizardDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
