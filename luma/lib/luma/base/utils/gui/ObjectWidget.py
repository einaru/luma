# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>                                                             
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
import base64
from sets import Set
import string

from base.backend.ServerList import ServerList
from base.utils import isBinaryAttribute, encodeBase64
import environment
from base.utils.gui.AddAttributeWizard import AddAttributeWizard
from base.backend.LumaConnection import LumaConnection
from base.utils.gui.PasswordDialog import PasswordDialog
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo


class ObjectWidget(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)
        
        # Load the pixmaps
        self.iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        self.addPixmap = QPixmap(os.path.join(self.iconPath, "single.png"))
        self.deletePixmap = QPixmap(os.path.join(self.iconPath, "deleteEntry.png"))
        self.deleteSmallPixmap = QPixmap(os.path.join(self.iconPath, "editdelete.png"))
        self.savePixmap = QPixmap(os.path.join(self.iconPath, "save.png"))
        self.displayAllPixmap = QPixmap(os.path.join(self.iconPath, "displayall.png"))
        self.reloadPixmap = QPixmap(os.path.join(self.iconPath, "reload.png"))
        self.binaryPixmap = QPixmap(os.path.join(self.iconPath, "binary.png"))
        self.deleteAttributePixmap = os.path.join(self.iconPath, "clear.png")
        self.newAttributePixmap = os.path.join(self.iconPath, "new.png")
        self.editPixmap = QPixmap(os.path.join(self.iconPath, "edit.png"))
        self.exportBinaryPixmap = QPixmap(os.path.join(self.iconPath, "exportBinary.png"))
        
        self.mainLayout = QHBoxLayout(self)
        
        #create a scrollable frame
        self.attributeFrame = QScrollView(self,"attributeFrame")
        self.attributeFrame.setMinimumSize(QSize(300,100))
        self.attributeFrame.setFrameShape(QFrame.NoFrame)
        self.attributeFrame.setResizePolicy(QScrollView.AutoOneFit)
        self.mainLayout.addWidget(self.attributeFrame)


        # create the widget containing all attributes
        self.attributeWidget = QWidget(self.attributeFrame.viewport())
        self.attributeWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.attributeGrid = QGridLayout(self.attributeWidget, 1, 1, 11, 6, "gridLayout")
        self.attributeFrame.addChild(self.attributeWidget)


        # name of server
        self.SERVER = ""
        
        # dn of the current ldap object
        self.DN = ""
        
        # values of the current object
        self.CURRENTVALUES = {}
        
        # list of widgets assiciated with ldap attributes
        self.WIDGETLIST = []
        
        # instance of ObjectClassAttributeInfo
        # initialized when a ldap object should be displayed
        self.SERVERMETA = None
        
        # boolean to indicate if the current ldap object has been modified
        self.EDITED = False
        
        # is the current object a leaf of the ldap tree?
        self.ISLEAF = False
        
        # do we create a completely new object?
        self.CREATE = False
        
        # indicates if the list of objectClasses has changed
        # important for saving. a simple modify doesn't work. object has to
        # be recreated from scratch
        self.OBJECTCLASS_CHANGED = False
        
        # disable toolbuttons on startup
        #self.enableToolButtons(False)

###############################################################################

    def displayValues(self):
        self.clearView()

        
        # create first header
        header1 = QLabel(self.attributeWidget, "LDAP_HEADER")
        header1.setText(self.trUtf8("<b>Attributes</b>"))
        header1.setAlignment(Qt.AlignLeft)
        header1.setSizePolicy(QSizePolicy(5,0,0,0,header1.sizePolicy().hasHeightForWidth()))
        header1.show()

        # create second header
        header2 = QLabel(self.attributeWidget, "LDAP_HEADER")
        header2.setText(self.trUtf8("<b>Values</b>"))
        header2.setAlignment(Qt.AlignHCenter)
        header2.setSizePolicy(QSizePolicy(5,0,0,0,header2.sizePolicy().hasHeightForWidth()))
        header2.show()

        self.attributeGrid.addWidget(header1, 0, 0)
        self.attributeGrid.addWidget(header2, 0, 1)

        self.WIDGETLIST.append([header1, header2])

        offset = 1
        
        # create dn
        editable = self.CREATE
        offset = self.addEntries("dn", [self.DN], offset, editable, 1, None)

        # use a temporary copy of data values to create the widgets
        dataCopy = copy.deepcopy(self.CURRENTVALUES)
        
        # add objectclasses
        offset = self.addEntries("objectClass", dataCopy["objectClass"], offset, False, 1, None)
        tmpObjectClasses = copy.deepcopy(dataCopy["objectClass"])
        del dataCopy["objectClass"]

        # create entries for all attributes
        for x in dataCopy.keys():
            offset = self.addEntries(x, dataCopy[x], offset, True, 0, tmpObjectClasses)

        # create a foo label and destroy it.
        # otherwise widgets don't have a proper layout.
        # have to look further into this.
        fooLabel = QLabel(self.attributeWidget, "LDAP__FOO__")
        fooLabel.show()
        self.attributeGrid.addWidget(fooLabel, offset, 0)
        self.attributeWidget.removeChild(fooLabel)
        
        self.enableToolButtons(True)

###############################################################################

    def saveView(self):
        
        tmpObject = ServerList()
        tmpObject.readServerList()
        serverMeta = tmpObject.getServerObject(self.SERVER)
        
        lumaConnection = LumaConnection(serverMeta)
        lumaConnection.bind()
        
        success = False
        
        # clean out attributes which were given by the template but got no value
        # by the user.
        for x in self.CURRENTVALUES.keys():
            if self.CURRENTVALUES[x] == [None]:
                del self.CURRENTVALUES[x]
                
        
        if self.CREATE:
            modlist = ldap.modlist.addModlist(self.CURRENTVALUES)
            success = lumaConnection.add(self.DN, modlist)
        else:
            oldEntry = lumaConnection.search(self.DN, ldap.SCOPE_BASE)[0][1]
            modlist =  ldap.modlist.modifyModlist(oldEntry, self.CURRENTVALUES, [], 0)
            success = lumaConnection.modify(self.DN, modlist)
            
        lumaConnection.unbind()
        
        if not success:
            QMessageBox.warning(self,
            self.trUtf8("Error"),
            self.trUtf8("""Could not save object data. 
Please read console output for more information."""),
            None,
            None,
            None,
            0, -1)
        else:
            self.refreshView()

###############################################################################

    def refreshView(self):
        tmpObject = ServerList()
        tmpObject.readServerList()
        serverMeta = tmpObject.getServerObject(self.SERVER)
        self.CURRENTVALUES = {}
        
        lumaConnection = LumaConnection(serverMeta)
        lumaConnection.bind()
        result = lumaConnection.search(self.DN, ldap.SCOPE_BASE)[0][1]
        lumaConnection.unbind()
        
        self.CURRENTVALUES = result
        self.EDITED = False
        self.displayValues()

###############################################################################

    def addEntries(self, attribute, valueList=[], offset=0, editable=False, bold=0, objectClasses=None):
        laenge = range(offset, len(valueList)+offset)
        
        for x in laenge:
            value = None
            data = valueList[x-offset]
            
            label = QLabel(self.attributeWidget, "LDAP_ATTRIBUTE")
            
            text = attribute
            
            if (bold) or (self.SERVERMETA.isMust(attribute, objectClasses)):
                text = "<b>" + attribute + "</b>"
                
            if data == None:
                text = """<font color="#ff0000">""" + text + "</font>"
                
            label.setText(text)
            label.setAlignment(Qt.AlignLeft)
            
            isBinary = False
            
            #if not (attribute=="dn" or attribute=="objectClass"):
            #    print dir(self.SERVERMETA.matchingRule(attribute))
            
            if (self.SERVERMETA.isBinary(attribute) or isBinaryAttribute(data)) and not (data == None):
                if attribute == 'jpegPhoto':
                    isBinary = True
                    picture = QImage()
                    picture.loadFromData(data)
                    value = QLabel(self.attributeWidget, "LDAP_ATTRIBUTE")
                    value.setPixmap(QPixmap(picture))
                    value.setAlignment(Qt.AlignLeft)
                else:
                    try:
                        data = data.decode('utf-8')
                        value = QLineEdit(self.attributeWidget, "LDAP_VALUE")
                        value.setText(data)
                        value.setAlignment(Qt.AlignLeft)
                        value.setReadOnly(1)
                    except UnicodeDecodeError, e:
                        isBinary = True
                        value = QLabel(self.attributeWidget, "LDAP_ATTRIBUTE")
                        value.setPixmap(QPixmap(self.binaryPixmap))
                        value.setAlignment(Qt.AlignLeft)
                        QToolTip.add(value, self.trUtf8("Binary value"))
            else:
                if not (data == None):
                    data = data.decode('utf-8')

                value = None
                if data == None:
                    value = QLabel(self.attributeWidget, "LDAP_VALUE")
                    value.setText("""<font color="#ff0000">Value not set.</font>""")
                    value.setAlignment(Qt.AlignLeft)
                else:
                    value = QLineEdit(self.attributeWidget, "LDAP_VALUE")
                    value.setText(data)
                    value.setAlignment(Qt.AlignLeft)
                    value.setReadOnly(1)

            self.attributeGrid.addWidget(label, x, 0)
            self.attributeGrid.addWidget(value, x, 1)
            label.show()
            value.show()
            
            editButton = None
            deleteButton = None
            
            tmpList = [label, value]
            
            if editable:
                editButton  = QPushButton(self.attributeWidget, "LDAP_EDIT" + attribute + str(x-offset))
                editButton.setPixmap(self.editPixmap)
                editButton.installEventFilter(self)
                QToolTip.add(editButton, self.trUtf8("Edit..."))
                editButton.show()
                self.attributeGrid.addWidget(editButton, x, 2)
                tmpList.append(editButton)
                
            if not((attribute=="objectClass") or (attribute=="dn")) and (not(self.SERVERMETA.isMust(attribute, self.CURRENTVALUES["objectClass"])) or (len(valueList) > 1)):
                deleteButton  = QPushButton(self.attributeWidget, "LDAP_DELETE" + attribute + str(x-offset))
                deleteButton.setPixmap(self.deletePixmap)
                deleteButton.installEventFilter(self)
                QToolTip.add(deleteButton, self.trUtf8("Delete"))
                deleteButton.show()
                self.attributeGrid.addWidget(deleteButton, x, 3)
                tmpList.append(deleteButton)
                
            #if self.SERVERMETA.isBinary(attribute) or isBinaryAttribute(data):
            if isBinary:
                exportBinaryButton = QPushButton(self.attributeWidget, "LDAP_EXPORT" + attribute + str(x-offset))
                exportBinaryButton.setPixmap(self.exportBinaryPixmap)
                exportBinaryButton.installEventFilter(self)
                QToolTip.add(exportBinaryButton, self.trUtf8("Export..."))
                exportBinaryButton.show()
                self.attributeGrid.addWidget(exportBinaryButton, x, 4)
                tmpList.append(exportBinaryButton)
                
                
            self.WIDGETLIST.append(tmpList)
            
        return len(valueList)+offset

###############################################################################

    def setServer(self, server):
        if not (server == self.SERVER):
            self.SERVER = server
            self.SERVERMETA = ObjectClassAttributeInfo(self.SERVER)


###############################################################################

    def convertValues(self, values):
        tmpTupel = values[0]
        self.CURRENTVALUES = tmpTupel[1]
        self.DN = tmpTupel[0]

###############################################################################

    def initView(self, server, values, create=False):
        self.setServer(server)
        self.convertValues(values)
        
        if create:
            self.EDITED = True
            self.ISLEAF = False
            self.CREATE = True
        else:
            self.EDITED = False
        
            # check if current object is a leaf of the ldap tree
            isLeave = False
        
            try:
                tmpObject = ServerList()
                tmpObject.readServerList()
                serverMeta = tmpObject.getServerObject(self.SERVER)
        
                lumaConnection = LumaConnection(serverMeta)
        
                lumaConnection.bind()
                result = lumaConnection.search(self.DN, ldap.SCOPE_ONELEVEL, filter="(objectClass=*)", attrList=None, attrsonly=1)
                lumaConnection.unbind()
                if result == None:
                    isLeave = True
            except Exception:
                print "Could not check if object is a leaf in the ldap tree."
          
            self.ISLEAF = isLeave
            self.CREATE = False
            
        self.displayValues()
        
        self.enableToolButtons(True)

###############################################################################

    def eventFilter(self, object, event):
        if (event.type() == QEvent.MouseButtonPress):
            name = unicode(object.name())
            
            # i don't like part of code.
            # the position of the current element of an attribute in the list 
            # is stored as an integer at the end of the widget's name. we need
            # to find out, how many chars belong to this number. there may be more
            # than nine elements for an attribute.
            # WARNING: this assumes that no attributes exist which end with a
            #          number!!!!!!!!!!!!
            numberLength = 1
            try:
                while True:
                    foo = int(name[-(numberLength)])
                    numberLength += 1
            except:
                numberLength -= 1
                
            position = int(name[-numberLength:])
            
            
            if name[:9] == "LDAP_EDIT":
                attribute = name[9:-numberLength]
                binary = False
                if self.SERVERMETA.isBinary(attribute) or (name[-8:-numberLength] == ";binary"):
                    binary = True

                if "password" in string.lower(attribute):
                    self.editPasswordAttribute(attribute, position)
                elif binary:
                    self.editBinaryAttribute(attribute, position)
                else:
                    self.editAttribute(attribute, position)
                    
            if name[:11] == "LDAP_DELETE":
                attribute = name[11:-numberLength]
                self.deleteAttribute(attribute, position)
                
            if name[:11] == "LDAP_EXPORT":
                attribute = name[11:-numberLength]
                self.exportBinaryAttribute(attribute, position)
        
        # Fixes a bug with buttons. After the dialog is shown, the button
        # is pressed forever. We don't want that.
        # I don't know the exact reason but this fix should cause no problems.
        if "setDown" in dir(object):
            object.setDown(False)
            
        return False
        
###############################################################################

    def enableToolButtons(self, enable):
        if self.EDITED:
            self.saveButton.setEnabled(enable)
        else:
            self.saveButton.setEnabled(False)
            
        if self.ISLEAF:
            self.deleteObjectButton.setEnabled(enable)
        else:
            self.deleteObjectButton.setEnabled(False)
           
        if self.CREATE:
            self.reloadButton.setEnabled(False)
        else:
            self.reloadButton.setEnabled(enable)
            
        self.addAttributeButton.setEnabled(enable)
        
###############################################################################

    def addAttribute(self):
        dialog = AddAttributeWizard(self)
        dialog.setData(copy.deepcopy(self.CURRENTVALUES), self.SERVERMETA)
        
        dialog.exec_loop()
        
        if dialog.result() == QDialog.Rejected:
            return
        
        attribute = str(dialog.attributeBox.currentText())
        showAll = dialog.enableAllBox.isChecked()
        
        attributeList = Set([attribute])
        
        if showAll and not(attribute in dialog.possibleAttributes):
            self.OBJECTCLASS_CHANGED = True
            objectclass = str(dialog.classBox.currentText())
            self.CURRENTVALUES['objectClass'].append(objectclass)
            mustAttributes = self.SERVERMETA.getAllMusts([objectclass])
            mustAttributes = mustAttributes.difference(Set(self.CURRENTVALUES.keys()))
            attributeList = mustAttributes.union(Set([attribute]))
            
        for x in attributeList:
            if self.CURRENTVALUES.has_key(x):
                self.CURRENTVALUES[x].append(None)
            else:
                self.CURRENTVALUES[x] = [None]
            
        self.displayValues()
        
###############################################################################

    def editBinaryAttribute(self, attribute, position):
        fileName = QFileDialog.getOpenFileName(\
                                None,
                                None,
                                self, None,
                                self.trUtf8("Select file to change binary value"),
                                None, 1)
                                
        # if cancel button has been pressed, leave function
        if unicode(fileName) == "":
            return
            
        content = open(str(fileName), "r").readlines()
        
        self.CURRENTVALUES[attribute][position] = "".join(content)
        self.EDITED = True
        self.displayValues()
        
###############################################################################

    def editAttribute(self, attribute, position):
        oldValue = None
        
        if self.CREATE and (attribute == "dn"):
            oldValue = self.DN
        else:
            oldValue = self.CURRENTVALUES[attribute][position]
            
        if oldValue == None:
            oldValue = ""
            
        text = QInputDialog.getText(\
                    self.trUtf8("Edit attribute"),
                    unicode(attribute) + unicode(":"),
                    QLineEdit.Normal,
                    oldValue.decode("utf-8"), self, None)
                    

        
        # if cancel button has been pressed, leave function
        if text[1] == False:
            return
            
        val = unicode(text[0]).encode("utf-8")

        
        if self.CREATE and (attribute == "dn"):
            self.DN = val
        else:
            self.CURRENTVALUES[attribute][position] = val
            self.EDITED = True
            
        self.displayValues()
        
###############################################################################

    def editPasswordAttribute(self, attribute, position):
        dialog = PasswordDialog(self)
        dialog.exec_loop()
        
        if dialog.result() == 1:
            passwordHash = dialog.passwordHash
            self.CURRENTVALUES[attribute][position] = passwordHash
            self.EDITED = True

        self.displayValues()

###############################################################################

    def deleteAttribute(self, attribute, position):
        if len(self.CURRENTVALUES[attribute]) > 1:
            del self.CURRENTVALUES[attribute][position]
        else:
            del self.CURRENTVALUES[attribute]
        
        self.EDITED = True
        self.displayValues()
        
###############################################################################

    def exportBinaryAttribute(self, attribute, position):
        value = self.CURRENTVALUES[attribute][position]
        
        SAVED = False
        
        while not SAVED:
            fileName = unicode(QFileDialog.getSaveFileName(\
                                None,
                                None,
                                self, None,
                                self.trUtf8("Export binary attribute to file"),
                                None, 1))

            if unicode(fileName) == "":
                return
            
            try:
                fileHandler = open(fileName, "w")
                fileHandler.write(value)
                fileHandler.close()
                SAVED = True
            except IOError, e:
                result = QMessageBox.warning(None,
                    self.trUtf8("Export binary attribute"),
                    self.trUtf8("""Could not export binary data to file. Reason:
""" + str(e) + """\n\nPlease select another filename."""),
                    self.trUtf8("&Cancel"),
                    self.trUtf8("&OK"),
                    None,
                    1, -1)
                    
                if result == 0:
                    return 
                    
###############################################################################

    def aboutToChange(self):
        """Is called as a slot when new data arrives. 
        
        This way we are able to save the changed values.
        """
    
        if not self.EDITED:
            return
            
        value =QMessageBox.question(None,
            self.trUtf8("Save entry"),
            self.trUtf8("""The entry has been modified. Do you want to save it?"""),
            self.trUtf8("&Yes"),
            self.trUtf8("&No"),
            None,
            0, -1)
            
        # button order says, that 'yes' is zero
        if value == 0:
            self.saveView()
            
###############################################################################

    def clearView(self):
        """delete widgets previously associated with a ldap object"""
    
        self.WIDGETLIST = []
        for x in  self.attributeWidget.children():
            name = unicode(x.name())
            if name[:4] == "LDAP":
                x.deleteLater()
                
###############################################################################

    def deleteObject(self):
        """Delete the current object.
        """
        
        reallyDelete = QMessageBox.question(self,
            self.trUtf8("Delete object"),
            self.trUtf8("""Do you really want to delete the object?"""),
            self.trUtf8("&Yes"),
            self.trUtf8("&No"),
            None,
            0, -1)
            
        if reallyDelete == 1:
            return

        
        tmpObject = ServerList()
        tmpObject.readServerList()
        serverMeta = tmpObject.getServerObject(self.SERVER)
        
        lumaConnection = LumaConnection(serverMeta)
        
        lumaConnection.bind()
        result = lumaConnection.delete(self.DN)
        lumaConnection.unbind()
        
        if result == 0:
            QMessageBox.warning(None,
            self.trUtf8("Error"),
            self.trUtf8("""Could not delete object. 
Please read console output for more information."""),
            None,
            None,
            None,
            0, -1)
        else:
            self.clearView()
            self.enableToolButtons(False)
            
###############################################################################

    def buildToolBar(self, parent):
        toolBar = QToolBar(parent)
        
        
        # Reload button
        self.reloadButton = QToolButton(toolBar, "reloadEntry")
        self.reloadButton.setIconSet(QIconSet(self.reloadPixmap))
        self.reloadButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.reloadButton.setAutoRaise(True)
        self.reloadButton.setBackgroundMode(self.backgroundMode())
        QToolTip.add(self.reloadButton, self.trUtf8("Reload"))
        self.connect(self.reloadButton, SIGNAL("clicked()"), self.refreshView)
        
        # Save button
        self.saveButton = QToolButton(toolBar, "saveValues")
        self.saveButton.setIconSet(QIconSet(self.savePixmap))
        self.saveButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.saveButton.setAutoRaise(True)
        self.saveButton.setBackgroundMode(self.backgroundMode())
        QToolTip.add(self.saveButton, self.trUtf8("Save"))
        self.connect(self.saveButton, SIGNAL("clicked()"), self.saveView)
        
        toolBar.addSeparator()
        
        # Add attribute button
        self.addAttributeButton = QToolButton(toolBar, "addAttribute")
        self.addAttributeButton.setIconSet(QIconSet(self.addPixmap))
        self.addAttributeButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.addAttributeButton.setAutoRaise(True)
        self.addAttributeButton.setBackgroundMode(self.backgroundMode())
        QToolTip.add(self.addAttributeButton, self.trUtf8("Add attribute..."))
        self.connect(self.addAttributeButton, SIGNAL("clicked()"), self.addAttribute)
        
        # Delete button
        self.deleteObjectButton = QToolButton(toolBar)
        self.deleteObjectButton.setIconSet(QIconSet(self.deleteSmallPixmap))
        self.deleteObjectButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.deleteObjectButton.setAutoRaise(True)
        self.deleteObjectButton.setBackgroundMode(self.backgroundMode())
        QToolTip.add(self.deleteObjectButton, self.trUtf8("Delete object"))
        self.connect(self.deleteObjectButton, SIGNAL("clicked()"), self.deleteObject)
        
        self.enableToolButtons(False)
