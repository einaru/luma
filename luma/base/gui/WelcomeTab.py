# -*- coding: utf-8 -*-
#
# base.gui.WelcomeTab
#
# Copyright (c) 2011:
#     Johannes Harestad, <johanhar@stud.ntnu.no>
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

from PyQt4.QtGui import (QApplication, QWidget)
from PyQt4.QtCore import (QEvent, QSettings, Qt)

from ..gui.design.WelcomeTabDesign import Ui_WelcomeTab


class WelcomeTab(QWidget, Ui_WelcomeTab):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.retranslate(all=False)
        self.settings = QSettings()
        show = self.settings.value('showWelcome', 2).toInt()[0]
        self.checkBox.setCheckState(Qt.CheckState(show))

    def dontShow(self, state):
        self.settings.setValue('showWelcome', state)

    def changeEvent(self, event):
        """For dynamic translation support.
        """
        if QEvent.LanguageChange == event.type():
            self.retranslate()
        else:
            QWidget.changeEvent(self, event)

    def retranslate(self, all=True):
        """For dynamic translation.
        """
        if all:
            self.retranslateUi(self)
        # In order to make the job a little bit easier for translators
        # we should avoid the (ultra verbose) Qt Designer generated
        # html. If you are going to edit the following html, it might
        # be more convenient to edit the ``welcome.html`` file in the
        # resource folder, and copy paste in here afterwards.
        self.textBrowser.setHtml(QApplication.translate('WelcomeTab', """
<html>
<head>
<style type="text/css">
body { padding: 5px; margin: 5px; font-family: sans-serif; }
h1, h2 { color: #61a7e0; }
a { color: #306ebd; }
p { font-size: 10pt; }
</style>
</head>
<body>
<h1>Welcome to Luma</h1>

<p><strong><em>Luma is LDAP management made easy</em></strong></p>

<p><em>Luma</em> provides useful LDAP administration and management
functionality, through a number of plugins.</p>

<h2>Getting started</h2>

<p>The first thing you need to do is to edit the <em>serverlist</em>: Select
(<b>Edit</b> &rarr; <b>Server List</b>) from the menubar or use the keyboard
shortcut (<b>CTRL</b>+<b>SHIFT</b>+<b>S</b> on Linux/Windwos, <b>CMD</b>+<b>SHIFT</b>+<b>S</b> on Mac Os X).</p>

<p>After you have added one or more servers, you must activate the plugins you
want to use: Select (<b>Edit</b> &rarr; <b>Settings</b>) from the
menubar to open the <em>Settings dialog</em>, and select the <b>Plugins</b> tab.</p>

<p>If you need additional help on how to use the application and/or a spesific
plugin, please refer to the online
<a href="http://folk.ntnu.no/einaru/luma/doc/userguide.html">User guide</a>.</p>

<p>If you cannot find a plugin that suits your needs or you have ideas for a
great Luma plugin, please feel free to
<a href="http://luma.sf.net/">contact us</a> or even
<a href="http://folk.ntnu.no/einaru/luma/doc/HACKING.html">contribute one your self</a>.</p>

<h2>Problems and bugs</h2>

<p>Application errors and various debug information can be seen in the Logger
Window: Select (<b>View</b> &rarr; <b>Logger Window</b>) from the menubar or
use the keyboard shortcut (<b>CTRL</b>+<b>L</b> on Linux/Windows, <b>CMD</b>+<b>L</b> on Mac Os X).</p>

<p>If you encounter errors or bugs in the application, please take your time
to fill in a bugreport on our
<a href="http://sourceforge.net/tracker/?group_id=89105">bugtracker</a>.</p>

<h2>Contact</h2>

<p>You can find contact information in the About Luma dialog: Select
(<b>Help</b> &rarr; <b>About Luma</b>) or use the keyboard shortcut
(<b>F12</b>), and on the <a href="http://luma.sf.net/">Luma website</a>.</p>

<p style="font-size: 8pt; color: #306ebd; padding-top: 25px">
<em>Copyright &copy; 2003 - 2011 Wido Depping and the Luma devel team</em></p>
</body>
</html>
"""))



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
