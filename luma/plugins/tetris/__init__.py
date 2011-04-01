# -*- coding: utf-8 -*-

import os

from PyQt4 import QtGui
from PyQt4 import QtCore
from .Tetris import Tetris


lumaPlugin = True
pluginName = "Tetris"
pluginUserString = "Tetris"
version = "0.2"
author = "Per Ove"

def getIcon():
    return QtGui.QIcon(':/icons/luma-256')
    

def getPluginWidget(parent, mainwin):
    widget = Tetris()
    return widget
    

def getPluginSettingsWidget(parent):
    widget = Tetris()
    return widget
    

def postprocess():
    return

class Example(QtGui.QWidget):
    
    def changeEvent(self, e):
        if e.type() == QtCore.QEvent.LanguageChange:
            print "lolr"
        else:
            QtGui.QWidget.changeEvent(self, e)
            
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.initUI()


    def initUI(self):

        self.label = QtGui.QLabel(self)
        edit = QtGui.QLineEdit(self)
        
        edit.move(60, 100)
        self.label.move(60, 40)

        self.connect(edit, QtCore.SIGNAL('textChanged(QString)'), 
            self.onChanged)

        self.setWindowTitle('QLineEdit')
        self.setGeometry(250, 200, 350, 250)
        

    def onChanged(self, text):
        self.label.setText(text)
        self.label.adjustSize()



