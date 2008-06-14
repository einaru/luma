# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from PyQt4 import QtCore
from PyQt4.QtGui import *

from base.utils.gui.BrowserWidget import BrowserWidget
#from base.utils.gui.AdvancedObjectWidget import AdvancedObjectWidget

class BrowserView(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setObjectName("PLUGIN_BROWSER")

        self.splitter = QSplitter(self)
        self.mainLayout = QHBoxLayout(self)
        self.entryList = BrowserWidget(self.splitter)
        self.entryList.setMinimumWidth(200)
        # FIXME: qt4 migration needed
        #self.entryView = AdvancedObjectWidget(self.splitter)
        self.entryView = QWidget(self.splitter)
        #self.connect(self.entryList, QtCore.SIGNAL("ldap_result"), self.entryView.initView)
        #self.connect(self.entryList, QtCore.SIGNAL("about_to_change"), self.entryView.aboutToChange)
        #self.connect(self.entryView, QtCore.SIGNAL("REOPEN_PARENT"), self.entryList.reopenDN)
        #self.connect(self.entryList, QtCore.SIGNAL("ADD_ATTRIBUTE"), self.entryView.addAttribute)
        self.mainLayout.addWidget(self.splitter)

###############################################################################

    def buildToolBar(self, parent):
        self.entryView.buildToolBar(parent)
