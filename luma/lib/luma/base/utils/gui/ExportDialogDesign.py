# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/ExportDialogDesign.ui'
#
# Created: Tue Feb 8 21:00:39 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class ExportDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ExportDialogDesign")


        ExportDialogDesignLayout = QGridLayout(self,1,1,6,6,"ExportDialogDesignLayout")

        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        ExportDialogDesignLayout.addWidget(self.textLabel2,0,1)

        self.line2 = QFrame(self,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)

        ExportDialogDesignLayout.addMultiCellWidget(self.line2,1,1,0,1)

        self.iconLabel = QLabel(self,"iconLabel")
        self.iconLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.iconLabel.sizePolicy().hasHeightForWidth()))
        self.iconLabel.setMinimumSize(QSize(64,64))

        ExportDialogDesignLayout.addWidget(self.iconLabel,0,0)
        spacer3_2 = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        ExportDialogDesignLayout.addItem(spacer3_2,3,1)

        layout4 = QGridLayout(None,1,1,0,6,"layout4")

        self.fileEdit = QLineEdit(self,"fileEdit")

        layout4.addWidget(self.fileEdit,1,1)

        self.fileButton = QPushButton(self,"fileButton")

        layout4.addWidget(self.fileButton,1,2)

        self.textLabel1 = QLabel(self,"textLabel1")

        layout4.addWidget(self.textLabel1,0,0)

        self.fileLabel = QLabel(self,"fileLabel")

        layout4.addWidget(self.fileLabel,2,1)

        self.formatBox = QComboBox(0,self,"formatBox")

        layout4.addWidget(self.formatBox,0,1)

        self.textLabel2_2 = QLabel(self,"textLabel2_2")

        layout4.addWidget(self.textLabel2_2,1,0)

        ExportDialogDesignLayout.addMultiCellLayout(layout4,2,2,0,1)

        layout4_2 = QHBoxLayout(None,0,6,"layout4_2")
        spacer1 = QSpacerItem(340,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout4_2.addItem(spacer1)

        self.startButton = QPushButton(self,"startButton")
        self.startButton.setSizePolicy(QSizePolicy(1,0,0,0,self.startButton.sizePolicy().hasHeightForWidth()))
        layout4_2.addWidget(self.startButton)

        self.pushButton2 = QPushButton(self,"pushButton2")
        self.pushButton2.setDefault(1)
        layout4_2.addWidget(self.pushButton2)

        ExportDialogDesignLayout.addMultiCellLayout(layout4_2,6,6,0,1)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        ExportDialogDesignLayout.addMultiCellWidget(self.line1,5,5,0,1)

        layout5 = QGridLayout(None,1,1,0,6,"layout5")

        self.resultLabel = QLabel(self,"resultLabel")

        layout5.addMultiCellWidget(self.resultLabel,2,2,0,1)

        self.removeButton = QPushButton(self,"removeButton")
        self.removeButton.setSizePolicy(QSizePolicy(1,0,0,0,self.removeButton.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.removeButton,1,1)

        self.itemView = QListView(self,"itemView")
        self.itemView.addColumn(self.__tr("1"))
        self.itemView.addColumn(self.__tr("DN"))
        self.itemView.addColumn(self.__tr("Message"))
        self.itemView.setSizePolicy(QSizePolicy(7,7,0,0,self.itemView.sizePolicy().hasHeightForWidth()))
        self.itemView.setSelectionMode(QListView.Extended)
        self.itemView.setAllColumnsShowFocus(1)
        self.itemView.setShowSortIndicator(1)
        self.itemView.setResizeMode(QListView.LastColumn)

        layout5.addMultiCellWidget(self.itemView,0,0,0,1)
        spacer3 = QSpacerItem(120,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout5.addItem(spacer3,1,0)

        ExportDialogDesignLayout.addMultiCellLayout(layout5,4,4,0,1)

        self.languageChange()

        self.resize(QSize(543,468).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton2,SIGNAL("clicked()"),self.reject)
        self.connect(self.removeButton,SIGNAL("clicked()"),self.removeItems)
        self.connect(self.startButton,SIGNAL("clicked()"),self.exportItems)
        self.connect(self.fileButton,SIGNAL("clicked()"),self.showFileDialog)
        self.connect(self.fileEdit,SIGNAL("textChanged(const QString&)"),self.updateFileName)


    def languageChange(self):
        self.setCaption(self.__tr("Export items"))
        self.textLabel2.setText(self.__tr("The following entries will be exported to the format of your choice. You can remove items from the list if you don't want them to be exported. Press start to begin with export.."))
        self.iconLabel.setText(self.__tr("DL","DO NOT TRANSLATE"))
        self.fileButton.setText(self.__tr("A","DO NOT TRANSLATE"))
        self.textLabel1.setText(self.__tr("Export format:"))
        self.fileLabel.setText(self.__tr("foo"))
        self.formatBox.clear()
        self.formatBox.insertItem(self.__tr("LDIF"))
        self.formatBox.insertItem(self.__tr("DSML"))
        self.textLabel2_2.setText(self.__tr("Output file:"))
        self.startButton.setText(self.__tr("&Export"))
        self.startButton.setAccel(self.__tr("Alt+E"))
        self.pushButton2.setText(self.__tr("&Cancel"))
        self.pushButton2.setAccel(self.__tr("Alt+C"))
        self.resultLabel.setText(self.__tr("foo"))
        self.removeButton.setText(self.__tr("&Remove from list"))
        self.removeButton.setAccel(self.__tr("Alt+R"))
        self.itemView.header().setLabel(0,self.__tr("1"))
        self.itemView.header().setLabel(1,self.__tr("DN"))
        self.itemView.header().setLabel(2,self.__tr("Message"))


    def removeItems(self):
        print "ExportDialogDesign.removeItems(): Not implemented yet"

    def exportItems(self):
        print "ExportDialogDesign.exportItems(): Not implemented yet"

    def showFileDialog(self):
        print "ExportDialogDesign.showFileDialog(): Not implemented yet"

    def updateFileName(self):
        print "ExportDialogDesign.updateFileName(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ExportDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ExportDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
