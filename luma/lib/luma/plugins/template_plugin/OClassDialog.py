# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path

from plugins.template_plugin.OClassDialogDesign import OClassDialogDesign
import environment
from base.backend.ServerObject import ServerObject
from base.backend.ServerList import ServerList
from base.utils.backend.templateutils import *


class OClassDialog(OClassDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        OClassDialogDesign.__init__(self,parent,name,modal,fl)

        tmpFile  = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons", "secure.png")
        securePixmap = QPixmap(tmpFile)

        self.serverListObject = ServerList()
        self.serverListObject.readServerList()

        self.serverList = self.serverListObject.serverList
        for x in self.serverList:
            if x.tls == 1:
                self.serverBox.insertItem(securePixmap, x.name)
            else:
                self.serverBox.insertItem(x.name)

        self.server_selected(self.serverBox.currentText())

###############################################################################

    def add_class(self):
        tmpText = str(self.classBox.currentText())
        if not(tmpText in self.get_class_list()):
            tmpItem  = QListViewItem(self.classView, tmpText)

            attrDict = self.objectInfo.objectClassesDict[tmpText]
            tmpDict = {}
            tmpDict['CLASSNAME'] = tmpText
            tmpDict['ATTRIBUTES'] = []
            for x in attrDict['MUST']:
                isSingle = self.objectInfo.isSingle(x)
                tmpDict['ATTRIBUTES'].append({'NAME' : x, 'MUST': 1 , 'SINGLE': isSingle, 'SHOW': 0 })

            for x in attrDict['MAY']:
                isSingle = self.objectInfo.isSingle(x)
                tmpDict['ATTRIBUTES'].append({'NAME' : x, 'MUST': 0 , 'SINGLE': isSingle, 'SHOW': 0 })

            self.template.tData.append(tmpDict)
            self.create_content()


###############################################################################

    def delete_class(self):
        if self.classView.selectedItem() == None:
            return
        curItemText = str(self.classView.selectedItem().text(0))
        position = None
        for x in self.template.tData:
            if x['CLASSNAME'] == curItemText:
                position = self.template.tData.index(x)
                break
        if not (position == None):
            del self.template.tData[position]
        self.create_content()




###############################################################################

    def get_class_list(self):
        tmpList = []
        fChild = self.classView.firstChild()
        if self.classView.childCount() == 0:
            return []
        tmpList.append(fChild)
        while fChild.nextSibling():
            tmpList.append(fChild.nextSibling())
            fChild = tmpList[-1]

        nameList = []
        for x in tmpList:
            nameList.append(str(x.text(0)))
        return nameList

###############################################################################

    def server_selected(self, serverName):
        self.classBox.clear()
        self.objectInfo = environment.getServerMeta(str(serverName))

        tmpList = self.objectInfo.objectClassesDict.keys()
        tmpList.sort()
        for x in tmpList:
            self.classBox.insertItem(x)

###############################################################################

    def create_content(self):
        self.save_attribute_values()
        self.classView.clear()
        self.attributeView.clear()
        for x in self.template.get_objectclasses():
            tmpItem = QListViewItem(self.classView, x)
            self.classView.insertItem(tmpItem)

        aList = self.template.get_attributeinfos()
        for x in aList.keys():
            tmpItem = QCheckListItem(self.attributeView, x, QCheckListItem.CheckBox )
            if aList[x]['MUST'] == 1:
                tmpItem.setOn(1)
                tmpItem.setEnabled(0)
            if aList[x]['SHOW'] == 1:
                tmpItem.setOn(1)
            self.attributeView.insertItem(tmpItem)

###############################################################################

    def save_attribute_values(self):
        child = self.attributeView.firstChild()
        if not (child == None):
            self.template.set_attribute_show(str(child.text()), child.isOn())
            while child.nextSibling():
                child = child.nextSibling()
                self.template.set_attribute_show(str(child.text()), child.isOn())









