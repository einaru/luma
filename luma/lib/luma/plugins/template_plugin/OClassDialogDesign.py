# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/template_plugin/OClassDialogDesign.ui'
#
# Created: Thu Jan 1 17:35:31 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.8.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class OClassDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("OClassDialogDesign")


        OClassDialogDesignLayout = QGridLayout(self,1,1,11,6,"OClassDialogDesignLayout")

        self.splitter8_2 = QSplitter(self,"splitter8_2")
        self.splitter8_2.setMinimumSize(QSize(253,84))
        self.splitter8_2.setOrientation(QSplitter.Horizontal)

        self.classView = QListView(self.splitter8_2,"classView")
        self.classView.addColumn(self.__tr("ObjectClass"))
        self.classView.setSizePolicy(QSizePolicy(4,4,0,0,self.classView.sizePolicy().hasHeightForWidth()))
        self.classView.setResizeMode(QListView.AllColumns)

        self.attributeView = QListView(self.splitter8_2,"attributeView")
        self.attributeView.addColumn(self.__tr("Attribute"))
        self.attributeView.setSizePolicy(QSizePolicy(4,4,0,0,self.attributeView.sizePolicy().hasHeightForWidth()))
        self.attributeView.setResizeMode(QListView.AllColumns)

        OClassDialogDesignLayout.addMultiCellWidget(self.splitter8_2,3,3,0,5)

        self.okButton = QPushButton(self,"okButton")

        OClassDialogDesignLayout.addWidget(self.okButton,4,5)
        spacer = QSpacerItem(150,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        OClassDialogDesignLayout.addMultiCell(spacer,2,2,2,3)

        self.textLabel2_2 = QLabel(self,"textLabel2_2")

        OClassDialogDesignLayout.addWidget(self.textLabel2_2,1,0)

        self.textLabel1_2 = QLabel(self,"textLabel1_2")

        OClassDialogDesignLayout.addWidget(self.textLabel1_2,0,0)

        self.addButton = QPushButton(self,"addButton")

        OClassDialogDesignLayout.addMultiCellWidget(self.addButton,2,2,4,5)

        self.classBox = QComboBox(0,self,"classBox")

        OClassDialogDesignLayout.addMultiCellWidget(self.classBox,1,1,1,5)

        self.deleteButton = QPushButton(self,"deleteButton")

        OClassDialogDesignLayout.addWidget(self.deleteButton,2,1)

        self.serverBox = QComboBox(0,self,"serverBox")

        OClassDialogDesignLayout.addMultiCellWidget(self.serverBox,0,0,1,5)
        spacer_2 = QSpacerItem(131,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        OClassDialogDesignLayout.addMultiCell(spacer_2,4,4,0,2)

        self.cancelButton = QPushButton(self,"cancelButton")

        OClassDialogDesignLayout.addMultiCellWidget(self.cancelButton,4,4,3,4)

        self.languageChange()

        self.resize(QSize(508,531).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.okButton,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.cancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.addButton,SIGNAL("clicked()"),self.add_class)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.delete_class)
        self.connect(self.serverBox,SIGNAL("activated(const QString&)"),self.server_selected)

        self.setTabOrder(self.cancelButton,self.okButton)


    def languageChange(self):
        self.setCaption(self.__tr("Luma"))
        self.classView.header().setLabel(0,self.__tr("ObjectClass"))
        self.attributeView.header().setLabel(0,self.__tr("Attribute"))
        self.okButton.setText(self.__tr("Ok"))
        self.textLabel2_2.setText(self.__tr("ObjectClass:"))
        self.textLabel1_2.setText(self.__tr("Server:"))
        self.addButton.setText(self.__tr("Add ObjectClass"))
        self.deleteButton.setText(self.__tr("Delete selected Class"))
        self.cancelButton.setText(self.__tr("Cancel"))


    def add_class(self):
        print "OClassDialogDesign.add_class(): Not implemented yet"

    def delete_class(self):
        print "OClassDialogDesign.delete_class(): Not implemented yet"

    def server_selected(self):
        print "OClassDialogDesign.server_selected(): Not implemented yet"

    def class_selected(self):
        print "OClassDialogDesign.class_selected(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("OClassDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = OClassDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
