# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/template_plugin/TemplateFormDesign.ui'
#
# Created: Sun Aug 29 00:49:08 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.12
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class TemplateFormDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("TemplateFormDesign")


        TemplateFormDesignLayout = QGridLayout(self,1,1,11,6,"TemplateFormDesignLayout")

        self.groupBox2 = QGroupBox(self,"groupBox2")
        self.groupBox2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2.layout().setSpacing(6)
        self.groupBox2.layout().setMargin(11)
        groupBox2Layout = QGridLayout(self.groupBox2.layout())
        groupBox2Layout.setAlignment(Qt.AlignTop)

        self.infoView = QListView(self.groupBox2,"infoView")
        self.infoView.addColumn(self.__tr("Type"))
        self.infoView.addColumn(self.__tr("Name"))
        self.infoView.addColumn(self.__tr("Must"))
        self.infoView.addColumn(self.__tr("Single"))
        self.infoView.addColumn(self.__tr("Show"))
        self.infoView.setAllColumnsShowFocus(1)
        self.infoView.setResizeMode(QListView.AllColumns)

        groupBox2Layout.addMultiCellWidget(self.infoView,0,0,0,2)

        self.saveButton = QPushButton(self.groupBox2,"saveButton")

        groupBox2Layout.addWidget(self.saveButton,1,2)

        self.classButton = QPushButton(self.groupBox2,"classButton")

        groupBox2Layout.addWidget(self.classButton,1,1)
        spacer6 = QSpacerItem(220,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox2Layout.addItem(spacer6,1,0)

        TemplateFormDesignLayout.addWidget(self.groupBox2,1,0)

        self.groupBox2_2 = QGroupBox(self,"groupBox2_2")
        self.groupBox2_2.setSizePolicy(QSizePolicy(5,5,0,0,self.groupBox2_2.sizePolicy().hasHeightForWidth()))
        self.groupBox2_2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2_2.layout().setSpacing(6)
        self.groupBox2_2.layout().setMargin(11)
        groupBox2_2Layout = QGridLayout(self.groupBox2_2.layout())
        groupBox2_2Layout.setAlignment(Qt.AlignTop)

        self.delTemplateButton = QPushButton(self.groupBox2_2,"delTemplateButton")

        groupBox2_2Layout.addWidget(self.delTemplateButton,1,1)
        spacer5 = QSpacerItem(31,7,QSizePolicy.Minimum,QSizePolicy.Preferred)
        groupBox2_2Layout.addItem(spacer5,2,1)

        self.addTemplateButton = QPushButton(self.groupBox2_2,"addTemplateButton")

        groupBox2_2Layout.addWidget(self.addTemplateButton,0,1)

        self.templateView = QListView(self.groupBox2_2,"templateView")
        self.templateView.addColumn(self.__tr("Template Name"))
        self.templateView.setSizePolicy(QSizePolicy(3,0,0,0,self.templateView.sizePolicy().hasHeightForWidth()))
        self.templateView.setResizeMode(QListView.AllColumns)

        groupBox2_2Layout.addMultiCellWidget(self.templateView,0,2,0,0)

        TemplateFormDesignLayout.addWidget(self.groupBox2_2,0,0)

        self.languageChange()

        self.resize(QSize(367,392).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.addTemplateButton,SIGNAL("clicked()"),self.add_template)
        self.connect(self.delTemplateButton,SIGNAL("clicked()"),self.delete_template)
        self.connect(self.templateView,SIGNAL("selectionChanged()"),self.update_view)
        self.connect(self.classButton,SIGNAL("clicked()"),self.edit_classes)
        self.connect(self.saveButton,SIGNAL("clicked()"),self.save_template)
        self.connect(self.infoView,SIGNAL("doubleClicked(QListViewItem*)"),self.toggleShow)


    def languageChange(self):
        self.setCaption(self.__tr("TemplateFormDesign"))
        self.groupBox2.setTitle(self.__tr("Template Info"))
        self.infoView.header().setLabel(0,self.__tr("Type"))
        self.infoView.header().setLabel(1,self.__tr("Name"))
        self.infoView.header().setLabel(2,self.__tr("Must"))
        self.infoView.header().setLabel(3,self.__tr("Single"))
        self.infoView.header().setLabel(4,self.__tr("Show"))
        self.saveButton.setText(self.__tr("&Save"))
        self.saveButton.setAccel(self.__tr("Alt+S"))
        self.classButton.setText(self.__tr("&Edit..."))
        self.classButton.setAccel(self.__tr("Alt+E"))
        self.groupBox2_2.setTitle(self.__tr("Template List"))
        self.delTemplateButton.setText(self.__tr("&Delete"))
        self.delTemplateButton.setAccel(self.__tr("Alt+D"))
        self.addTemplateButton.setText(self.__tr("&Add..."))
        self.addTemplateButton.setAccel(self.__tr("Alt+A"))
        self.templateView.header().setLabel(0,self.__tr("Template Name"))


    def add_template(self):
        print "TemplateFormDesign.add_template(): Not implemented yet"

    def delete_template(self):
        print "TemplateFormDesign.delete_template(): Not implemented yet"

    def update_view(self):
        print "TemplateFormDesign.update_view(): Not implemented yet"

    def edit_classes(self):
        print "TemplateFormDesign.edit_classes(): Not implemented yet"

    def edit_attributes(self):
        print "TemplateFormDesign.edit_attributes(): Not implemented yet"

    def save_template(self):
        print "TemplateFormDesign.save_template(): Not implemented yet"

    def toggleShow(self):
        print "TemplateFormDesign.toggleShow(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("TemplateFormDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = TemplateFormDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
