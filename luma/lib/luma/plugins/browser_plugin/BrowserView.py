# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *

from base.utils.gui.BrowserWidget import BrowserWidget
from base.utils.gui.AdvancedObjectWidget import AdvancedObjectWidget

class BrowserView(QWidget):

    def __init__(self, parent=None, name=None, fl=0):
        QWidget.__init__(self, parent, name, fl)

        self.setName("PLUGIN_BROWSER")

        self.splitter = QSplitter(self)
        self.mainLayout = QHBoxLayout(self)
        self.entryList = BrowserWidget(self.splitter)
        self.entryList.setMinimumWidth(200)
        self.entryView = AdvancedObjectWidget(self.splitter)
        self.connect (self.entryList, PYSIGNAL("ldap_result"), self.entryView.initView)
        self.connect (self.entryList, PYSIGNAL("about_to_change"), self.entryView.aboutToChange)
        self.connect (self.entryView, PYSIGNAL("REOPEN_PARENT"), self.entryList.reopenDN)
        self.mainLayout.addWidget(self.splitter)

###############################################################################

    def buildToolBar(self, parent):
        self.entryView.buildToolBar(parent)
