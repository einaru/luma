# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/addressbook/CategoryEditDialogDesign.ui'
#
# Created: Tue Feb 3 23:58:07 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.10
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

        CategoryEditDialogDesignLayout.addMultiCellWidget(self.categoryView,3,3,0,2)

        self.line11 = QFrame(self,"line11")
        self.line11.setFrameShape(QFrame.HLine)
        self.line11.setFrameShadow(QFrame.Sunken)
        self.line11.setFrameShape(QFrame.HLine)

        CategoryEditDialogDesignLayout.addMultiCellWidget(self.line11,5,5,0,2)
        spacer = QSpacerItem(321,31,QSizePolicy.Expanding,QSizePolicy.Minimum)
        CategoryEditDialogDesignLayout.addMultiCell(spacer,6,7,0,0)

        self.cancelButton = QPushButton(self,"cancelButton")

        CategoryEditDialogDesignLayout.addWidget(self.cancelButton,7,1)

        self.okButton = QPushButton(self,"okButton")

        CategoryEditDialogDesignLayout.addWidget(self.okButton,7,2)

        layout4 = QHBoxLayout(None,0,6,"layout4")

        self.deleteButton = QPushButton(self,"deleteButton")
        layout4.addWidget(self.deleteButton)

        self.addButton = QPushButton(self,"addButton")
        layout4.addWidget(self.addButton)

        CategoryEditDialogDesignLayout.addMultiCellLayout(layout4,4,4,0,2)

        self.languageChange()

        self.resize(QSize(309,308).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.okButton,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteCategory)
        self.connect(self.addButton,SIGNAL("clicked()"),self.addCategory)


    def languageChange(self):
        self.setCaption(self.__tr("Edit categories"))
        self.categoryView.header().setLabel(0,self.__tr("Categories"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))
        self.okButton.setText(self.__tr("&Ok"))
        self.okButton.setAccel(self.__tr("Alt+O"))
        self.deleteButton.setText(self.__tr("&Delete"))
        self.deleteButton.setAccel(self.__tr("Alt+D"))
        self.addButton.setText(self.__tr("&Add"))
        self.addButton.setAccel(self.__tr("Alt+A"))


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
