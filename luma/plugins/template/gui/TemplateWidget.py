'''
Created on 15. mars 2011

@author: Simen
'''

from PyQt4.QtGui import QWidget, QDataWidgetMapper, QItemSelectionModel
from PyQt4.QtGui import QInputDialog, QMessageBox, QStyledItemDelegate
from PyQt4 import QtCore
from PyQt4.QtCore import QModelIndex
from base.backend.ServerList import ServerList
from .TemplateWidgetDesign import Ui_TemplateWidget
from .AddAttributeDialog import AddAttributeDialog
from .AddObjectclassDialog import AddObjectclassDialog
from .AddTemplateDialog import AddTemplateDialog
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
        
        self.templateTM = TemplateTableModel(self._templateList)
        self.listViewTemplates.setModel(self.templateTM)
        
        self.objectclassTM = ObjectclassTableModel(self._templateList) 
        self.listViewObjectclasses.setModel(self.objectclassTM)
        
        self.attributeTM = AttributeTableModel(self._templateList)
        self.tableViewAttributes.setModel(self.attributeTM)

        # Enable/disable editing depending on if we have a server to edit
        if self.templateTM.rowCount(QModelIndex()) > 0:
            self.setRightSideEnabled(True)
        else:
            self.setRightSideEnabled(False)


        # Select the first server in the model)
        index = self.listViewTemplates.model().index(0,0)
        # Select it in the view
        self.listViewTemplates.selectionModel().select(index, QItemSelectionModel.ClearAndSelect) 
        self.listViewTemplates.selectionModel().setCurrentIndex(index, QItemSelectionModel.ClearAndSelect)
        
        self.listViewTemplates.selectionModel().selectionChanged.connect(self.selectedTemplate)
        
        # Map columns of the model to fields in the gui
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.templateTM)
        
        
        
        self.mapper.addMapping(self.lineEditDescription, 2)


        # Select the first servers (as the serverlistview does)
        self.selectedTemplate()

    def selectedTemplate(self):
        index = self.listViewTemplates.selectionModel().currentIndex().row()
        if index >= 0:
            self.mapper.setCurrentIndex(index)
            self.labelServerName.setText(self._templateList._templateList[index].server)
            self.setObjectclasses()
            self.setAttributes()

    def setObjectclasses(self):
        templateObject = self.getSelectedTemplateObject()
        if templateObject:
            self.listViewObjectclasses.model().setTemplateObject(templateObject)
            
            
    def setAttributes(self):
        templateObject = self.getSelectedTemplateObject()
        if templateObject:
            self.tableViewAttributes.model().setTemplateObject(templateObject)
            
            
    def setRightSideEnabled(self, enabled):
        self.lineEditDescription.setEnabled(enabled)
        self.groupBoxObjectclasses.setEnabled(enabled)
        self.groupBoxAttributes.setEnabled(enabled)
        
    def clearAll(self):
        self.lineEditDescription.clear()
        self.labelServerName.clear()
        self.listViewObjectclasses.model().setTemplateObject(None)
        self.tableViewAttributes.model().setTemplateObject(None)

    def getSelectedTemplateObject(self):
        templateIndexes = self.listViewTemplates.selectedIndexes()
        if len(templateIndexes) > 0:
            return self._templateList.getTable()[templateIndexes[0].row()]
        return None
    
    def getSelectedObjectclass(self, index):
        return self.listViewObjectclasses.model().getObjectclass(index)

    def getSelectedAttribute(self, index):
        return self.tableViewAttributes.model().getAttribute(index)
        
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
            
            m = self.listViewTemplates.model()
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
            index = self.listViewTemplates.selectionModel().currentIndex() #Currently selected
            
            # Delete the template
            self.listViewTemplates.model().beginRemoveRows(QModelIndex(), index.row(), index.row())
            self.listViewTemplates.model().removeRow(index.row())
            self.listViewTemplates.model().endRemoveRows()
            
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
        if len(name) < 1 or self._templateList.getTemplateObject(name) != None:
            QMessageBox.information(self, 'Error', "Invalid name or already used.")
            return
        tO = copy.deepcopy(self.getSelectedTemplateObject())
        tO.templateName = name

        m = self.listViewTemplates.model()
        m.beginInsertRows(QModelIndex(), m.rowCount(), m.rowCount())
        m.insertRow(tO)
        m.endInsertRows()

        i = m.index(m.rowCount()-1,0)
        self.listViewTemplates.selectionModel().select(i, QItemSelectionModel.ClearAndSelect)
        self.listViewTemplates.selectionModel().setCurrentIndex(i, QItemSelectionModel.ClearAndSelect) #Mark it as current
        self.mapper.setCurrentIndex(i.row())
        self.selectedTemplate()
    
    def saveTemplate(self):
        self._templateList.save()
        
    def addObjectclass(self):
        dialog = AddObjectclassDialog()
        dialog.exec_()
        
    def deleteObjectclass(self):
        pass
#        for i in self.listViewObjectclasses.selectedIndexes():
#            objectclass = self.getSelectedObjectclass(i)
#            self.objectclassTM.beginRemoveColumns(QModelIndex(), i.row(), i.row())
#            self.objectclassTM.removeRow(objectclass)
#            self.objectclassTM.endRemoveRows()
        
    def addAttribute(self):
        dialog = AddAttributeDialog()
        dialog.exec_()
        
    def deleteAttribute(self):
        for i in self.tableViewAttributes.selectedIndexes(): 
            print i
#        rows = []
#        self.attributeTM.beginRemoveColumns(QModelIndex(), 0, self.getSelectedTemplateObject().getCountAttributes())
#        for i in self.tableViewAttributes.selectedIndexes():
#            if not i.row() in rows:
#                rows.append(i.row())
#                attribute = self.getSelectedAttribute(i)
#                self.attributeTM.removeRow(attribute)
#        
#        self.attributeTM.endRemoveRows()