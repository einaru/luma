# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/DeleteDialogDesign.ui'
#
# Created: Thu Jan 6 17:42:41 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class DeleteDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("DeleteDialogDesign")


        DeleteDialogDesignLayout = QGridLayout(self,1,1,6,6,"DeleteDialogDesignLayout")

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        DeleteDialogDesignLayout.addMultiCellWidget(self.line1,3,3,0,2)

        layout1 = QHBoxLayout(None,0,6,"layout1")
        spacer1 = QSpacerItem(321,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout1.addItem(spacer1)

        self.pushButton2 = QPushButton(self,"pushButton2")
        layout1.addWidget(self.pushButton2)

        DeleteDialogDesignLayout.addMultiCellLayout(layout1,4,4,0,2)

        self.iconLabel = QLabel(self,"iconLabel")
        self.iconLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.iconLabel.sizePolicy().hasHeightForWidth()))
        self.iconLabel.setMinimumSize(QSize(64,64))

        DeleteDialogDesignLayout.addWidget(self.iconLabel,0,0)

        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        DeleteDialogDesignLayout.addMultiCellWidget(self.textLabel2,0,0,1,2)

        self.line2 = QFrame(self,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)

        DeleteDialogDesignLayout.addMultiCellWidget(self.line2,1,1,0,2)

        self.itemView = QListView(self,"itemView")
        self.itemView.addColumn(QString.null)
        self.itemView.addColumn(self.__tr("DN"))
        self.itemView.addColumn(self.__tr("Message"))
        self.itemView.setSizePolicy(QSizePolicy(7,7,0,0,self.itemView.sizePolicy().hasHeightForWidth()))
        self.itemView.setSelectionMode(QListView.Extended)
        self.itemView.setAllColumnsShowFocus(1)
        self.itemView.setShowSortIndicator(1)
        self.itemView.setResizeMode(QListView.LastColumn)

        DeleteDialogDesignLayout.addMultiCellWidget(self.itemView,2,2,0,1)

        layout2 = QVBoxLayout(None,0,6,"layout2")

        self.startButton = QPushButton(self,"startButton")
        self.startButton.setSizePolicy(QSizePolicy(4,0,0,0,self.startButton.sizePolicy().hasHeightForWidth()))
        layout2.addWidget(self.startButton)

        self.removeButton = QPushButton(self,"removeButton")
        self.removeButton.setSizePolicy(QSizePolicy(4,0,0,0,self.removeButton.sizePolicy().hasHeightForWidth()))
        layout2.addWidget(self.removeButton)
        spacer3 = QSpacerItem(21,171,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout2.addItem(spacer3)

        DeleteDialogDesignLayout.addLayout(layout2,2,2)

        self.languageChange()

        self.resize(QSize(600,320).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton2,SIGNAL("clicked()"),self.reject)
        self.connect(self.removeButton,SIGNAL("clicked()"),self.removeItems)
        self.connect(self.startButton,SIGNAL("clicked()"),self.deleteItems)


    def languageChange(self):
        self.setCaption(self.__tr("Delete items"))
        self.pushButton2.setText(self.__tr("&Cancel"))
        self.pushButton2.setAccel(self.__tr("Alt+C"))
        self.iconLabel.setText(self.__tr("DL"))
        self.textLabel2.setText(self.__tr("The following entries will be deleted from the server. You can remove items from the list if you don't want them to be deleted. Press start to begin with deletion."))
        self.itemView.header().setLabel(0,QString.null)
        self.itemView.header().setLabel(1,self.__tr("DN"))
        self.itemView.header().setLabel(2,self.__tr("Message"))
        self.startButton.setText(self.__tr("&Start"))
        self.startButton.setAccel(self.__tr("Alt+S"))
        self.removeButton.setText(self.__tr("&Remove"))
        self.removeButton.setAccel(self.__tr("Alt+R"))


    def removeItems(self):
        print "DeleteDialogDesign.removeItems(): Not implemented yet"

    def deleteItems(self):
        print "DeleteDialogDesign.deleteItems(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("DeleteDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = DeleteDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()