# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/addressbook/CategoryEditDialogDesign.ui'
#
# Created: Wed Aug 17 15:23:45 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt4.QtGui import *


class CategoryEditDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("CategoryEditDialogDesign")


        CategoryEditDialogDesignLayout = QGridLayout(self,1,1,11,6,"CategoryEditDialogDesignLayout")

        self.categoryView = QListView(self,"categoryView")
        self.categoryView.addColumn(self.__tr("Categories"))
        self.categoryView.setResizeMode(QListView.AllColumns)

        CategoryEditDialogDesignLayout.addMultiCellWidget(self.categoryView,0,2,0,0)

        self.addButton = QPushButton(self,"addButton")

        CategoryEditDialogDesignLayout.addWidget(self.addButton,0,1)

        self.deleteButton = QPushButton(self,"deleteButton")

        CategoryEditDialogDesignLayout.addWidget(self.deleteButton,1,1)
        spacer2 = QSpacerItem(21,200,QSizePolicy.Minimum,QSizePolicy.Minimum)
        CategoryEditDialogDesignLayout.addItem(spacer2,2,1)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        CategoryEditDialogDesignLayout.addMultiCellWidget(self.line1,3,3,0,1)

        layout2 = QHBoxLayout(None,0,6,"layout2")
        spacer12 = QSpacerItem(120,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer12)

        self.okButton = QPushButton(self,"okButton")
        self.okButton.setDefault(1)
        layout2.addWidget(self.okButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        layout2.addWidget(self.cancelButton)

        CategoryEditDialogDesignLayout.addMultiCellLayout(layout2,4,4,0,1)

        self.languageChange()

        self.resize(QSize(283,514).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.okButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteCategory)
        self.connect(self.addButton,SIGNAL("clicked()"),self.addCategory)


    def languageChange(self):
        self.setCaption(self.__tr("Edit categories"))
        self.categoryView.header().setLabel(0,self.__tr("Categories"))
        self.addButton.setText(self.__tr("&Add..."))
        self.addButton.setAccel(self.__tr("Alt+A"))
        self.deleteButton.setText(self.__tr("&Delete"))
        self.deleteButton.setAccel(self.__tr("Alt+D"))
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
