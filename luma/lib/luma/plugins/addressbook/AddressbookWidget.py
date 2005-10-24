# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *
import os.path
import ldap
import copy

import environment
from plugins.addressbook.AddressbookWidgetDesign import AddressbookWidgetDesign
from plugins.addressbook.NameDialog import NameDialog
from base.utils.gui.MailDialog import MailDialog
from plugins.addressbook.CategoryEditDialog import CategoryEditDialog
from base.backend.LumaConnection import LumaConnection
from base.backend.ServerList import ServerList
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.utils.gui.LumaErrorDialog import LumaErrorDialog


class AddressbookWidget(AddressbookWidgetDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        AddressbookWidgetDesign.__init__(self,parent,name,fl)
        
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons", "plugins", "addressbook")
        
        self.entryIcon = QPixmap (os.path.join (iconDir, "person.png"))
        
        personIcon = QPixmap (os.path.join (iconDir, "personal.png"))
        phoneIcon = QPixmap (os.path.join (iconDir, "phone.png"))
        self.mailIcon = QPixmap (os.path.join (iconDir, "email.png"))
        urlIcon = QPixmap (os.path.join (iconDir, "url.png"))
        categoryIcon = QPixmap (os.path.join (iconDir, "category.png"))
        addressIcon = QPixmap (os.path.join (iconDir, "home.png"))
        workIcon = QPixmap (os.path.join (iconDir, "work.png"))
        
        self.personLabel.setPixmap(personIcon)
        self.phoneLabel.setPixmap(phoneIcon)
        self.mailLabel.setPixmap(self.mailIcon)
        self.webPageLabel.setPixmap(urlIcon)
        self.categoryLabel.setPixmap(categoryIcon)
        self.homeLabel.setPixmap(addressIcon)
        self.workLabel.setPixmap(workIcon)
        self.personalLabel.setPixmap(personIcon)
        self.notesLabel.setPixmap(urlIcon)
        
        # Instance of SmartDataObject
        self.dataObject = None
        
        self.allowedAttributes = None
        
        self.attributeWidgets = {'cn': self.cnEdit,
            'title': self.titleEdit,
            'o': self.organisationEdit,
            'mail': self.mailBox,
            'labeledURI': self.labeledURIEdit,
            'category': self.categoryEdit,
            'homePhone': self.homePhoneEdit,
            'telephoneNumber': self.telephoneNumberEdit,
            'mobile': self.mobileEdit,
            'facsimileTelephoneNumber': self.facsimileTelephoneNumberEdit,
            'ou': self.ouEdit,
            'roomNumber': self.roomNumberEdit,
            'businessRole': self.businessRoleEdit,
            'managerName': self.managerNameEdit,
            'assistantName': self.assistantNameEdit,
            'displayName': self.displayNameEdit,
            'spouseName': self.spouseNameEdit,
            'note': self.noteEdit,
            'birthDate': self.birthDateEdit,
            'anniversary': self.anniversaryEdit,
            'postalAddress': self.addressEdit,
            'homePostalAddress': self.addressEdit,
            'otherPostalAddress': self.addressEdit
            }
                                                
        self.enableWidget(0)
        self.DISABLED = 1
        self.ENABLE_SAVE = False
        self.DIALOG_MODE = False
        
        self.addressID = 0

###############################################################################

    def clearView(self):
        """Clear all input fields from possible content.
        """
        
        # Create a list of all inputs fields with method 'clear' and call it
        tmpList = self.attributeWidgets.values()
        
        tmpList.remove(self.birthDateEdit)
        tmpList.remove(self.anniversaryEdit)
        
        map (lambda x: x.clear(), tmpList)
        
        # Clear date fields
        self.birthDateEdit.setDate(QDate())
        self.anniversaryEdit.setDate(QDate())
        
###############################################################################

    def initView(self, dataObject):
        self.clearView()
        self.enableWidget(1)
        
        self.dataObject = dataObject
            
        must, may = self.dataObject.getPossibleAttributes()
        self.enableContactFields(must.union(may))
        
        
        self.addressBox.setEnabled(1)
        
        for x in self.dataObject.getAttributeList():
            if x == 'cn':
                value = self.dataObject.getAttributeValue(x, 0)
                self.cnEdit.setText(value)
                
            if x == 'title':
                value = self.dataObject.getAttributeValue(x, 0)
                self.titleEdit.setText(value)
                
            if x == 'o':
                value = self.dataObject.getAttributeValue(x, 0)
                self.organisationEdit.setText(value)
                
            if x == 'mail':
                tmpList = self.dataObject.getAttributeValueList('mail')
                tmpList.sort()
                map(self.mailBox.insertItem, tmpList)
            
            if x == 'labeledURI':
                value = self.dataObject.getAttributeValue(x, 0)
                self.labeledURIEdit.setText(value)
                
            if x == 'category':
                tmpString = ",".join(self.dataObject.getAttributeValueList(x))
                self.categoryEdit.setText(tmpString)
        
            if x == 'homePhone':
                value = self.dataObject.getAttributeValue(x, 0)
                self.homePhoneEdit.setText(value)
                
            if x == 'telephoneNumber':
                value = self.dataObject.getAttributeValue(x, 0)
                self.telephoneNumberEdit.setText(value)
                
            if x == 'mobile':
                value = self.dataObject.getAttributeValue(x, 0)
                self.mobileEdit.setText(value)
               
            if x == 'facsimileTelephoneNumber':
                value = self.dataObject.getAttributeValue(x, 0)
                self.facsimileTelephoneNumberEdit.setText(value)
                
                
            if x == 'ou':
                value = self.dataObject.getAttributeValue(x, 0)
                self.ouEdit.setText(value)
                
            if x == 'roomNumber':
                value = self.dataObject.getAttributeValue(x, 0)
                self.roomNumberEdit.setText(value)
                
            if x == 'businessRole':
                value = self.dataObject.getAttributeValue(x, 0)
                self.businessRoleEdit.setText(value)
            
            if x == 'managerName':
                value = self.dataObject.getAttributeValue(x, 0)
                self.managerNameEdit.setText(value)
                
            if x == 'assistantName':
                value = self.dataObject.getAttributeValue(x, 0)
                self.assistantNameEdit.setText(value)
                
            if x == 'displayName':
                value = self.dataObject.getAttributeValue(x, 0)
                self.displayNameEdit.setText(value)
                
            if x == 'spouseName':
                value = self.dataObject.getAttributeValue(x, 0)
                self.spouseNameEdit.setText(value)
                
            if x == 'note':
                value = self.dataObject.getAttributeValue(x, 0)
                self.noteEdit.setText(value)
                
            if x == 'birthDate':
                tmpList = self.dataObject.getAttributeValue(x, 0).split('-')
                self.birthDateEdit.setDate(QDate(int(tmpList[0]), int(tmpList[1]), int(tmpList[2])))
                
            if x == 'anniversary':
                tmpList = self.dataObject.getAttributeValue(x, 0).split('-')
                self.birthDateEdit.setDate(QDate(int(tmpList[0]), int(tmpList[1]), int(tmpList[2])))
                
        self.addressID = 0
        self.initAddress(0, False)
        self.ENABLE_SAVE = True
        self.setSaveButton()
    
###############################################################################

    def showNameDialog(self):
        dialog = NameDialog()
        
        sn = ""
        if self.dataObject.hasAttribute('sn'):
            sn = self.dataObject.getAttributeValue('sn', 0)
            
        givenName = None
        suffix = None
        title = None
        middleName = None
        sureNamePosition = None
        
        cn = ''
        if self.dataObject.hasAttribute('cn'):
            cn = self.dataObject.getAttributeValue('cn', 0)
        
        tmpList = cn.split(' ')
        if sn in tmpList:
            sureNamePosition = tmpList.index(sn)
        else:
            sureNamePosition = len(tmpList) - 1
        
        # find the given name
        if self.dataObject.hasAttribute('givenName'):
            givenName = self.dataObject.getAttributeValue('givenName', 0).strip()
        
        # find the suffix
        if not sureNamePosition == (len(tmpList) - 1):
            suffix = " ".join(tmpList[sureNamePosition+1:])

        # find the title and middle name
        if givenName == None:
            frontList = tmpList[:sureNamePosition]
            if len(frontList) == 1:
                givenName = frontList[0]
            
            if len(frontList) > 1:
                givenName = frontList[0]
                middleName = " ".join(frontList[1:])
        else:
            if not givenName in tmpList:
                frontList = tmpList[:sureNamePosition]
                if len(frontList) == 1:
                    givenName = frontList[0]
            
                if len(frontList) > 1:
                    givenName = frontList[0]
                    middleName = " ".join(frontList[1:])
            else:
                givenNamePosition = tmpList.index(givenName)
                if not givenNamePosition == 0:
                    title = " ".join(tmpList[:givenNamePosition])
            
                if (sureNamePosition-givenNamePosition) > 1:
                    middleName = " ".join(tmpList[givenNamePosition+1 : sureNamePosition])
            
            
            
        dialog.lastEdit.setText(sn)
        if not givenName == None:
            dialog.firstEdit.setText(givenName)
        if not suffix == None:
            dialog.suffixBox.setCurrentText(suffix)
        if not title == None:
            dialog.titleBox.setCurrentText(title)
        if not middleName == None:
            dialog.middleEdit.setText(middleName)
        
        dialog.exec_loop()
        
        
        if (dialog.result() == QDialog.Accepted):
            tmpSn = unicode(dialog.lastEdit.text()).strip()
            
            if tmpSn == '':
                return
                
            if self.dataObject.hasAttribute('sn'):
                self.dataObject.setAttributeValue('sn', 0, tmpSn)
            else:
                self.dataObject.addAttributeValue('sn', [tmpSn])
            
            tmpList = []
            tmpList.append(self.__normalizeQtString(dialog.titleBox.currentText()))
            tmpList.append(self.__normalizeQtString(dialog.firstEdit.text()))
            tmpList.append(self.__normalizeQtString(dialog.middleEdit.text()))
            tmpList.append(self.__normalizeQtString(dialog.lastEdit.text()))
            tmpList.append(self.__normalizeQtString(dialog.suffixBox.currentText()))
            
            for x in self.allowedAttributes:
                if "givenname" == x.lower():
                    givenName = unicode(dialog.firstEdit.text())
                    givenName = givenName.strip()
                    if '' == givenName:
                        self.dataObject.deleteAttribute('givenName')
                    else:
                        self.dataObject.addAttributeValue('givenName', [givenName], True)
            
            value = ''.join(tmpList)
            self.cnEdit.setText(value)
            if '' == value:
                self.dataObject.deleteAttribute('cn')
            else:
                self.dataObject.addAttributeValue('cn', [value])
            
###############################################################################

    def __normalizeQtString(self, tmpString):
        tmpString = unicode(tmpString).strip()
        
        if (len(tmpString) > 0):
            tmpString = tmpString + ' '
            
        return tmpString

###############################################################################

    def deleteMail(self):
        if self.mailBox.count() == 0:
            return
            
        self.mailBox.removeItem(self.mailBox.currentItem())
        
        if self.mailBox.count() > 0:
            self.mailBox.setCurrentItem(0)
            
###############################################################################

    def addMail(self):
        dialog = MailDialog()
        
        dialog.exec_loop()
        
        if (dialog.result() == QDialog.Accepted):
            mail = unicode(dialog.mailEdit.text()).strip()
            
            if not(mail == ''):
                currentMails = []
                for x in range(0, self.mailBox.count()):
                    currentMails.append(unicode(self.mailBox.text(x)))
                    
                if not (mail in currentMails):
                    currentMails.append(mail)
                    
                currentMails.sort()
                self.mailBox.clear()
                map(self.mailBox.insertItem, currentMails)
                self.mailBox.setCurrentItem(self.mailBox.count()-1)

###############################################################################

    def editCategories(self):
        dialog = CategoryEditDialog()
        tmpString = unicode(self.categoryEdit.text()).strip()
        if not(tmpString == ''):
            dialog.setCategories(tmpString.split(','))
        
        dialog.exec_loop()
        
        if (dialog.result() == QDialog.Accepted):
            newCategories = dialog.getCategories()
            
            if not(newCategories == None):
                self.categoryEdit.setText(",".join(newCategories))
                
###############################################################################

    def serverChanged(self):
        self.enableWidget(0)
        self.clearView()
        self.DISABLED = 1
        self.ENABLE_SAVE = False
        self.setSaveButton()
                
###############################################################################

    def initAddress(self, id, saveValue=True):
        # The order os the attributes resembles the order of apearance in the widget
        addressType = ['postalAddress', 'homePostalAddress', 'otherPostalAddress']
        
        if saveValue:
            if self.dataObject.isAttributeAllowed(addressType[self.addressID]):
                value = unicode(self.addressEdit.text())
                if not (value==''):
                    self.dataObject.addAttributeValue(addressType[self.addressID], [value], True)
        
        self.addressID = id
        self.addressEdit.clear()
        if self.dataObject.hasAttribute(addressType[id]):
            tmpAddress = self.dataObject.getAttributeValue(addressType[id], 0)
            self.addressEdit.setText(tmpAddress)
        
        
###############################################################################

    def enableWidget(self, val):
        self.setEnabled(val)
        self.emit(PYSIGNAL("enable_save"), (val,))
        
###############################################################################

    def updateValues(self):
        if 'cn' in self.allowedAttributes:
            tmpString = unicode(self.cnEdit.text())
            if not('' == tmpString):
                self.dataObject.addAttributeValue('cn', [tmpString], True)
                if self.dataObject.isAttributeAllowed('gecos'):
                    self.dataObject.addAttributeValue('gecos', [tmpString], True)
            else:
                if not self.dataObject.isAttributeMust('cn'):
                    self.dataObject.deleteAttribute('cn')
        
        if 'title' in self.allowedAttributes:
            value = unicode(self.titleEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('title', [value], True)
            else:
                if not self.dataObject.isAttributeMust('title'):
                    self.dataObject.deleteAttribute('title')
            
        if 'o' in self.allowedAttributes:
            value = unicode(self.organisationEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('o', [value], True)
            else:
                if not self.dataObject.isAttributeMust('o'):
                    self.dataObject.deleteAttribute('o')
        
        if 'mail' in self.allowedAttributes:
            tmpMail = []
            for x in range(0, self.mailBox.count()):
                tmpMail.append(unicode(self.mailBox.text(x)))
            if len(tmpMail) == 0:
                if not self.dataObject.isAttributeMust('mail'):
                    self.dataObject.deleteAttribute('mail')
            else:
                self.dataObject.addAttributeValue('mail', tmpMail, True)
        
        if 'labeledURI' in self.allowedAttributes:
            value = unicode(self.labeledURIEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('labeledURI', [value], True)
            else:
                if not self.dataObject.isAttributeMust('labeledURI'):
                    self.dataObject.deleteAttribute('labeledURI')
            
        if 'category' in self.allowedAttributes:
            valueList = unicode(self.categoryEdit.text()).split(',')
            valueList = filter(lambda x: not ('' == x), valueList)
            if 0 == len(valueList):
                self.dataObject.deleteAttribute('category')
            else:
                self.dataObject.addAttributeValue('category',  valueList, True)
            
        if 'homePhone' in self.allowedAttributes:
            value = unicode(self.homePhoneEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('homePhone', [value], True)
            else:
                if not self.dataObject.isAttributeMust('homePhone'):
                    self.dataObject.deleteAttribute('homePhone')
            
        if 'telephoneNumber' in self.allowedAttributes:
            value = unicode(self.telephoneNumberEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('telephoneNumber', [value], True)
            else:
                if not self.dataObject.isAttributeMust('telephoneNumber'):
                    self.dataObject.deleteAttribute('telephoneNumber')
            
        if 'mobile' in self.allowedAttributes:
            value = unicode(self.mobileEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('mobile', [value], True)
            else:
                if not self.dataObject.isAttributeMust('mobile'):
                    self.dataObject.deleteAttribute('mobile')
            
        if 'facsimileTelephoneNumber' in self.allowedAttributes:
            value = unicode(self.facsimileTelephoneNumberEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('facsimileTelephoneNumber', [value], True)
            else:
                if not self.dataObject.isAttributeMust('facsimileTelephoneNumber'):
                    self.dataObject.deleteAttribute('facsimileTelephoneNumber')
            
        if 'ou' in self.allowedAttributes:
            value = unicode(self.ouEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('ou', [value], True)
            else:
                if not self.dataObject.isAttributeMust('ou'):
                    self.dataObject.deleteAttribute('ou')
            
        if 'roomNumber' in self.allowedAttributes:
            value = unicode(self.roomNumberEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('roomNumber', [value], True)
            else:
                if not self.dataObject.isAttributeMust('roomNumber'):
                    self.dataObject.deleteAttribute('roomNumber')
            
        if 'businessRole' in self.allowedAttributes:
            value = unicode(self.businessRoleEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('businessRole', [value], True)
            else:
                if not self.dataObject.isAttributeMust('businessRole'):
                    self.dataObject.deleteAttribute('businessRole')
            
        if 'managerName' in self.allowedAttributes:
            value = unicode(self.managerNameEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('managerName', [value], True)
            else:
                if not self.dataObject.isAttributeMust('managerName'):
                    self.dataObject.deleteAttribute('managerName')
            
        if 'assistantName' in self.allowedAttributes:
            value = unicode(self.assistantNameEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('assistantName', [value], True)
            else:
                if not self.dataObject.isAttributeMust('assistantName'):
                    self.dataObject.deleteAttribute('assistantName')
            
        if 'displayName' in self.allowedAttributes:
            value = unicode(self.displayNameEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('displayName', [value], True)
            else:
                if not self.dataObject.isAttributeMust('displayName'):
                    self.dataObject.deleteAttribute('displayName')
        
        if 'spouseName' in self.allowedAttributes:
            value = unicode(self.spouseNameEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('spouseName', [value], True)
            else:
                if not self.dataObject.isAttributeMust('spouseName'):
                    self.dataObject.deleteAttribute('spouseName')
            
        if 'note' in self.allowedAttributes:
            value = unicode(self.noteEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue('note', [value], True)
            else:
                if not self.dataObject.isAttributeMust('note'):
                    self.dataObject.deleteAttribute('note')
        
        if 'birthDate' in self.allowedAttributes:
            tmpDate = unicode(self.birthDateEdit.date().toString(Qt.ISODate))
            if tmpDate == '':
                self.dataObject.deleteAttribute('birthDate')
            else:
                self.dataObject.addAttributeValue('birthDate', [tmpDate], True)
            
        if 'anniversary' in self.allowedAttributes:
            tmpDate = unicode(self.anniversaryEdit.date().toString(Qt.ISODate))
            if tmpDate == '':
                self.dataObject.deleteAttribute('anniversary')
            else:
                self.dataObject.addAttributeValue('anniversary', [tmpDate], True)
        
        
        addressType = ['postalAddress', 'homePostalAddress', 'otherPostalAddress']
        id = self.addressBox.currentItem()
        if addressType[id] in self.allowedAttributes:
            value = unicode(self.addressEdit.text())
            if not('' == value):
                self.dataObject.addAttributeValue(addressType[id], [value], True)
            else:
                self.dataObject.deleteAttribute(addressType[id])
        
###############################################################################

    def saveEntry(self):
        self.setEnabled(False)
        self.updateValues()
        
        lumaConnection = LumaConnection(self.dataObject.getServerMeta())
        bindSuccess, exceptionObject = lumaConnection.bind()
        
        if not bindSuccess:
                self.setEnabled(True)
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                return
                
        success, exceptionObject = lumaConnection.updateDataObject(self.dataObject)
        lumaConnection.unbind()
        
        if success:
            self.setEnabled(True)
            
            # If we create a new contact, we want the list updated. 
            # Otherwise simple saving will be done.
            if self.DIALOG_MODE:
                self.emit(PYSIGNAL("contact_saved"), ())
        else:
            self.setEnabled(True)
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not save entry.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
        
###############################################################################

    def enableContactFields(self, attributes):
        self.allowedAttributes = attributes
        
        for x in self.attributeWidgets.keys():
            widget = self.attributeWidgets[x]
            if x in self.allowedAttributes:
                widget.setEnabled(True)
                if (x == 'cn'):
                    self.nameButton.setEnabled(True)
                    
                if (x == 'category'):
                    self.categoryButton.setEnabled(True)
            else:
                widget.setEnabled(False)
                if (x == 'cn'):
                    self.nameButton.setEnabled(False)
                    
                if (x == 'category'):
                    self.categoryButton.setEnabled(False)

###############################################################################

    def buildToolBar(self, parent):
        toolBar = QToolBar(parent)
        
        lumaIconPath = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons")
        savePixmap = QPixmap(os.path.join(lumaIconPath, "save.png"))
    
        self.saveButton = QToolButton(toolBar, "saveValues")
        self.saveButton.setIconSet(QIconSet(savePixmap))
        self.saveButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.saveButton.setAutoRaise(True)
        self.saveButton.setBackgroundMode(self.backgroundMode())
        QToolTip.add(self.saveButton, self.trUtf8("Save"))
        self.connect(self.saveButton, SIGNAL("clicked()"), self.saveEntry)
        self.saveButton.setEnabled(self.ENABLE_SAVE)
        
###############################################################################

    def setSaveButton(self):
        # If we are in dialog mode, we have no save button.
        if not hasattr(self, "saveButton"):
            return
            
        self.saveButton.setEnabled(self.ENABLE_SAVE)
    
    
