# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/template_plugin/OClassDialogDesign.ui'
#
# Created: Tue Mar 30 20:13:10 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
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
        self.splitter8_2.setMinimumSize(QSize(241,80))
        self.splitter8_2.setOrientation(QSplitter.Horizontal)

        self.classView = QListView(self.splitter8_2,"classView")
        self.classView.addColumn(self.__tr("ObjectClass"))
        self.classView.setSizePolicy(QSizePolicy(4,4,0,0,self.classView.sizePolicy().hasHeightForWidth()))
        self.classView.setResizeMode(QListView.AllColumns)

        self.attributeView = QListView(self.splitter8_2,"attributeView")
        self.attributeView.addColumn(self.__tr("Attribute"))
        self.attributeView.setSizePolicy(QSizePolicy(4,4,0,0,self.attributeView.sizePolicy().hasHeightForWidth()))
        self.attributeView.setResizeMode(QListView.AllColumns)

        OClassDialogDesignLayout.addMultiCellWidget(self.splitter8_2,3,3,0,3)

        self.textLabel2_2 = QLabel(self,"textLabel2_2")

        OClassDialogDesignLayout.addWidget(self.textLabel2_2,1,0)

        self.textLabel1_2 = QLabel(self,"textLabel1_2")

        OClassDialogDesignLayout.addWidget(self.textLabel1_2,0,0)

        self.classBox = QComboBox(0,self,"classBox")

        OClassDialogDesignLayout.addMultiCellWidget(self.classBox,1,1,1,3)

        self.serverBox = QComboBox(0,self,"serverBox")

        OClassDialogDesignLayout.addMultiCellWidget(self.serverBox,0,0,1,3)

        self.addButton = QPushButton(self,"addButton")

        OClassDialogDesignLayout.addWidget(self.addButton,2,3)

        self.deleteButton = QPushButton(self,"deleteButton")
        self.deleteButton.setSizePolicy(QSizePolicy(1,1,0,0,self.deleteButton.sizePolicy().hasHeightForWidth()))

        OClassDialogDesignLayout.addWidget(self.deleteButton,2,2)
        spacer6_2 = QSpacerItem(250,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        OClassDialogDesignLayout.addItem(spacer6_2,2,1)

        layout1 = QHBoxLayout(None,0,6,"layout1")
        spacer4 = QSpacerItem(330,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout1.addItem(spacer4)

        self.okButton = QPushButton(self,"okButton")
        layout1.addWidget(self.okButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        layout1.addWidget(self.cancelButton)

        OClassDialogDesignLayout.addMultiCellLayout(layout1,4,4,0,3)

        self.languageChange()

        self.resize(QSize(508,533).expandedTo(self.minimumSizeHint()))
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
        self.textLabel2_2.setText(self.__tr("Object Class:"))
        self.textLabel1_2.setText(self.__tr("Server:"))
        self.addButton.setText(self.__tr("&Add"))
        self.addButton.setAccel(self.__tr("Alt+A"))
        self.deleteButton.setText(self.__tr("&Delete"))
        self.deleteButton.setAccel(self.__tr("Alt+D"))
        self.okButton.setText(self.__tr("&Ok"))
        self.okButton.setAccel(self.__tr("Alt+O"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))


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
