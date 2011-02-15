#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PluginLoaderDesign import Ui_PluginLoader
import sys
from random import randint

class PluginLoader(QDialog, Ui_PluginLoader):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self._model = PluginsModel()
        self.listView.setModel(self._model)
        
        for n in range(10):
            item = QStandardItem('Item %s' % randint(1, 100))
            check = Qt.Checked if randint(0, 1) == 1 else Qt.Unchecked
            item.setCheckState(check)
            item.setCheckable(True)
            item.setEditable(False)
            item.pluginObject = "A"
            self._model.appendRow(item)

###############################################################################

    def pluginSelected(self, index):
        """
        Whenever a plugin is selected, the groupbox should be filled
        with a widget from the plugin for its settings.
        If no such widget is made for the plugin, the box will be empty.
        """
        plugin = self._model.itemFromIndex(index)
        print plugin.pluginObject
        pass
    
###############################################################################
        
    def close(self):
        pass

###############################################################################
    
    def closeButton(self):
        pass


###############################################################################
                
class PluginsModel(QStandardItemModel):
    def __init__(self, parent = None):
        QStandardItemModel.__init__(self, parent)
        self.pluginObject = None
        
###############################################################################
    
def main():
    app = QApplication(sys.argv)
    pluginloader = PluginLoader()
    pluginloader.show()
    app.exec_()

###############################################################################

if __name__ == '__main__':
    main()    

###############################################################################