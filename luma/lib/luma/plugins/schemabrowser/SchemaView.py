# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path
import string

import environment
from plugins.schemabrowser.SchemaViewDesign import SchemaViewDesign
from base.backend.ServerObject import ServerObject
from base.backend.ServerList import ServerList
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.utils.gui.LumaErrorDialog import LumaErrorDialog


class SchemaView(SchemaViewDesign):

    def __init__(self,parent = None,name = None,fl = 0):
        SchemaViewDesign.__init__(self,parent,name,fl)
        
        tmpFile  = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons", "secure.png")
        securePixmap = QPixmap(tmpFile)
        
        self.serverListObject = ServerList()
        self.serverListObject.readServerList()
        self.serverList = self.serverListObject.serverList
        
        self.currentServer = None
        
        if not (self.serverList == None):
            tmpDict = {}
            for x in self.serverList:
                if x.tls == 1:
                    tmpDict[x.name] = True
                else:
                    tmpDict[x.name] = False
                    
            self.serverBox.insertItem("")
            
            tmpList = tmpDict.keys()
            tmpList.sort()
            for x in tmpList:
                if tmpDict[x]:
                    self.serverBox.insertItem(securePixmap, x)
                else:
                    self.serverBox.insertItem(x)
                    
        self.schemaInfo = None
        self.classFilterString = ''
        self.attributeFilterString = ''
        self.syntaxFilterString = ''
        self.matchingFilterString = ''
        
        self.usageDict = {0: 'User Application', 1: "Directory Operation", 
            2: "Distributed Operation", 3:"DSA Operation"}
                    
###############################################################################

    def serverChanged(self, stringItem):
        # Clean all widgets from old entries
        self.clearClassWidget()
        self.clearAttributeWidget()
        self.clearSyntaxWidget()
        self.clearMatchingWidget()
        self.classBox.clear()
        self.attributeBox.clear()
        self.syntaxBox.clear()
        self.matchingBox.clear()
        
        
        
        serverString = unicode(stringItem)
        self.currentServer = self.serverListObject.getServerObject(serverString)
        self.schemaInfo = ObjectClassAttributeInfo(self.currentServer)
        
        if self.schemaInfo.failure:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not fetch schema information from server.<br><br>Reason: ")
            errorMsg.append(str(self.schemaInfo.failureException))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            return 
        
        # Init classes
        self.classList = self.schemaInfo.getObjectClasses()
        self.classList.sort()
        self.displayClassItems()
        
        # Init attributes
        self.attributeList = self.schemaInfo.getAttributeList()
        self.attributeList.sort()
        self.displayAttributeItems()
        
        # Init matching rules
        self.matchingList = self.schemaInfo.getMatchingRuleList()
        self.matchingList.sort()
        self.displayMatchingRuleItems()
        
        
        # Init syntaxes
        self.syntaxList = self.schemaInfo.getSyntaxList()
        self.syntaxList.sort()
        self.displaySyntaxItems()
        
###############################################################################

    def displayClassItems(self):
        self.classBox.clear()
        for x in self.classList:
            if '' == self.classFilterString:
                self.classBox.insertItem(x)
            elif self.classFilterString in string.lower(x):
                self.classBox.insertItem(x)
                
###############################################################################

    def displayAttributeItems(self):
        self.attributeBox.clear()
        for x in self.attributeList:
            if '' == self.attributeFilterString:
                self.attributeBox.insertItem(x)
            elif self.attributeFilterString in string.lower(x):
                self.attributeBox.insertItem(x)
                
###############################################################################

    def displaySyntaxItems(self):
        self.syntaxBox.clear()
        for x in self.syntaxList:
            if '' == self.syntaxFilterString:
                self.syntaxBox.insertItem(x)
            elif self.syntaxFilterString in string.lower(x):
                self.syntaxBox.insertItem(x)
                
###############################################################################

    def displayMatchingRuleItems(self):
        self.matchingBox.clear()
        for x in self.matchingList:
            if '' == self.matchingFilterString:
                self.matchingBox.insertItem(x)
            elif self.matchingFilterString in string.lower(x):
                self.matchingBox.insertItem(x)
    
        
###############################################################################

    def toolBoxChanged(self, pageId):
        self.widgetStack.raiseWidget(pageId)
            
###############################################################################

    def classSelected(self, tmpItem):
        className = str(tmpItem.text())
        classDataDict = self.schemaInfo.objectClassesDict[string.lower(className)]
        
        self.clearClassWidget()
        
        labelString = "<b>" + className + "</b><br>" + classDataDict['DESC']
        self.classLabel.setText(labelString)
        
        if len(classDataDict['PARENTS']) > 0:
            self.superiorClassEdit.setText(classDataDict['PARENTS'][0])
            
        self.oidClassEdit.setText(classDataDict['OID'])
        self.kindClassEdit.setText(classDataDict['KIND'])
        
        tmpTupel = classDataDict['MUST']
        tmpList = map(lambda x: x, tmpTupel)
        tmpList.sort()
        map(self.mustAttributeBox.insertItem, tmpList)
        
        tmpTupel = classDataDict['MAY']
        tmpList = map(lambda x: x, tmpTupel)
        tmpList.sort()
        map(self.mayAttributeBox.insertItem, tmpList)
        
###############################################################################

    def attributeSelected(self, tmpItem):
        attributeName = str(tmpItem.text())
        attributeDataDict = self.schemaInfo.attributeDict[string.lower(attributeName)]
        
        self.clearAttributeWidget()
        
        descString = attributeDataDict['DESC']
        
        if None == descString:
            labelString = "<b>" + attributeName + "</b><br>"
            self.attributeLabel.setText(labelString)
        else:
            labelString = "<b>" + attributeName + "</b><br>" + descString
            self.attributeLabel.setText(labelString)
        
        if len(attributeDataDict['SUP']) > 0:
            self.superiorAttributeEdit.setText(attributeDataDict['SUP'][0])
            
        self.oidAttributeEdit.setText(attributeDataDict['OID'])
        
        #print attributeDataDict['USAGE'], type(attributeDataDict['USAGE']
        usageValue = attributeDataDict['USAGE']
        self.usageAttributeEdit.setText(self.usageDict[usageValue])
        self.equalityAttributeEdit.setText(attributeDataDict['EQUALITY'])
        
        syntaxLen = attributeDataDict['SYNTAX_LEN']
        if None == syntaxLen:
            syntaxString = attributeDataDict['SYNTAX']
            self.syntaxAttributeEdit.setText(syntaxString)
        else:
            syntaxString = attributeDataDict['SYNTAX'] + "{" + str(syntaxLen) + "}"
            self.syntaxAttributeEdit.setText(syntaxString)
        
        self.orderingAttributeEdit.setText(attributeDataDict['ORDERING'])
        self.singleAttributeBox.setOn(attributeDataDict['SINGLE'])
        self.collectiveAttributeBox.setOn(attributeDataDict['COLLECTIVE'])
        self.obsoleteAttributeBox.setOn(attributeDataDict['OBSOLETE'])
        
        mustSet, maySet = self.schemaInfo.getAllObjectclassesForAttr(attributeName)
        tmpSet = mustSet.union(maySet)
        tmpList = map(lambda x: x, tmpSet)
        tmpList.sort()
        for x in tmpList:
            self.usedInClassBox.insertItem(x)
            
            
###############################################################################

    def syntaxSelected(self, tmpItem):
        syntaxName = str(tmpItem.text())
        syntaxDataDict = self.schemaInfo.syntaxDict[string.lower(syntaxName)]
        
        self.clearSyntaxWidget()
        
        descString = syntaxDataDict['DESC']
        
        if None == descString:
            labelString = "<b>" + syntaxName + "</b><br>"
            self.syntaxLabel.setText(labelString)
        else:
            labelString = "<b>" + syntaxName + "</b><br>" + descString
            self.syntaxLabel.setText(labelString)
            
        self.oidSyntaxEdit.setText(syntaxDataDict['OID'])
        
        attributeSyntaxList = self.schemaInfo.getAttributeListForSyntax(syntaxName)
        map(self.attributeSyntaxlistBox.insertItem, attributeSyntaxList)
        
        matchingSyntaxList = self.schemaInfo.getMachtingListForSyntax(syntaxName)
        map(self.matchingSyntaxBox.insertItem, matchingSyntaxList)
        
###############################################################################

    def matchingRuleSelected(self, tmpItem):
        matchingName = str(tmpItem.text())
        matchingDataDict = self.schemaInfo.matchingDict[string.lower(matchingName)]
        
        self.clearMatchingWidget()
        
        descString = matchingDataDict['DESC']
        
        if None == descString:
            labelString = "<b>" + matchingName + "</b><br>"
            self.matchingLabel.setText(labelString)
        else:
            labelString = "<b>" + matchingName + "</b><br>" + descString
            self.syntaxLabel.setText(labelString)
            
        self.oidMatchingEdit.setText(matchingDataDict['OID'])
        self.syntaxMatchingEdit.setText(matchingDataDict['SYNTAX'])
        
        attributeMatchingList = self.schemaInfo.getAttributeListForMatchingRule(matchingName)
        map(self.attributeMatchingBox.insertItem, attributeMatchingList)
        
###############################################################################


    def clearAttributeWidget(self):
        self.attributeLabel.setText(self.trUtf8("""<b>Attribute name</b><br>Description"""))
        self.superiorAttributeEdit.clear()
        self.oidAttributeEdit.clear()
        self.usageAttributeEdit.clear()
        self.equalityAttributeEdit.clear()
        self.syntaxAttributeEdit.clear()
        self.orderingAttributeEdit.clear()
        self.singleAttributeBox.setChecked(False)
        self.collectiveAttributeBox.setChecked(False)
        self.obsoleteAttributeBox.setChecked(False)
        self.usedInClassBox.clear()
            
###############################################################################

    def clearClassWidget(self):
        self.classLabel.setText(self.trUtf8("""<b>Class Name</b><br>Description"""))
        self.superiorClassEdit.clear()
        self.oidClassEdit.clear()
        self.kindClassEdit.clear()
        self.mustAttributeBox.clear()
        self.mayAttributeBox.clear()
            
###############################################################################

    def clearSyntaxWidget(self):
        self.syntaxLabel.setText(self.trUtf8("""<b>Syntax</b><br>Description"""))
        self.oidSyntaxEdit.clear()
        self.attributeSyntaxlistBox.clear()
        self.matchingSyntaxBox.clear()
        
###############################################################################

    def clearMatchingWidget(self):
        self.matchingLabel.setText(self.trUtf8("""<b>Matching rule</b><br>Description"""))
        self.oidMatchingEdit.clear()
        self.syntaxMatchingEdit.clear()
        self.attributeMatchingBox.clear()
        
###############################################################################

    def classFilterChanged(self, tmpString):
        tmpString = unicode(tmpString).encode("utf-8")
        self.classFilterString = string.lower(tmpString)
        self.displayClassItems()
        
###############################################################################

    def attributeFilterChanged(self, tmpString):
        tmpString = unicode(tmpString).encode("utf-8")
        self.attributeFilterString = string.lower(tmpString)
        self.displayAttributeItems()
        
###############################################################################

    def syntaxFilterChanged(self, tmpString):
        tmpString = unicode(tmpString).encode("utf-8")
        self.syntaxFilterString = string.lower(tmpString)
        self.displaySyntaxItems()
            
###############################################################################

    def matchingFilterChanged(self, tmpString):
        tmpString = unicode(tmpString).encode("utf-8")
        self.matchingFilterString = string.lower(tmpString)
        self.displayMatchingRuleItems()
            
            
###############################################################################

    def attributeDoubleClicked(self, boxItem):
        """ Raise the widget for attribute information when an attribute item 
        has been double-clicked somewhere in the schemabrowser.
        """
        
        self.toolBox.setCurrentItem(self.toolBox.item(1))
        tmpItem = self.attributeBox.findItem(str(boxItem.text()), Qt.ExactMatch)
        self.attributeBox.setSelected(tmpItem, True)
        self.attributeBox.centerCurrentItem()
        
###############################################################################
            
    def objectClassDoubleClicked(self, boxItem):
        """ Raise the widget for objectClass information when an objectClass item 
        has been double-clicked somewhere in the schemabrowser.
        """
        
        self.toolBox.setCurrentItem(self.toolBox.item(0))
        tmpItem = self.classBox.findItem(str(boxItem.text()), Qt.ExactMatch)
        self.classBox.setSelected(tmpItem, True)
        self.classBox.centerCurrentItem()
        
###############################################################################

    def matchingRuleDoubleClicked(self, boxItem):
        """ Raise the widget for matchingRule information when an matchingRule item 
        has been double-clicked somewhere in the schemabrowser.
        """
        
        self.toolBox.setCurrentItem(self.toolBox.item(2))
        tmpItem = self.matchingBox.findItem(str(boxItem.text()), Qt.ExactMatch)
        self.matchingBox.setSelected(tmpItem, True)
        self.matchingBox.centerCurrentItem()
            
            
            
            
            
            
            
            
            
