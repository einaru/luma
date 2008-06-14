# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4.QtGui import *
from base.gui.BaseSelectorDesign import Ui_BaseSelectorDesign
from base.utils.gui.LumaErrorDialog import LumaErrorDialog


class BaseSelector(QDialog, Ui_BaseSelectorDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self)
        self.setupUi(self)
        
        self.baseList = []
        self.connection = None
        
###############################################################################

    def addBase(self):
        tmpBase = unicode(self.baseEdit.text()).strip()
        if tmpBase == u"":
            return
        if tmpBase in self.baseList:
            return
            
        self.baseList.append(tmpBase)
        self.baseList.sort()
        self.displayBase()
        
###############################################################################

    def deleteBase(self):
        for tmpItem in self.baseView.selectedItems():
            if not (None == tmpItem):
                baseName = unicode(tmpItem.text())
                self.baseList.remove(baseName)
                self.displayBase()
        
###############################################################################

    def addServerBase(self):
        success, serverBaseList, exceptionObject = self.connection.getBaseDNList()
        
        if success:
            for x in serverBaseList:
                if not (x in self.baseList):
                    self.baseList.append(x)
                    self.baseList.sort()
            self.displayBase()
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not retrieve baseDN.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
        
###############################################################################

    def displayBase(self):
        self.baseView.clear()
        for x in self.baseList:
            tmpItem = QListWidgetItem(x)
            self.baseView.addItem(tmpItem)
