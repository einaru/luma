# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *
from string import strip

from plugins.addressbook.CategoryEditDialogDesign import CategoryEditDialogDesign
from plugins.addressbook.NewCategoryDialog import NewCategoryDialog


class CategoryEditDialog(CategoryEditDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        CategoryEditDialogDesign.__init__(self,parent,name,modal,fl)

###############################################################################

    def setCategories(self, list):
        for x in list:
            item = QListViewItem(self.categoryView, x)
            self.categoryView.insertItem(item)

###############################################################################

    def getCategories(self):
        categoryList = []
        itemList = []
        
        curItem = self.categoryView.firstChild()
        if not (curItem == None):
            while not(curItem.itemBelow() == None):
                itemList.append(curItem)
                curItem = curItem.itemBelow()
            itemList.append(curItem)
            
        for x in itemList:
            categoryList.append(unicode(x.text(0)))
            
        return categoryList
        
        
###############################################################################

    def deleteCategory(self):
        selectedItem = self.categoryView.selectedItem()
        self.categoryView.takeItem(selectedItem)
        self.categoryView.setSelected(self.categoryView.firstChild(), 1)
        
###############################################################################

    def addCategory(self):
        dialog = NewCategoryDialog()
        dialog.exec_loop()
        
        if (dialog.result() == QDialog.Accepted):
            category = strip(unicode(dialog.categoryBox.currentText()))
            
            if not(category == ''):
                currentCategoryList = self.getCategories()
                
                if not(category in currentCategoryList):
                    item = QListViewItem(self.categoryView, category)
                    self.categoryView.insertItem(item)
        

        
        
        
        
        
        
        
        

