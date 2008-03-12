# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/editors/RdnEditorDesign.ui'
#
# Created: Wed Aug 17 15:23:51 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt4.QtGui import *


class RdnEditorDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("RdnEditorDesign")


        RdnEditorDesignLayout = QGridLayout(self,1,1,11,6,"RdnEditorDesignLayout")

        self.iconLabel = QLabel(self,"iconLabel")
        self.iconLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.iconLabel.sizePolicy().hasHeightForWidth()))
        self.iconLabel.setMinimumSize(QSize(64,64))

        RdnEditorDesignLayout.addWidget(self.iconLabel,0,0)
        spacer4 = QSpacerItem(20,201,QSizePolicy.Minimum,QSizePolicy.Expanding)
        RdnEditorDesignLayout.addMultiCell(spacer4,1,5,0,0)

        layout1 = QHBoxLayout(None,0,6,"layout1")
        spacer1 = QSpacerItem(390,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout1.addItem(spacer1)

        self.okButton = QPushButton(self,"okButton")
        self.okButton.setDefault(1)
        layout1.addWidget(self.okButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        self.cancelButton.setDefault(0)
        layout1.addWidget(self.cancelButton)

        RdnEditorDesignLayout.addMultiCellLayout(layout1,7,7,0,2)

        self.line2 = QFrame(self,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)

        RdnEditorDesignLayout.addMultiCellWidget(self.line2,6,6,0,2)

        self.textLabel3 = QLabel(self,"textLabel3")

        RdnEditorDesignLayout.addWidget(self.textLabel3,3,1)

        self.textLabel2 = QLabel(self,"textLabel2")

        RdnEditorDesignLayout.addWidget(self.textLabel2,4,1)

        self.attributeLabel = QLabel(self,"attributeLabel")
        self.attributeLabel.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        RdnEditorDesignLayout.addMultiCellWidget(self.attributeLabel,0,0,1,2)

        self.attributeBox = QComboBox(0,self,"attributeBox")

        RdnEditorDesignLayout.addWidget(self.attributeBox,2,2)

        self.valueEdit = QLineEdit(self,"valueEdit")

        RdnEditorDesignLayout.addWidget(self.valueEdit,3,2)
        spacer4_2 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        RdnEditorDesignLayout.addItem(spacer4_2,1,2)
        spacer5 = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        RdnEditorDesignLayout.addItem(spacer5,5,2)

        self.dnLabel = QLabel(self,"dnLabel")

        RdnEditorDesignLayout.addWidget(self.dnLabel,4,2)

        self.textLabel1 = QLabel(self,"textLabel1")

        RdnEditorDesignLayout.addWidget(self.textLabel1,2,1)

        self.languageChange()

        self.resize(QSize(436,246).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.okButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.cancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.valueEdit,SIGNAL("textChanged(const QString&)"),self.updateValue)
        self.connect(self.attributeBox,SIGNAL("activated(const QString&)"),self.updateValue)

        self.setTabOrder(self.valueEdit,self.okButton)
        self.setTabOrder(self.okButton,self.cancelButton)


    def languageChange(self):
        self.setCaption(self.__tr("Edit DN"))
        self.iconLabel.setText(self.__tr("IT","DO NOT TRANSLATE"))
        self.okButton.setText(self.__tr("&OK"))
        self.okButton.setAccel(self.__tr("Alt+O"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))
        self.textLabel3.setText(self.__tr("Value:"))
        self.textLabel2.setText(self.__tr("DN:"))
        self.attributeLabel.setText(self.__tr("Please choose an attribute and enter a value for it. These values will be part of distinguished name for the new object."))
        self.dnLabel.setText(QString.null)
        self.textLabel1.setText(self.__tr("Attribute:"))


    def updateValue(self):
        print "RdnEditorDesign.updateValue(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("RdnEditorDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = RdnEditorDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
