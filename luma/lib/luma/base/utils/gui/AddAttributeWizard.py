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
import string
import copy

import environment
from base.utils.gui.AddAttributeWizardDesign import AddAttributeWizardDesign
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo


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

    def setData(self, dataObject):
        """ Sets the current object data, schema information and initializes
        the attribute box and wizard buttons.
        """
        
        self.ldapDataObject = dataObject
        
        #self.OBJECTVALUES = objectValues
        self.SCHEMAINFO = ObjectClassAttributeInfo(self.ldapDataObject.getServerMeta())
        self.processData()
        self.initAttributeBox()
        
        currentPageWidget = self.page(0)
        self.setFinishEnabled(currentPageWidget, True)
        self.setHelpEnabled(currentPageWidget, False)
        self.setNextEnabled(currentPageWidget, False)

###############################################################################

    def processData(self):
        """ Compute all attributes which can be added according to the data of
        the object. Single values which are already given are sorted out.
        """
        
        objectClasses = self.ldapDataObject.getObjectClasses()
        possibleMust, possibleMay = self.SCHEMAINFO.getAllAttributes(objectClasses)
        
        # attributes used by the current objectClass
        #usedAttributes = Set(objectAttributes).difference(Set(['objectClass']))
        usedAttributes = self.ldapDataObject.getAttributeList()
        
        # set of attribute which are used and have to be single
        singleAttributes = Set(filter(self.SCHEMAINFO.isSingle, usedAttributes))
        
        # create a set of attributes which may be added
        self.possibleAttributes = (possibleMust.union(possibleMay)).difference(singleAttributes)
        self.possibleAttributes = map(lambda x: string.lower(x), self.possibleAttributes)
        
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
            tmpList = copy.deepcopy(self.allPossibleAttributes)
        else:
            tmpList = copy.deepcopy(self.possibleAttributes)
        
        structuralClass = self.ldapDataObject.getStructuralClasses()
        
        # only show attributes whose objectclass combinations don't violate 
        # the objectclass chain (not two structural classes)
        if len(structuralClass) > 0:
            classList = filter(lambda x: not self.SCHEMAINFO.isStructural(x), self.SCHEMAINFO.getObjectClasses())
            for x in structuralClass:
                classList += self.SCHEMAINFO.getParents(x)
                
            for x in self.ldapDataObject.getObjectClasses():
                if not (x in classList):
                    classList.append(x)
                    
            mustAttributes, mayAttributes = self.SCHEMAINFO.getAllAttributes(classList)
            attributeList = mustAttributes.union(mayAttributes)
            
            cleanList = filter(lambda x: string.lower(x) in tmpList, attributeList)
            cleanList.sort()
            map(self.attributeBox.insertItem, cleanList)
        else:
            tmpList.sort()
            map(self.attributeBox.insertItem, tmpList)
        
        self.newSelection(self.attributeBox.currentText())
            
        
###############################################################################

    def newSelection(self, attribute):
        attribute = string.lower(str(attribute))
        
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
        
        if self.ldapDataObject.hasStructuralClass():
            structList = filter(lambda x: self.SCHEMAINFO.isStructural(x), classList)
            classList = filter(lambda x: not self.SCHEMAINFO.isStructural(x), classList)
            
            for x in structList:
                for y in self.ldapDataObject.getObjectClasses():
                    if self.SCHEMAINFO.sameObjectClassChain(x, y):
                        classList.append(x)
                        
        classList.sort()
                
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
        
        
        
    
