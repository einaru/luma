# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/utils/gui/LoggerWidgetDesign.ui'
#
# Created: Wed Aug 17 15:23:52 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt4.QtGui import *

image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x10\x00\x00\x00\x10" \
    "\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\x00\x00\x00" \
    "\xb1\x49\x44\x41\x54\x38\x8d\x95\x93\x4b\x0e\xc3" \
    "\x20\x0c\x44\x9f\xab\xde\x0b\x7a\xb2\x90\x93\x61" \
    "\x4e\x36\x5d\x90\x1f\x69\x43\xc8\x48\xec\xfc\xc6" \
    "\x63\x5b\x98\xa4\xc8\x03\x95\x42\x8e\xd1\x90\xf4" \
    "\x01\x78\x3d\x85\xdd\x01\x12\x66\x96\x01\x6c\x34" \
    "\xc1\x0e\x57\xa5\x34\x57\xa3\x11\x83\x33\xbc\x9b" \
    "\xd8\xfd\x08\xd7\xf0\x0c\xdc\xec\xa0\x0f\x27\x24" \
    "\x7d\x2e\x0d\x46\xe0\xeb\x04\xa5\xe4\x10\x60\x9a" \
    "\xfa\x30\x00\x92\x62\xf3\xdc\xe5\x20\x07\xad\x4a" \
    "\x49\x82\xa4\x5a\xde\xd6\xb7\x57\x28\x25\x97\x18" \
    "\x9b\xae\x41\xc2\xec\x4f\xe7\x45\xef\x1e\x0c\x30" \
    "\x9b\xad\x49\x7f\xe0\x7d\x07\x17\xb0\x03\xa9\x03" \
    "\x03\x98\xdc\xb5\x85\x38\x98\x8c\xc0\x35\x41\x08" \
    "\x5b\x41\x58\xee\x36\x0a\x57\x03\xe0\x68\xf2\x04" \
    "\x86\xd3\x67\x9a\xcd\xf2\x13\x18\xe0\x0b\xb8\xbc" \
    "\xa8\x22\xac\xb4\x8f\x12\x00\x00\x00\x00\x49\x45" \
    "\x4e\x44\xae\x42\x60\x82"

class LoggerWidgetDesign(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("LoggerWidgetDesign")


        LoggerWidgetDesignLayout = QVBoxLayout(self,6,6,"LoggerWidgetDesignLayout")

        self.messageEdit = QTextEdit(self,"messageEdit")
        self.messageEdit.setReadOnly(1)
        LoggerWidgetDesignLayout.addWidget(self.messageEdit)

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.textLabel1 = QLabel(self,"textLabel1")
        layout2.addWidget(self.textLabel1)

        self.errorBox = QCheckBox(self,"errorBox")
        self.errorBox.setChecked(1)
        layout2.addWidget(self.errorBox)

        self.debugBox = QCheckBox(self,"debugBox")
        self.debugBox.setChecked(1)
        layout2.addWidget(self.debugBox)

        self.infoBox = QCheckBox(self,"infoBox")
        self.infoBox.setChecked(1)
        layout2.addWidget(self.infoBox)
        spacer2 = QSpacerItem(141,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer2)

        self.clearButton = QToolButton(self,"clearButton")
        self.clearButton.setIconSet(QIconSet(self.image0))
        self.clearButton.setAutoRaise(1)
        layout2.addWidget(self.clearButton)
        LoggerWidgetDesignLayout.addLayout(layout2)

        self.languageChange()

        self.resize(QSize(516,217).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.clearButton,SIGNAL("clicked()"),self.clearLogger)


    def languageChange(self):
        self.setCaption(self.__tr("Form"))
        self.textLabel1.setText(self.__tr("Display message types:"))
        self.errorBox.setText(self.__tr("Errors"))
        self.debugBox.setText(self.__tr("Debug"))
        self.infoBox.setText(self.__tr("Info"))
        self.clearButton.setText(QString.null)
        QToolTip.add(self.clearButton,self.__tr("Clear"))


    def clearLogger(self):
        print "LoggerWidgetDesign.clearLogger(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("LoggerWidgetDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = LoggerWidgetDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
