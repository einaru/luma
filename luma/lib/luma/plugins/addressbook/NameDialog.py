# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './lib/luma/plugins/addressbook/NameDialog.ui'
#
# Created: Tue Mar 1 22:48:53 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14
#
# WARNING! All changes made in this file will be lost!


from qt import *


class NameDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("NameDialog")


        NameDialogLayout = QVBoxLayout(self,11,6,"NameDialogLayout")

        layout3 = QGridLayout(None,1,1,0,6,"layout3")

        self.suffixBox = QComboBox(0,self,"suffixBox")
        self.suffixBox.setEditable(1)

        layout3.addWidget(self.suffixBox,4,1)

        self.textLabel3 = QLabel(self,"textLabel3")
        self.textLabel3.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout3.addWidget(self.textLabel3,2,0)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))
        self.textLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout3.addWidget(self.textLabel1,0,0)

        self.textLabel5 = QLabel(self,"textLabel5")
        self.textLabel5.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout3.addWidget(self.textLabel5,4,0)

        self.middleEdit = QLineEdit(self,"middleEdit")

        layout3.addWidget(self.middleEdit,2,1)

        self.titleBox = QComboBox(0,self,"titleBox")
        self.titleBox.setEditable(1)

        layout3.addWidget(self.titleBox,0,1)

        self.textLabel4 = QLabel(self,"textLabel4")
        self.textLabel4.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter | QLabel.AlignRight)

        layout3.addWidget(self.textLabel4,3,0)

        self.firstEdit = QLineEdit(self,"firstEdit")

        layout3.addWidget(self.firstEdit,1,1)

        self.lastEdit = QLineEdit(self,"lastEdit")

        layout3.addWidget(self.lastEdit,3,1)

        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout3.addWidget(self.textLabel2,1,0)
        NameDialogLayout.addLayout(layout3)
        spacer10 = QSpacerItem(31,16,QSizePolicy.Minimum,QSizePolicy.Preferred)
        NameDialogLayout.addItem(spacer10)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)
        NameDialogLayout.addWidget(self.line1)

        layout2 = QHBoxLayout(None,0,6,"layout2")
        spacer9 = QSpacerItem(271,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer9)

        self.okButton = QPushButton(self,"okButton")
        self.okButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.okButton.sizePolicy().hasHeightForWidth()))
        self.okButton.setDefault(1)
        layout2.addWidget(self.okButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        self.cancelButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.cancelButton.sizePolicy().hasHeightForWidth()))
        self.cancelButton.setAutoDefault(0)
        layout2.addWidget(self.cancelButton)
        NameDialogLayout.addLayout(layout2)

        self.languageChange()

        self.resize(QSize(331,234).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.okButton,SIGNAL("clicked()"),self.accept)

        self.setTabOrder(self.titleBox,self.firstEdit)
        self.setTabOrder(self.firstEdit,self.middleEdit)
        self.setTabOrder(self.middleEdit,self.lastEdit)
        self.setTabOrder(self.lastEdit,self.suffixBox)
        self.setTabOrder(self.suffixBox,self.okButton)
        self.setTabOrder(self.okButton,self.cancelButton)


    def languageChange(self):
        self.setCaption(self.__tr("Full name"))
        self.suffixBox.clear()
        self.suffixBox.insertItem(QString.null)
        self.suffixBox.insertItem(self.__tr("Sr."))
        self.suffixBox.insertItem(self.__tr("Jr."))
        self.suffixBox.insertItem(self.__tr("I"))
        self.suffixBox.insertItem(self.__tr("II"))
        self.suffixBox.insertItem(self.__tr("III"))
        self.suffixBox.insertItem(self.__tr("Esq."))
        self.textLabel3.setText(self.__tr("Middle:"))
        self.textLabel1.setText(self.__tr("Title:"))
        self.textLabel5.setText(self.__tr("Suffix:"))
        self.titleBox.clear()
        self.titleBox.insertItem(QString.null)
        self.titleBox.insertItem(self.__tr("Mr."))
        self.titleBox.insertItem(self.__tr("Mrs."))
        self.titleBox.insertItem(self.__tr("Ms."))
        self.titleBox.insertItem(self.__tr("Miss"))
        self.titleBox.insertItem(self.__tr("Dr."))
        self.textLabel4.setText(self.__tr("<b>Last:</b>"))
        QToolTip.add(self.textLabel4,self.__tr("This attribute must be set."))
        self.textLabel2.setText(self.__tr("First:"))
        self.okButton.setText(self.__tr("&Ok"))
        self.okButton.setAccel(self.__tr("Alt+O"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(self.__tr("Alt+C"))


    def __tr(self,s,c = None):
        return qApp.translate("NameDialog",s,c)
