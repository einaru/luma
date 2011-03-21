# -*- coding: utf-8 -*-
#
# base.gui.ServerDialog
#
# Copyright (c) 2011
#     Christian Forfang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

from PyQt4.QtGui import QStyledItemDelegate, QListWidgetItem
from PyQt4.QtCore import QVariant, Qt

class ServerDelegate(QStyledItemDelegate):
    """ Maps QComboBoxes with set content (descriptions) to the model
    (ints), as well as populating a QListView with strings from a list
    (baseDNs).
    """
    
    def __init__(self):
        QStyledItemDelegate.__init__(self)
        
    def setEditorData(self, editor, index):
        """ Specifies how the given editor should be filled out with
        the data from the model (at the index)
        """
        
        if not index.isValid():
            return
        
        # if BaseDNs
        if index.column() == 5:
                        
            # List of strings
            d = index.data().toPyObject()
            
            ## Get rid of empty strings
            #newList = []
            #for x in d:
            #    x = x.trimmed() #QString
            #    if not len(x) == 0:
            #        newList.append(unicode(x)) 
            #
            ## the view (editor) is a QListView in this case,
            ## so lets give it a model to display
            #if editor.model() == None:
            #    editor.setModel(QStringListModel(newList))
            #    return
            #m = editor.model()
            #m.setStringList(QStringList(newList))

            editor.clear()
            for tmpBase in d:
                # The editor is the items parent, so it gets added to the list
                QListWidgetItem(tmpBase, editor)
                # Can also do this
                #editor.addItem(QListWidgetItem(tmpBase))
            return
        
        # if QComboBox, just set the index it should display (the strings displayed is in the .ui-file)
        if editor.property("currentIndex").isValid(): #QComboBoxes has currentIndex
            editor.setProperty("currentIndex", index.data()) # just give it the data (the int)
            return
        
        # else - default
        QStyledItemDelegate.setEditorData(self, editor, index) #if not, do as you always do
        
    def setModelData(self, editor, model, index):
        """ Specifies how the model should be filled out with data from
        the editor
        """
    
        # if the baseDNs
        if index.column() == 5:
                    
            ## get strings from the model of the QListView displaying
            ## the baseDNs
            #m = editor.model()
            #
            ## Populate the list again
            #d = []
            #for i in xrange(m.rowCount()):
            #    data = m.data(m.index(i,0), Qt.DisplayRole)
            #    d.append(data)
            #
            #m = editor.model()
            returnList = []
            for i in xrange(editor.count()):
                returnList.append(editor.item(i).data(Qt.DisplayRole).toPyObject())
                #returnList.append(m.data(m.index(i,0)).toPyObject())

            # now that we have constructed the list, give it to the model
            model.setData(index,QVariant(returnList))
            return 
        
        # if a combobox, get the index and give it to the model
        value = editor.property("currentIndex")
        if value.isValid():
            model.setData(index, value)
            return
        
        # else - default
        QStyledItemDelegate.setModelData(self, editor, model, index)
        