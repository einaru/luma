# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/SearchResultViewDesign.ui'
#
# Created: Tue Feb 3 23:58:02 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.10
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class SearchResultViewDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("SearchResultViewDesign")


        SearchResultViewDesignLayout = QGridLayout(self,1,1,11,6,"SearchResultViewDesignLayout")

        self.resultListView = QListView(self,"resultListView")
        self.resultListView.setSelectionMode(QListView.Extended)
        self.resultListView.setAllColumnsShowFocus(1)
        self.resultListView.setResizeMode(QListView.AllColumns)

        SearchResultViewDesignLayout.addWidget(self.resultListView,0,0)

        self.languageChange()

        self.resize(QSize(600,482).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.resultListView,SIGNAL("doubleClicked(QListViewItem*)"),self.show_entry)


    def languageChange(self):
        self.setCaption(QString.null)


    def show_entry(self):
        print "SearchResultViewDesign.show_entry(): Not implemented yet"

    def set_result(self):
        print "SearchResultViewDesign.set_result(): Not implemented yet"

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = SearchResultViewDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
