# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *

from base.utils.gui.SearchForm import SearchForm
from base.utils.gui.SearchResultView import SearchResultView

class SearchView(QWidget):

    def __init__(self, parent=None, name=None, fl=0):
        QWidget.__init__(self, parent, name, fl)

        self.vLayout = QVBoxLayout(self)

        self.searchForm = SearchForm(self)
        self.resultView = SearchResultView(self)

        self.vLayout.addWidget(self.searchForm)
        self.vLayout.addWidget(self.resultView)

        self.connect(self.searchForm, PYSIGNAL("ldap_result"), \
                self.resultView.setResult)
