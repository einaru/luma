# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *
import os.path
from string import strip
#import ldap
#from ConfigParser import *

import environment
from plugins.addressbook.AddressbookWidgetDesign import AddressbookWidgetDesign
from plugins.addressbook.NameDialog import NameDialog
#from base.backend.ServerObject import ServerObject
#from base.backend.ServerList import ServerList
#from base.backend.LumaConnection import LumaConnection



class AddressbookWidget(AddressbookWidgetDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        AddressbookWidgetDesign.__init__(self,parent,name,fl)
        
        iconDir = os.path.join (environment.lumaInstallationPrefix, "lib", "luma", "plugins", "addressbook", "icons")
        
        self.entryIcon = QPixmap (os.path.join (iconDir, "person.png"))
        
        personIcon = QPixmap (os.path.join (iconDir, "personal.png"))
        phoneIcon = QPixmap (os.path.join (iconDir, "phone.png"))
        mailIcon = QPixmap (os.path.join (iconDir, "email.png"))
        urlIcon = QPixmap (os.path.join (iconDir, "url.png"))
        categoryIcon = QPixmap (os.path.join (iconDir, "category.png"))
        addressIcon = QPixmap (os.path.join (iconDir, "home.png"))
        workIcon = QPixmap (os.path.join (iconDir, "work.png"))
        
        self.personLabel.setPixmap(personIcon)
        self.phoneLabel.setPixmap(phoneIcon)
        self.mailLabel.setPixmap(mailIcon)
        self.webPageLabel.setPixmap(urlIcon)
        self.categoryLabel.setPixmap(categoryIcon)
        self.homeLabel.setPixmap(addressIcon)
        self.workLabel.setPixmap(workIcon)
        self.personalLabel.setPixmap(personIcon)
        self.notesLabel.setPixmap(urlIcon)

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

    def init_view(self, dn, data, server):
        self.clearView()
        
        self.dn = dn
        self.data = data
        self.server = server
        
        for x in self.data.keys():
            if x == 'cn':
                self.cnEdit.setText(self.data[x][0])
                
            if x == 'title':
                self.titleEdit.setText(self.data[x][0])
                
            if x == 'o':
                self.organisationEdit.setText(self.data[x][0])
                
            if x == 'mail':
                for y in self.data[x]:
                    self.mailBox.insertItem(y)
            
            if x == 'labeledURI':
                self.labeledURIEdit.setText(self.data[x][0])
                
            if x == 'category':
                self.categoryEdit.setText(",".join(self.data[x]))
        
            if x == 'homePhone':
                self.homePhoneEdit.setText(self.data[x][0])
                
            if x == 'telephoneNumber':
                self.telephoneNumberEdit.setText(self.data[x][0])
                
            if x == 'mobile':
                self.mobileEdit.setText(self.data[x][0])
               
            if x == 'facsimileTelephoneNumber':
                self.facsimileTelephoneNumberEdit.setText(self.data[x][0])
                
            if x == 'ou':
                self.ouEdit.setText(self.data[x][0])
                
            if x == 'roomNumber':
                self.roomNumberEdit.setText(self.data[x][0])
                
            if x == 'businessRole':
                self.businessRoleEdit.setText(self.data[x][0])
            
            if x == 'managerName':
                self.managerNameEdit.setText(self.data[x][0])
                
            if x == 'assistantName':
                self.assistantNameEdit.setText(self.data[x][0])
                
            if x == 'displayName':
                self.displayNameEdit.setText(self.data[x][0])
                
            if x == 'spouseName':
                self.spouseNameEdit.setText(self.data[x][0])
                
            if x == 'note':
                self.noteEdit.setText(self.data[x][0])
                
            if x == 'birthDate':
                pass
                
            if x == 'anniversary':
                pass
    
###############################################################################

    def showNameDialog(self):
        try:
            dialog = NameDialog()
            
            
            sn = self.data['sn'][0]
            tmpList = str(self.cnEdit.text()).split(sn)
            tmpList[0] = strip(tmpList[0])
            print tmpList
            
            prefix = tmpList[0].split(' ')
            for x in range(0, len(prefix)):
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
        except:
            print "Error"
        
        if (dialog.result() == QDialog.Accepted):
            self.data['sn'][0] = str(dialog.lastEdit.text())
            print self.data['sn']
            
            tmpList = []
            
            tmpList.append(self.__normalizeQtString(dialog.titleBox.currentText()))
            tmpList.append(self.__normalizeQtString(dialog.firstEdit.text()))
            tmpList.append(self.__normalizeQtString(dialog.middleEdit.text()))
            tmpList.append(self.__normalizeQtString(dialog.lastEdit.text()))
            tmpList.append(self.__normalizeQtString(dialog.suffixBox.currentText()))
            
            self.cnEdit.setText(''.join(tmpList))
            
###############################################################################

    def __normalizeQtString(self, tmpString):
        tmpString = strip(str(tmpString))
        
        if (len(tmpString) > 0):
            tmpString = tmpString + ' '
            
        return tmpString
