'''
Created on 15. mars 2011

@author: Simen
'''

from PyQt4.QtGui import QWidget, QDataWidgetMapper, QItemSelectionModel
from PyQt4.QtGui import QInputDialog, QMessageBox
from PyQt4.QtCore import QModelIndex
from .TemplateWidgetDesign import Ui_TemplateWidget
from .AddAttributeDialog import AddAttributeDialog
from .AddObjectclassDialog import AddObjectclassDialog
from ..TemplateList import TemplateList
from ..TemplateDelegate import TemplateDelegate
from ..TemplateObject import TemplateObject
from ..model.TemplateTableModel import TemplateTableModel
from ..model.ObjectclassTableModel import ObjectclassTableModel
from ..model.AttributeTableModel import AttributeTableModel

import copy

class TemplateWidget(QWidget, Ui_TemplateWidget):
    
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        
        templateList = TemplateList()
        self._templateList = copy.deepcopy(templateList)
        self._templateListCopy = None
        self._returnList = None
        
        self.templateTM = TemplateTableModel(self._templateList)
        self.listViewTemplates.setModel(self.templateTM)
        
        self.objectclassTM = ObjectclassTableModel(self._templateList) 
        self.tableViewObjectclasses.setModel(self.objectclassTM)
        
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
        
#        self.connect(self.serverListView.selectionModel(),  QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'), self.setBaseDN)

        # Map columns of the model to fields in the gui
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.templateTM)
        # Handles the comboboxes and to-from the list of custom baseDNs
        self.templateDelegate = TemplateDelegate()
        self.mapper.setItemDelegate(self.templateDelegate) 
        
        self.mapper.addMapping(self.lineEditName, 0)
        self.mapper.addMapping(self.lineEditServer, 1)
        self.mapper.addMapping(self.lineEditDescription, 2)

        #self.mapper.addMapping(self.baseDNWidget, 5)

        # Select the first servers (as the serverlistview does)
        self.mapper.setCurrentIndex(0)
#        
#        # Let the mapper know when another server is selected in the list
        self.listViewTemplates.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex)
#        
#        # Workaround to avoid the button stealing the focus from the baseDNView thus invalidating it's selection
#        # maning we don't know what do delete
#        #self.deleteBaseDNButton.setFocusPolicy(Qt.NoFocus)
#        self.setBaseDN()

    def setRightSideEnabled(self, enabled):
        self.lineEditName.setEnabled(enabled)
        self.lineEditServer.setEnabled(enabled)
        self.lineEditDescription.setEnabled(enabled)
        self.groupBoxObjectclasses.setEnabled(enabled)
        self.groupBoxAttributes.setEnabled(enabled)
        
    def clearAll(self):
        self.lineEditName.clear()
        self.lineEditServer.clear()
        self.lineEditDescription.clear()
        self.tableViewObjectclasses.model().reset()
        self.tableViewAttributes.model().reset()

    def addTemplate(self):
        name, ok = QInputDialog.getText(self, 'Add server', 'Name:')
        if ok:
            if len(name) < 1 or self._templateList.getTemplateObject(name) != None:
                QMessageBox.information(self, 'Error', "Invalid name or already used.")
                return
            
            tO = TemplateObject()
            tO.templateName = unicode(name)
            
            m = self.listViewTemplates.model()
            m.beginInsertRows(QModelIndex(), m.rowCount(), m.rowCount()+1)
            m.addRow(tO)
            m.endInsertRows()
            
            s = m.index(m.rowCount()-1,0)
            self.listViewTemplates.selectionModel().select(s, QItemSelectionModel.ClearAndSelect)
            self.listViewTemplates.selectionModel().setCurrentIndex(s, QItemSelectionModel.ClearAndSelect) #Mark it as current
            self.mapper.setCurrentIndex(s.row())
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
        for i in self.templateTM._templateList.getTable(): 
            print i
    
    def saveTemplate(self):
        self._templateList.save()
        
    def addObjectclass(self):
        dialog = AddObjectclassDialog()
        dialog.exec_()
        
    def deleteObjectclass(self):
        pass
        
    def addAttribute(self):
        dialog = AddAttributeDialog()
        dialog.exec_()
        
    def deleteAttribute(self):
        pass