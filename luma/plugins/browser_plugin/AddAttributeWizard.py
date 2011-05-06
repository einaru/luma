# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

#from qt import *
import os.path
import copy

#import environment
import PyQt4
from PyQt4.QtCore import QString, pyqtSlot
from PyQt4.QtGui import QWizard
from .gui.AddAttributeWizardDesign import Ui_AddAttributeWizardDesign
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.util.IconTheme import pixmapFromTheme


class AddAttributeWizard(QWizard, Ui_AddAttributeWizardDesign):

    def __init__(self, parent = None, flags = PyQt4.QtCore.Qt.Widget):
        QWizard.__init__(self, parent, flags)
        self.setupUi(self)
        # need to initialize the pages before connecting signals
        self.restart()

        attributePixmap = pixmapFromTheme(
            "addattribute", ":/icons/64/add-attribute")
        objectclassPixmap = pixmapFromTheme(
            "objectclass", ":/icons/64/objectclass")
        self.imageLabel.setPixmap(attributePixmap)
        self.objectclassLabel.setPixmap(objectclassPixmap)
        
        self.enableAllBox.toggled.connect(self.initAttributeBox)
        self.attributeBox.activated[str].connect(self.newSelection)
        self.classBox.itemSelectionChanged.connect(self.classSelection)
        
        # attribute values of the current ldap object
        self.OBJECTVALUES = None
        
        # schema information for the ldap server
        self.SCHEMAINFO = None
        
        # set of attributes which are possible with the current objectclasses
        self.possibleAttributes = None
        
        # set of all attributes which are supported by the server
        self.allPossibleAttributes = None
        
###############################################################################

    def setData(self, smartObject):
        """ Sets the current object data, schema information and initializes
        the attribute box and wizard buttons.
        """
        
        self.smartObject = smartObject
        
        self.SCHEMAINFO = ObjectClassAttributeInfo(self.smartObject.getServerMeta())
        self.processData()
        self.initAttributeBox()
        
        currentPageWidget = self.page(0)
        #self.button(QWizard.FinishButton).setDisabled(False)
        #self.button(QWizard.NextButton).setDisabled(True)

###############################################################################

    def processData(self):
        """ Compute all attributes which can be added according to the data of
        the object. Single values which are already given are sorted out.
        """

        possibleMust, possibleMay = self.smartObject.getPossibleAttributes()
        
        # attributes used by the current objectClass
        #usedAttributes = set(objectAttributes).difference(set(['objectClass']))
        usedAttributes = self.smartObject.getAttributeList()
        
        # set of attribute which are used and have to be single
        singleAttributes = set(filter(self.SCHEMAINFO.isSingle, usedAttributes))
        
        # create a set of attributes which may be added
        self.possibleAttributes = (possibleMust.union(possibleMay)).difference(singleAttributes)
        self.possibleAttributes = map(lambda x: x.lower(), self.possibleAttributes)
        
        # create a set of attributes which are supported by the server
        self.allPossibleAttributes = set(self.SCHEMAINFO.attributeDict.keys()).difference(singleAttributes)

###############################################################################

    def initAttributeBox(self):
        self.attributeBox.clear()
        
        currentPageWidget = self.currentPage()
        
        showAll = self.enableAllBox.isChecked()
        currentPageWidget.setFinalPage(True)
        currentPageWidget.setCommitPage(False)
        #self.button(QWizard.FinishButton).setDisabled(False)
        
        tmpList = None
        if showAll:
            tmpList = copy.deepcopy(self.allPossibleAttributes)
        else:
            tmpList = copy.deepcopy(self.possibleAttributes)
        
        structuralClass = self.smartObject.getStructuralClasses()
        
        # only show attributes whose objectclass combinations don't violate 
        # the objectclass chain (not two structural classes)
        if len(structuralClass) > 0:
            classList = filter(lambda x: not self.SCHEMAINFO.isStructural(x), self.SCHEMAINFO.getObjectClasses())
            for x in structuralClass:
                classList += self.SCHEMAINFO.getParents(x)
                
            for x in self.smartObject.getObjectClasses():
                if not (x in classList):
                    classList.append(x)
                    
            mustAttributes, mayAttributes = self.SCHEMAINFO.getAllAttributes(classList)
            attributeList = mustAttributes.union(mayAttributes)
            
            cleanList = filter(lambda x: x.lower() in tmpList, attributeList)
            tmpList = cleanList

        tmpList.sort()
        tmpList = filter(lambda x: not (x.lower() == "objectclass"), tmpList)
        map(self.attributeBox.addItem, tmpList)
            
        self.newSelection(self.attributeBox.currentText())
            
        
###############################################################################

    @pyqtSlot(int)
    def newSelection(self, attribute):
        pass

    @pyqtSlot("QString")
    def newSelection(self, attribute):
        attribute = str(attribute).lower()
        
        currentPageWidget = self.currentPage()
        
        mustSet, maySet = self.SCHEMAINFO.getAllObjectclassesForAttr(attribute)
        tmpSet = mustSet.union(maySet)
        
        if (attribute in self.possibleAttributes) or (len(tmpSet) == 0):
            currentPageWidget.setFinalPage(True)
            #self.button(QWizard.FinishButton).setDisabled(False)
            self.button(QWizard.NextButton).setDisabled(True)
        else:
            currentPageWidget.setFinalPage(False)
            #self.button(QWizard.FinishButton).setDisabled(True)
            self.button(QWizard.NextButton).setDisabled(False)
            
###############################################################################

    def initClassPage(self):
        currentPageWidget = self.currentPage()
        #self.button(QWizard.FinishButton).setDisabled(True)
    
        self.classBox.clear()
        self.mustAttributeBox.clear()
        
        attribute = str(self.attributeBox.currentText())
        mustSet, maySet = self.SCHEMAINFO.getAllObjectclassesForAttr(attribute)
        classList = mustSet.union(maySet)
        
        if self.smartObject.hasStructuralClass():
            structList = filter(lambda x: self.SCHEMAINFO.isStructural(x), classList)
            classList = filter(lambda x: not self.SCHEMAINFO.isStructural(x), classList)
            
            for x in structList:
                for y in self.smartObject.getObjectClasses():
                    if self.SCHEMAINFO.sameObjectClassChain(x, y):
                        classList.append(x)
                        
        classList.sort()
                
        map(self.classBox.addItem, classList)
        
###############################################################################

    def classSelection(self):
        self.mustAttributeBox.clear()
        
        objectclass = str(self.classBox.currentItem().text())
        
        mustAttributes = self.SCHEMAINFO.getAllMusts([objectclass])
        
        attribute = set([str(self.attributeBox.currentText())])
        
        map(self.mustAttributeBox.addItem, mustAttributes.difference(attribute))
        
        currentPageWidget = self.currentPage()
        #self.button(QWizard.FinishButton).setDisabled(False)
        
###############################################################################
    
    def initializePage(self, id):
        if id == 1:
            self.initClassPage()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
