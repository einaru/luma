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
from base.utils.backend.templateutils import *
from plugins.template_plugin.AddObjectClassDialog import AddObjectClassDialog
from plugins.template_plugin.AddAttributeDialog import AddAttributeDialog
from plugins.template_plugin.ClassDeleteDialog import ClassDeleteDialog
import environment
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo


class TemplateWidget(TemplateWidgetDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        TemplateWidgetDesign.__init__(self,parent,name,fl)
        
        self.iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        self.okIcon = QPixmap(os.path.join(self.iconPath, "ok.png"))
        self.noIcon = QPixmap(os.path.join(self.iconPath, "no.png"))
        
        self.templateList = []
        self.preloadedServerMeta = {}
        self.currentTemplate = None
        self.clearTemplateFields()
        self.enableButtons(False)
        
        self.loadTemplates()
        self.displayTemplates()
        
        self.saveTemplateButton.setEnabled(False)
        
###############################################################################

    def loadTemplates(self):
        self.templateList = TemplateList().templateList
        
###############################################################################

    def addTemplate(self):
        dialog = AddTemplateDialog()
        
        # Provide the dialog with a list of already existing templates
        dialog.templateList = map(lambda x: x.name, self.templateList)
        
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
        
        self.templateLabel.setText("")
        self.serverLabel.setText("")
        self.descriptionLabel.setText("")
        
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
        serverList = ServerList()
        serverList.readServerList()
        serverMeta = serverList.getServerObject(serverName)
        self.preloadedServerMeta[serverName] = ObjectClassAttributeInfo(serverMeta)
    
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
        
        self.displayAttributes()
        self.displayObjectClasses()
        
###############################################################################

    def displayObjectClasses(self):
        self.classView.clear()
        
        for x in self.currentTemplate.objectClasses:
            item = QListViewItem(self.classView, x)
        
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
        
        templateClasses = Set(self.currentTemplate.getObjectClasses())
        
        structural = False
        structuralList = []
        for x in templateClasses:
            if metaInfo.isStructural(x):
                structural = True
                structuralList.append(x)
                
        tmpClasses = metaInfo.getObjectClasses()
        if structural:
            nonStructClasses = filter(lambda x: not metaInfo.isStructural(x), tmpClasses)
            structClasses = filter(lambda x: metaInfo.isStructural(x), tmpClasses)
                
            tmpClasses = nonStructClasses
            
            for x in structClasses:
                if metaInfo.classAllowed(x, structuralList):
                    tmpClasses.append(x)
                
        objectClasses = Set(tmpClasses)
                
        objectClasses -= templateClasses
        
        for x in objectClasses:
            tmpItem = QListViewItem(dialog.classView, x)
        
        dialog.exec_loop()
        
        if dialog.result() == QDialog.Rejected:
            return
            
        newClasses = []
        
        listIterator = QListViewItemIterator(dialog.classView)
        while listIterator.current():
            item = listIterator.current()
            
            if item.isSelected():
                newClasses.append(str(item.text(0)))
                
            listIterator += 1
        
        parentClasses = []
        for x in newClasses:
            parentList = metaInfo.getParents(x)
            parentClasses += parentList
            
        newClasses = Set(newClasses).union(Set(parentClasses))
        
        for x in newClasses:
            self.currentTemplate.addObjectClass(x)
            
        mustAttributes = metaInfo.getAllMusts(newClasses)
        for x in mustAttributes:
            # WARNING!!! DO NOT REMOVE THIS CODE!!!
            # If you choose the objectClass 'top', it has the attribute 
            # 'objectClass'. This overwrites the objectClass attribute value
            # from the python data structure and causes errors. So we filter it 
            # out.
            if x == "objectClass":
                continue
                
            must = metaInfo.isMust(x, newClasses)
            single = metaInfo.isSingle(x)
            binary = metaInfo.isBinary(x)
            self.currentTemplate.addAttribute(x, must, single, binary, None)
            
        self.displayAttributes()
        self.displayObjectClasses()
        self.saveTemplateButton.setEnabled(True)
        
###############################################################################

    def enableButtons(self, buttonBool):
        self.addClassButton.setEnabled(buttonBool)
        self.deleteClassButton.setEnabled(buttonBool)
        self.addAttributeButton.setEnabled(buttonBool)
        self.deleteAttributeButton.setEnabled(buttonBool)
        
###############################################################################

    def deleteObjectClass(self):
        serverName = self.currentTemplate.serverName
        self.loadServerMeta(serverName)
        metaInfo = self.preloadedServerMeta[serverName]
        
        item = self.classView.selectedItem()
        if item == None:
            return
            
        currentAttributes = self.currentTemplate.getAttributeList()
        
        className = str(item.text(0))
        mustSet, maySet = metaInfo.getAllAttributes([className])
        
        obsoleteAttributes = filter(lambda x: x in (mustSet|maySet), currentAttributes)
        remainingAttributes = filter(lambda x: not x in (mustSet|maySet), currentAttributes)
            
        dialog = ClassDeleteDialog()
        tmpText = dialog.textLabel.text().arg(className)
        dialog.textLabel.setText(tmpText)
        
        for x in obsoleteAttributes:
            QListViewItem(dialog.attributeView, x)
        dialog.exec_loop()
        
        if dialog.result() == QDialog.Accepted:
            for x in obsoleteAttributes:
                self.currentTemplate.deleteAttribute(x)
                
            self.currentTemplate.deleteObjectClass(className)
            
            self.displayObjectClasses()
            self.displayAttributes()
        
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
                item.setRenameEnabled(4, True)
                
            if attribute.defaultValue == None:
                item.setText(4, "")
            else:
                item.setText(4, attribute.defaultValue)
                

###############################################################################

    def saveTemplates(self):
        templates = TemplateList(copy.deepcopy(self.templateList))
        templates.save()
        self.saveTemplateButton.setEnabled(False)
        
###############################################################################

    def editAttribute(self, item, row, text):
        attributeName = str(item.text(0))
        newValue = unicode(text).strip()
        if newValue == "":
            newValue = None
        
        self.currentTemplate.setAttributeDefaultValue(attributeName, newValue)
        self.saveTemplateButton.setEnabled(True)
    
###############################################################################

    def deleteTemplate(self):
        item = self.templateView.selectedItem()
        
        if item == None:
            return
            
        templateName = str(item.text(0))
            
        tmpDialog = QMessageBox(self.trUtf8("Delete template"),
            self.trUtf8("Do you really want to delete the selected template?"),
            QMessageBox.Critical,
            QMessageBox.Yes,
            QMessageBox.No,
            QMessageBox.NoButton,
            self)
        
        tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
        tmpDialog.exec_loop()
        
        if tmpDialog.result() == 4:
            return
            
        # Create a new template list without the old one
        self.templateList = filter(lambda x: x.name != templateName, self.templateList)
        self.currentTemplate = None
        
        self.displayTemplates()
        self.saveTemplateButton.setEnabled(True)
        
###############################################################################

    def duplicateTemplate(self):
        item = self.templateView.selectedItem()
        
        if item == None:
            return
            
        template = filter(lambda x: x.name == str(item.text(0)), self.templateList)[0]
        
        dialog = AddTemplateDialog()
        dialog.nameEdit.setText(template.name)
        dialog.serverBox.setCurrentText(template.serverName)
        dialog.descriptionEdit.setText(template.description)
        
        # Provide the dialog with a list of already existing templates
        dialog.templateList = map(lambda x: x.name, self.templateList)
        dialog.valuesChanged()
        
        dialog.exec_loop()
        if dialog.result() == QDialog.Rejected:
            return
            

        newTemplate = LdapTemplate()
        newTemplate.name = strip(unicode(dialog.nameEdit.text()))
        newTemplate.serverName = unicode(dialog.serverBox.currentText())
        newTemplate.description = strip(unicode(dialog.descriptionEdit.text()))
        
        self.loadServerMeta(newTemplate.serverName)
        metaInfo = self.preloadedServerMeta[newTemplate.serverName]
        
        for x in template.getObjectClasses():
            if metaInfo.hasObjectClass(x):
                newTemplate.addObjectClass(x)
                
                mustAttributes = metaInfo.getAllMusts([x])
                for y in mustAttributes:
                    must = metaInfo.isMust(y, [x])
                    single = metaInfo.isSingle(y)
                    binary = metaInfo.isBinary(y)
                    newTemplate.addAttribute(y, must, single, binary, None)
        
        self.templateList.append(newTemplate)
        self.currentTemplate = newTemplate
        self.displayTemplates(newTemplate.name)
        
        self.saveTemplateButton.setEnabled(True)
        
###############################################################################

    def deleteAttribute(self):
        item = self.attributeView.selectedItem()
        
        if item == None:
            return
            
        attributeName = str(item.text(0))
        
        tmpDialog = QMessageBox(self.trUtf8("Delete attribute"),
            self.trUtf8("Do you really want to delete the attribute?"),
            QMessageBox.Critical,
            QMessageBox.Yes,
            QMessageBox.No,
            QMessageBox.NoButton,
            self)
        
        tmpDialog.setIconPixmap(QPixmap(os.path.join(self.iconPath, "warning_big.png")))
        tmpDialog.exec_loop()
        
        if tmpDialog.result() == 4:
            return
        
        self.currentTemplate.deleteAttribute(attributeName)
        self.displayAttributes()
        self.saveTemplateButton.setEnabled(True)
        
###############################################################################

    def attributeSelectionChanged(self, item):
        attributeName = str(item.text(0))
        
        serverName = self.currentTemplate.serverName
        self.loadServerMeta(serverName)
        metaInfo = self.preloadedServerMeta[serverName]
        
        mustAttributes = metaInfo.getAllMusts(self.currentTemplate.getObjectClasses())
        
        if attributeName in mustAttributes:
            self.deleteAttributeButton.setEnabled(False)
        else:
            self.deleteAttributeButton.setEnabled(True)
