# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/addressbook/CategoryEditDialogDesign.ui'
#
# Created: Thu Mar 25 00:32:43 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class CategoryEditDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("CategoryEditDialogDesign")


        CategoryEditDialogDesignLayout = QGridLayout(self,1,1,11,6,"CategoryEditDialogDesignLayout")

        self.categoryView = QListView(self,"categoryView")
        self.categoryView.addColumn(self.__tr("Categories"))
        self.categoryView.setResizeMode(QListView.AllColumns)

        CategoryEditDialogDesignLayout.addWidget(self.categoryView,0,0)

        self.line11 = QFrame(self,"line11")
        self.line11.setFrameShape(QFrame.HLine)
        self.line11.setFrameShadow(QFrame.Sunken)
        self.line11.setFrameShape(QFrame.HLine)

        CategoryEditDialogDesignLayout.addWidget(self.line11,2,0)

        layout4 = QHBoxLayout(None,0,6,"layout4")

        self.deleteButton = QPushButton(self,"deleteButton")
        layout4.addWidget(self.deleteButton)

        self.addButton = QPushButton(self,"addButton")
        layout4.addWidget(self.addButton)

        CategoryEditDialogDesignLayout.addLayout(layout4,1,0)

        layout2 = QHBoxLayout(None,0,6,"layout2")
        spacer12 = QSpacerItem(120,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer12)

        self.okButton = QPushButton(self,"okButton")
        layout2.addWidget(self.okButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        layout2.addWidget(self.cancelButton)

        CategoryEditDialogDesignLayout.addLayout(layout2,3,0)

        self.languageChange()

        self.resize(QSize(291,376).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.okButton,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteCategory)
        self.connect(self.addButton,SIGNAL("clicked()"),self.addCategory)


    def languageChange(self):
        self.setCaption(self.__tr("Edit categories"))
        self.categoryView.header().setLabel(0,self.__tr("Categories"))
        self.deleteButton.setText(self.__tr("&Delete"))
        self.deleteButton.setAccel(self.__tr("Alt+D"))
        self.addButton.setText(self.__tr("&Add"))
        self.addButton.setAccel(self.__tr("Alt+A"))
        self.okButton.setText(self.__tr("&Ok"))
        self.okButton.setAccel(self.__tr("Alt+O"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))


    def deleteCategory(self):
        print "CategoryEditDialogDesign.deleteCategory(): Not implemented yet"

    def addCategory(self):
        print "CategoryEditDialogDesign.addCategory(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("CategoryEditDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = CategoryEditDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
