# -*- coding: <utf-8> -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <wido.depping@tu-clausthal.de>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *

from plugins.addressbook.AddressbookWidget import AddressbookWidget

class AddressbookView(QWidget):

    def __init__(self, parent=None, name=None, fl=0):
        QWidget.__init__(self, parent, name, fl)

        #self.setName("PLUGIN_BROWSER")

        self.splitter = QSplitter(self)
        self.mainLayout = QHBoxLayout(self)
        self.entryList = BrowserWidget(self.splitter)
        self.entryList.setMinimumWidth(200)
        self.entryView = ObjectWidget(self.splitter)
        self.connect (self.entryList, PYSIGNAL("ldap_result"), self.entryView.init_view)
        self.mainLayout.addWidget(self.splitter)
