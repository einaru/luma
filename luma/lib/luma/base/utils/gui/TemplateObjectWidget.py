# -*- coding: utf-8 -*-

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
import os.path

from base.backend.ServerList import ServerList
import environment
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo

class TemplateObjectWidget(QWidget):
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

        # create restore button
        self.restoreButton = QPushButton(self.buttonFrame,"restoreButton")
        self.restoreButton.setText(self.trUtf8("Reset Values"))
        self.buttonFrameLayout.addWidget(self.restoreButton)
        spacer = QSpacerItem(100,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.buttonFrameLayout.addItem(spacer)
        
        # create display-all button
        self.displayAllButton = QPushButton(self.buttonFrame,"displayAllButton")
        self.displayAllButton.setText(self.trUtf8("Display all Attributes"))
        self.buttonFrameLayout.addWidget(self.displayAllButton)
        spacer = QSpacerItem(100,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.buttonFrameLayout.addItem(spacer)
        
        # create save button
        self.saveButton = QPushButton(self.buttonFrame,"applyButton")
        self.saveButton.setText(self.trUtf8("Save"))
        self.buttonFrameLayout.addWidget(self.saveButton)

        self.mainGrid.addWidget(self.buttonFrame,1,0)

        # connect signals and slots for buttons
        self.connect(self.saveButton,SIGNAL("clicked()"),self.save_view)
        self.connect(self.displayAllButton, SIGNAL("clicked()"), self.display_all_attributes)
        self.connect(self.restoreButton,SIGNAL("clicked()"),self.restore_view)

        self.attributeWidget = QWidget(self.attributeFrame.viewport())
        self.attributeWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.attributeGrid = QGridLayout(self.attributeWidget, 1, 1, 11, 6, "gridLayout")
        self.attributeFrame.addChild(self.attributeWidget)


        self.SERVER = ""
        self.DN = ""
        self.WIDGETLIST = []


###############################################################################

    def display_values(self):
        self.WIDGETLIST = []
        for x in  self.attributeWidget.children():
            name = str(x.name())
            if name[:4] == "LDAP":
                x.deleteLater()


        header1 = QLabel(self.attributeWidget, "LDAP_HEADER")
        header1.setText("<b>Attributes</b>")
        header1.setAlignment(Qt.AlignLeft)
        header1.setSizePolicy(QSizePolicy(5,0,0,0,header1.sizePolicy().hasHeightForWidth()))
        header1.show()

        header2 = QLabel(self.attributeWidget, "LDAP_HEADER")
        header2.setText("<b>Values</b>")
        header2.setAlignment(Qt.AlignHCenter)
        header2.setSizePolicy(QSizePolicy(5,0,0,0,header2.sizePolicy().hasHeightForWidth()))
        header2.show()

        self.attributeGrid.addWidget(header1, 0, 0)
        self.attributeGrid.addWidget(header2, 0, 1)
        self.WIDGETLIST.append([header1, header2])
        
        label = QLabel(self.attributeWidget, 'LDAP_LABEL')
        label.setText('<b>dn</b>')
        label.setAlignment(Qt.AlignLeft)
        label.show()

        value = QLineEdit(self.attributeWidget, 'LDAP_VALUE')
        value.setText(self.DN)
        value.setAlignment(Qt.AlignLeft)
        value.show()
        
        self.attributeGrid.addWidget(label, 1, 0)
        self.attributeGrid.addWidget(value, 1, 1)
        self.WIDGETLIST.append([label, value])

        offset = 1
        offset = self.add_entries(offset, 1)
        offset = self.add_entries(offset, 0)

        # create a foo label
        fooLabel = QLabel(self.attributeWidget, "LDAP__FOO__")
        fooLabel.show()
        self.attributeGrid.addWidget(fooLabel, offset+1, 0)

        # deletes the foo label
        self.attributeWidget.removeChild(fooLabel)

###############################################################################

    def get_values(self):
        for x in self.attributes.keys():
            self.attributes[x]['VALUES'] = []
        for x in self.WIDGETLIST[1:]:
            labelText = str(x[0].text())
            if (labelText[0:3] == '<b>'):
                labelText = labelText[3:-4]
            valueText = str(x[1].text()).strip()
            if labelText == 'objectClass':
                continue
            if labelText == 'dn':
                self.DN = valueText[:]
                continue
            if valueText == '':
                continue
            self.attributes[labelText]['VALUES'].append(valueText[:])
            
            
            
    
###############################################################################

    def save_view(self):
        self.get_values()
        tmpModlist = []
        
        # commented out because it wouldn't work. but it did before
        # maybe a change in python-ldap???
        #for x in self.objectClasses:
        #    tmpModlist.append(('objectClass', x))
        tmpModlist.append(('objectClass', self.objectClasses))
        
        for x in self.attributes.keys():
            if len(self.attributes[x]['VALUES']) > 0:
                tmpModlist.append((x, self.attributes[x]['VALUES']))
        
        tmpObject = ServerList()
        tmpObject.readServerList()
        serverMeta = tmpObject.get_serverobject(self.SERVER)

        try:
            ldapServerObject = ldap.open(serverMeta.host, serverMeta.port)
            ldapServerObject.protocol_version = ldap.VERSION3
            if serverMeta.tls == 1:
                ldapServerObject.start_tls_s()
            ldapServerObject.simple_bind_s(serverMeta.bindDN,
                                serverMeta.bindPassword)
            searchResult = ldapServerObject.add_s(self.DN, tmpModlist)
            ldapServerObject.unbind()
            self.close()
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            QMessageBox.information(self, 'Error!!!', str(e))

###############################################################################

    def add_entries(self, offset, OClass = 0):
        laenge = 0
        tmpIconDir = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        newIcon = os.path.join(tmpIconDir, "new.png")
        delIcon = os.path.join(tmpIconDir, "clear.png")
        if OClass:
            for x in self.objectClasses:
                label = QLabel(self.attributeWidget, "LDAP_ATTRIBUTE")
                label.setText("<b>objectClass</b>")
                label.setAlignment(Qt.AlignLeft)
                
                value = QLineEdit(self.attributeWidget, "LDAP_VALUE")
                value.setText(x)
                value.setAlignment(Qt.AlignLeft)
                value.setReadOnly(1)
                
                laenge += 1
                
                self.attributeGrid.addWidget(label, offset+laenge, 0)
                self.attributeGrid.addWidget(value, offset+laenge, 1)
                
                label.show()
                value.show()
        else:
            for x in self.attributes.keys():
                if not (self.attributes[x].has_key('VALUES')):
                    self.attributes[x]['VALUES'] = ['']
                elif len(self.attributes[x]['VALUES']) == 0:
                    self.attributes[x]['VALUES'] = ['']
                    
                if not (self.attributes[x]['SHOW']):
                    continue
                    
                for y in self.attributes[x]['VALUES']:
                    label = QLabel(self.attributeWidget, 'LDAP_ATTRIBUTE')
                    if self.attributes[x]['MUST']:
                        label.setText('<b>' + x + '</b>')
                    else:
                        label.setText(x)
                    label.setAlignment(Qt.AlignLeft)
                    label.show()
                    
                    value = QLineEdit(self.attributeWidget, 'LDAP_VALUE')
                    value.setText(y)
                    value.setAlignment(Qt.AlignLeft)
                    value.show()
                    
                    laenge += 1
                    
                    self.attributeGrid.addWidget(label, offset+laenge, 0)
                    self.attributeGrid.addWidget(value, offset+laenge, 1)
                    
                    if not (self.attributes[x]['SINGLE']):
                        addButton = QPushButton(self.attributeWidget, "LDAP_" + x)
                        addButton.setPixmap(QPixmap(newIcon))
                        addButton.show()
                        self.connect(addButton,SIGNAL("clicked()"),self.display_values)
                        addButton.installEventFilter(self)
                        self.attributeGrid.addWidget(addButton, offset+laenge, 2)
                        self.WIDGETLIST.append([label, value, addButton])
                    else:
                        self.WIDGETLIST.append([label, value])
                
        return laenge+offset

###############################################################################

    def convert_values(self, template):
        self.objectClasses = template.get_objectclasses()
        self.attributes = template.get_attributeinfos()

###############################################################################

    def display_all_attributes(self):
        self.get_values()
        for x in self.attributes.keys():
            self.attributes[x]['SHOW'] = 1
        self.display_values()

###############################################################################

    def init_view(self, fqn, template):
        self.FQN = fqn
        tmpList = fqn.split(',')
        
        # set the server from the end of string
        # string is the senders dn plus server, separated through comma
        self.SERVER = copy.copy(tmpList[-1])
        
        #reconstruct the dn without server
        self.DN = ','.join(tmpList[:-1]).decode('utf-8')
        
        self.template = template
        self.convert_values(copy.deepcopy(template))
        self.display_values()

###############################################################################

    def eventFilter(self, object, event):
        if (event.type() == QEvent.MouseButtonPress):
            name = str(object.name())
            self.get_values()
            self.attributes[name[5:]]['VALUES'].append('')
        return 0
        
###############################################################################

    def restore_view(self):
        self.init_view(copy.deepcopy(self.FQN), copy.deepcopy(self.template))
