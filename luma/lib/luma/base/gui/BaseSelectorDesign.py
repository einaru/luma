# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/gui/BaseSelectorDesign.ui'
#
# Created: Tue Feb 3 23:58:05 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.10
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class BaseSelectorDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("BaseSelectorDesign")


        BaseSelectorDesignLayout = QGridLayout(self,1,1,11,6,"BaseSelectorDesignLayout")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(1,4,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))

        BaseSelectorDesignLayout.addWidget(self.textLabel1,0,0)

        self.dnBox = QComboBox(0,self,"dnBox")

        BaseSelectorDesignLayout.addWidget(self.dnBox,1,0)
        spacer = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        BaseSelectorDesignLayout.addItem(spacer,2,0)

        layout2 = QHBoxLayout(None,0,6,"layout2")
        spacer_2 = QSpacerItem(60,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer_2)

        self.cancelButton = QPushButton(self,"cancelButton")
        layout2.addWidget(self.cancelButton)

        self.okButton = QPushButton(self,"okButton")
        layout2.addWidget(self.okButton)

        BaseSelectorDesignLayout.addLayout(layout2,4,0)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        BaseSelectorDesignLayout.addWidget(self.line1,3,0)

        self.languageChange()

        self.resize(QSize(353,129).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.okButton,SIGNAL("clicked()"),self,SLOT("accept()"))


    def languageChange(self):
        self.setCaption(self.__tr("Select Base DN"))
        self.textLabel1.setText(self.__tr("Available Base DNs:"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))
        self.okButton.setText(self.__tr("&Ok"))
        self.okButton.setAccel(self.__tr("Alt+O"))


    def __tr(self,s,c = None):
        return qApp.translate("BaseSelectorDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = BaseSelectorDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
