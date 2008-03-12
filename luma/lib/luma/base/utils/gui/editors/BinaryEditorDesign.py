# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/editors/BinaryEditorDesign.ui'
#
# Created: Wed Aug 17 15:23:50 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt4.QtGui import *


class BinaryEditorDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("BinaryEditorDesign")


        BinaryEditorDesignLayout = QGridLayout(self,1,1,11,6,"BinaryEditorDesignLayout")

        self.iconLabel = QLabel(self,"iconLabel")
        self.iconLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.iconLabel.sizePolicy().hasHeightForWidth()))
        self.iconLabel.setMinimumSize(QSize(64,64))

        BinaryEditorDesignLayout.addWidget(self.iconLabel,0,0)
        spacer4 = QSpacerItem(20,201,QSizePolicy.Minimum,QSizePolicy.Expanding)
        BinaryEditorDesignLayout.addItem(spacer4,1,0)

        layout1 = QHBoxLayout(None,0,6,"layout1")
        spacer1 = QSpacerItem(390,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout1.addItem(spacer1)

        self.okButton = QPushButton(self,"okButton")
        self.okButton.setDefault(1)
        layout1.addWidget(self.okButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        layout1.addWidget(self.cancelButton)

        BinaryEditorDesignLayout.addMultiCellLayout(layout1,3,3,0,1)

        self.line2 = QFrame(self,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)

        BinaryEditorDesignLayout.addMultiCellWidget(self.line2,2,2,0,1)

        layout2 = QGridLayout(None,1,1,0,6,"layout2")

        self.fileButton = QPushButton(self,"fileButton")

        layout2.addWidget(self.fileButton,2,2)
        spacer4_2 = QSpacerItem(21,10,QSizePolicy.Minimum,QSizePolicy.Fixed)
        layout2.addItem(spacer4_2,1,1)

        self.valueEdit = QLineEdit(self,"valueEdit")

        layout2.addWidget(self.valueEdit,2,1)

        self.attributeLabel = QLabel(self,"attributeLabel")

        layout2.addMultiCellWidget(self.attributeLabel,0,0,0,2)
        spacer5 = QSpacerItem(21,5,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout2.addItem(spacer5,4,1)

        self.informationLabel = QLabel(self,"informationLabel")
        self.informationLabel.setMinimumSize(QSize(0,30))
        self.informationLabel.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        layout2.addMultiCellWidget(self.informationLabel,3,3,0,1)

        self.textLabel3 = QLabel(self,"textLabel3")

        layout2.addWidget(self.textLabel3,2,0)

        BinaryEditorDesignLayout.addMultiCellLayout(layout2,0,1,1,1)

        self.languageChange()

        self.resize(QSize(431,195).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.okButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.valueEdit,SIGNAL("textChanged(const QString&)"),self.updateValue)
        self.connect(self.fileButton,SIGNAL("clicked()"),self.showFileDialog)

        self.setTabOrder(self.valueEdit,self.fileButton)
        self.setTabOrder(self.fileButton,self.okButton)
        self.setTabOrder(self.okButton,self.cancelButton)


    def languageChange(self):
        self.setCaption(self.__tr("Edit attribute"))
        self.iconLabel.setText(self.__tr("IT","DO NOT TRANSLATE"))
        self.okButton.setText(self.__tr("&OK"))
        self.okButton.setAccel(self.__tr("Alt+O"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))
        self.fileButton.setText(self.__tr("F","DO NOT TRANSLATE"))
        self.attributeLabel.setText(self.__tr("Please enter a file location from where to load binary data for the attribute <b>%1</b>."))
        self.informationLabel.setText(self.__tr("IL"))
        self.textLabel3.setText(self.__tr("Location:"))


    def updateValue(self):
        print "BinaryEditorDesign.updateValue(): Not implemented yet"

    def showFileDialog(self):
        print "BinaryEditorDesign.showFileDialog(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("BinaryEditorDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = BinaryEditorDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
