# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/usermanagement/GroupDialogDesign.ui'
#
# Created: Wed Aug 17 15:23:47 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class GroupDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("GroupDialogDesign")

        self.setSizeGripEnabled(1)

        GroupDialogDesignLayout = QGridLayout(self,1,1,11,6,"GroupDialogDesignLayout")
        spacer7 = QSpacerItem(20,31,QSizePolicy.Fixed,QSizePolicy.Minimum)
        GroupDialogDesignLayout.addItem(spacer7,9,0)

        self.textLabel2 = QLabel(self,"textLabel2")

        GroupDialogDesignLayout.addMultiCellWidget(self.textLabel2,2,2,0,3)

        self.groupNumberBox = QSpinBox(self,"groupNumberBox")
        self.groupNumberBox.setMinimumSize(QSize(70,0))
        self.groupNumberBox.setMaxValue(655535)

        GroupDialogDesignLayout.addWidget(self.groupNumberBox,5,2)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))
        self.textLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        GroupDialogDesignLayout.addWidget(self.textLabel1,4,1)

        self.infoLabel = QLabel(self,"infoLabel")
        self.infoLabel.setTextFormat(QLabel.PlainText)
        self.infoLabel.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        GroupDialogDesignLayout.addMultiCellWidget(self.infoLabel,3,3,1,3)
        spacer4 = QSpacerItem(20,31,QSizePolicy.Fixed,QSizePolicy.Minimum)
        GroupDialogDesignLayout.addItem(spacer4,3,0)
        spacer5 = QSpacerItem(20,31,QSizePolicy.Fixed,QSizePolicy.Minimum)
        GroupDialogDesignLayout.addMultiCell(spacer5,4,5,0,0)
        spacer6 = QSpacerItem(20,31,QSizePolicy.Fixed,QSizePolicy.Minimum)
        GroupDialogDesignLayout.addItem(spacer6,8,0)

        self.infoLabel2 = QLabel(self,"infoLabel2")

        GroupDialogDesignLayout.addMultiCellWidget(self.infoLabel2,8,8,1,3)

        self.groupNameBox = QComboBox(0,self,"groupNameBox")
        self.groupNameBox.setEditable(0)

        GroupDialogDesignLayout.addWidget(self.groupNameBox,4,2)
        spacer2 = QSpacerItem(217,50,QSizePolicy.Preferred,QSizePolicy.Minimum)
        GroupDialogDesignLayout.addMultiCell(spacer2,4,5,3,3)

        self.groupView = QListView(self,"groupView")
        self.groupView.addColumn(self.__tr("Group"))
        self.groupView.addColumn(self.__tr("ID"))
        self.groupView.addColumn(self.__tr("Location"))
        self.groupView.setResizeMode(QListView.LastColumn)

        GroupDialogDesignLayout.addMultiCellWidget(self.groupView,9,9,1,3)

        self.textLabel1_2 = QLabel(self,"textLabel1_2")

        GroupDialogDesignLayout.addMultiCellWidget(self.textLabel1_2,7,7,0,3)

        self.textLabel3 = QLabel(self,"textLabel3")
        self.textLabel3.setAlignment(QLabel.AlignVCenter)

        GroupDialogDesignLayout.addWidget(self.textLabel3,5,1)
        spacer3 = QSpacerItem(31,25,QSizePolicy.Minimum,QSizePolicy.Fixed)
        GroupDialogDesignLayout.addItem(spacer3,6,2)

        self.line2 = QFrame(self,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)

        GroupDialogDesignLayout.addMultiCellWidget(self.line2,1,1,0,3)

        layout10 = QHBoxLayout(None,0,6,"layout10")

        self.groupLabel = QLabel(self,"groupLabel")
        self.groupLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.groupLabel.sizePolicy().hasHeightForWidth()))
        self.groupLabel.setMinimumSize(QSize(64,64))
        layout10.addWidget(self.groupLabel)

        self.textLabel = QLabel(self,"textLabel")
        layout10.addWidget(self.textLabel)

        GroupDialogDesignLayout.addMultiCellLayout(layout10,0,0,0,3)
        spacer8 = QSpacerItem(21,20,QSizePolicy.Minimum,QSizePolicy.Fixed)
        GroupDialogDesignLayout.addItem(spacer8,10,3)

        layout7 = QHBoxLayout(None,0,6,"layout7")
        Horizontal_Spacing2 = QSpacerItem(290,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout7.addItem(Horizontal_Spacing2)

        self.okButton = QPushButton(self,"okButton")
        self.okButton.setAutoDefault(0)
        self.okButton.setDefault(1)
        layout7.addWidget(self.okButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        self.cancelButton.setAutoDefault(0)
        layout7.addWidget(self.cancelButton)

        GroupDialogDesignLayout.addMultiCellLayout(layout7,12,12,0,3)

        self.line2_2 = QFrame(self,"line2_2")
        self.line2_2.setFrameShape(QFrame.HLine)
        self.line2_2.setFrameShadow(QFrame.Sunken)
        self.line2_2.setFrameShape(QFrame.HLine)

        GroupDialogDesignLayout.addMultiCellWidget(self.line2_2,11,11,0,3)

        self.languageChange()

        self.resize(QSize(522,595).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("clicked()"),self.reject)
        self.connect(self.okButton,SIGNAL("clicked()"),self.accept)
        self.connect(self.groupNameBox,SIGNAL("activated(const QString&)"),self.groupNameChanged)
        self.connect(self.groupNumberBox,SIGNAL("valueChanged(int)"),self.groupNumberChanged)

        self.setTabOrder(self.groupNameBox,self.groupNumberBox)
        self.setTabOrder(self.groupNumberBox,self.groupView)
        self.setTabOrder(self.groupView,self.okButton)
        self.setTabOrder(self.okButton,self.cancelButton)

        self.infoLabel2.setBuddy(self.groupView)


    def languageChange(self):
        self.setCaption(self.__tr("Edit group membership"))
        self.textLabel2.setText(self.__tr("<b>Primary Group</b>"))
        self.textLabel1.setText(self.__tr("LDAP Groups:"))
        self.infoLabel.setText(self.__tr("You may select from the groups available in the LDAP database or enter any ID that is valid on the system below."))
        self.infoLabel2.setText(self.__tr("Select any additional groups the <b>%1</b> user should belong to from the list below."))
        self.groupView.header().setLabel(0,self.__tr("Group"))
        self.groupView.header().setLabel(1,self.__tr("ID"))
        self.groupView.header().setLabel(2,self.__tr("Location"))
        self.textLabel1_2.setText(self.__tr("<b>Additional Groups</b>"))
        self.textLabel3.setText(self.__tr("Group ID:"))
        self.groupLabel.setText(self.__tr("GR","DO NOT TRANSLATE"))
        self.textLabel.setText(self.__tr("Select the groups the <strong>%1</strong> user should belong to."))
        self.okButton.setText(self.__tr("&OK"))
        self.okButton.setAccel(QString.null)
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(QString.null)


    def groupNameChanged(self):
        print "GroupDialogDesign.groupNameChanged(): Not implemented yet"

    def groupNumberChanged(self):
        print "GroupDialogDesign.groupNumberChanged(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("GroupDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = GroupDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
