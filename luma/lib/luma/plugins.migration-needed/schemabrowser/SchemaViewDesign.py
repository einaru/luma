# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/schemabrowser/SchemaViewDesign.ui'
#
# Created: Wed Aug 17 15:23:52 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt4.QtGui import *


class SchemaViewDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("SchemaViewDesign")


        SchemaViewDesignLayout = QVBoxLayout(self,6,6,"SchemaViewDesignLayout")

        self.splitter4 = QSplitter(self,"splitter4")
        self.splitter4.setOrientation(QSplitter.Horizontal)

        LayoutWidget = QWidget(self.splitter4,"layout2")
        layout2 = QGridLayout(LayoutWidget,1,1,2,6,"layout2")

        self.serverBox = QComboBox(0,LayoutWidget,"serverBox")

        layout2.addWidget(self.serverBox,0,1)

        self.textLabel1 = QLabel(LayoutWidget,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))

        layout2.addWidget(self.textLabel1,0,0)

        self.toolBox = QToolBox(LayoutWidget,"toolBox")
        self.toolBox.setCurrentIndex(3)

        self.page1 = QWidget(self.toolBox,"page1")
        self.page1.setBackgroundMode(QWidget.PaletteBackground)
        page1Layout = QGridLayout(self.page1,1,1,6,6,"page1Layout")

        self.textLabel2 = QLabel(self.page1,"textLabel2")

        page1Layout.addWidget(self.textLabel2,0,0)

        self.classFilterEdit = QLineEdit(self.page1,"classFilterEdit")

        page1Layout.addWidget(self.classFilterEdit,0,1)

        self.classBox = QListBox(self.page1,"classBox")

        page1Layout.addMultiCellWidget(self.classBox,1,1,0,1)
        self.toolBox.addItem(self.page1,QString.fromLatin1(""))

        self.page2 = QWidget(self.toolBox,"page2")
        self.page2.setBackgroundMode(QWidget.PaletteBackground)
        page2Layout = QGridLayout(self.page2,1,1,6,6,"page2Layout")

        self.textLabel3 = QLabel(self.page2,"textLabel3")

        page2Layout.addWidget(self.textLabel3,0,0)

        self.attributeFilterEdit = QLineEdit(self.page2,"attributeFilterEdit")

        page2Layout.addWidget(self.attributeFilterEdit,0,1)

        self.attributeBox = QListBox(self.page2,"attributeBox")

        page2Layout.addMultiCellWidget(self.attributeBox,1,1,0,1)
        self.toolBox.addItem(self.page2,QString.fromLatin1(""))

        self.page = QWidget(self.toolBox,"page")
        self.page.setBackgroundMode(QWidget.PaletteBackground)
        pageLayout = QGridLayout(self.page,1,1,6,6,"pageLayout")

        self.matchingBox = QListBox(self.page,"matchingBox")

        pageLayout.addMultiCellWidget(self.matchingBox,1,1,0,1)

        self.matchingFilterEdit = QLineEdit(self.page,"matchingFilterEdit")

        pageLayout.addWidget(self.matchingFilterEdit,0,1)

        self.textLabel3_3 = QLabel(self.page,"textLabel3_3")

        pageLayout.addWidget(self.textLabel3_3,0,0)
        self.toolBox.addItem(self.page,QString.fromLatin1(""))

        self.page_2 = QWidget(self.toolBox,"page_2")
        self.page_2.setBackgroundMode(QWidget.PaletteBackground)
        pageLayout_2 = QGridLayout(self.page_2,1,1,6,6,"pageLayout_2")

        self.syntaxBox = QListBox(self.page_2,"syntaxBox")

        pageLayout_2.addMultiCellWidget(self.syntaxBox,1,1,0,1)

        self.syntaxFilterEdi = QLineEdit(self.page_2,"syntaxFilterEdi")

        pageLayout_2.addWidget(self.syntaxFilterEdi,0,1)

        self.textLabel3_4 = QLabel(self.page_2,"textLabel3_4")

        pageLayout_2.addWidget(self.textLabel3_4,0,0)
        self.toolBox.addItem(self.page_2,QString.fromLatin1(""))

        layout2.addMultiCellWidget(self.toolBox,1,1,0,1)

        self.widgetStack = QWidgetStack(self.splitter4,"widgetStack")
        self.widgetStack.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred,0,0,self.widgetStack.sizePolicy().hasHeightForWidth()))

        self.WStackPage = QWidget(self.widgetStack,"WStackPage")
        WStackPageLayout = QGridLayout(self.WStackPage,1,1,3,6,"WStackPageLayout")

        self.classLabel = QLabel(self.WStackPage,"classLabel")

        WStackPageLayout.addMultiCellWidget(self.classLabel,0,0,0,2)
        spacer1 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        WStackPageLayout.addItem(spacer1,1,1)

        layout6 = QGridLayout(None,1,1,0,6,"layout6")

        self.oidClassEdit = QLineEdit(self.WStackPage,"oidClassEdit")
        self.oidClassEdit.setReadOnly(1)

        layout6.addWidget(self.oidClassEdit,1,1)

        self.textLabel8 = QLabel(self.WStackPage,"textLabel8")

        layout6.addWidget(self.textLabel8,2,0)

        self.textLabel7 = QLabel(self.WStackPage,"textLabel7")

        layout6.addWidget(self.textLabel7,1,0)

        self.textLabel12 = QLabel(self.WStackPage,"textLabel12")

        layout6.addWidget(self.textLabel12,0,0)

        self.kindClassEdit = QLineEdit(self.WStackPage,"kindClassEdit")
        self.kindClassEdit.setReadOnly(1)

        layout6.addWidget(self.kindClassEdit,2,1)

        self.superiorClassEdit = QLineEdit(self.WStackPage,"superiorClassEdit")
        self.superiorClassEdit.setReadOnly(1)

        layout6.addWidget(self.superiorClassEdit,0,1)

        WStackPageLayout.addMultiCellLayout(layout6,2,2,0,2)

        layout8 = QVBoxLayout(None,0,6,"layout8")

        self.textLabel14 = QLabel(self.WStackPage,"textLabel14")
        self.textLabel14.setAlignment(QLabel.AlignVCenter)
        layout8.addWidget(self.textLabel14)

        self.mustAttributeBox = QListBox(self.WStackPage,"mustAttributeBox")
        layout8.addWidget(self.mustAttributeBox)

        WStackPageLayout.addLayout(layout8,3,0)
        spacer3 = QSpacerItem(16,21,QSizePolicy.Fixed,QSizePolicy.Minimum)
        WStackPageLayout.addItem(spacer3,3,1)

        layout9 = QVBoxLayout(None,0,6,"layout9")

        self.textLabel13 = QLabel(self.WStackPage,"textLabel13")
        self.textLabel13.setAlignment(QLabel.AlignVCenter)
        layout9.addWidget(self.textLabel13)

        self.mayAttributeBox = QListBox(self.WStackPage,"mayAttributeBox")
        layout9.addWidget(self.mayAttributeBox)

        WStackPageLayout.addLayout(layout9,3,2)
        self.widgetStack.addWidget(self.WStackPage,0)

        self.WStackPage_2 = QWidget(self.widgetStack,"WStackPage_2")
        WStackPageLayout_2 = QGridLayout(self.WStackPage_2,1,1,6,6,"WStackPageLayout_2")
        spacer1_2 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        WStackPageLayout_2.addItem(spacer1_2,1,2)

        self.attributeLabel = QLabel(self.WStackPage_2,"attributeLabel")

        WStackPageLayout_2.addMultiCellWidget(self.attributeLabel,0,0,0,2)

        layout9_2 = QVBoxLayout(None,0,6,"layout9_2")

        self.textLabel8_2 = QLabel(self.WStackPage_2,"textLabel8_2")
        self.textLabel8_2.setAlignment(QLabel.AlignVCenter)
        layout9_2.addWidget(self.textLabel8_2)

        self.usedInClassBox = QListBox(self.WStackPage_2,"usedInClassBox")
        layout9_2.addWidget(self.usedInClassBox)

        WStackPageLayout_2.addMultiCellLayout(layout9_2,6,7,2,2)
        spacer6 = QSpacerItem(16,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        WStackPageLayout_2.addItem(spacer6,6,1)
        spacer5 = QSpacerItem(21,90,QSizePolicy.Minimum,QSizePolicy.Expanding)
        WStackPageLayout_2.addItem(spacer5,7,0)

        layout8_2 = QVBoxLayout(None,0,6,"layout8_2")

        self.singleAttributeBox = QCheckBox(self.WStackPage_2,"singleAttributeBox")
        self.singleAttributeBox.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.singleAttributeBox.sizePolicy().hasHeightForWidth()))
        layout8_2.addWidget(self.singleAttributeBox)

        self.collectiveAttributeBox = QCheckBox(self.WStackPage_2,"collectiveAttributeBox")
        self.collectiveAttributeBox.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.collectiveAttributeBox.sizePolicy().hasHeightForWidth()))
        layout8_2.addWidget(self.collectiveAttributeBox)

        self.obsoleteAttributeBox = QCheckBox(self.WStackPage_2,"obsoleteAttributeBox")
        self.obsoleteAttributeBox.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.obsoleteAttributeBox.sizePolicy().hasHeightForWidth()))
        layout8_2.addWidget(self.obsoleteAttributeBox)

        WStackPageLayout_2.addLayout(layout8_2,6,0)
        spacer7 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        WStackPageLayout_2.addItem(spacer7,5,2)

        layout13 = QGridLayout(None,1,1,0,6,"layout13")

        self.textLabel6 = QLabel(self.WStackPage_2,"textLabel6")

        layout13.addWidget(self.textLabel6,0,0)

        self.syntaxAttributeEdit = QLineEdit(self.WStackPage_2,"syntaxAttributeEdit")
        self.syntaxAttributeEdit.setReadOnly(1)

        layout13.addWidget(self.syntaxAttributeEdit,0,1)

        self.textLabel7_2 = QLabel(self.WStackPage_2,"textLabel7_2")

        layout13.addWidget(self.textLabel7_2,1,0)

        self.orderingAttributeEdit = QLineEdit(self.WStackPage_2,"orderingAttributeEdit")
        self.orderingAttributeEdit.setReadOnly(1)

        layout13.addWidget(self.orderingAttributeEdit,1,1)

        WStackPageLayout_2.addMultiCellLayout(layout13,4,4,0,2)
        spacer4 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        WStackPageLayout_2.addItem(spacer4,3,2)

        layout14 = QGridLayout(None,1,1,0,6,"layout14")

        self.equalityAttributeEdit = QLineEdit(self.WStackPage_2,"equalityAttributeEdit")
        self.equalityAttributeEdit.setReadOnly(1)

        layout14.addWidget(self.equalityAttributeEdit,2,1)

        self.textLabel3_2 = QLabel(self.WStackPage_2,"textLabel3_2")

        layout14.addWidget(self.textLabel3_2,0,0)

        self.textLabel4 = QLabel(self.WStackPage_2,"textLabel4")

        layout14.addWidget(self.textLabel4,3,0)

        self.usageAttributeEdit = QLineEdit(self.WStackPage_2,"usageAttributeEdit")
        self.usageAttributeEdit.setReadOnly(1)

        layout14.addWidget(self.usageAttributeEdit,3,1)

        self.superiorAttributeEdit = QLineEdit(self.WStackPage_2,"superiorAttributeEdit")
        self.superiorAttributeEdit.setReadOnly(1)

        layout14.addWidget(self.superiorAttributeEdit,1,1)

        self.oidAttributeEdit = QLineEdit(self.WStackPage_2,"oidAttributeEdit")
        self.oidAttributeEdit.setReadOnly(1)

        layout14.addWidget(self.oidAttributeEdit,0,1)

        self.textLabel2_2 = QLabel(self.WStackPage_2,"textLabel2_2")

        layout14.addWidget(self.textLabel2_2,1,0)

        self.textLabel5 = QLabel(self.WStackPage_2,"textLabel5")

        layout14.addWidget(self.textLabel5,2,0)

        WStackPageLayout_2.addMultiCellLayout(layout14,2,2,0,2)
        self.widgetStack.addWidget(self.WStackPage_2,1)

        self.WStackPage_3 = QWidget(self.widgetStack,"WStackPage_3")
        WStackPageLayout_3 = QVBoxLayout(self.WStackPage_3,6,6,"WStackPageLayout_3")

        self.matchingLabel = QLabel(self.WStackPage_3,"matchingLabel")
        WStackPageLayout_3.addWidget(self.matchingLabel)
        spacer1_2_2 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        WStackPageLayout_3.addItem(spacer1_2_2)

        layout19 = QGridLayout(None,1,1,0,6,"layout19")

        self.textLabel15 = QLabel(self.WStackPage_3,"textLabel15")

        layout19.addWidget(self.textLabel15,1,0)

        self.oidMatchingEdit = QLineEdit(self.WStackPage_3,"oidMatchingEdit")

        layout19.addWidget(self.oidMatchingEdit,0,1)

        self.textLabel14_2 = QLabel(self.WStackPage_3,"textLabel14_2")

        layout19.addWidget(self.textLabel14_2,0,0)

        self.syntaxMatchingEdit = QLineEdit(self.WStackPage_3,"syntaxMatchingEdit")

        layout19.addWidget(self.syntaxMatchingEdit,1,1)
        WStackPageLayout_3.addLayout(layout19)
        spacer1_2_2_3 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        WStackPageLayout_3.addItem(spacer1_2_2_3)

        self.textLabel16 = QLabel(self.WStackPage_3,"textLabel16")
        self.textLabel16.setAlignment(QLabel.AlignVCenter)
        WStackPageLayout_3.addWidget(self.textLabel16)

        self.attributeMatchingBox = QListBox(self.WStackPage_3,"attributeMatchingBox")
        WStackPageLayout_3.addWidget(self.attributeMatchingBox)
        self.widgetStack.addWidget(self.WStackPage_3,2)

        self.WStackPage_4 = QWidget(self.widgetStack,"WStackPage_4")
        WStackPageLayout_4 = QGridLayout(self.WStackPage_4,1,1,6,6,"WStackPageLayout_4")

        self.textLabel10 = QLabel(self.WStackPage_4,"textLabel10")

        WStackPageLayout_4.addWidget(self.textLabel10,2,0)
        spacer8 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        WStackPageLayout_4.addItem(spacer8,1,1)

        self.syntaxLabel = QLabel(self.WStackPage_4,"syntaxLabel")

        WStackPageLayout_4.addMultiCellWidget(self.syntaxLabel,0,0,0,1)
        spacer9 = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        WStackPageLayout_4.addItem(spacer9,3,1)

        self.oidSyntaxEdit = QLineEdit(self.WStackPage_4,"oidSyntaxEdit")
        self.oidSyntaxEdit.setReadOnly(1)

        WStackPageLayout_4.addWidget(self.oidSyntaxEdit,2,1)

        layout18 = QGridLayout(None,1,1,0,6,"layout18")

        self.textLabel11 = QLabel(self.WStackPage_4,"textLabel11")

        layout18.addWidget(self.textLabel11,0,0)

        self.matchingSyntaxBox = QListBox(self.WStackPage_4,"matchingSyntaxBox")

        layout18.addWidget(self.matchingSyntaxBox,1,2)

        self.textLabel12_2 = QLabel(self.WStackPage_4,"textLabel12_2")
        self.textLabel12_2.setAlignment(QLabel.AlignVCenter)

        layout18.addWidget(self.textLabel12_2,0,2)
        spacer10 = QSpacerItem(16,21,QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout18.addItem(spacer10,1,1)

        self.attributeSyntaxlistBox = QListBox(self.WStackPage_4,"attributeSyntaxlistBox")

        layout18.addWidget(self.attributeSyntaxlistBox,1,0)

        WStackPageLayout_4.addMultiCellLayout(layout18,4,4,0,1)
        self.widgetStack.addWidget(self.WStackPage_4,3)
        SchemaViewDesignLayout.addWidget(self.splitter4)

        self.languageChange()

        self.resize(QSize(639,501).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.serverBox,SIGNAL("activated(const QString&)"),self.serverChanged)
        self.connect(self.toolBox,SIGNAL("currentChanged(int)"),self.toolBoxChanged)
        self.connect(self.classBox,SIGNAL("selectionChanged(QListBoxItem*)"),self.classSelected)
        self.connect(self.classFilterEdit,SIGNAL("textChanged(const QString&)"),self.classFilterChanged)
        self.connect(self.attributeFilterEdit,SIGNAL("textChanged(const QString&)"),self.attributeFilterChanged)
        self.connect(self.attributeBox,SIGNAL("selectionChanged(QListBoxItem*)"),self.attributeSelected)
        self.connect(self.syntaxFilterEdi,SIGNAL("textChanged(const QString&)"),self.syntaxFilterChanged)
        self.connect(self.syntaxBox,SIGNAL("selectionChanged(QListBoxItem*)"),self.syntaxSelected)
        self.connect(self.matchingFilterEdit,SIGNAL("textChanged(const QString&)"),self.matchingFilterChanged)
        self.connect(self.matchingBox,SIGNAL("selectionChanged(QListBoxItem*)"),self.matchingRuleSelected)
        self.connect(self.mustAttributeBox,SIGNAL("doubleClicked(QListBoxItem*)"),self.attributeDoubleClicked)
        self.connect(self.mayAttributeBox,SIGNAL("doubleClicked(QListBoxItem*)"),self.attributeDoubleClicked)
        self.connect(self.attributeMatchingBox,SIGNAL("doubleClicked(QListBoxItem*)"),self.attributeDoubleClicked)
        self.connect(self.attributeSyntaxlistBox,SIGNAL("doubleClicked(QListBoxItem*)"),self.attributeDoubleClicked)
        self.connect(self.usedInClassBox,SIGNAL("doubleClicked(QListBoxItem*)"),self.objectClassDoubleClicked)
        self.connect(self.matchingSyntaxBox,SIGNAL("doubleClicked(QListBoxItem*)"),self.matchingRuleDoubleClicked)
        self.connect(self.singleAttributeBox,SIGNAL("clicked()"),self.singleAttributeBox.toggle)
        self.connect(self.collectiveAttributeBox,SIGNAL("clicked()"),self.collectiveAttributeBox.toggle)
        self.connect(self.obsoleteAttributeBox,SIGNAL("clicked()"),self.obsoleteAttributeBox.toggle)

        self.setTabOrder(self.serverBox,self.classFilterEdit)
        self.setTabOrder(self.classFilterEdit,self.classBox)
        self.setTabOrder(self.classBox,self.attributeFilterEdit)
        self.setTabOrder(self.attributeFilterEdit,self.attributeBox)
        self.setTabOrder(self.attributeBox,self.matchingFilterEdit)
        self.setTabOrder(self.matchingFilterEdit,self.matchingBox)
        self.setTabOrder(self.matchingBox,self.syntaxFilterEdi)
        self.setTabOrder(self.syntaxFilterEdi,self.syntaxBox)
        self.setTabOrder(self.syntaxBox,self.superiorClassEdit)
        self.setTabOrder(self.superiorClassEdit,self.oidClassEdit)
        self.setTabOrder(self.oidClassEdit,self.kindClassEdit)
        self.setTabOrder(self.kindClassEdit,self.mustAttributeBox)
        self.setTabOrder(self.mustAttributeBox,self.mayAttributeBox)
        self.setTabOrder(self.mayAttributeBox,self.oidAttributeEdit)
        self.setTabOrder(self.oidAttributeEdit,self.superiorAttributeEdit)
        self.setTabOrder(self.superiorAttributeEdit,self.equalityAttributeEdit)
        self.setTabOrder(self.equalityAttributeEdit,self.usageAttributeEdit)
        self.setTabOrder(self.usageAttributeEdit,self.syntaxAttributeEdit)
        self.setTabOrder(self.syntaxAttributeEdit,self.orderingAttributeEdit)
        self.setTabOrder(self.orderingAttributeEdit,self.singleAttributeBox)
        self.setTabOrder(self.singleAttributeBox,self.collectiveAttributeBox)
        self.setTabOrder(self.collectiveAttributeBox,self.obsoleteAttributeBox)
        self.setTabOrder(self.obsoleteAttributeBox,self.usedInClassBox)
        self.setTabOrder(self.usedInClassBox,self.oidMatchingEdit)
        self.setTabOrder(self.oidMatchingEdit,self.syntaxMatchingEdit)
        self.setTabOrder(self.syntaxMatchingEdit,self.attributeMatchingBox)
        self.setTabOrder(self.attributeMatchingBox,self.oidSyntaxEdit)
        self.setTabOrder(self.oidSyntaxEdit,self.attributeSyntaxlistBox)
        self.setTabOrder(self.attributeSyntaxlistBox,self.matchingSyntaxBox)


    def languageChange(self):
        self.setCaption(self.__tr("Form"))
        self.textLabel1.setText(self.__tr("Server:"))
        self.textLabel2.setText(self.__tr("Filter:"))
        self.toolBox.setItemLabel(self.toolBox.indexOf(self.page1),self.__tr("ObjectClasses"))
        self.textLabel3.setText(self.__tr("Filter:"))
        self.toolBox.setItemLabel(self.toolBox.indexOf(self.page2),self.__tr("Attributes"))
        self.textLabel3_3.setText(self.__tr("Filter:"))
        self.toolBox.setItemLabel(self.toolBox.indexOf(self.page),self.__tr("Matching rules"))
        self.textLabel3_4.setText(self.__tr("Filter:"))
        self.toolBox.setItemLabel(self.toolBox.indexOf(self.page_2),self.__tr("LDAP syntaxes"))
        self.classLabel.setText(self.__tr("<b>Class Name</b><br>\n"
"Description"))
        self.textLabel8.setText(self.__tr("Kind:"))
        self.textLabel7.setText(self.__tr("OID:"))
        self.textLabel12.setText(self.__tr("Superior:"))
        self.textLabel14.setText(self.__tr("<b>Required attributes</b>"))
        self.textLabel13.setText(self.__tr("<b>Allowed attributes</b>"))
        self.attributeLabel.setText(self.__tr("<b>Attribute name</b><br>\n"
"Description"))
        self.textLabel8_2.setText(self.__tr("<b>Used in ObjectClasses</b>"))
        self.singleAttributeBox.setText(self.__tr("Single value"))
        self.collectiveAttributeBox.setText(self.__tr("Collective"))
        self.obsoleteAttributeBox.setText(self.__tr("Obsolete"))
        self.textLabel6.setText(self.__tr("Syntax {length}:"))
        self.textLabel7_2.setText(self.__tr("Ordering:"))
        self.textLabel3_2.setText(self.__tr("OID:"))
        self.textLabel4.setText(self.__tr("Usage:"))
        self.textLabel2_2.setText(self.__tr("Superior:"))
        self.textLabel5.setText(self.__tr("Equality:"))
        self.matchingLabel.setText(self.__tr("<b>Matching rule</b><br>\n"
"Description"))
        self.textLabel15.setText(self.__tr("Syntax:"))
        self.textLabel14_2.setText(self.__tr("OID:"))
        self.textLabel16.setText(self.__tr("<b>Used in Attribute</b>"))
        self.textLabel10.setText(self.__tr("OID:"))
        self.syntaxLabel.setText(self.__tr("<b>Syntax</b><br>\n"
"Description"))
        self.textLabel11.setText(self.__tr("<b>Used in attributes</b>"))
        self.textLabel12_2.setText(self.__tr("<b>Used in matching rules</b>"))


    def serverChanged(self):
        print "SchemaViewDesign.serverChanged(): Not implemented yet"

    def toolBoxChanged(self):
        print "SchemaViewDesign.toolBoxChanged(): Not implemented yet"

    def classSelected(self):
        print "SchemaViewDesign.classSelected(): Not implemented yet"

    def classFilterChanged(self):
        print "SchemaViewDesign.classFilterChanged(): Not implemented yet"

    def attributeFilterChanged(self):
        print "SchemaViewDesign.attributeFilterChanged(): Not implemented yet"

    def attributeSelected(self):
        print "SchemaViewDesign.attributeSelected(): Not implemented yet"

    def syntaxFilterChanged(self):
        print "SchemaViewDesign.syntaxFilterChanged(): Not implemented yet"

    def syntaxSelected(self):
        print "SchemaViewDesign.syntaxSelected(): Not implemented yet"

    def matchingFilterChanged(self):
        print "SchemaViewDesign.matchingFilterChanged(): Not implemented yet"

    def matchingRuleSelected(self):
        print "SchemaViewDesign.matchingRuleSelected(): Not implemented yet"

    def attributeDoubleClicked(self):
        print "SchemaViewDesign.attributeDoubleClicked(): Not implemented yet"

    def objectClassDoubleClicked(self):
        print "SchemaViewDesign.objectClassDoubleClicked(): Not implemented yet"

    def matchingRuleDoubleClicked(self):
        print "SchemaViewDesign.matchingRuleDoubleClicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("SchemaViewDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = SchemaViewDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
