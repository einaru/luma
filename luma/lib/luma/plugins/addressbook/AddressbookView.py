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
from base.utils.gui.LumaIconView import LumaIconView

class AddressbookView(QWidget):

    def __init__(self, parent=None, name=None, fl=0):
        QWidget.__init__(self, parent, name, fl)

        #self.setName("PLUGIN_BROWSER")

        self.splitter = QSplitter(self)
        self.mainLayout = QHBoxLayout(self)
        self.entryList = LumaIconView(self.splitter)
        self.entryList.setMinimumWidth(200)
        self.addressBookWidget = AddressbookWidget(self.splitter)
        self.connect (self.entryList, PYSIGNAL("ldap_result"), self.addressBookWidget.init_view)
        self.connect(self.entryList, PYSIGNAL("server_changed"), self.addressBookWidget.serverChanged)
        self.mainLayout.addWidget(self.splitter)
