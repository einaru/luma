# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BaseSelectorDesign.ui'
#
# Created: Thu Nov 13 02:17:50 2003
#      by: The PyQt User Interface Compiler (pyuic) 3.7
#
# WARNING! All changes made in this file will be lost!


from qt import *


class BaseSelectorDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("BaseSelectorDesign")


        BaseSelectorDesignLayout = QVBoxLayout(self,11,6,"BaseSelectorDesignLayout")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(1,4,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))
        BaseSelectorDesignLayout.addWidget(self.textLabel1)

        self.dnBox = QComboBox(0,self,"dnBox")
        BaseSelectorDesignLayout.addWidget(self.dnBox)
        spacer = QSpacerItem(21,91,QSizePolicy.Minimum,QSizePolicy.Expanding)
        BaseSelectorDesignLayout.addItem(spacer)

        layout1 = QHBoxLayout(None,0,6,"layout1")

        self.cancelButton = QPushButton(self,"cancelButton")
        layout1.addWidget(self.cancelButton)
        spacer_2 = QSpacerItem(250,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout1.addItem(spacer_2)

        self.okButton = QPushButton(self,"okButton")
        layout1.addWidget(self.okButton)
        BaseSelectorDesignLayout.addLayout(layout1)

        self.languageChange()

        self.resize(QSize(438,121).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.okButton,SIGNAL("clicked()"),self,SLOT("accept()"))


    def languageChange(self):
        self.setCaption(self.__tr("Available Base DN"))
        self.textLabel1.setText(self.__tr("Select Base DN:"))
        self.cancelButton.setText(self.__tr("Cancel"))
        self.okButton.setText(self.__tr("Ok"))


    def __tr(self,s,c = None):
        return qApp.translate("BaseSelectorDesign",s,c)
