###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *
from plugins.admin_utils.AdminPanelDesign import AdminPanelDesign
from base.utils.backend.CryptPwGenerator import CryptPwGenerator
from base.utils.backend.DateHelper import DateHelper


class AdminPanel(AdminPanelDesign):

###############################################################################

    def __init__(self,parent = None,name = None,fl = 0):
        AdminPanelDesign.__init__(self,parent,name,fl)
        
        self.pwHandler = CryptPwGenerator()
        self.dateHandler = DateHelper()
        
###############################################################################

    def create_random(self):
        password, cryptPw = self.pwHandler.get_random_password()
        self.randomPwEdit.setText(password)
        self.randomCryptEdit.setText(cryptPw)
        
###############################################################################

    def crypt_password(self):
        tmpPassword = str(self.pwEdit.text())
        self.cryptEdit.setText(self.pwHandler.encrypt_password(tmpPassword)[1])
        
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
        
        
        
        
        
        
