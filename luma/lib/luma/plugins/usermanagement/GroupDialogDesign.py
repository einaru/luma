# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/usermanagement/GroupDialogDesign.ui'
#
# Created: Mon Apr 26 16:00:33 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
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

        GroupDialogDesignLayout = QVBoxLayout(self,11,6,"GroupDialogDesignLayout")

        layout6 = QHBoxLayout(None,0,6,"layout6")

        self.groupLabel = QLabel(self,"groupLabel")
        self.groupLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.groupLabel.sizePolicy().hasHeightForWidth()))
        self.groupLabel.setMinimumSize(QSize(64,64))
        layout6.addWidget(self.groupLabel)

        self.textLabel = QLabel(self,"textLabel")
        layout6.addWidget(self.textLabel)
        GroupDialogDesignLayout.addLayout(layout6)

        self.line2 = QFrame(self,"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)
        GroupDialogDesignLayout.addWidget(self.line2)

        self.infoLabel = QLabel(self,"infoLabel")
        GroupDialogDesignLayout.addWidget(self.infoLabel)

        layout4 = QGridLayout(None,1,1,0,6,"layout4")

        self.groupNumberBox = QSpinBox(self,"groupNumberBox")
        self.groupNumberBox.setMinimumSize(QSize(70,0))
        self.groupNumberBox.setMaxValue(655535)

        layout4.addWidget(self.groupNumberBox,1,1)

        self.groupNameBox = QComboBox(0,self,"groupNameBox")
        self.groupNameBox.setEditable(0)

        layout4.addWidget(self.groupNameBox,0,1)

        self.textLabel3 = QLabel(self,"textLabel3")
        self.textLabel3.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout4.addWidget(self.textLabel3,1,0)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))
        self.textLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout4.addWidget(self.textLabel1,0,0)
        spacer2 = QSpacerItem(236,31,QSizePolicy.Preferred,QSizePolicy.Minimum)
        layout4.addItem(spacer2,0,2)
        GroupDialogDesignLayout.addLayout(layout4)

        self.line4 = QFrame(self,"line4")
        self.line4.setFrameShape(QFrame.HLine)
        self.line4.setFrameShadow(QFrame.Sunken)
        self.line4.setFrameShape(QFrame.HLine)
        GroupDialogDesignLayout.addWidget(self.line4)

        self.infoLabel2 = QLabel(self,"infoLabel2")
        GroupDialogDesignLayout.addWidget(self.infoLabel2)

        self.groupView = QListView(self,"groupView")
        self.groupView.addColumn(self.__tr("Group"))
        self.groupView.addColumn(self.__tr("ID"))
        self.groupView.addColumn(self.__tr("Location"))
        self.groupView.setAllColumnsShowFocus(1)
        self.groupView.setResizeMode(QListView.LastColumn)
        GroupDialogDesignLayout.addWidget(self.groupView)

        layout3 = QGridLayout(None,1,1,0,6,"layout3")
        Horizontal_Spacing2 = QSpacerItem(348,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout3.addItem(Horizontal_Spacing2,1,0)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        layout3.addMultiCellWidget(self.line1,0,0,0,2)

        self.cancelButton = QPushButton(self,"cancelButton")
        self.cancelButton.setAutoDefault(0)

        layout3.addWidget(self.cancelButton,1,2)

        self.okButton = QPushButton(self,"okButton")
        self.okButton.setAutoDefault(0)
        self.okButton.setDefault(0)

        layout3.addWidget(self.okButton,1,1)
        GroupDialogDesignLayout.addLayout(layout3)

        self.languageChange()

        self.resize(QSize(495,570).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.okButton,SIGNAL("clicked()"),self,SLOT("accept()"))
        self.connect(self.groupNameBox,SIGNAL("activated(const QString&)"),self.groupNameChanged)
        self.connect(self.groupNumberBox,SIGNAL("valueChanged(int)"),self.groupNumberChanged)

        self.infoLabel2.setBuddy(self.groupView)


    def languageChange(self):
        self.setCaption(self.__tr("Edit group membership"))
        self.groupLabel.setText(self.__tr("GR","DO NOT TRANSLATE"))
        self.textLabel.setText(self.__tr("Select the groups the <strong>%1</strong> user should belong to."))
        self.infoLabel.setText(self.__tr("<b>Primary Group</b><br>\n"
"You may select from the groups available in the LDAP database or enter any ID that is valid on the system below."))
        self.textLabel3.setText(self.__tr("Group ID:"))
        self.textLabel1.setText(self.__tr("LDAP Groups:"))
        self.infoLabel2.setText(self.__tr("<b>Additional Groups</b><br>\n"
"Select any additional groups the <b>%1</b> user should belong to from the list below."))
        self.groupView.header().setLabel(0,self.__tr("Group"))
        self.groupView.header().setLabel(1,self.__tr("ID"))
        self.groupView.header().setLabel(2,self.__tr("Location"))
        self.cancelButton.setText(self.__tr("&Cancel"))
        self.cancelButton.setAccel(QString.null)
        self.okButton.setText(self.__tr("&OK"))
        self.okButton.setAccel(QString.null)


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
