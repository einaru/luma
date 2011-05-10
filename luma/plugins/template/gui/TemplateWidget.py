'''
Created on 15. mars 2011

@author: Simen
'''

from PyQt4.QtGui import QWidget, QDataWidgetMapper, QItemSelectionModel
from PyQt4.QtGui import QInputDialog, QMessageBox, QStyledItemDelegate
from PyQt4.QtGui import QHeaderView
from PyQt4 import QtCore
from PyQt4.QtCore import QModelIndex

from base.backend.ServerList import ServerList
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo

from .TemplateWidgetDesign import Ui_TemplateWidget
from .AddAttributeDialog import AddAttributeDialog
from .AddObjectclassDialog import AddObjectclassDialog
from .AddTemplateDialog import AddTemplateDialog
from .DeleteObjectclassDialog import DeleteObjectclassDialog
from ..TemplateList import TemplateList
from ..TemplateObject import TemplateObject
from ..model.TemplateTableModel import TemplateTableModel
from ..model.ObjectclassTableModel import ObjectclassTableModel
from ..model.AttributeTableModel import AttributeTableModel

import copy
from PyQt4.uic.Compiler.qtproxies import QtGui

class TemplateWidget(QWidget, Ui_TemplateWidget):
    
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        
        self._serverList = ServerList()
        
        templateList = TemplateList()
        self._templateList = copy.deepcopy(templateList)
        self._templateListCopy = None
        self._returnList = None
        
        #ObjectclassAttributeInfo
        self.preloadedServerMeta = {}
        
        self.templateTM = TemplateTableModel(self._templateList, self)
        self.listViewTemplates.setModel(self.templateTM)
        
        self.objectclassTM = ObjectclassTableModel(self) 
        self.listViewObjectclasses.setModel(self.objectclassTM)
        
        self.attributeTM = AttributeTableModel(self)
        self.tableViewAttributes.setModel(self.attributeTM)

        # Enable/disable editing depending on if we have a server to edit
        if self.templateTM.rowCount(QModelIndex()) > 0:
            self.setRightSideEnabled(True)
        else:
            self.setRightSideEnabled(False)
        # Select the first template in the model)
        index = self.templateTM.index(0,0)
        # Select the template in the view
        self.listViewTemplates.selectionModel().select(index, QItemSelectionModel.ClearAndSelect) 
        self.listViewTemplates.selectionModel().setCurrentIndex(index, QItemSelectionModel.ClearAndSelect)
        self.listViewTemplates.selectionModel().selectionChanged.connect(self.selectedTemplate)
        # Map columns of the model to fields in the gui
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.templateTM)
        self.mapper.addMapping(self.lineEditDescription, 2)
        # Set-up of the non-mapped information  
        self.selectedTemplate()
        
    def selectedTemplate(self):
        index = self.listViewTemplates.selectionModel().currentIndex().row()
        if index >= 0:
            self.mapper.setCurrentIndex(index)
            
            server = self._templateList._templateList[index].server
            self.labelServerName.setText(server)
            self.loadServerMeta(server)
            
            self.setObjectclasses()
            self.setAttributes()
            self.tableViewAttributes.resizeColumnsToContents()
            self.tableViewAttributes.resizeRowsToContents()

    def setObjectclasses(self):
        templateObject = self.getSelectedTemplateObject()
        if templateObject:
            self.objectclassTM.setTemplateObject(templateObject)
            
            
    def setAttributes(self):
        templateObject = self.getSelectedTemplateObject()
        if templateObject:
            self.attributeTM.setTemplateObject(templateObject)
            
    def loadServerMeta(self, serverName):
        serverName = unicode(serverName)
        if not (serverName in self.preloadedServerMeta.keys()):
            serverMeta = self._serverList.getServerObject(serverName)
            self.preloadedServerMeta[serverName] = ObjectClassAttributeInfo(serverMeta)
        return self.preloadedServerMeta[serverName]
    
    def setRightSideEnabled(self, enabled):
        self.lineEditDescription.setEnabled(enabled)
        self.groupBoxObjectclasses.setEnabled(enabled)
        self.groupBoxAttributes.setEnabled(enabled)
        
    def clearAll(self):
        self.lineEditDescription.clear()
        self.labelServerName.clear()
        self.objectclassTM.setTemplateObject(None)
        self.attributeTM.setTemplateObject(None)

    def getSelectedTemplateObject(self):
        templateIndexes = self.listViewTemplates.selectedIndexes()
        if len(templateIndexes) > 0:
            return self._templateList.getTable()[templateIndexes[0].row()]
        return None
    
    def getSelectedObjectclass(self, index):
        return self.objectclassTM.getObjectclass(index)

    def getSelectedAttribute(self, index):
        return self.attributeTM.getAttribute(index)
        
    def addTemplate(self):
        dialog = AddTemplateDialog(self._serverList)
        if dialog.exec_():
            name = dialog.lineEditTemplateName.text()
            if len(name) < 1 or self._templateList.getTemplateObject(name) != None:
                QMessageBox.information(self, 'Error', "Invalid name or already used.")
                return
            server = dialog.comboBoxServer.currentText()
            if len(server) < 1:
                QMessageBox.information(self, 'Error', "Invalid server.")
                return
            description = dialog.lineEditDescription.text()
            tO = TemplateObject(name, server, description)
            
            m = self.templateTM
            m.beginInsertRows(QModelIndex(), m.rowCount(), m.rowCount())
            m.insertRow(tO)
            m.endInsertRows()
            
            i = m.index(m.rowCount()-1,0)
            self.listViewTemplates.selectionModel().select(i, QItemSelectionModel.ClearAndSelect)
            self.listViewTemplates.selectionModel().setCurrentIndex(i, QItemSelectionModel.ClearAndSelect) #Mark it as current
            self.mapper.setCurrentIndex(i.row())
            self.selectedTemplate()
            if i.row() == 0:
                self.setRightSideEnabled(True)

        
    def deleteTemplate(self):
        if self.listViewTemplates.selectionModel().currentIndex().row() < 0:
            return
        
        re = QMessageBox.question(self, "Delete", "Are you sure?", QMessageBox.Yes, QMessageBox.No)
        
        if re == QMessageBox.Yes:
            index = self.listViewTemplates.selectedIndexes()[0] #Currently selected
            
            # Delete the template
            self.listViewTemplates.model().removeRow(index)
            
            # When deleting, the view gets updated and selects a new current.
            # Get it and give it to the mapper
            newIndex = self.listViewTemplates.selectionModel().currentIndex()
            self.mapper.setCurrentIndex(newIndex.row())
        
        # Disable editing if no templates left
        if self.templateTM.rowCount() == 0:
            self.setRightSideEnabled(False)
            self.clearAll()
    
    def duplicateTemplate(self):
        name, ok = QInputDialog.getText(self, 'Duplicate', 'Template name')
        if ok:
            if len(name) < 1 or self._templateList.getTemplateObject(name) != None:
                QMessageBox.information(self, 'Error', "Invalid name or already used.")
                return
            tO = copy.deepcopy(self.getSelectedTemplateObject())
            tO.templateName = name
    
            m = self.listViewTemplates.model()
            m.insertRow(tO)
            i = m.index(m.rowCount()-1,0)
            self.listViewTemplates.selectionModel().select(i, QItemSelectionModel.ClearAndSelect)
            self.listViewTemplates.selectionModel().setCurrentIndex(i, QItemSelectionModel.ClearAndSelect) #Mark it as current
            self.mapper.setCurrentIndex(i.row())
            self.selectedTemplate()

    def saveTemplate(self):
        self._templateList.save()

    def addObjectclass(self):
        server = self.labelServerName.text()
        dialog = AddObjectclassDialog(self.loadServerMeta(server), self.getSelectedTemplateObject())
        if dialog.exec_():
            for i in dialog.listWidgetObjectclasses.selectedIndexes():
                item = dialog.listWidgetObjectclasses.itemFromIndex(i)
                self.objectclassTM.insertRow(str(item.text()))
                
        self.refreshMustAttributes()

    def deleteObjectclass(self):
        dOc = self.listViewObjectclasses.selectedIndexes()
        if dOc:
            server = self.labelServerName.text()
            tO = self.getSelectedTemplateObject()
            attributes = self.attributeTM.attributes
            dialog = DeleteObjectclassDialog(self.loadServerMeta(server), tO, dOc, attributes)
            if dialog.exec_():
                self.objectclassTM.removeRows(dOc)
                self.refreshAllAttributes()
        
    
    def refreshMustAttributes(self):
        tO = self.getSelectedTemplateObject()
        for attr in tO.attributes.values():
            if attr.must:
                self.attributeTM.removeAlways(attr)
                
        
        server = self.labelServerName.text()
        ocai = self.loadServerMeta(server)
        attributeNameList = ocai.getAllMusts(tO.objectclasses)
        for name in attributeNameList:
            single = ocai.isSingle(name)
            binary = ocai.isBinary(name)
            self.attributeTM.addRow(name, True, single, binary, "", False)
            
    def refreshAllAttributes(self):
        tO = self.getSelectedTemplateObject()
        server = self.labelServerName.text()
        ocai = self.loadServerMeta(server)
        must, may = ocai.getAllAttributes(tO.objectclasses)
        for attr in tO.attributes.items():
            if (not attr[0] in must) and (not attr[0] in may):
                self.attributeTM.removeAlways(attr[1])
            elif not attr[0] in must:
                attr[1].must = False

    def addAttribute(self):
        server = self.labelServerName.text()
        dialog = AddAttributeDialog(self.loadServerMeta(server), self.getSelectedTemplateObject())
        if dialog.exec_():
            for i in dialog.tableView.selectedIndexes():
                if(i.column() == 0):
                    a = dialog.attributeTM.getAttribute(i)
                    self.attributeTM.addRow(a.attributeName, a.must, a.single, a.binary, a.defaultValue, a.customMust)
                    
        self.tableViewAttributes.resizeRowsToContents()
        self.tableViewAttributes.resizeColumnsToContents()

    def deleteAttributes(self):
        if len(self.tableViewAttributes.selectedIndexes()):
            re = QMessageBox.question(self, self.tr('Delete'),
                                      self.tr("Are you sure you want to delete the selected attributes?"), QMessageBox.Yes, QMessageBox.No)
            if re == QMessageBox.Yes:
                self.attributeTM.removeRows(self.tableViewAttributes.selectedIndexes())

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
