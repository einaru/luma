# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/FilterWizardDesign.ui'
#
# Created: Thu Jan 1 17:35:30 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.8.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class FilterWizardDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("FilterWizardDesign")

        self.setSizePolicy(QSizePolicy(5,5,0,0,self.sizePolicy().hasHeightForWidth()))

        FilterWizardDesignLayout = QVBoxLayout(self,11,6,"FilterWizardDesignLayout")

        self.groupBox1 = QGroupBox(self,"groupBox1")
        self.groupBox1.setSizePolicy(QSizePolicy(5,0,0,0,self.groupBox1.sizePolicy().hasHeightForWidth()))
        self.groupBox1.setColumnLayout(0,Qt.Vertical)
        self.groupBox1.layout().setSpacing(6)
        self.groupBox1.layout().setMargin(11)
        groupBox1Layout = QVBoxLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(Qt.AlignTop)

        self.frame3 = QFrame(self.groupBox1,"frame3")
        self.frame3.setSizePolicy(QSizePolicy(5,0,0,0,self.frame3.sizePolicy().hasHeightForWidth()))
        self.frame3.setFrameShape(QFrame.StyledPanel)
        self.frame3.setFrameShadow(QFrame.Raised)
        frame3Layout = QVBoxLayout(self.frame3,11,6,"frame3Layout")

        layout6 = QHBoxLayout(None,0,6,"layout6")

        self.classButton = QRadioButton(self.frame3,"classButton")
        self.classButton.setSizePolicy(QSizePolicy(0,0,0,0,self.classButton.sizePolicy().hasHeightForWidth()))
        self.classButton.setChecked(0)
        layout6.addWidget(self.classButton)

        self.attributeButton = QRadioButton(self.frame3,"attributeButton")
        self.attributeButton.setSizePolicy(QSizePolicy(0,0,0,0,self.attributeButton.sizePolicy().hasHeightForWidth()))
        layout6.addWidget(self.attributeButton)

        self.objectBox = QComboBox(0,self.frame3,"objectBox")
        layout6.addWidget(self.objectBox)
        frame3Layout.addLayout(layout6)

        self.filterTypeBox = QComboBox(0,self.frame3,"filterTypeBox")
        frame3Layout.addWidget(self.filterTypeBox)

        layout7 = QHBoxLayout(None,0,6,"layout7")

        self.textLabel3 = QLabel(self.frame3,"textLabel3")
        self.textLabel3.setSizePolicy(QSizePolicy(0,0,0,0,self.textLabel3.sizePolicy().hasHeightForWidth()))
        layout7.addWidget(self.textLabel3)

        self.expressionEdit = QLineEdit(self.frame3,"expressionEdit")
        layout7.addWidget(self.expressionEdit)

        self.addObjectButton = QPushButton(self.frame3,"addObjectButton")
        self.addObjectButton.setSizePolicy(QSizePolicy(0,0,0,0,self.addObjectButton.sizePolicy().hasHeightForWidth()))
        layout7.addWidget(self.addObjectButton)
        frame3Layout.addLayout(layout7)
        groupBox1Layout.addWidget(self.frame3)

        self.frame5 = QFrame(self.groupBox1,"frame5")
        self.frame5.setFrameShape(QFrame.StyledPanel)
        self.frame5.setFrameShadow(QFrame.Raised)
        frame5Layout = QHBoxLayout(self.frame5,11,6,"frame5Layout")

        self.textLabel4 = QLabel(self.frame5,"textLabel4")
        self.textLabel4.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel4.sizePolicy().hasHeightForWidth()))
        frame5Layout.addWidget(self.textLabel4)

        self.concatBox = QComboBox(0,self.frame5,"concatBox")
        frame5Layout.addWidget(self.concatBox)

        self.concatButton = QPushButton(self.frame5,"concatButton")
        self.concatButton.setSizePolicy(QSizePolicy(0,0,0,0,self.concatButton.sizePolicy().hasHeightForWidth()))
        frame5Layout.addWidget(self.concatButton)
        groupBox1Layout.addWidget(self.frame5)
        FilterWizardDesignLayout.addWidget(self.groupBox1)

        self.groupBox5 = QGroupBox(self,"groupBox5")
        self.groupBox5.setColumnLayout(0,Qt.Vertical)
        self.groupBox5.layout().setSpacing(6)
        self.groupBox5.layout().setMargin(11)
        groupBox5Layout = QVBoxLayout(self.groupBox5.layout())
        groupBox5Layout.setAlignment(Qt.AlignTop)

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.textLabel1 = QLabel(self.groupBox5,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(0,0,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))
        layout3.addWidget(self.textLabel1)

        self.bookmarkBox = QComboBox(0,self.groupBox5,"bookmarkBox")
        self.bookmarkBox.setSizeLimit(200)
        layout3.addWidget(self.bookmarkBox)

        self.delBookmarkButton = QPushButton(self.groupBox5,"delBookmarkButton")
        self.delBookmarkButton.setSizePolicy(QSizePolicy(0,0,0,0,self.delBookmarkButton.sizePolicy().hasHeightForWidth()))
        layout3.addWidget(self.delBookmarkButton)
        groupBox5Layout.addLayout(layout3)

        self.line1 = QFrame(self.groupBox5,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)
        groupBox5Layout.addWidget(self.line1)

        self.searchFilterEdit = QLineEdit(self.groupBox5,"searchFilterEdit")
        groupBox5Layout.addWidget(self.searchFilterEdit)

        layout4 = QHBoxLayout(None,0,6,"layout4")
        spacer = QSpacerItem(301,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout4.addItem(spacer)

        self.addBookmarkButton = QPushButton(self.groupBox5,"addBookmarkButton")
        self.addBookmarkButton.setSizePolicy(QSizePolicy(0,0,0,0,self.addBookmarkButton.sizePolicy().hasHeightForWidth()))
        layout4.addWidget(self.addBookmarkButton)
        groupBox5Layout.addLayout(layout4)
        FilterWizardDesignLayout.addWidget(self.groupBox5)
        spacer_2 = QSpacerItem(41,110,QSizePolicy.Minimum,QSizePolicy.Expanding)
        FilterWizardDesignLayout.addItem(spacer_2)

        self.pushButton11 = QPushButton(self,"pushButton11")
        FilterWizardDesignLayout.addWidget(self.pushButton11)

        self.languageChange()

        self.resize(QSize(398,416).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton11,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(self.addObjectButton,SIGNAL("clicked()"),self.add_criteria)
        self.connect(self.concatButton,SIGNAL("clicked()"),self.add_concat)
        self.connect(self.attributeButton,SIGNAL("clicked()"),self.attribute_choice_changed)
        self.connect(self.classButton,SIGNAL("clicked()"),self.class_choice_changed)
        self.connect(self.bookmarkBox,SIGNAL("activated(const QString&)"),self.bookmark_selected)
        self.connect(self.delBookmarkButton,SIGNAL("clicked()"),self.delete_bookmark)
        self.connect(self.addBookmarkButton,SIGNAL("clicked()"),self.add_bookmark)


    def languageChange(self):
        self.setCaption(self.__tr("Search Filter Wizard"))
        self.groupBox1.setTitle(self.__tr("Search Criteria"))
        self.classButton.setText(self.__tr("ObjectClass"))
        self.attributeButton.setText(self.__tr("Attribute"))
        self.filterTypeBox.clear()
        self.filterTypeBox.insertItem(self.__tr("=  (equal)"))
        self.filterTypeBox.insertItem(self.__tr("-=  (approx)"))
        self.filterTypeBox.insertItem(self.__tr(">=  (greater)"))
        self.filterTypeBox.insertItem(self.__tr("<=  (less)"))
        self.textLabel3.setText(self.__tr("Expression:"))
        self.addObjectButton.setText(self.__tr("Add"))
        self.textLabel4.setText(self.__tr("Concatenation:"))
        self.concatBox.clear()
        self.concatBox.insertItem(self.__tr("and"))
        self.concatBox.insertItem(self.__tr("or"))
        self.concatBox.insertItem(self.__tr("not"))
        self.concatButton.setText(self.__tr("Add"))
        self.groupBox5.setTitle(self.__tr("Search Filter"))
        self.textLabel1.setText(self.__tr("Bookmark:"))
        self.delBookmarkButton.setText(self.__tr("Delete"))
        self.addBookmarkButton.setText(self.__tr("Add to Bookmarks"))
        self.pushButton11.setText(self.__tr("Ok"))


    def class_choice_changed(self):
        print "FilterWizardDesign.class_choice_changed(): Not implemented yet"

    def add_criteria(self):
        print "FilterWizardDesign.add_criteria(): Not implemented yet"

    def add_concat(self):
        print "FilterWizardDesign.add_concat(): Not implemented yet"

    def attribute_choice_changed(self):
        print "FilterWizardDesign.attribute_choice_changed(): Not implemented yet"

    def bookmark_selected(self):
        print "FilterWizardDesign.bookmark_selected(): Not implemented yet"

    def delete_bookmark(self):
        print "FilterWizardDesign.delete_bookmark(): Not implemented yet"

    def add_bookmark(self):
        print "FilterWizardDesign.add_bookmark(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("FilterWizardDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = FilterWizardDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
