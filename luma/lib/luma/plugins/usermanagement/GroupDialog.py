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

import environment
from plugins.usermanagement.GroupDialogDesign import GroupDialogDesign
from base.backend.LumaConnection import LumaConnection
from base.utils.gui.LumaErrorDialog import LumaErrorDialog


class GroupDialog(GroupDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        GroupDialogDesign.__init__(self,parent,name,modal,fl)
        
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons", "plugins", "usermanagement")
        groupPixmap = QPixmap(os.path.join(iconDir, "groupbig.png"))
        self.groupLabel.setPixmap(groupPixmap)
        
        
        self.serverMeta = None
        self.userName = None
        
        self.groupData = {}

###############################################################################

    def retrieveGroups(self):
        tmpText = self.textLabel.text().arg(self.userName)
        self.textLabel.setText(tmpText)
        
        tmpText = self.infoLabel2.text().arg(self.userName)
        self.infoLabel2.setText(tmpText)
        
        connectionObject = LumaConnection(self.serverMeta)
        bindSuccess, exceptionObject = connectionObject.bind()
        
        if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
        
        success, resultList, exceptionObject = connectionObject.search(self.serverMeta.currentBase, ldap.SCOPE_SUBTREE, 
                "objectClass=posixGroup", )
                
        connectionObject.unbind()
        
        if success:
            self.processResults(resultList)
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could retrieve other group information.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
        
###############################################################################

    def processResults(self, results):
        for x in results:
            self.groupData[x.getDN()] = x
           
        tmpList = ['']
        for x in self.groupData.keys():
            name = self.groupData[x].getAttributeValue('cn', 0)
            groupNumber = self.groupData[x].getAttributeValue('gidNumber', 0)
            
            item = QCheckListItem(self.groupView, name, QCheckListItem.CheckBox)
            if self.groupData[x].hasAttribute("memberUid"):
                if self.userName in self.groupData[x].getAttributeValueList("memberUid"):
                    item.setOn(True)
            item.setText(1, groupNumber)
            item.setText(2, x)
            
            tmpList.append(name)
            
        tmpList.sort()
        map(self.groupNameBox.insertItem, tmpList)
        
###############################################################################

    def groupNameChanged(self, groupString):
        groupString = unicode(groupString)
        
        for x in self.groupData.keys():
            if self.groupData[x].getAttributeValue('cn', 0) == groupString:
                self.groupNumberBox.blockSignals(True)
                self.groupNumberBox.setValue(int(self.groupData[x].getAttributeValue('gidNumber',0)))
                self.groupNumberBox.blockSignals(False)
        
###############################################################################
        
    def groupNumberChanged(self, groupNumber):
        newGroup = None
        
        for x in self.groupData.keys():
            if int(self.groupData[x].getAttributeValue('gidNumber', 0)) == groupNumber:
                newGroup = self.groupData[x].getAttributeValue('cn', 0)
                break
                
        # If the groupnumber belongs to a non-ldap group, reset the group in 
        # the toolbox.
        if newGroup == None:
            newGroup = ""
            
        self.groupNameBox.blockSignals(True)
        self.groupNameBox.setCurrentText(newGroup)
        self.groupNameBox.blockSignals(False)
        
        
        
        
