# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ServerDialogDesign.ui'
#
# Created: Wed Nov 12 19:30:41 2003
#      by: The PyQt User Interface Compiler (pyuic) 3.7
#
# WARNING! All changes made in this file will be lost!


from qt import *

image0_data = [
"16 16 118 2",
"Qt c None",
"#I c None",
".h c None",
"#N c None",
"#Y c None",
"#S c None",
".a c None",
".t c None",
".K c None",
".u c None",
".9 c None",
"#O c None",
".Z c None",
".i c None",
".n c None",
"#W c #ffb500",
".b c #ffcd00",
"#R c #a25d03",
".L c #ffd52a",
"#f c #ba6910",
"#Z c #d47615",
"#X c #fd9c12",
".8 c #d87e1b",
"#V c #da740e",
"#m c #ffbc23",
".m c #f89e0f",
".Y c #ea8f27",
"#J c #ffa020",
"#l c #e3881f",
".d c #ffb51f",
".o c #fda60e",
".e c #ffc326",
"#H c #ffaa24",
"#v c #ffc22d",
"#T c #fb951e",
".s c #ee9f28",
".w c #ffe54e",
".I c #ffbe54",
".x c #ffe14f",
".# c #ffc512",
"#u c #ffa22a",
".g c #ffbd3d",
".H c #ffba57",
".v c #fff338",
"#. c #f9b53b",
".j c #fecc6a",
".y c #ffd958",
"#e c #f09a2d",
".G c #f1b663",
"#K c #f29319",
".F c #f2c787",
"#z c #f59a1a",
"#g c #f5c03b",
".7 c #f9ac37",
".A c #f9e5bb",
"#U c #fa8b0a",
".E c #fbf2ca",
".X c #fcc355",
"#M c #fd9c1c",
"#n c #fdc92a",
"## c #fee450",
"#P c #ffa113",
"#D c #ffa228",
"#G c #ffa31f",
".J c #ffa426",
"#Q c #ffac22",
"#F c #ffb208",
"#y c #ffb21f",
"#L c #ffb30b",
"#A c #ffb51b",
".0 c #ffc043",
"#x c #ffc11b",
"#E c #ffc12f",
"#w c #ffc818",
"#C c #ffc81a",
"#B c #ffc919",
"#k c #ffca39",
"#p c #ffce2a",
"#s c #ffcf28",
"#t c #ffcf2e",
"#o c #ffd028",
"#r c #ffd029",
"#q c #ffd128",
".M c #ffd155",
".z c #ffd57c",
"#i c #ffda35",
"#j c #ffda36",
"#h c #ffdc35",
".c c #ffdc79",
"#d c #ffdd52",
"#b c #ffe542",
"#c c #ffe641",
"#a c #ffe642",
".6 c #ffee59",
".4 c #ffef51",
".3 c #fff050",
".2 c #fff24c",
".l c #fff2b4",
".5 c #fff350",
".1 c #fffa85",
".S c #fffd5e",
".R c #fffe5b",
".T c #fffe5c",
".q c #ffff53",
".Q c #ffff58",
".U c #ffff5a",
".C c #ffff5b",
".D c #ffff63",
".P c #ffff66",
".V c #ffff6c",
".k c #ffff6d",
".O c #ffff74",
".W c #ffff7f",
".B c #ffff80",
".r c #ffffae",
".p c #ffffc1",
".N c #ffffd2",
".f c #fffff0",
"QtQtQtQtQtQtQt.#.aQtQtQtQtQtQtQt",
"QtQtQtQtQtQt.b.c.dQtQtQtQtQtQtQt",
"QtQtQtQtQtQt.e.f.g.hQtQtQtQtQtQt",
"QtQtQtQtQt.i.j.k.l.mQtQtQtQtQtQt",
"QtQtQtQt.n.o.p.q.r.s.t.uQtQtQtQt",
".v.w.x.y.z.A.B.C.D.E.F.G.H.I.J.K",
".L.M.N.O.P.Q.R.S.T.Q.U.V.W.X.YQt",
"Qt.Z.0.1.2.3.4.4.4.3.5.6.7.8QtQt",
"QtQt.9#.###a#b#b#b#c#d#e#fQtQtQt",
"QtQtQt.9#g#h#i#i#j#h#k#lQtQtQtQt",
"QtQtQt#m#n#o#p#q#r#s#t#uQtQtQtQt",
"QtQtQt#v#w#x#y#z#A#B#C#DQtQtQtQt",
"QtQtQt#E#F#G#H#I#J#K#L#M#NQtQtQt",
"QtQt#O#P#Q#RQtQtQt#S#T#U#VQtQtQt",
"QtQt#W#XQtQtQtQtQtQtQt#Y#ZQtQtQt",
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
        self.basednButton.setPixmap(self.image0)

        tabLayout_2.addWidget(self.basednButton,0,2)
        self.tabWidget2.insertTab(self.tab_2,QString(""))

        groupBox3Layout.addMultiCellWidget(self.tabWidget2,1,1,0,2)

        self.saveButton = QPushButton(self.groupBox3,"saveButton")

        groupBox3Layout.addWidget(self.saveButton,2,2)

        ServerDialogDesignLayout.addWidget(self.groupBox3,1,0)

        self.languageChange()

        self.resize(QSize(626,578).expandedTo(self.minimumSizeHint()))
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
        self.closeButton.setText(self.__tr("Close Dialog"))
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
