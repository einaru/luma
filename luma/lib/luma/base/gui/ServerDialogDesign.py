# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/wido/src/luma/lib/luma/base/gui/ServerDialogDesign.ui'
#
# Created: Sat Jan 10 00:41:42 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.8.1
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

        self.groupBox4 = QGroupBox(self,"groupBox4")
        self.groupBox4.setSizePolicy(QSizePolicy(5,3,0,0,self.groupBox4.sizePolicy().hasHeightForWidth()))
        self.groupBox4.setColumnLayout(0,Qt.Vertical)
        self.groupBox4.layout().setSpacing(6)
        self.groupBox4.layout().setMargin(11)
        groupBox4Layout = QGridLayout(self.groupBox4.layout())
        groupBox4Layout.setAlignment(Qt.AlignTop)

        self.serverIconView = QIconView(self.groupBox4,"serverIconView")
        self.serverIconView.setMinimumSize(QSize(0,120))
        self.serverIconView.setResizeMode(QIconView.Adjust)
        self.serverIconView.setItemsMovable(0)

        groupBox4Layout.addMultiCellWidget(self.serverIconView,0,0,0,2)

        self.addButton = QPushButton(self.groupBox4,"addButton")

        groupBox4Layout.addWidget(self.addButton,1,0)

        self.deleteButton = QPushButton(self.groupBox4,"deleteButton")

        groupBox4Layout.addWidget(self.deleteButton,1,2)

        self.modifyButton = QPushButton(self.groupBox4,"modifyButton")

        groupBox4Layout.addWidget(self.modifyButton,1,1)

        ServerDialogDesignLayout.addWidget(self.groupBox4,0,0)

        self.closeButton = QPushButton(self,"closeButton")

        ServerDialogDesignLayout.addWidget(self.closeButton,3,0)
        spacer = QSpacerItem(41,70,QSizePolicy.Minimum,QSizePolicy.Expanding)
        ServerDialogDesignLayout.addItem(spacer,2,0)

        self.groupBox3 = QGroupBox(self,"groupBox3")
        self.groupBox3.setColumnLayout(0,Qt.Vertical)
        self.groupBox3.layout().setSpacing(6)
        self.groupBox3.layout().setMargin(11)
        groupBox3Layout = QGridLayout(self.groupBox3.layout())
        groupBox3Layout.setAlignment(Qt.AlignTop)

        self.textLabel11 = QLabel(self.groupBox3,"textLabel11")
        self.textLabel11.setSizePolicy(QSizePolicy(5,5,0,0,self.textLabel11.sizePolicy().hasHeightForWidth()))
        self.textLabel11.setMinimumSize(QSize(120,0))

        groupBox3Layout.addWidget(self.textLabel11,0,0)

        self.nameLineEdit = QLineEdit(self.groupBox3,"nameLineEdit")

        groupBox3Layout.addMultiCellWidget(self.nameLineEdit,0,0,1,2)
        spacer_2 = QSpacerItem(340,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox3Layout.addMultiCell(spacer_2,2,2,0,1)

        self.tabWidget2 = QTabWidget(self.groupBox3,"tabWidget2")

        self.tab = QWidget(self.tabWidget2,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")

        self.textLabel8 = QLabel(self.tab,"textLabel8")
        self.textLabel8.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel8.sizePolicy().hasHeightForWidth()))
        self.textLabel8.setMinimumSize(QSize(140,0))

        tabLayout.addWidget(self.textLabel8,0,0)

        self.hostLineEdit = QLineEdit(self.tab,"hostLineEdit")

        tabLayout.addWidget(self.hostLineEdit,0,1)

        self.textLabel9 = QLabel(self.tab,"textLabel9")
        self.textLabel9.setSizePolicy(QSizePolicy(0,5,0,0,self.textLabel9.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.textLabel9,1,0)

        self.portSpinBox = QSpinBox(self.tab,"portSpinBox")
        self.portSpinBox.setSizePolicy(QSizePolicy(7,0,0,0,self.portSpinBox.sizePolicy().hasHeightForWidth()))
        self.portSpinBox.setMaxValue(65535)
        self.portSpinBox.setMinValue(1)

        tabLayout.addWidget(self.portSpinBox,1,1)

        self.tlsCheckBox = QCheckBox(self.tab,"tlsCheckBox")
        self.tlsCheckBox.setSizePolicy(QSizePolicy(0,0,0,0,self.tlsCheckBox.sizePolicy().hasHeightForWidth()))

        tabLayout.addWidget(self.tlsCheckBox,2,0)
        spacer_3 = QSpacerItem(21,81,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabLayout.addItem(spacer_3,3,0)
        self.tabWidget2.insertTab(self.tab,QString(""))

        self.tab_2 = QWidget(self.tabWidget2,"tab_2")
        tabLayout_2 = QGridLayout(self.tab_2,1,1,11,6,"tabLayout_2")

        self.textLabel1 = QLabel(self.tab_2,"textLabel1")

        tabLayout_2.addWidget(self.textLabel1,0,0)

        self.groupBox5 = QGroupBox(self.tab_2,"groupBox5")
        self.groupBox5.setColumnLayout(0,Qt.Vertical)
        self.groupBox5.layout().setSpacing(6)
        self.groupBox5.layout().setMargin(11)
        groupBox5Layout = QGridLayout(self.groupBox5.layout())
        groupBox5Layout.setAlignment(Qt.AlignTop)

        self.bindAnonBox = QCheckBox(self.groupBox5,"bindAnonBox")

        groupBox5Layout.addMultiCellWidget(self.bindAnonBox,0,0,0,1)

        self.textLabel10 = QLabel(self.groupBox5,"textLabel10")

        groupBox5Layout.addWidget(self.textLabel10,1,0)

        self.bindLineEdit = QLineEdit(self.groupBox5,"bindLineEdit")

        groupBox5Layout.addWidget(self.bindLineEdit,1,1)

        self.textLabel12 = QLabel(self.groupBox5,"textLabel12")

        groupBox5Layout.addWidget(self.textLabel12,2,0)

        self.passwordLineEdit = QLineEdit(self.groupBox5,"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        groupBox5Layout.addWidget(self.passwordLineEdit,2,1)
        spacer_4 = QSpacerItem(21,61,QSizePolicy.Minimum,QSizePolicy.Expanding)
        groupBox5Layout.addItem(spacer_4,3,0)

        tabLayout_2.addMultiCellWidget(self.groupBox5,1,1,0,2)

        self.baseLineEdit = QLineEdit(self.tab_2,"baseLineEdit")

        tabLayout_2.addWidget(self.baseLineEdit,0,1)

        self.basednButton = QPushButton(self.tab_2,"basednButton")
        self.basednButton.setEnabled(0)
        self.basednButton.setPixmap(self.image0)

        tabLayout_2.addWidget(self.basednButton,0,2)
        self.tabWidget2.insertTab(self.tab_2,QString(""))

        groupBox3Layout.addMultiCellWidget(self.tabWidget2,1,1,0,2)

        self.saveButton = QPushButton(self.groupBox3,"saveButton")

        groupBox3Layout.addWidget(self.saveButton,2,2)

        ServerDialogDesignLayout.addWidget(self.groupBox3,1,0)

        self.languageChange()

        self.resize(QSize(399,582).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.closeButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.deleteServer)
        self.connect(self.saveButton,SIGNAL("clicked()"),self.saveServer)
        self.connect(self.serverIconView,SIGNAL("selectionChanged()"),self.serverSelectionChanged)
        self.connect(self.addButton,SIGNAL("clicked()"),self.addServer)
        self.connect(self.modifyButton,SIGNAL("clicked()"),self.modifyServer)
        self.connect(self.bindAnonBox,SIGNAL("toggled(bool)"),self.bind_anon)
        self.connect(self.basednButton,SIGNAL("clicked()"),self.searchBaseDN)

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
        self.groupBox4.setTitle(self.__tr("Server List"))
        self.addButton.setText(self.__tr("Add Server"))
        self.deleteButton.setText(self.__tr("Delete Server"))
        self.modifyButton.setText(self.__tr("Modify Server"))
        self.closeButton.setText(self.__tr("Close"))
        self.groupBox3.setTitle(self.__tr("Server Info"))
        self.textLabel11.setText(self.__tr("Server Name:"))
        self.textLabel8.setText(self.__tr("LDAP Host:"))
        self.textLabel9.setText(self.__tr("LDAP Port:"))
        self.tlsCheckBox.setText(self.__tr("Use TLS"))
        QToolTip.add(self.tlsCheckBox,self.__tr("User Transport Layer Security"))
        self.tabWidget2.changeTab(self.tab,self.__tr("Server Options"))
        self.textLabel1.setText(self.__tr("Base DN:"))
        self.groupBox5.setTitle(self.__tr("Authentification Method"))
        self.bindAnonBox.setText(self.__tr("Bind anonymously"))
        self.textLabel10.setText(self.__tr("Bind DN:"))
        self.textLabel12.setText(self.__tr("Bind Password:"))
        self.basednButton.setText(QString.null)
        self.tabWidget2.changeTab(self.tab_2,self.__tr("Connection Options"))
        self.saveButton.setText(self.__tr("Save Server Information"))


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
