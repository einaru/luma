# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *
import os.path

import environment
from plugins.admin_utils.AdminPanelDesign import AdminPanelDesign
from base.utils.backend.CryptPwGenerator import CryptPwGenerator
from base.utils.backend.DateHelper import DateHelper
from base.utils.backend.mkpasswd import mkpasswd

class AdminPanel(AdminPanelDesign):

###############################################################################

    def __init__(self,parent = None,name = None,fl = 0):
        AdminPanelDesign.__init__(self,parent,name,fl)
        
        iconDir = os.path.join (environment.lumaInstallationPrefix, "lib", "luma", "plugins", "admin_utils", "icons")
        secureIcon = QPixmap (os.path.join (iconDir, "secure.png"))
        dateIcon = QPixmap (os.path.join (iconDir, "date.png"))
        
        self.secureLabel.setPixmap (secureIcon)
        self.dateLabel.setPixmap (dateIcon)
        
        self.pwHandler = CryptPwGenerator()
        self.dateHandler = DateHelper()
        
###############################################################################

    def create_random(self):
        #password, cryptPw = self.pwHandler.get_random_password()
        #self.randomPwEdit.setText(password)
        #self.randomCryptEdit.setText(cryptPw)
        
        tmpPassword = self.pwHandler.create_random_string(8)
        self.randomPwEdit.setText(tmpPassword)
        method = str(self.methodBox.currentText())
        password = mkpasswd(tmpPassword, 3, method)
        self.randomCryptEdit.setText(password)
        
###############################################################################

    def crypt_password(self):
        tmpPassword = str(self.pwEdit.text())
        method = str(self.methodBox.currentText())
        password = mkpasswd(tmpPassword, 3, method)
        self.cryptEdit.setText(password)
        
###############################################################################

    def convert_date(self):
        tmpDate = self.dateEdit.date()
        year = tmpDate.year()
        month = tmpDate.month()
        day = tmpDate.day()
        tmpDays = self.dateHandler.date_to_unix(year, month, day)
        self.convDateEdit.setText(str(tmpDays))
        
###############################################################################

    def convert_duration(self):
        tmpValue = self.durationBox.value()
        tmpDays = self.dateHandler.dateduration_to_unix(tmpValue)
        self.convDurationEdit.setText(str(tmpDays))
        
        
        
        
        
        
