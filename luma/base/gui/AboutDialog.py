# -*- coding: utf-8 -*-
#
# base.gui.AboutDialog
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

from PyQt4.QtGui import qApp
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QPixmap

from ..gui.design.AboutDialogDesign import Ui_AboutDialog
from ..gui.design.AboutLicenseDesign import Ui_AboutLicense
from ..gui.design.AboutCreditsDesign import Ui_AboutCredits
from ..util.IconTheme import iconFromTheme


class AboutDialog(QDialog, Ui_AboutDialog):
    """ A simple about dialog.
    
    It includes basic application information, a short outline of the
    application license, and of course credit is given where credit is
    due.
    """

    def __init__(self, parent=None):

        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.setWindowIcon(iconFromTheme('help-about', ':/icons/16/help-about'))
        self.logo.setPixmap(QPixmap(':/icons/64/luma'))
        version = qApp.applicationVersion()
        self.nameAndVersion.setText('Luma {0}'.format(version))

    def showLicense(self):
        """Displays a simple dialog containing the application license
        """
        license = QDialog()
        Ui_AboutLicense().setupUi(license)
        license.exec_()

    def giveCreditWhereCreditIsDue(self):
        """Displays a simple dialog containing developer information,
        and credit is given where credit is due
        """
        credits = QDialog()
        Ui_AboutCredits().setupUi(credits)
        credits.exec_ ()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
