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


class GroupDialog(GroupDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        GroupDialogDesign.__init__(self,parent,name,modal,fl)
        
        iconDir = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons", "plugins", "usermanagement")
        groupPixmap = QPixmap(os.path.join(iconDir, "groupbig.png"))
        self.groupLabel.setPixmap(groupPixmap)
        
        
        self.SERVERMETA = None
        self.userName = None
        
        self.groupData = {}

###############################################################################

    def retrieveGroups(self):
        tmpText = self.textLabel.text().arg(self.userName)
        self.textLabel.setText(tmpText)
        
        tmpText = self.infoLabel2.text().arg(self.userName)
        self.infoLabel2.setText(tmpText)
        
        connectionObject = LumaConnection(self.SERVERMETA)
        connectionObject.bind()
        
        results = connectionObject.search(self.SERVERMETA.baseDN, ldap.SCOPE_SUBTREE, 
                "objectClass=posixGroup", )
                
        connectionObject.unbind()
        
        self.processResults(results)
        
###############################################################################

    def processResults(self, results):
        for x in results:
            self.groupData[x[0]] = x[1]
           
        tmpList = ['']
        for x in self.groupData.keys():
            name = self.groupData[x]['cn'][0]
            groupNumber = self.groupData[x]['gidNumber'][0]
            
            item = QCheckListItem(self.groupView, name, QCheckListItem.CheckBox)
            if self.groupData[x].has_key("memberUid"):
                if self.userName in self.groupData[x]["memberUid"]:
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
            if self.groupData[x]['cn'][0] == groupString:
                self.groupNumberBox.blockSignals(True)
                self.groupNumberBox.setValue(int(self.groupData[x]['gidNumber'][0]))
                self.groupNumberBox.blockSignals(False)
        
###############################################################################
        
    def groupNumberChanged(self, groupNumber):
        newGroup = ""
        
        for x in self.groupData.keys():
            if int(self.groupData[x]['gidNumber'][0]) == groupNumber:
                newGroup = self.groupData[x]['cn'][0]
                break
                
                    
        self.groupNameBox.blockSignals(True)
        self.groupNameBox.setCurrentText(newGroup)
        self.groupNameBox.blockSignals(False)
        
        
        
        
