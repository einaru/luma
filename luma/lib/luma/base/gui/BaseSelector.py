# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
from base.gui.BaseSelectorDesign import BaseSelectorDesign


class BaseSelector(BaseSelectorDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        BaseSelectorDesign.__init__(self,parent,name,modal,fl)
        
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
        tmpItem = self.baseView.selectedItem()
        if not (None == tmpItem):
            baseName = unicode(tmpItem.text(0))
            self.baseList.remove(baseName)
            self.displayBase()
        
###############################################################################

    def addServerBase(self):
        serverBaseList = self.connection.getBaseDNList()
        for x in serverBaseList:
            if not (x in self.baseList):
                self.baseList.append(x)
                self.baseList.sort()
        self.displayBase()
        
###############################################################################

    def displayBase(self):
        self.baseView.clear()
        for x in self.baseList:
            tmpItem = QListViewItem(self.baseView, x)
