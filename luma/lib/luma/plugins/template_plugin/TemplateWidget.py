# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
from string import strip
from sets import Set
import copy

from plugins.template_plugin.TemplateWidgetDesign import TemplateWidgetDesign
from plugins.template_plugin.AddTemplateDialog import AddTemplateDialog
from base.backend.ServerList import ServerList
from base.backend.ServerObject import ServerObject
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.utils.backend.templateutils import *
from plugins.template_plugin.AddObjectClassDialog import AddObjectClassDialog
from plugins.template_plugin.AddAttributeDialog import AddAttributeDialog
import environment


class TemplateWidget(TemplateWidgetDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        TemplateWidgetDesign.__init__(self,parent,name,fl)
        
        iconPrefix = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        self.okIcon = QPixmap(os.path.join(iconPrefix, "ok.png"))
        self.noIcon = QPixmap(os.path.join(iconPrefix, "no.png"))
        
        self.templateList = []
        self.preloadedServerMeta = {}
        self.currentTemplate = None
        self.clearTemplateFields()
        self.enableButtons(False)
        
        self.saveTemplateButton.setEnabled(False)
        
###############################################################################

    def addTemplate(self):
        dialog = AddTemplateDialog()
        
        # FIXME: initialisierung der blacklist fehlt
        #dialog.templateList.append("foo")
        
        dialog.exec_loop()
        if dialog.result() == QDialog.Rejected:
            return

        newTemplate = LdapTemplate()
        newTemplate.name = strip(unicode(dialog.nameEdit.text()))
        newTemplate.serverName = unicode(dialog.serverBox.currentText())
        newTemplate.description = strip(unicode(dialog.descriptionEdit.text()))
        
        self.templateList.append(newTemplate)
        self.currentTemplate = newTemplate
        self.displayTemplates(newTemplate.name)
        
        self.saveTemplateButton.setEnabled(True)
        
###############################################################################

    def displayTemplates(self, selectedTemplateName=None):
        self.templateView.clear()
        self.classView.clear()
        self.attributeView.clear()
        
        selected = None
        
        for x in self.templateList:
            item = QListViewItem(self.templateView, x.name, x.serverName, x.description)
            self.templateView.insertItem(item)
            
            if not selectedTemplateName == None:
                selected = item
                
        if not selected == None:
            self.templateView.setSelected(selected, True)
                
###############################################################################

    def loadServerMeta(self, serverName):
        if not (serverName in self.preloadedServerMeta.keys()):
            self.preloadedServerMeta[serverName] = ObjectClassAttributeInfo(serverName)
    
###############################################################################

    def displayTemplateInfo(self, selected):
        for x in self.templateList:
            if x.name == unicode(selected.text(0)):
                self.currentTemplate = x
                self.enableButtons(True)
                break
    
        self.displayData()
        
###############################################################################

    def displayData(self):
        self.templateLabel.setText(self.currentTemplate.name)
        self.serverLabel.setText(self.currentTemplate.serverName)
        self.descriptionLabel.setText(self.currentTemplate.description)
        
###############################################################################

    def clearTemplateFields(self):
        self.templateLabel.setText(None)
        self.serverLabel.setText(None)
        self.descriptionLabel.setText(None)
        
###############################################################################

    def addObjectClass(self):
        serverName = self.currentTemplate.serverName
        self.loadServerMeta(serverName)
        
        dialog = AddObjectClassDialog()
        metaInfo = self.preloadedServerMeta[serverName]
        
        objectClasses = Set(metaInfo.getObjectClasses())
        templateClasses = Set(self.currentTemplate.getObjectClasses())
        objectClasses -= templateClasses
        
        for x in objectClasses:
            item = QCheckListItem(dialog.classView, x, QCheckListItem.CheckBox)
        
        dialog.exec_loop()
        
        if dialog.result() == QDialog.Rejected:
            return
            
        newClasses = []
        listIterator = QListViewItemIterator(dialog.classView)
        
        while listIterator.current():
            item = listIterator.current()
            
            if item.isOn():
                newClasses.append(str(item.text(0)))
                
            listIterator += 1
            
        for x in newClasses:
            item = QListViewItem(self.classView, x)
            self.currentTemplate.addObjectClass(x)
         
         
        mustAttributes = metaInfo.getAllMusts(newClasses)
        for x in mustAttributes:
            must = metaInfo.isMust(x, newClasses)
            single = metaInfo.isSingle(x)
            binary = metaInfo.isBinary(x)
            self.currentTemplate.addAttribute(x, must, single, binary, None)
            
        self.displayAttributes()
        self.saveTemplateButton.setEnabled(True)
        
###############################################################################

    def enableButtons(self, buttonBool):
        self.addClassButton.setEnabled(buttonBool)
        self.deleteClassButton.setEnabled(buttonBool)
        self.addAttributeButton.setEnabled(buttonBool)
        self.editAttributeButton.setEnabled(buttonBool)
        self.deleteAttributeButton.setEnabled(buttonBool)
        
###############################################################################

    def deleteObjectClass(self):
        item = self.classView.currentItem()
        self.saveTemplateButton.setEnabled(True)
        
###############################################################################

    def addAttribute(self):
        serverName = self.currentTemplate.serverName
        self.loadServerMeta(serverName)
        metaInfo = self.preloadedServerMeta[serverName]
        
        currentClasses = self.currentTemplate.getObjectClasses()
        mustAttributes, mayAttributes = metaInfo.getAllAttributes(currentClasses)
        usedAttributes = Set(self.currentTemplate.getAttributeList())
        allowedAttributes = mustAttributes | mayAttributes
        allowedAttributes -= usedAttributes
        
        
        dialog = AddAttributeDialog()
        
        dialog.attributes = allowedAttributes
        dialog.objectClasses = currentClasses
        dialog.metaInfo = metaInfo
        
        for x in allowedAttributes:
            item = QCheckListItem(dialog.attributeView, x, QCheckListItem.CheckBox)
        
        dialog.exec_loop()
        
        if dialog.result() == QDialog.Rejected:
            return
        
        newAttributes = []
        listIterator = QListViewItemIterator(dialog.attributeView)
        
        while listIterator.current():
            item = listIterator.current()
            
            if item.isOn():
                newAttributes.append(str(item.text(0)))
                
            listIterator += 1
            
        for x in newAttributes:
            must = metaInfo.isMust(x, currentClasses)
            single = metaInfo.isSingle(x)
            binary = metaInfo.isBinary(x)
            defaultValue = None
            if dialog.defaultValues.has_key(x):
                defaultValue = dialog.defaultValues[x]
        
            self.currentTemplate.addAttribute(x, must, single, binary, defaultValue)
            
        self.displayAttributes()
        self.saveTemplateButton.setEnabled(True)
        
###############################################################################

    def displayAttributes(self):
        self.attributeView.clear()
        for x in self.currentTemplate.getAttributeList():
            attribute = self.currentTemplate.attributes[x]
            
            item = QListViewItem(self.attributeView, x)
            
            if attribute.must:
                item.setPixmap(1, self.okIcon)
            else:
                item.setPixmap(1, self.noIcon)
                
            if attribute.single:
                item.setPixmap(2, self.okIcon)
            else:
                item.setPixmap(2, self.noIcon)
                
            if attribute.binary:
                item.setPixmap(3, self.okIcon)
            else:
                item.setPixmap(3, self.noIcon)
                
            if attribute.defaultValue == None:
                item.setText(4, "")
            else:
                item.setText(4, attribute.defaultValue)

###############################################################################

    def saveTemplates(self):
        templates = TemplateList(copy.deepcopy(self.templateList))
        templates.save()
        self.saveTemplateButton.setEnabled(False)
    
