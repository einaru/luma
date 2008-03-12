# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/SearchResultViewDesign.ui'
#
# Created: Wed Aug 17 15:23:41 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt4.QtGui import *


class SearchResultViewDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("SearchResultViewDesign")


        SearchResultViewDesignLayout = QGridLayout(self,1,1,11,6,"SearchResultViewDesignLayout")

        self.resultListView = QListView(self,"resultListView")
        self.resultListView.setSelectionMode(QListView.Extended)
        self.resultListView.setAllColumnsShowFocus(1)
        self.resultListView.setShowToolTips(0)
        self.resultListView.setResizeMode(QListView.AllColumns)

        SearchResultViewDesignLayout.addWidget(self.resultListView,0,0)

        self.languageChange()

        self.resize(QSize(600,484).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.resultListView,SIGNAL("doubleClicked(QListViewItem*)"),self.showEntry)


    def languageChange(self):
        self.setCaption(self.__tr("SearchResultViewDesign"))


    def showEntry(self):
        print "SearchResultViewDesign.showEntry(): Not implemented yet"

    def setResult(self):
        print "SearchResultViewDesign.setResult(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("SearchResultViewDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = SearchResultViewDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
