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

from plugins.template_plugin.TemplateWidgetDesign import TemplateWidgetDesign
from plugins.template_plugin.AddTemplateDialog import AddTemplateDialog
from base.backend.ServerList import ServerList
from base.backend.ServerObject import ServerObject
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.utils.backend.templateutils import *

class TemplateWidget(TemplateWidgetDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        TemplateWidgetDesign.__init__(self,parent,name,fl)
        
        self.templateList = []
        self.preloadedServerMeta = {}
        self.currentTemplate = None
        self.clearTemplateFields()
        
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
        
###############################################################################

    def displayTemplates(self, selectedTemplateName=None):
        self.templateView.clear()
        
        tmpList = self.preloadedServerMeta.keys()
        selected = None
        
        for x in self.templateList:
            if not x.serverName in tmpList:
                self.loadServerMeta(x.serverName)
            
            item = QListViewItem(self.templateView, x.name, x.serverName, x.description)
            self.templateView.insertItem(item)
            
            if not selectedTemplateName == None:
                selected = item
                
        if not selected == None:
            self.templateView.setSelected(selected, True)
                
###############################################################################

    def loadServerMeta(self, serverName):
        self.preloadedServerMeta[serverName] = ObjectClassAttributeInfo(serverName)
    
###############################################################################

    def displayTemplateInfo(self, selected):
        for x in self.templateList:
            if x.name == unicode(selected.text(0)):
                self.currentTemplate = x
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
    
