# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import copy
import os.path

from plugins.template_plugin.TemplateFormDesign import TemplateFormDesign
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.utils.backend.templateutils import *
import environment
from base.backend.ServerObject import ServerObject
from base.backend.ServerList import ServerList
from plugins.template_plugin.OClassDialog import OClassDialog



class TemplateForm(TemplateFormDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        TemplateFormDesign.__init__ (self,parent,name,fl)

        self.iconPath = os.path.join (environment.lumaInstallationPrefix, "share", "luma", "icons")
        self.okIcon = QPixmap (os.path.join (self.iconPath, "ok.png") )
        self.noIcon = QPixmap (os.path.join (self.iconPath, "no.png") )

        self.tplFile = None

        self.update_template_view()


###############################################################################

    def add_template(self):
        templateText = QInputDialog.getText(self.trUtf8("Add Template"), self.trUtf8("Enter template name:"))[0]
        if templateText.isEmpty():
            return
        else:
            templateText = str(templateText)
        templateList = self.get_template_list()
        if templateText in templateList:
            QMessageBox.warning(self, self.trUtf8("Add Template"), self.trUtf8("Template name already exists!"))
        else:
            tmpItem = QListViewItem(self.templateView, templateText)
            self.templateView.insertItem(tmpItem)
            self.templateView.setSelected(tmpItem, 1)
            newTemplate = LdapTemplate()
            newTemplate.name = templateText
            self.tplFile.tplList.append(copy.deepcopy(newTemplate))

###############################################################################

    def delete_template(self):
        if self.templateView.selectedItem() == None:
            return
        itemText = str(self.templateView.selectedItem().text(0))
        position = self.tplFile.tplList.index(self.tplFile.get_templateobject(itemText))
        del self.tplFile.tplList[position]
        self.tplFile.save_to_file()
        self.update_template_view()
        self.update_view(1)

###############################################################################

    def get_template_list(self):
        tmpList = []
        fChild = self.templateView.firstChild()
        if self.templateView.childCount() == 0:
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

    def update_view(self, reloadView=1):
        self.infoView.clear()
        if self.templateView.selectedItem() == None:
            return
        curItem = str(self.templateView.selectedItem().text(0))
        if reloadView:
            self.tplFile = TemplateFile()
        
        x = self.tplFile.get_templateobject(curItem)
        if x == None:
            return
        for y in x.get_objectclasses():
            tmpItem = QListViewItem(self.infoView, "objectClass", y)
        tmpDict = x.get_attributeinfos()
        for y in tmpDict.keys():
            tmpItem = QListViewItem(self.infoView)
            tmpItem.setText(0, 'attribute')
            tmpItem.setText(1, y)
            if tmpDict[y]['MUST']:
                tmpItem.setPixmap(2, self.okIcon)
            else:
                tmpItem.setPixmap(2, self.noIcon)
            if tmpDict[y]['SINGLE']:
                tmpItem.setPixmap(3, self.okIcon)
            else:
                tmpItem.setPixmap(3, self.noIcon)
            if tmpDict[y]['SHOW']:
                tmpItem.setPixmap(4, self.okIcon)
            else:
                tmpItem.setPixmap(4, self.noIcon)

###############################################################################

    def edit_classes(self):
        template = None
        dialog = OClassDialog()
        dialog.classView.clear()
        if self.templateView.selectedItem() == None:
            return
        curItem = str(self.templateView.selectedItem().text(0))
        position = None
        for x in self.tplFile.tplList:
            if x.name == curItem:
                position = self.tplFile.tplList.index(x)
                dialog.template = copy.deepcopy(x)
        dialog.create_content()
        dialog.exec_loop()
        dialog.save_attribute_values()
        if dialog.result():
            template = dialog.template
            self.tplFile.tplList[position] = copy.deepcopy(template)
            self.update_view(0)

###############################################################################

    def update_template_view(self):
        self.tplFile = TemplateFile()
        self.templateView.clear()
        for x in self.tplFile.tplList:
            tmpItem = QListViewItem(self.templateView, x.name)
            self.templateView.insertItem(tmpItem)

###############################################################################

    def save_template(self):
        self.tplFile.save_to_file()
















