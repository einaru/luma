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
from string import strip
import ldap

import environment
from plugins.addressbook.AddressbookWidgetDesign import AddressbookWidgetDesign
from plugins.addressbook.NameDialog import NameDialog
from base.utils.gui.MailDialog import MailDialog
from plugins.addressbook.CategoryEditDialog import CategoryEditDialog
from base.backend.LumaConnection import LumaConnection
from base.backend.ServerList import ServerList
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo


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
        
        self.ocInfo = ObjectClassAttributeInfo()
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

###############################################################################

    def clearView(self):
        self.cnEdit.clear()
        self.titleEdit.clear()
        self.organisationEdit.clear()
        
        self.mailBox.clear()
        
        self.labeledURIEdit.clear()
        
        self.categoryEdit.clear()
        
        self.homePhoneEdit.clear()
        self.telephoneNumberEdit.clear()
        self.mobileEdit.clear()
        self.facsimileTelephoneNumberEdit.clear()
        self.addressEdit.clear()
        
        self.ouEdit.clear()
        self.roomNumberEdit.clear()
        self.businessRoleEdit.clear()
        self.managerNameEdit.clear()
        self.assistantNameEdit.clear()
        self.displayNameEdit.clear()
        self.spouseNameEdit.clear()
        self.noteEdit.clear()
        self.birthDateEdit.setDate(QDate())
        self.anniversaryEdit.setDate(QDate())
        
###############################################################################

    def initView(self, dn, data, server):
        self.clearView()
        self.enableWidget(1)
        
        self.dn = dn
        self.data = data
        self.serverMeta = server
        
        if (self.DISABLED == 1):
            self.ocInfo.setServer(self.serverMeta.name)
            self.ocInfo.retrieveInfoFromServer()
            self.DISABLED = 0
            
        must, may = self.ocInfo.getAllAttributes(self.data['objectClass'])
        self.enableContactFields(must.union(may))
        
        
        self.addressBox.setEnabled(1)
        
        for x in self.data.keys():
            if x == 'cn':
                self.cnEdit.setText((self.data[x][0]).decode('utf-8'))
                
            if x == 'title':
                self.titleEdit.setText(self.data[x][0].decode('utf-8'))
                
            if x == 'o':
                self.organisationEdit.setText(self.data[x][0].decode('utf-8'))
                
            if x == 'mail':
                tmpList = self.data['mail']
                tmpList.sort()
                for y in tmpList:
                    self.mailBox.insertItem(y.decode('utf-8'))
            
            if x == 'labeledURI':
                self.labeledURIEdit.setText(self.data[x][0].decode('utf-8'))
                
            if x == 'category':
                self.categoryEdit.setText(",".join(self.data[x]).decode('utf-8'))
        
            if x == 'homePhone':
                self.homePhoneEdit.setText(self.data[x][0].decode('utf-8'))
                
            if x == 'telephoneNumber':
                self.telephoneNumberEdit.setText(self.data[x][0].decode('utf-8'))
                
            if x == 'mobile':
                self.mobileEdit.setText(self.data[x][0].decode('utf-8'))
               
            if x == 'facsimileTelephoneNumber':
                self.facsimileTelephoneNumberEdit.setText(self.data[x][0].decode('utf-8'))
                
                
            if x == 'ou':
                self.ouEdit.setText(self.data[x][0].decode('utf-8'))
                
            if x == 'roomNumber':
                self.roomNumberEdit.setText(self.data[x][0].decode('utf-8'))
                
            if x == 'businessRole':
                self.businessRoleEdit.setText(self.data[x][0].decode('utf-8'))
            
            if x == 'managerName':
                self.managerNameEdit.setText(self.data[x][0].decode('utf-8'))
                
            if x == 'assistantName':
                self.assistantNameEdit.setText(self.data[x][0].decode('utf-8'))
                
            if x == 'displayName':
                self.displayNameEdit.setText(self.data[x][0].decode('utf-8'))
                
            if x == 'spouseName':
                self.spouseNameEdit.setText(self.data[x][0].decode('utf-8'))
                
            if x == 'note':
                self.noteEdit.setText(self.data[x][0].decode('utf-8'))
                
            if x == 'birthDate':
                tmpList = self.data[x][0].split('-')
                self.birthDateEdit.setDate(QDate(int(tmpList[0]), int(tmpList[1]), int(tmpList[2])))
                
            if x == 'anniversary':
                tmpList = self.data[x][0].split('-')
                self.birthDateEdit.setDate(QDate(int(tmpList[0]), int(tmpList[1]), int(tmpList[2])))
                
        self.initAddress(0, 1)
        self.addressID = 0
    
###############################################################################

    def showNameDialog(self):
        dialog = NameDialog()
        try:
            sn = self.data['sn'][0].decode('utf-8')
            tmpList = unicode(self.cnEdit.text()).split(sn)
            tmpList[0] = strip(tmpList[0])
            
            prefix = tmpList[0].split(' ')
            for x in range(0, len(prefix)-1):
                prefix[x] = strip(prefix[x])
            
            dialog.lastEdit.setText(sn)
            if (len(tmpList) == 2):
                dialog.suffixBox.setCurrentText(tmpList[1])
              
            if (len(prefix) == 1):
                dialog.firstEdit.setText(prefix[0])
            if  (len(prefix) == 2):
                dialog.titleBox.setCurrentText(prefix[0])
                dialog.firstEdit.setText(prefix[1])
            if (len(prefix) > 2):
                dialog.titleBox.setCurrentText(prefix[0])
                dialog.firstEdit.setText(prefix[1])
                tmpString = " ".join(prefix[2:])
                dialog.middleEdit.setText(tmpString)
            
            dialog.exec_loop()
        except Exception, e:
            dialog.exec_loop()
        
        if (dialog.result() == QDialog.Accepted):
            tmpSn = strip(unicode(dialog.lastEdit.text()))
            
            if tmpSn == '':
                return
                
            self.data['sn'][0] = tmpSn.encode('utf-8')
            
            tmpList = []
            tmpList.append(self.__normalizeQtString(dialog.titleBox.currentText()))
            tmpList.append(self.__normalizeQtString(dialog.firstEdit.text()))
            tmpList.append(self.__normalizeQtString(dialog.middleEdit.text()))
            tmpList.append(self.__normalizeQtString(dialog.lastEdit.text()))
            tmpList.append(self.__normalizeQtString(dialog.suffixBox.currentText()))
            
            self.cnEdit.setText(''.join(tmpList))
            
###############################################################################

    def __normalizeQtString(self, tmpString):
        tmpString = strip(unicode(tmpString))
        
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
            mail = strip(unicode(dialog.mailEdit.text()))
            
            if not(mail == ''):
                currentMails = []
                for x in range(0, self.mailBox.count()):
                    currentMails.append(unicode(self.mailBox.text(x)))
                    
                if not (mail in currentMails):
                    self.mailBox.insertItem(mail)
                    self.mailBox.setCurrentItem(self.mailBox.count()-1)

###############################################################################

    def editCategories(self):
        dialog = CategoryEditDialog()
        tmpString = strip(unicode(self.categoryEdit.text()))
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
                
###############################################################################

    def initAddress(self, id, fresh=0):
        # The order os the attributes resembles the order of apearance in the widget
        addressType = ['postalAddress', 'homePostalAddress', 'otherPostalAddress']
        
        if fresh == 0:
            self.data[addressType[self.addressID]] = [unicode(self.addressEdit.text()).encode('utf-8')]
        
        self.addressID = id
        self.addressEdit.clear()
        if self.data.has_key(addressType[id]):
            tmpAddress = self.data[addressType[id]][0]
            self.addressEdit.setText(tmpAddress.decode('utf-8'))
        
        
###############################################################################

    def enableWidget(self, val):
        self.setEnabled(val)
        self.emit(PYSIGNAL("enable_save"), (val,))
        
###############################################################################

    def getValues(self):
        values = {}
        
        if 'cn' in self.allowedAttributes:
            tmpString = unicode(self.cnEdit.text()).encode('utf-8')
            values['cn'] = [tmpString]
        
        if 'title' in self.allowedAttributes:
            values['title'] = [unicode(self.titleEdit.text()).encode('utf-8')]
            
        if 'o' in self.allowedAttributes:
            values['o'] = [unicode(self.organisationEdit.text()).encode('utf-8')]
        
        if 'mail' in self.allowedAttributes:
            tmpMail = []
            for x in range(0, self.mailBox.count()):
                tmpMail.append(unicode(self.mailBox.text(x)).encode('utf-8'))
            if len(tmpMail) == 0:
                tmpMail = ['']
            values['mail'] = tmpMail
        
        if 'labeledURI' in self.allowedAttributes:
            values['labeledURI'] = [unicode(self.labeledURIEdit.text()).encode('utf-8')]
            
        if 'category' in self.allowedAttributes:
            values['category'] = unicode(self.categoryEdit.text()).encode('utf-8').split(',')
            
        if 'homePhone' in self.allowedAttributes:
            values['homePhone'] = [unicode(self.homePhoneEdit.text()).encode('utf-8')]
            
        if 'telephoneNumber' in self.allowedAttributes:
            values['telephoneNumber'] = [unicode(self.telephoneNumberEdit.text()).encode('utf-8')]
            
        if 'mobile' in self.allowedAttributes:
            values['mobile'] = [unicode(self.mobileEdit.text()).encode('utf-8')]
            
        if 'facsimileTelephoneNumber' in self.allowedAttributes:
            values['facsimileTelephoneNumber'] = [unicode(self.facsimileTelephoneNumberEdit.text()).encode('utf-8')]
            
        if 'ou' in self.allowedAttributes:
            values['ou'] = [unicode(self.ouEdit.text()).encode('utf-8')]
            
        if 'roomNumber' in self.allowedAttributes:
            values['roomNumber'] = [unicode(self.roomNumberEdit.text()).encode('utf-8')]
            
        if 'businessRole' in self.allowedAttributes:
            values['businessRole'] = [unicode(self.businessRoleEdit.text()).encode('utf-8')]
            
        if 'managerName' in self.allowedAttributes:
            values['managerName'] = [unicode(self.managerNameEdit.text()).encode('utf-8')]
            
        if 'assistantName' in self.allowedAttributes:
            values['assistantName'] = [unicode(self.assistantNameEdit.text()).encode('utf-8')]
            
        if 'displayName' in self.allowedAttributes:
            values['displayName'] = [unicode(self.displayNameEdit.text()).encode('utf-8')]
        
        if 'spouseName' in self.allowedAttributes:
            values['spouseName'] = [unicode(self.spouseNameEdit.text()).encode('utf-8')]
            
        if 'note' in self.allowedAttributes:
            values['note'] = [unicode(self.noteEdit.text()).encode('utf-8')]
        
        if 'birthDate' in self.allowedAttributes:
            tmpDate = unicode(self.birthDateEdit.date().toString(Qt.ISODate)).encode('utf-8')
            if not (tmpDate == ''):
                values['birthDate'] = [tmpDate]
            
        if 'anniversary' in self.allowedAttributes:
            tmpDate = unicode(self.anniversaryEdit.date().toString(Qt.ISODate)).encode('utf-8')
            if not (tmpDate == ''):
                values['anniversary'] = [tmpDate]
        
        if 'postalAddress' in self.allowedAttributes:
            if self.data.has_key('postalAddress'):
                values['postalAddress'] = self.data['postalAddress']
            
        if 'homePostalAddress' in self.allowedAttributes:
            if self.data.has_key('homePostalAddress'):
                values['homePostalAddress'] = self.data['homePostalAddress']
            
        if 'otherPostalAddress' in self.allowedAttributes:
            if self.data.has_key('otherPostalAddress'):
                values['otherPostalAddress'] = self.data['otherPostalAddress']
            
        
        values['sn'] = self.data['sn']
        addressType = ['postalAddress', 'homePostalAddress', 'otherPostalAddress']
        id = self.addressBox.currentItem()
        if addressType[id] in self.allowedAttributes:
            values[addressType[id]] = [unicode(self.addressEdit.text()).encode('utf-8')]
        
        for x in values.keys():
            if values[x][0] == '':
                values[x] = []
                
        return values
        
###############################################################################

    def saveEntry(self):
        values = self.getValues()
        
        ldapValues = self.getLdapValues()
        modlist =  ldap.modlist.modifyModlist(ldapValues, values, [], 1)
        
        connection = LumaConnection(self.serverMeta)
        connection.bind()
        result = connection.modify_s(self.dn, modlist)
        connection.unbind()
        
        if result == 0:
            QMessageBox.warning(None,
            self.trUtf8("Error"),
            self.trUtf8("""Could not save contact data. 
Please read console output for more information."""),
            None,
            None,
            None,
            0, -1)
        else:
            self.emit(PYSIGNAL("contact_saved"), ())
        
###############################################################################

    def getLdapValues(self):
        connection = LumaConnection(self.serverMeta)
        
        connection.bind()
        result = connection.search_s(self.dn)
        connection.unbind()
        
        return result[0][1]
        
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


    
