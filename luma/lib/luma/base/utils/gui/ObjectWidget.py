###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import copy
import ldap
import ldap.modlist
import re
import time
from qt import *

from base.backend.ServerList import ServerList
from base.backend.DirUtils import DirUtils
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo

class ObjectWidget(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        self.mainGrid = QGridLayout(self, 1, 1, 11, 6)

        self.attributeFrame = QScrollView(self,"attributeFrame")
        self.attributeFrame.setMinimumSize(QSize(300,100))
        self.attributeFrame.setFrameShape(QFrame.StyledPanel)
        self.attributeFrame.setFrameShadow(QFrame.Raised)
        self.attributeFrame.setResizePolicy(QScrollView.AutoOneFit)
        self.mainGrid.addWidget(self.attributeFrame,0,0)

        self.buttonFrame = QFrame(self, "buttonFrame")
        self.buttonFrame.setSizePolicy(QSizePolicy(5,0,0,0,
            self.buttonFrame.sizePolicy().hasHeightForWidth()))
        self.buttonFrame.setFrameShape(QFrame.StyledPanel)
        self.buttonFrame.setFrameShadow(QFrame.Raised)
        self.buttonFrameLayout = QHBoxLayout(self.buttonFrame,11,6,"buttonFrameLayout")

        self.applyButton = QPushButton(self.buttonFrame,"applyButton")
        self.applyButton.setText(self.trUtf8("Apply"))
        self.buttonFrameLayout.addWidget(self.applyButton)
        spacer = QSpacerItem(100,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.buttonFrameLayout.addItem(spacer)

        self.displayAllButton = QPushButton(self.buttonFrame,"displayAllButton")
        self.displayAllButton.setText(self.trUtf8("Display all Attributes"))
        self.buttonFrameLayout.addWidget(self.displayAllButton)
        spacer = QSpacerItem(100,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.buttonFrameLayout.addItem(spacer)

        self.refreshButton = QPushButton(self.buttonFrame,"refeshButton")
        self.refreshButton.setText(self.trUtf8("Refresh"))
        self.buttonFrameLayout.addWidget(self.refreshButton)

        self.mainGrid.addWidget(self.buttonFrame,1,0)

        self.connect(self.applyButton,SIGNAL("clicked()"),self.apply_view)
        self.connect(self.refreshButton,SIGNAL("clicked()"),self.refresh_view)
        self.connect(self.displayAllButton, SIGNAL("clicked()"), self.display_all_attributes)

        self.attributeWidget = QWidget(self.attributeFrame.viewport())
        self.attributeWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.attributeGrid = QGridLayout(self.attributeWidget, 1, 1, 11, 6, "gridLayout")
        self.attributeFrame.addChild(self.attributeWidget)


        self.SERVER = ""
        self.DN = ""
        self.CURRENTVALUES = {}
        self.WIDGETLIST = []
        self.ADDED_ATTRIBUTES = []

        self.SERVERMETA = None

###############################################################################

    def display_values(self):
        self.WIDGETLIST = []
        for x in  self.attributeWidget.children():
            name = str(x.name())
            if name[:4] == "LDAP":
                x.deleteLater()


        header1 = QLabel(self.attributeWidget, "LDAP_HEADER")
        header1.setText(self.trUtf8("<b>Attributes</b>"))
        header1.setAlignment(Qt.AlignLeft)
        header1.setSizePolicy(QSizePolicy(5,0,0,0,header1.sizePolicy().hasHeightForWidth()))
        header1.show()

        header2 = QLabel(self.attributeWidget, "LDAP_HEADER")
        header2.setText(self.trUtf8("<b>Values</b>"))
        header2.setAlignment(Qt.AlignHCenter)
        header2.setSizePolicy(QSizePolicy(5,0,0,0,header2.sizePolicy().hasHeightForWidth()))
        header2.show()

        self.attributeGrid.addWidget(header1, 0, 0)
        self.attributeGrid.addWidget(header2, 0, 1)

        self.WIDGETLIST.append([header1, header2])

        offset = 1
        offset = self.__add_entries("dn", [self.DN], offset, 0, 1, None)

        dataCopy = copy.deepcopy(self.CURRENTVALUES)
        offset = self.__add_entries("objectClass", dataCopy["objectClass"], offset, 0, 1, None)
        tmpObjectClasses = copy.deepcopy(dataCopy["objectClass"])
        del dataCopy["objectClass"]

        keyList = dataCopy.keys()
        for x in keyList:
            tmpOffset = offset + len(dataCopy[x])
            self.__add_entries(x, dataCopy[x], offset, 1, 0, tmpObjectClasses)
            offset = tmpOffset

        # create a foo label
        fooLabel = QLabel(self.attributeWidget, "LDAP__FOO__")
        fooLabel.show()
        self.attributeGrid.addWidget(fooLabel, offset, 0)

        # deletes the foo label
        self.attributeWidget.removeChild(fooLabel)

###############################################################################

    def apply_view(self):
        modListDict = {}
        for x in self.WIDGETLIST[2:]:
            labelText = str(x[0].text())
            if (labelText[0:3] == "<b>"):
                labelText = labelText[3:-4]
            valueText = str(x[1].text())
            if not ((labelText in modListDict.keys()) and (valueText == '')):
                if modListDict.has_key(labelText):
                    modListDict[labelText].append(valueText)
                else:
                    modListDict[labelText] = [valueText]
        tmpObjectClasses = copy.deepcopy(modListDict['objectClass'])
        del modListDict['objectClass']

        tmpModlist = []
        for x in modListDict.keys():
            if not ((self.SERVERMETA.is_must(x, tmpObjectClasses)) and (len(modListDict[x]) == 1) and (modListDict[x][0] == '')):
                if not (x in self.ADDED_ATTRIBUTES):
                    tmpModlist.append((1, x, None))
                tmpList = []
                for y in modListDict[x]:
                    if not (y == ''):
                        tmpList.append(y)
                if not(len(tmpList) == 0):
                    tmpModlist.append((0, x, tmpList))

        tmpObject = ServerList()
        tmpObject.readServerList()
        serverMeta = ""
        for x in tmpObject.SERVERLIST:
            if x.name == self.SERVER:
                serverMeta = x
                break
        try:
            ldapServerObject = ldap.open(serverMeta.host, serverMeta.port)
            ldapServerObject.protocol_version = ldap.VERSION3
            if serverMeta.tls == "1":
                ldapServerObject.start_tls_s()
            ldapServerObject.simple_bind_s(serverMeta.bindDN,
                                serverMeta.bindPassword)
            searchResult = ldapServerObject.modify_s(self.DN, tmpModlist)
            ldapServerObject.unbind()
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
        self.refresh_view()


###############################################################################

    def refresh_view(self):
        tmpObject = ServerList()
        tmpObject.readServerList()
        serverMeta = tmpObject.get_serverobject(self.SERVER)
        self.ADDED_ATTRIBUTES = []
        self.CURRENTVALUES = {}
        try:
            ldapServerObject = ldap.open(serverMeta.host, serverMeta.port)
            ldapServerObject.protocol_version = ldap.VERSION3
            if serverMeta.tls == "1":
                ldapServerObject.start_tls_s()
            ldapServerObject.simple_bind_s(serverMeta.bindDN,
                                serverMeta.bindPassword)
            searchResult = ldapServerObject.search_s(self.DN, ldap.SCOPE_BASE)
            ldapServerObject.unbind()
            self.convert_values(searchResult)
            self.display_values()
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)

###############################################################################

    def __add_entries(self, attribute, valueList=[], offset=0, editable=0, bold=0, objectClasses=None):
        laenge = range(offset, len(valueList)+offset)
        tmpIconDir = DirUtils().PREFIX + "/share/luma/icons"
        newIcon = tmpIconDir + "/new.png"
        delIcon = tmpIconDir + "/clear.png"
        for x in laenge:
            label = QLabel(self.attributeWidget, "LDAP_ATTRIBUTE")
            if (bold) or (self.SERVERMETA.is_must(attribute, objectClasses)):
                label.setText("<b>" + attribute + "</b>")
            else:
                label.setText(attribute)
            label.setAlignment(Qt.AlignLeft)

            value = QLineEdit(self.attributeWidget, "LDAP_VALUE")
            value.setText(valueList[x-offset])
            value.setAlignment(Qt.AlignLeft)
            if not editable:
                value.setReadOnly(1)

            self.attributeGrid.addWidget(label, x, 0)
            self.attributeGrid.addWidget(value, x, 1)
            label.show()
            value.show()

            if (not (self.SERVERMETA.is_single(attribute)) and
                                (not((attribute=="objectClass") or (attribute=="dn")))):
                addButton = QPushButton(self.attributeWidget, "LDAP_" + attribute)
                addButton.setPixmap(QPixmap(newIcon))
                addButton.show()
                self.connect(addButton,SIGNAL("clicked()"),self.display_values)
                addButton.installEventFilter(self)
                self.attributeGrid.addWidget(addButton, x, 2)
                self.WIDGETLIST.append([label, value, addButton])
            else:
                self.WIDGETLIST.append([label, value])
        return len(valueList)+offset

###############################################################################

    def set_server(self, server):
        if not (server == self.SERVER):
            self.SERVER = server
            self.SERVERMETA = ObjectClassAttributeInfo(self.SERVER)


###############################################################################

    def convert_values(self, values):
        tmpTupel = values[0]
        self.CURRENTVALUES = tmpTupel[1]
        self.DN = tmpTupel[0]

###############################################################################

    def display_all_attributes(self):
        allAttributes = self.SERVERMETA.get_all_attributes(self.CURRENTVALUES['objectClass'])
        for x in allAttributes:
            if not (self.CURRENTVALUES.has_key(x)):
                self.CURRENTVALUES[x] = ['']
                self.ADDED_ATTRIBUTES.append(x)
        self.display_values()

###############################################################################

    def init_view(self, server, values):
        self.set_server(server)
        self.convert_values(values)
        self.display_values()

###############################################################################

    def eventFilter(self, object, event):
        if (event.type() == QEvent.MouseButtonPress):
            name = str(object.name())
            self.CURRENTVALUES[name[5:]].append('')
        return 0
