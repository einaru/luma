# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/LumaEntryBrowserDesign.ui'
#
# Created: Mon Apr 26 16:00:33 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class LumaEntryBrowserDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("LumaEntryBrowserDesign")


        LumaEntryBrowserDesignLayout = QGridLayout(self,1,1,11,6,"LumaEntryBrowserDesignLayout")

        self.goButton = QPushButton(self,"goButton")

        LumaEntryBrowserDesignLayout.addWidget(self.goButton,1,3)

        self.searchEdit = QLineEdit(self,"searchEdit")

        LumaEntryBrowserDesignLayout.addWidget(self.searchEdit,1,2)

        self.textLabel13 = QLabel(self,"textLabel13")
        self.textLabel13.setFrameShape(QLabel.NoFrame)
        self.textLabel13.setFrameShadow(QLabel.Plain)

        LumaEntryBrowserDesignLayout.addMultiCellWidget(self.textLabel13,1,1,0,1)

        self.serverBox = QComboBox(0,self,"serverBox")

        LumaEntryBrowserDesignLayout.addMultiCellWidget(self.serverBox,0,0,2,3)

        self.textLabel12 = QLabel(self,"textLabel12")

        LumaEntryBrowserDesignLayout.addMultiCellWidget(self.textLabel12,0,0,0,1)

        layout1 = QHBoxLayout(None,0,6,"layout1")
        spacer5 = QSpacerItem(150,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout1.addItem(spacer5)

        self.addButton = QPushButton(self,"addButton")
        self.addButton.setSizePolicy(QSizePolicy(0,0,0,0,self.addButton.sizePolicy().hasHeightForWidth()))
        layout1.addWidget(self.addButton)

        self.deleteButton = QPushButton(self,"deleteButton")
        self.deleteButton.setSizePolicy(QSizePolicy(0,0,0,0,self.deleteButton.sizePolicy().hasHeightForWidth()))
        layout1.addWidget(self.deleteButton)

        LumaEntryBrowserDesignLayout.addMultiCellLayout(layout1,5,5,0,3)

        self.widgetStack = QWidgetStack(self,"widgetStack")

        self.WStackPage = QWidget(self.widgetStack,"WStackPage")
        WStackPageLayout = QVBoxLayout(self.WStackPage,0,0,"WStackPageLayout")

        self.itemIconView = QIconView(self.WStackPage,"itemIconView")
        self.itemIconView.setResizePolicy(QIconView.AutoOneFit)
        self.itemIconView.setGridX(100)
        self.itemIconView.setGridY(100)
        self.itemIconView.setResizeMode(QIconView.Adjust)
        self.itemIconView.setItemsMovable(0)
        WStackPageLayout.addWidget(self.itemIconView)
        self.widgetStack.addWidget(self.WStackPage,0)

        self.WStackPage_2 = QWidget(self.widgetStack,"WStackPage_2")
        WStackPageLayout_2 = QVBoxLayout(self.WStackPage_2,0,0,"WStackPageLayout_2")

        self.itemListView = QListView(self.WStackPage_2,"itemListView")
        self.itemListView.addColumn(self.__tr("Object"))
        self.itemListView.setResizeMode(QListView.LastColumn)
        WStackPageLayout_2.addWidget(self.itemListView)
        self.widgetStack.addWidget(self.WStackPage_2,1)

        LumaEntryBrowserDesignLayout.addMultiCellWidget(self.widgetStack,4,4,0,3)
        spacer2 = QSpacerItem(260,31,QSizePolicy.Expanding,QSizePolicy.Minimum)
        LumaEntryBrowserDesignLayout.addMultiCell(spacer2,3,3,2,3)

        self.iconViewButton = QToolButton(self,"iconViewButton")
        self.iconViewButton.setSizePolicy(QSizePolicy(0,0,0,0,self.iconViewButton.sizePolicy().hasHeightForWidth()))
        self.iconViewButton.setMinimumSize(QSize(24,24))
        self.iconViewButton.setAutoRaise(1)

        LumaEntryBrowserDesignLayout.addWidget(self.iconViewButton,3,1)

        self.listViewButton = QToolButton(self,"listViewButton")
        self.listViewButton.setSizePolicy(QSizePolicy(0,0,0,0,self.listViewButton.sizePolicy().hasHeightForWidth()))
        self.listViewButton.setMinimumSize(QSize(24,0))
        self.listViewButton.setAutoRaise(1)

        LumaEntryBrowserDesignLayout.addWidget(self.listViewButton,3,0)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        LumaEntryBrowserDesignLayout.addMultiCellWidget(self.line1,2,2,0,3)

        self.languageChange()

        self.resize(QSize(357,741).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.serverBox,SIGNAL("activated(const QString&)"),self.serverChanged)
        self.connect(self.searchEdit,SIGNAL("returnPressed()"),self.search)
        self.connect(self.goButton,SIGNAL("clicked()"),self.search)
        self.connect(self.itemIconView,SIGNAL("selectionChanged(QIconViewItem*)"),self.iconClicked)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteItem)
        self.connect(self.addButton,SIGNAL("clicked()"),self.addItem)
        self.connect(self.listViewButton,SIGNAL("clicked()"),self.raiseListView)
        self.connect(self.iconViewButton,SIGNAL("clicked()"),self.raiseIconView)
        self.connect(self.itemListView,SIGNAL("selectionChanged(QListViewItem*)"),self.listItemClicked)


    def languageChange(self):
        self.setCaption(self.__tr("LumaIconViewDesign"))
        self.goButton.setText(self.__tr("&Go"))
        self.goButton.setAccel(self.__tr("Alt+G"))
        self.textLabel13.setText(self.__tr("Filter:"))
        self.textLabel12.setText(self.__tr("Server:"))
        self.addButton.setText(self.__tr("&Add..."))
        self.addButton.setAccel(self.__tr("Alt+A"))
        self.deleteButton.setText(self.__tr("&Delete"))
        self.deleteButton.setAccel(self.__tr("Alt+D"))
        self.itemListView.header().setLabel(0,self.__tr("Object"))
        self.iconViewButton.setText(self.__tr("...","DO NOT TRANSLATE"))
        self.listViewButton.setText(self.__tr("...","DO NOT TRANSLATE"))


    def serverChanged(self):
        print "LumaEntryBrowserDesign.serverChanged(): Not implemented yet"

    def search(self):
        print "LumaEntryBrowserDesign.search(): Not implemented yet"

    def iconClicked(self):
        print "LumaEntryBrowserDesign.iconClicked(): Not implemented yet"

    def deleteItem(self):
        print "LumaEntryBrowserDesign.deleteItem(): Not implemented yet"

    def addItem(self):
        print "LumaEntryBrowserDesign.addItem(): Not implemented yet"

    def raiseListView(self):
        print "LumaEntryBrowserDesign.raiseListView(): Not implemented yet"

    def raiseIconView(self):
        print "LumaEntryBrowserDesign.raiseIconView(): Not implemented yet"

    def listItemClicked(self):
        print "LumaEntryBrowserDesign.listItemClicked(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("LumaEntryBrowserDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = LumaEntryBrowserDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
