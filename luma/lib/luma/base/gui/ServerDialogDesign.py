# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/gui/ServerDialogDesign.ui'
#
# Created: Thu Mar 25 00:32:37 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *

image0_data = [
"16 16 104 2",
"Qt c None",
"#F c #a25d03",
".8 c #ba6910",
"#L c #d47615",
".0 c #d87e1b",
"#I c #da740e",
"#c c #e3881f",
".R c #ea8f27",
".o c #ee9f28",
".7 c #f09a2d",
".A c #f1b663",
"#A c #f29319",
".z c #f2c787",
"#q c #f59a1a",
".9 c #f5c03b",
".j c #f89e0f",
".Z c #f9ac37",
".1 c #f9b53b",
".u c #f9e5bb",
"#H c #fa8b0a",
"#G c #fb951e",
".y c #fbf2ca",
".Q c #fcc355",
"#K c #fd9c12",
"#C c #fd9c1c",
".k c #fda60e",
"#e c #fdc92a",
".g c #fecc6a",
".2 c #fee450",
"#z c #ffa020",
"#D c #ffa113",
"#u c #ffa228",
"#l c #ffa22a",
"#x c #ffa31f",
".D c #ffa426",
"#y c #ffaa24",
"#E c #ffac22",
"#w c #ffb208",
"#p c #ffb21f",
"#B c #ffb30b",
"#J c #ffb500",
"#r c #ffb51b",
".c c #ffb51f",
".B c #ffba57",
"#d c #ffbc23",
".f c #ffbd3d",
".C c #ffbe54",
".S c #ffc043",
"#o c #ffc11b",
"#v c #ffc12f",
"#m c #ffc22d",
".d c #ffc326",
".# c #ffc512",
"#n c #ffc818",
"#t c #ffc81a",
"#s c #ffc919",
"#b c #ffca39",
".a c #ffcd00",
"#g c #ffce2a",
"#j c #ffcf28",
"#k c #ffcf2e",
"#f c #ffd028",
"#i c #ffd029",
"#h c #ffd128",
".F c #ffd155",
".E c #ffd52a",
".t c #ffd57c",
".s c #ffd958",
"## c #ffda35",
"#a c #ffda36",
"#. c #ffdc35",
".b c #ffdc79",
".6 c #ffdd52",
".r c #ffe14f",
".4 c #ffe542",
".q c #ffe54e",
".5 c #ffe641",
".3 c #ffe642",
".Y c #ffee59",
".W c #ffef51",
".V c #fff050",
".U c #fff24c",
".i c #fff2b4",
".p c #fff338",
".X c #fff350",
".T c #fffa85",
".L c #fffd5e",
".K c #fffe5b",
".M c #fffe5c",
".m c #ffff53",
".J c #ffff58",
".N c #ffff5a",
".w c #ffff5b",
".x c #ffff63",
".I c #ffff66",
".O c #ffff6c",
".h c #ffff6d",
".H c #ffff74",
".P c #ffff7f",
".v c #ffff80",
".n c #ffffae",
".l c #ffffc1",
".G c #ffffd2",
".e c #fffff0",
"QtQtQtQtQtQtQt.#QtQtQtQtQtQtQtQt",
"QtQtQtQtQtQt.a.b.cQtQtQtQtQtQtQt",
"QtQtQtQtQtQt.d.e.fQtQtQtQtQtQtQt",
"QtQtQtQtQtQt.g.h.i.jQtQtQtQtQtQt",
"QtQtQtQtQt.k.l.m.n.oQtQtQtQtQtQt",
".p.q.r.s.t.u.v.w.x.y.z.A.B.C.DQt",
".E.F.G.H.I.J.K.L.M.J.N.O.P.Q.RQt",
"QtQt.S.T.U.V.W.W.W.V.X.Y.Z.0QtQt",
"QtQtQt.1.2.3.4.4.4.5.6.7.8QtQtQt",
"QtQtQtQt.9#.#####a#.#b#cQtQtQtQt",
"QtQtQt#d#e#f#g#h#i#j#k#lQtQtQtQt",
"QtQtQt#m#n#o#p#q#r#s#t#uQtQtQtQt",
"QtQtQt#v#w#x#yQt#z#A#B#CQtQtQtQt",
"QtQtQt#D#E#FQtQtQtQt#G#H#IQtQtQt",
"QtQt#J#KQtQtQtQtQtQtQtQt#LQtQtQt",
"QtQtQtQtQtQtQtQtQtQtQtQtQtQtQtQt"
]

class ServerDialogDesign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        self.image0 = QPixmap(image0_data)

        if not name:
            self.setName("ServerDialogDesign")


        ServerDialogDesignLayout = QGridLayout(self,1,1,11,6,"ServerDialogDesignLayout")

        self.closeButton = QPushButton(self,"closeButton")

        ServerDialogDesignLayout.addWidget(self.closeButton,1,1)
        spacer6 = QSpacerItem(561,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        ServerDialogDesignLayout.addItem(spacer6,1,0)

        self.splitter4 = QSplitter(self,"splitter4")
        self.splitter4.setOrientation(QSplitter.Vertical)

        self.groupBox5_2 = QGroupBox(self.splitter4,"groupBox5_2")
        self.groupBox5_2.setColumnLayout(0,Qt.Vertical)
        self.groupBox5_2.layout().setSpacing(6)
        self.groupBox5_2.layout().setMargin(11)
        groupBox5_2Layout = QGridLayout(self.groupBox5_2.layout())
        groupBox5_2Layout.setAlignment(Qt.AlignTop)

        self.addButton = QPushButton(self.groupBox5_2,"addButton")

        groupBox5_2Layout.addWidget(self.addButton,0,1)

        self.deleteButton = QPushButton(self.groupBox5_2,"deleteButton")

        groupBox5_2Layout.addWidget(self.deleteButton,2,1)

        self.modifyButton = QPushButton(self.groupBox5_2,"modifyButton")

        groupBox5_2Layout.addWidget(self.modifyButton,1,1)
        spacer5 = QSpacerItem(20,22,QSizePolicy.Minimum,QSizePolicy.Expanding)
        groupBox5_2Layout.addItem(spacer5,3,1)

        self.serverIconView = QIconView(self.groupBox5_2,"serverIconView")
        self.serverIconView.setMinimumSize(QSize(0,120))
        self.serverIconView.setResizeMode(QIconView.Adjust)
        self.serverIconView.setItemsMovable(0)

        groupBox5_2Layout.addMultiCellWidget(self.serverIconView,0,3,0,0)

        self.groupBox4 = QGroupBox(self.splitter4,"groupBox4")
        self.groupBox4.setColumnLayout(0,Qt.Vertical)
        self.groupBox4.layout().setSpacing(6)
        self.groupBox4.layout().setMargin(11)
        groupBox4Layout = QGridLayout(self.groupBox4.layout())
        groupBox4Layout.setAlignment(Qt.AlignTop)

        self.textLabel11 = QLabel(self.groupBox4,"textLabel11")
        self.textLabel11.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel11.sizePolicy().hasHeightForWidth()))
        self.textLabel11.setMinimumSize(QSize(0,0))

        groupBox4Layout.addWidget(self.textLabel11,0,0)

        self.saveButton = QPushButton(self.groupBox4,"saveButton")

        groupBox4Layout.addWidget(self.saveButton,0,2)

        self.nameLineEdit = QLineEdit(self.groupBox4,"nameLineEdit")

        groupBox4Layout.addWidget(self.nameLineEdit,0,1)

        self.tabWidget2 = QTabWidget(self.groupBox4,"tabWidget2")

        self.tab = QWidget(self.tabWidget2,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")

        self.tlsCheckBox = QCheckBox(self.tab,"tlsCheckBox")
        self.tlsCheckBox.setSizePolicy(QSizePolicy(0,0,0,0,self.tlsCheckBox.sizePolicy().hasHeightForWidth()))

        tabLayout.addMultiCellWidget(self.tlsCheckBox,1,1,0,1)

        layout1 = QVBoxLayout(None,0,6,"layout1")

        self.textLabel8 = QLabel(self.tab,"textLabel8")
        self.textLabel8.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel8.sizePolicy().hasHeightForWidth()))
        layout1.addWidget(self.textLabel8)

        self.textLabel9 = QLabel(self.tab,"textLabel9")
        self.textLabel9.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel9.sizePolicy().hasHeightForWidth()))
        layout1.addWidget(self.textLabel9)

        tabLayout.addLayout(layout1,0,0)
        spacer3 = QSpacerItem(21,81,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer3,2,0)

        layout2 = QVBoxLayout(None,0,6,"layout2")

        self.hostLineEdit = QLineEdit(self.tab,"hostLineEdit")
        layout2.addWidget(self.hostLineEdit)

        self.portSpinBox = QSpinBox(self.tab,"portSpinBox")
        self.portSpinBox.setSizePolicy(QSizePolicy(7,0,0,0,self.portSpinBox.sizePolicy().hasHeightForWidth()))
        self.portSpinBox.setMaxValue(65535)
        self.portSpinBox.setMinValue(1)
        self.portSpinBox.setValue(389)
        layout2.addWidget(self.portSpinBox)

        tabLayout.addLayout(layout2,0,1)
        self.tabWidget2.insertTab(self.tab,QString(""))

        self.tab_2 = QWidget(self.tabWidget2,"tab_2")
        tabLayout_2 = QGridLayout(self.tab_2,1,1,11,6,"tabLayout_2")

        self.textLabel1 = QLabel(self.tab_2,"textLabel1")

        tabLayout_2.addWidget(self.textLabel1,0,0)

        self.baseLineEdit = QLineEdit(self.tab_2,"baseLineEdit")

        tabLayout_2.addWidget(self.baseLineEdit,0,1)

        self.basednButton = QPushButton(self.tab_2,"basednButton")
        self.basednButton.setEnabled(0)
        self.basednButton.setPixmap(self.image0)

        tabLayout_2.addWidget(self.basednButton,0,2)

        self.line3 = QFrame(self.tab_2,"line3")
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setFrameShadow(QFrame.Sunken)
        self.line3.setFrameShape(QFrame.HLine)

        tabLayout_2.addMultiCellWidget(self.line3,1,1,0,2)

        self.bindAnonBox = QCheckBox(self.tab_2,"bindAnonBox")

        tabLayout_2.addMultiCellWidget(self.bindAnonBox,2,2,0,1)
        spacer7 = QSpacerItem(20,101,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout_2.addItem(spacer7,5,1)

        self.textLabel10 = QLabel(self.tab_2,"textLabel10")
        self.textLabel10.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        tabLayout_2.addWidget(self.textLabel10,3,0)

        self.textLabel12 = QLabel(self.tab_2,"textLabel12")
        self.textLabel12.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        tabLayout_2.addWidget(self.textLabel12,4,0)

        self.bindLineEdit = QLineEdit(self.tab_2,"bindLineEdit")

        tabLayout_2.addMultiCellWidget(self.bindLineEdit,3,3,1,2)

        self.passwordLineEdit = QLineEdit(self.tab_2,"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        tabLayout_2.addMultiCellWidget(self.passwordLineEdit,4,4,1,2)
        self.tabWidget2.insertTab(self.tab_2,QString(""))

        groupBox4Layout.addMultiCellWidget(self.tabWidget2,1,1,0,2)

        ServerDialogDesignLayout.addMultiCellWidget(self.splitter4,0,0,0,1)

        self.languageChange()

        self.resize(QSize(487,486).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.closeButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(self.saveButton,SIGNAL("clicked()"),self.saveServer)
        self.connect(self.bindAnonBox,SIGNAL("toggled(bool)"),self.bind_anon)
        self.connect(self.basednButton,SIGNAL("clicked()"),self.searchBaseDN)
        self.connect(self.addButton,SIGNAL("clicked()"),self.addServer)
        self.connect(self.modifyButton,SIGNAL("clicked()"),self.modifyServer)
        self.connect(self.serverIconView,SIGNAL("selectionChanged()"),self.serverSelectionChanged)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteServer)

        self.setTabOrder(self.serverIconView,self.addButton)
        self.setTabOrder(self.addButton,self.modifyButton)
        self.setTabOrder(self.modifyButton,self.deleteButton)
        self.setTabOrder(self.deleteButton,self.nameLineEdit)
        self.setTabOrder(self.nameLineEdit,self.hostLineEdit)
        self.setTabOrder(self.hostLineEdit,self.portSpinBox)
        self.setTabOrder(self.portSpinBox,self.baseLineEdit)
        self.setTabOrder(self.baseLineEdit,self.bindLineEdit)
        self.setTabOrder(self.bindLineEdit,self.passwordLineEdit)
        self.setTabOrder(self.passwordLineEdit,self.saveButton)
        self.setTabOrder(self.saveButton,self.closeButton)


    def languageChange(self):
        self.setCaption(self.__tr("Manage Server List"))
        self.closeButton.setText(self.__tr("&Close"))
        self.closeButton.setAccel(self.__tr("Alt+C"))
        self.groupBox5_2.setTitle(self.__tr("Server List"))
        self.addButton.setText(self.__tr("&Add"))
        self.addButton.setAccel(self.__tr("Alt+A"))
        self.deleteButton.setText(self.__tr("&Delete"))
        self.deleteButton.setAccel(self.__tr("Alt+D"))
        self.modifyButton.setText(self.__tr("&Modify"))
        self.modifyButton.setAccel(self.__tr("Alt+M"))
        self.groupBox4.setTitle(self.__tr("Server Information"))
        self.textLabel11.setText(self.__tr("Server Name:"))
        self.saveButton.setText(self.__tr("&Save"))
        self.saveButton.setAccel(self.__tr("Alt+S"))
        self.tlsCheckBox.setText(self.__tr("Use TLS"))
        QToolTip.add(self.tlsCheckBox,self.__tr("User Transport Layer Security"))
        self.textLabel8.setText(self.__tr("Host:"))
        self.textLabel9.setText(self.__tr("Port:"))
        self.tabWidget2.changeTab(self.tab,self.__tr("Network Options"))
        self.textLabel1.setText(self.__tr("Base DN:"))
        self.basednButton.setText(QString.null)
        self.bindAnonBox.setText(self.__tr("Bind anonymously"))
        self.textLabel10.setText(self.__tr("Bind DN:"))
        self.textLabel12.setText(self.__tr("Bind Password:"))
        self.tabWidget2.changeTab(self.tab_2,self.__tr("Authentification Options"))


    def serverSelectionChanged(self):
        print "ServerDialogDesign.serverSelectionChanged(): Not implemented yet"

    def deleteServer(self):
        print "ServerDialogDesign.deleteServer(): Not implemented yet"

    def saveServer(self):
        print "ServerDialogDesign.saveServer(): Not implemented yet"

    def addServer(self):
        print "ServerDialogDesign.addServer(): Not implemented yet"

    def modifyServer(self):
        print "ServerDialogDesign.modifyServer(): Not implemented yet"

    def bind_anon(self):
        print "ServerDialogDesign.bind_anon(): Not implemented yet"

    def searchBaseDN(self):
        print "ServerDialogDesign.searchBaseDN(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ServerDialogDesign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ServerDialogDesign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
