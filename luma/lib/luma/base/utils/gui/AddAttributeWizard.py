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
from sets import Set

import environment
from base.utils.gui.AddAttributeWizardDesign import AddAttributeWizardDesign


class AddAttributeWizard(AddAttributeWizardDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        AddAttributeWizardDesign.__init__(self,parent,name,modal,fl)
        
        self.iconPath = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        attributePixmap = QPixmap(os.path.join(self.iconPath, "addattribute.png"))
        objectclassPixmap = QPixmap(os.path.join(self.iconPath, "objectclass.png"))
        
        self.imageLabel.setPixmap(attributePixmap)
        self.objectclassLabel.setPixmap(objectclassPixmap)
        
        # attribute values of the current ldap object
        self.OBJECTVALUES = None
        
        # schema information for the ldap server
        self.SCHEMAINFO = None
        
        # set of attributes which are possible with the current objectclasses
        self.possibleAttributes = None
        
        # set of all attributes which are supported by the server
        self.allPossibleAttributes = None
        
###############################################################################

    def setData(self, objectValues, schemaMeta):
        self.OBJECTVALUES = objectValues
        self.SCHEMAINFO = schemaMeta
        self.processData()
        self.initAttributeBox()
        
        currentPageWidget = self.page(0)
        self.setFinishEnabled(currentPageWidget, True)
        self.setHelpEnabled(currentPageWidget, False)
        self.setNextEnabled(currentPageWidget, False)

###############################################################################

    def processData(self):
        possibleMust, possibleMay = self.SCHEMAINFO.getAllAttributes(self.OBJECTVALUES['objectClass'])
        
        # attributes used by the current objectClass
        usedAttributes = Set(self.OBJECTVALUES).difference(Set(['objectClass']))
        
        # set of attribute which are used and have to be single
        singleAttributes = Set(filter(self.SCHEMAINFO.isSingle, usedAttributes))
        
        # create a set of attributes which may be added
        self.possibleAttributes = (possibleMust.union(possibleMay)).difference(singleAttributes)
        
        # create a set of attributes which are supported by the server
        self.allPossibleAttributes = Set(self.SCHEMAINFO.attributeDict.keys()).difference(singleAttributes)

###############################################################################

    def initAttributeBox(self):
        self.attributeBox.clear()
        
        currentPageWidget = self.currentPage()
        
        showAll = self.enableAllBox.isChecked()
        self.setFinishEnabled(currentPageWidget, True)
        self.setHelpEnabled(currentPageWidget, False)
        
        tmpList = None
        if showAll:
            tmpList = map(None, self.allPossibleAttributes)
            self.setNextEnabled(currentPageWidget, True)
            self.setFinishEnabled(currentPageWidget, False)
        else:
            tmpList = map(None, self.possibleAttributes)
            self.setNextEnabled(currentPageWidget, False)
            
        tmpList.sort()
        
        # init combobox with attributes supported by current objectclasses
        map(self.attributeBox.insertItem, tmpList)
        
        if showAll:
            self.newSelection(self.attributeBox.currentText())
        
###############################################################################

    def newSelection(self, attribute):
        attribute = str(attribute)
        
        currentPageWidget = self.currentPage()
        
        mustSet, maySet = self.SCHEMAINFO.getAllObjectclassesForAttr(attribute)
        tmpSet = mustSet.union(maySet)
        
        if (attribute in self.possibleAttributes) or (len(tmpSet) == 0):
            self.setFinishEnabled(currentPageWidget, True)
            self.setNextEnabled(currentPageWidget, False)
        else:
            self.setFinishEnabled(currentPageWidget, False)
            self.setNextEnabled(currentPageWidget, True)
            
###############################################################################

    def next(self):
        page = self.page(1)
        self.initClassPage()
        self.showPage(page)
        
###############################################################################

    def initClassPage(self):
        currentPageWidget = self.currentPage()
        self.setFinishEnabled(currentPageWidget, False)
        self.setHelpEnabled(currentPageWidget, False)
    
        self.classBox.clear()
        self.mustAttributeBox.clear()
        
        attribute = str(self.attributeBox.currentText())
        
        mustSet, maySet = self.SCHEMAINFO.getAllObjectclassesForAttr(attribute)
        
        classList = mustSet.union(maySet)
        
        map(self.classBox.insertItem, classList)
        
###############################################################################

    def classSelection(self):
        self.mustAttributeBox.clear()
        
        objectclass = str(self.classBox.currentText())
        
        mustAttributes = self.SCHEMAINFO.getAllMusts([objectclass])
        
        attribute = Set([str(self.attributeBox.currentText())])
        
        map(self.mustAttributeBox.insertItem, mustAttributes.difference(attribute))
        
        currentPageWidget = self.currentPage()
        self.setFinishEnabled(currentPageWidget, True)
        
        
        
    
