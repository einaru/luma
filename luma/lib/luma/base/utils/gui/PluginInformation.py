# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/PluginInformation.ui'
#
# Created: Thu Mar 25 00:32:42 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class PluginInformation(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("PluginInformation")


        PluginInformationLayout = QVBoxLayout(self,11,6,"PluginInformationLayout")

        layout8 = QHBoxLayout(None,0,6,"layout8")

        layout5 = QGridLayout(None,1,1,0,6,"layout5")

        self.iconLabel = QLabel(self,"iconLabel")
        self.iconLabel.setSizePolicy(QSizePolicy(0,0,0,0,self.iconLabel.sizePolicy().hasHeightForWidth()))
        self.iconLabel.setMinimumSize(QSize(64,64))
        self.iconLabel.setMaximumSize(QSize(64,64))

        layout5.addWidget(self.iconLabel,0,0)
        spacer7 = QSpacerItem(21,190,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout5.addItem(spacer7,1,0)
        layout8.addLayout(layout5)

        layout6 = QVBoxLayout(None,0,6,"layout6")

        self.textLabel3 = QLabel(self,"textLabel3")
        layout6.addWidget(self.textLabel3)

        self.informationEdit = QTextEdit(self,"informationEdit")
        self.informationEdit.setReadOnly(1)
        layout6.addWidget(self.informationEdit)
        layout8.addLayout(layout6)
        PluginInformationLayout.addLayout(layout8)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)
        PluginInformationLayout.addWidget(self.line1)

        layout7 = QHBoxLayout(None,0,6,"layout7")
        spacer8 = QSpacerItem(421,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout7.addItem(spacer8)

        self.closeButton = QPushButton(self,"closeButton")
        layout7.addWidget(self.closeButton)
        PluginInformationLayout.addLayout(layout7)

        self.languageChange()

        self.resize(QSize(382,266).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.closeButton,SIGNAL("clicked()"),self,SLOT("accept()"))


    def languageChange(self):
        self.setCaption(self.__tr("Plugin Information"))
        self.iconLabel.setText(self.__tr("Icon","DO NOT TRANSLATE"))
        self.textLabel3.setText(self.__tr("Information about this plugin:"))
        self.closeButton.setText(self.__tr("&Close"))
        self.closeButton.setAccel(self.__tr("Alt+C"))


    def __tr(self,s,c = None):
        return qApp.translate("PluginInformation",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = PluginInformation()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
