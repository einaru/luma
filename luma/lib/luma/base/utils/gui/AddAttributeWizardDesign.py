# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/AddAttributeWizardDesign.ui'
#
# Created: Thu Apr 29 18:00:27 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class AddAttributeWizardDesign(QWizard):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QWizard.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("AddAttributeWizardDesign")



        self.WizardPage = QWidget(self,"WizardPage")
        WizardPageLayout = QGridLayout(self.WizardPage,1,1,11,6,"WizardPageLayout")

        self.imageLabel = QLabel(self.WizardPage,"imageLabel")
        self.imageLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.imageLabel.sizePolicy().hasHeightForWidth()))
        self.imageLabel.setMinimumSize(QSize(64,64))

        WizardPageLayout.addWidget(self.imageLabel,0,0)
        spacer3 = QSpacerItem(21,260,QSizePolicy.Minimum,QSizePolicy.Expanding)
        WizardPageLayout.addItem(spacer3,5,1)

        self.enableAllBox = QCheckBox(self.WizardPage,"enableAllBox")

        WizardPageLayout.addMultiCellWidget(self.enableAllBox,4,4,0,1)

        self.attributeBox = QComboBox(0,self.WizardPage,"attributeBox")

        WizardPageLayout.addWidget(self.attributeBox,3,1)

        self.textLabel4 = QLabel(self.WizardPage,"textLabel4")
        self.textLabel4.setSizePolicy(QSizePolicy(0,0,0,0,self.textLabel4.sizePolicy().hasHeightForWidth()))

        WizardPageLayout.addWidget(self.textLabel4,3,0)

        self.line3 = QFrame(self.WizardPage,"line3")
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setFrameShadow(QFrame.Sunken)
        self.line3.setFrameShape(QFrame.HLine)

        WizardPageLayout.addMultiCellWidget(self.line3,2,2,0,1)
        spacer5 = QSpacerItem(20,50,QSizePolicy.Minimum,QSizePolicy.Fixed)
        WizardPageLayout.addItem(spacer5,1,0)

        self.textLabel2 = QLabel(self.WizardPage,"textLabel2")

        WizardPageLayout.addMultiCellWidget(self.textLabel2,0,1,1,1)
        self.addPage(self.WizardPage,QString(""))

        self.WizardPage_2 = QWidget(self,"WizardPage_2")
        WizardPageLayout_2 = QGridLayout(self.WizardPage_2,1,1,11,6,"WizardPageLayout_2")

        self.line4 = QFrame(self.WizardPage_2,"line4")
        self.line4.setFrameShape(QFrame.HLine)
        self.line4.setFrameShadow(QFrame.Sunken)
        self.line4.setFrameShape(QFrame.HLine)

        WizardPageLayout_2.addMultiCellWidget(self.line4,2,2,0,1)

        self.textLabel2_2 = QLabel(self.WizardPage_2,"textLabel2_2")

        WizardPageLayout_2.addMultiCellWidget(self.textLabel2_2,0,1,1,1)

        self.splitter1 = QSplitter(self.WizardPage_2,"splitter1")
        self.splitter1.setOrientation(QSplitter.Horizontal)
        self.splitter1.setChildrenCollapsible(0)

        LayoutWidget = QWidget(self.splitter1,"layout1")
        layout1 = QVBoxLayout(LayoutWidget,11,6,"layout1")

        self.textLabel3_2 = QLabel(LayoutWidget,"textLabel3_2")
        layout1.addWidget(self.textLabel3_2)

        self.classBox = QListBox(LayoutWidget,"classBox")
        layout1.addWidget(self.classBox)

        LayoutWidget_2 = QWidget(self.splitter1,"layout2")
        layout2 = QVBoxLayout(LayoutWidget_2,11,6,"layout2")

        self.textLabel4_2 = QLabel(LayoutWidget_2,"textLabel4_2")
        layout2.addWidget(self.textLabel4_2)

        self.mustAttributeBox = QListBox(LayoutWidget_2,"mustAttributeBox")
        layout2.addWidget(self.mustAttributeBox)

        WizardPageLayout_2.addMultiCellWidget(self.splitter1,3,3,0,1)

        self.objectclassLabel = QLabel(self.WizardPage_2,"objectclassLabel")
        self.objectclassLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.objectclassLabel.sizePolicy().hasHeightForWidth()))
        self.objectclassLabel.setMinimumSize(QSize(64,64))

        WizardPageLayout_2.addWidget(self.objectclassLabel,0,0)
        spacer4 = QSpacerItem(21,31,QSizePolicy.Minimum,QSizePolicy.Fixed)
        WizardPageLayout_2.addItem(spacer4,1,0)
        self.addPage(self.WizardPage_2,QString(""))

        self.languageChange()

        self.resize(QSize(493,505).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.enableAllBox,SIGNAL("toggled(bool)"),self.initAttributeBox)
        self.connect(self.attributeBox,SIGNAL("activated(const QString&)"),self.newSelection)
        self.connect(self.classBox,SIGNAL("selectionChanged()"),self.classSelection)


    def languageChange(self):
        self.setCaption(self.__tr("Add Attribute"))
        self.imageLabel.setText(self.__tr("PI","DO NOT TRANSLATE"))
        self.enableAllBox.setText(self.__tr("Enable all attributes which are supported by the server."))
        self.textLabel4.setText(self.__tr("Attribute:"))
        self.textLabel2.setText(self.__tr("<p>Please select an attribute you want to add to the current entry.</p>\n"
"<p>By default only attributes which are supported by the current \n"
"objectclasses are displayed. If you want to add an attribute which is \n"
"supported by other objectclasses, please enable this functionality below.\n"
"</p>"))
        self.setTitle(self.WizardPage,self.__tr("Select Attribute"))
        self.textLabel2_2.setText(self.__tr("<p>You have chosen to add an attribute which is not supported by the \n"
"objectclasses for the current entry.</p>\n"
"<p>Please select an objectclass which supports the new attribute. The \n"
"list on the right shows all attributes which must be added additionally with\n"
"the selected objectclass.</p>"))
        self.textLabel3_2.setText(self.__tr("<b>Objectclass</b>"))
        self.textLabel4_2.setText(self.__tr("<b>Additional attributes</b>"))
        self.objectclassLabel.setText(self.__tr("CL"))
        self.setTitle(self.WizardPage_2,self.__tr("Choose objectclass"))


    def initAttributeBox(self):
        print "AddAttributeWizardDesign.initAttributeBox(): Not implemented yet"

    def newSelection(self):
        print "AddAttributeWizardDesign.newSelection(): Not implemented yet"

    def classSelection(self):
        print "AddAttributeWizardDesign.classSelection(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("AddAttributeWizardDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = AddAttributeWizardDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
