# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/DeleteDialogDesign.ui'
#
# Created: Tue Feb 8 20:53:49 2005
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

        self.iconLabel = QLabel(self,"iconLabel")
        self.iconLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.iconLabel.sizePolicy().hasHeightForWidth()))
        self.iconLabel.setMinimumSize(QSize(64,64))

        DeleteDialogDesignLayout.addWidget(self.iconLabel,0,0)

        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        DeleteDialogDesignLayout.addWidget(self.textLabel2,0,1)

        self.line2 = QFrame(self,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)

        DeleteDialogDesignLayout.addMultiCellWidget(self.line2,1,1,0,1)

        layout3 = QHBoxLayout(None,0,6,"layout3")
        spacer1 = QSpacerItem(260,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout3.addItem(spacer1)

        self.startButton = QPushButton(self,"startButton")
        self.startButton.setSizePolicy(QSizePolicy(1,0,0,0,self.startButton.sizePolicy().hasHeightForWidth()))
        layout3.addWidget(self.startButton)

        self.pushButton2 = QPushButton(self,"pushButton2")
        self.pushButton2.setDefault(1)
        layout3.addWidget(self.pushButton2)

        DeleteDialogDesignLayout.addMultiCellLayout(layout3,4,4,0,1)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        DeleteDialogDesignLayout.addMultiCellWidget(self.line1,3,3,0,1)

        layout4 = QGridLayout(None,1,1,0,6,"layout4")

        self.removeButton = QPushButton(self,"removeButton")
        self.removeButton.setSizePolicy(QSizePolicy(1,0,0,0,self.removeButton.sizePolicy().hasHeightForWidth()))

        layout4.addWidget(self.removeButton,1,1)

        self.itemView = QListView(self,"itemView")
        self.itemView.addColumn(QString.null)
        self.itemView.addColumn(self.__tr("DN"))
        self.itemView.addColumn(self.__tr("Message"))
        self.itemView.setSizePolicy(QSizePolicy(7,7,0,0,self.itemView.sizePolicy().hasHeightForWidth()))
        self.itemView.setSelectionMode(QListView.Extended)
        self.itemView.setAllColumnsShowFocus(1)
        self.itemView.setShowSortIndicator(1)
        self.itemView.setResizeMode(QListView.LastColumn)

        layout4.addMultiCellWidget(self.itemView,0,0,0,1)
        spacer3 = QSpacerItem(122,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout4.addItem(spacer3,1,0)

        DeleteDialogDesignLayout.addMultiCellLayout(layout4,2,2,0,1)

        self.languageChange()

        self.resize(QSize(524,371).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton2,SIGNAL("clicked()"),self.reject)
        self.connect(self.removeButton,SIGNAL("clicked()"),self.removeItems)
        self.connect(self.startButton,SIGNAL("clicked()"),self.deleteItems)


    def languageChange(self):
        self.setCaption(self.__tr("Delete items"))
        self.iconLabel.setText(self.__tr("DL"))
        self.textLabel2.setText(self.__tr("The following entries will be deleted from the server. You can remove items from the list if you don't want them to be deleted. Press start to begin with deletion."))
        self.startButton.setText(self.__tr("&Delete"))
        self.startButton.setAccel(self.__tr("Alt+D"))
        self.pushButton2.setText(self.__tr("&Cancel"))
        self.pushButton2.setAccel(self.__tr("Alt+C"))
        self.removeButton.setText(self.__tr("&Remove from list"))
        self.removeButton.setAccel(self.__tr("Alt+R"))
        self.itemView.header().setLabel(0,QString.null)
        self.itemView.header().setLabel(1,self.__tr("DN"))
        self.itemView.header().setLabel(2,self.__tr("Message"))


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
