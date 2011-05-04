# -*- coding: utf-8 -*-
#
# base.gui.AbstractLumaPlugin
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
"""
This module is an attempt to bring together the pieces needed for
creating a working Luma plugin.

To get dynamic translation support for the plugin, you are required to
implement the retranslate method and overload the changeEvent signal,
in order to catch the LanguageChange event. The retranslate method
should be called if this event is caught.

If your plugin is to provide some sort of settings management, you
must implement the writeSettings method in the SettingsWidget class, as
this method will be called by the Luma SettingsDialog when the save
action is triggered.

For more information on developing plugins for the Luma application, 
please consult the documentation, both available with the source
distribution and on the Luma website, http://luma.sf.net/ .
"""
from PyQt4.QtCore import (QEvent)
from PyQt4.QtGui import (QWidget)

class AbstractLumaPlugin(QWidget):
    """Abstract Luma plugin.
    """
    
    def __init__(self, parent=None, *args, **kwargs):
        super(AbstractLumaPluginSettings, self).__init__(parent, args, kwargs)

    def retranslate(self):
        """Overload this method in order to get support for dynamic
        translation of plugin.
        """
        for widget in self.children():
            try:
                widget.retranslate()
            except AttributeError:
                pass

    def changeEvent(self, event):
        """Catch the LanguageChange event to be able to retranslate
        the plugin widget.
        """
        if event.type() == QEvent.LanguageChange:
            self.retranslate()
        else:
            QWidget.changeEvent(self, event)


class AbstractLumaPluginSettings(QWidget):
    """Abstract Luma plugin settings widget.
    """
    
    def __init__(self, parent=None, *args, **kwargs):
        super(AbstractLumaPluginSettings, self).__init__(self)
    
    def writeSettings(self):
        """This method will be called from the Luma SettingsDialog, if
        the plugin has provided a settings widget.
        """
        pass


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
