# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# Luma is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public Licence as published by 
# the Free Software Foundation; either version 2 of the Licence, or 
# (at your option) any later version.
#
# Luma is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence 
# for more details.
#
# You should have received a copy of the GNU General Public Licence along 
# with Luma; if not, write to the Free Software Foundation, Inc., 
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

from PyQt4.QtGui import QDialog

from base.gui.AboutDialogDesign import Ui_AboutDialog
from base.gui.AboutLicense import Ui_AboutLicense
from base.gui.AboutCredits import Ui_AboutCredits

class AboutDialog(QDialog, Ui_AboutDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)


    def showLicense(self):
        license = QDialog()
        Ui_AboutLicense().setupUi(license)
        license.exec_()
        print "GPL"


    def showCredits(self):
        credits = QDialog()
        Ui_AboutCredits().setupUi(credits)
        credits.exec_()
        print "Credits"


