# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import ldap
from qt import *
from base.utils.gui.BrowserWidget import BrowserWidget

class BrowserDialog(QDialog):
    """ A dialog for browsing available ldap server.
    """
    
    def __init__(self,parent = None,name = None,fl = 0):
        QDialog.__init__(self,parent,name,fl)
    
        self.setCaption("LDAP Browser")
        
        tmpLayout = QVBoxLayout(self)
        
        self.hWidget = QWidget(self)
        hLayout = QHBoxLayout(self.hWidget)
        hLayout.setMargin(5)
        
        self.okButton = QPushButton(self.hWidget)
        self.okButton.setText(self.trUtf8("Ok"))
        
        self.cancelButton = QPushButton(self.hWidget)
        self.cancelButton.setText(self.trUtf8("Cancel"))
        
        hLayout.addWidget(self.cancelButton)
        spacer = QSpacerItem(100,21,QSizePolicy.Preferred,QSizePolicy.Minimum)
        hLayout.addItem(spacer)
        hLayout.addWidget(self.okButton)
        
        self.tmpBrowser = BrowserWidget(self)
        
        tmpLayout.addWidget(self.tmpBrowser)
        tmpLayout.addWidget(self.hWidget)
    
        
        self.connect(self.okButton, SIGNAL("clicked()"), self.checkInput)
        self.connect(self.cancelButton, SIGNAL("clicked()"), self.cancel)
        
        #self.tmpBrowser.setMinimumWidth(500)
        self.exec_loop()
        

###############################################################################

    def getItemPath(self):
        """ Return the path of the selected item.
        """
        
        tmpItem = self.tmpBrowser.selectedItem()
        tmpText = self.tmpBrowser.get_full_path(tmpItem)
        return tmpText
            
###############################################################################

    def getLdapItem(self):
        """ Return ldap data of the selected item.
        """  
        tmpItem = self.tmpBrowser.selectedItem()
        tmpText = self.tmpBrowser.get_full_path(tmpItem)
        return self.tmpBrowser.getLdapItem(tmpText)
        
###############################################################################

    def checkInput(self):
        """ Check if a valid ldap object is selected and then close the dialog.
        """
        
        tmpItem = self.tmpBrowser.selectedItem()
        if tmpItem == None:
            pass
        else:
            tmpText = self.tmpBrowser.get_full_path(tmpItem)
            if len(tmpText.split(',')) > 1:
                self.accept()
        
###############################################################################

    def cancel(self):
        """ Close the dialog by calling reject().
        """
        
        self.reject()
        
        
        
