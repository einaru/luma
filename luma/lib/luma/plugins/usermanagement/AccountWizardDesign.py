# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/plugins/usermanagement/AccountWizardDesign.ui'
#
# Created: Mon Apr 26 16:00:34 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class AccountWizardDesign(QWizard):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QWizard.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("AccountWizardDesign")



        self.WizardPage = QWidget(self,"WizardPage")
        WizardPageLayout = QGridLayout(self.WizardPage,1,1,11,6,"WizardPageLayout")

        self.locationLabel = QLabel(self.WizardPage,"locationLabel")
        self.locationLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.locationLabel.sizePolicy().hasHeightForWidth()))
        self.locationLabel.setMinimumSize(QSize(64,64))

        WizardPageLayout.addWidget(self.locationLabel,0,0)

        self.line1 = QFrame(self.WizardPage,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        WizardPageLayout.addMultiCellWidget(self.line1,1,1,0,2)

        self.textLabel2 = QLabel(self.WizardPage,"textLabel2")
        self.textLabel2.setSizePolicy(QSizePolicy(5,1,0,0,self.textLabel2.sizePolicy().hasHeightForWidth()))

        WizardPageLayout.addMultiCellWidget(self.textLabel2,0,0,1,2)

        self.browserFrame = QFrame(self.WizardPage,"browserFrame")
        self.browserFrame.setFrameShape(QFrame.NoFrame)
        self.browserFrame.setFrameShadow(QFrame.Raised)

        WizardPageLayout.addMultiCellWidget(self.browserFrame,2,2,0,2)

        self.locationEdit = QLineEdit(self.WizardPage,"locationEdit")
        self.locationEdit.setReadOnly(1)

        WizardPageLayout.addWidget(self.locationEdit,3,2)

        self.textLabel3 = QLabel(self.WizardPage,"textLabel3")

        WizardPageLayout.addMultiCellWidget(self.textLabel3,3,3,0,1)
        self.addPage(self.WizardPage,QString(""))

        self.WizardPage_2 = QWidget(self,"WizardPage_2")
        WizardPageLayout_2 = QVBoxLayout(self.WizardPage_2,0,6,"WizardPageLayout_2")

        self.accountFrame = QFrame(self.WizardPage_2,"accountFrame")
        self.accountFrame.setFrameShape(QFrame.NoFrame)
        self.accountFrame.setFrameShadow(QFrame.Sunken)
        WizardPageLayout_2.addWidget(self.accountFrame)
        self.addPage(self.WizardPage_2,QString(""))

        self.languageChange()

        self.resize(QSize(617,486).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Add Contact"))
        self.locationLabel.setText(self.__tr("LOC","DO NOT TRANSLATE"))
        self.textLabel2.setText(self.__tr("Please select a location where the new account should be stored."))
        self.textLabel3.setText(self.__tr("Location:"))
        self.setTitle(self.WizardPage,self.__tr("Select location"))
        self.setTitle(self.WizardPage_2,self.__tr("Fill contact data"))


    def __tr(self,s,c = None):
        return qApp.translate("AccountWizardDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = AccountWizardDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
