# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutDialog.ui'
#
# Created: Sun Nov 9 00:44:30 2003
#      by: The PyQt User Interface Compiler (pyuic) 3.7
#
# WARNING! All changes made in this file will be lost!


from qt import *


class AboutDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("AboutDialog")


        AboutDialogLayout = QVBoxLayout(self,11,6,"AboutDialogLayout")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(3,3,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))
        AboutDialogLayout.addWidget(self.textLabel1)

        layout2 = QHBoxLayout(None,0,6,"layout2")
        spacer = QSpacerItem(210,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer)

        self.pushButton1 = QPushButton(self,"pushButton1")
        self.pushButton1.setSizePolicy(QSizePolicy(0,0,0,0,self.pushButton1.sizePolicy().hasHeightForWidth()))
        layout2.addWidget(self.pushButton1)
        spacer_2 = QSpacerItem(171,31,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer_2)
        AboutDialogLayout.addLayout(layout2)

        self.languageChange()

        self.resize(QSize(629,593).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton1,SIGNAL("clicked()"),self,SLOT("close()"))


    def languageChange(self):
        self.setCaption(self.__tr("About Luma"))
        self.textLabel1.setText(self.__tr("<p align=\"center\">Luma Version 1.0beta1</p>\n"
"<p align=\"center\">Copyright (C) 2003 Wido Depping. All rights reserved<br><br>\n"
"Luma is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.<br><br>\n"
"Luma is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.<br><br>\n"
"You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA\n"
"</p>"))
        self.pushButton1.setText(self.__tr("OK"))


    def __tr(self,s,c = None):
        return qApp.translate("AboutDialog",s,c)
