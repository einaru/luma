# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/gui/LanguageDialogDesign.ui'
#
# Created: Thu Jan 1 17:35:32 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.8.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class LanguageDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("LanguageDialogDesign")


        LanguageDialogDesignLayout = QGridLayout(self,1,1,11,6,"LanguageDialogDesignLayout")

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(4,5,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))
        layout3.addWidget(self.textLabel1)

        self.languageBox = QComboBox(0,self,"languageBox")
        layout3.addWidget(self.languageBox)

        LanguageDialogDesignLayout.addMultiCellLayout(layout3,0,0,0,2)
        spacer = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        LanguageDialogDesignLayout.addItem(spacer,1,0)

        self.okButton = QPushButton(self,"okButton")

        LanguageDialogDesignLayout.addWidget(self.okButton,3,2)

        self.cancelButton = QPushButton(self,"cancelButton")

        LanguageDialogDesignLayout.addWidget(self.cancelButton,3,1)
        spacer_2 = QSpacerItem(146,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        LanguageDialogDesignLayout.addItem(spacer_2,3,0)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        LanguageDialogDesignLayout.addMultiCellWidget(self.line1,2,2,0,2)

        self.languageChange()

        self.resize(QSize(327,116).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.okButton,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.cancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))


    def languageChange(self):
        self.setCaption(self.__tr("Choose Language"))
        self.textLabel1.setText(self.__tr("Language:"))
        self.okButton.setText(self.__tr("Ok"))
        self.cancelButton.setText(self.__tr("Cancel"))


    def __tr(self,s,c = None):
        return qApp.translate("LanguageDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = LanguageDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
