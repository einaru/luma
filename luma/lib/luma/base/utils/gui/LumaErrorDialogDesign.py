# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './lib/luma/base/utils/gui/LumaErrorDialogDesign.ui'
#
# Created: Tue Mar 1 22:47:19 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14
#
# WARNING! All changes made in this file will be lost!


from qt import *


class LumaErrorDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("LumaErrorDialogDesign")


        LumaErrorDialogDesignLayout = QGridLayout(self,1,1,6,6,"LumaErrorDialogDesignLayout")

        self.pixmapLabel = QLabel(self,"pixmapLabel")
        self.pixmapLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.pixmapLabel.sizePolicy().hasHeightForWidth()))
        self.pixmapLabel.setMinimumSize(QSize(64,64))

        LumaErrorDialogDesignLayout.addWidget(self.pixmapLabel,0,0)

        self.errorLabel = QLabel(self,"errorLabel")
        self.errorLabel.setTextFormat(QLabel.RichText)
        self.errorLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        LumaErrorDialogDesignLayout.addMultiCellWidget(self.errorLabel,0,1,1,1)
        spacer2 = QSpacerItem(21,290,QSizePolicy.Minimum,QSizePolicy.Expanding)
        LumaErrorDialogDesignLayout.addItem(spacer2,1,0)

        layout1 = QHBoxLayout(None,0,6,"layout1")
        spacer1 = QSpacerItem(490,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout1.addItem(spacer1)

        self.okButton = QPushButton(self,"okButton")
        layout1.addWidget(self.okButton)

        LumaErrorDialogDesignLayout.addMultiCellLayout(layout1,3,3,0,1)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        LumaErrorDialogDesignLayout.addMultiCellWidget(self.line1,2,2,0,1)

        self.languageChange()

        self.resize(QSize(398,213).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.okButton,SIGNAL("clicked()"),self.accept)


    def languageChange(self):
        self.setCaption(self.__tr("Error"))
        self.pixmapLabel.setText(self.__tr("EL"))
        self.errorLabel.setText(QString.null)
        self.okButton.setText(self.__tr("&OK"))
        self.okButton.setAccel(self.__tr("Alt+O"))


    def __tr(self,s,c = None):
        return qApp.translate("LumaErrorDialogDesign",s,c)
