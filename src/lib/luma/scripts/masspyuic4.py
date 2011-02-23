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

"""
assumed location of files:

luma
|--base
|  `--gui
|     `--*Design.py    : Ui generated python code
|--i18n
|  `--*.qm             : Compiled release translation files
|--plugins
|--resources
|  |--i18n
|  |  `--*.ts          : Translation source files
|  `--forms
|     `--*Design.ui    : All QtDesigner Ui files
|--scripts
|  `--masspyuic4.py    : This script
`--luma.pro            : The Luma project file
"""

import os

from PyQt4 import QtCore

path_to_uiforms = ['resources', 'forms']
path_to_pyforms = ['base', 'gui']
path_to_ts = ['resources', 'i18n']
path_to_qm = ['i18n']

def getPath(path):
    if os.path.split(os.path.abspath(u'.'))[1] == u'scripts':
        os.chdir(u'..')
    p = os.getcwd()
    for dir in path:
        p = os.path.join(p, dir)
    return p


def run(cmd):
    """
    This method is stolen from openLP, but runs a wicked command instead.
    
    @param cmd: The wicked command to be executed.
    """
    print cmd
    proc = QtCore.QProcess()
    proc.start(cmd)
    while proc.waitForReadyRead():
        print u'ReadyRead: %s' % QtCore.QString(proc.readAll())
    print u'Errors:\n%s' % proc.readAllStandardError()
    print u'Output:\n%s' % proc.readAllStandardOutput()


def compileUiFiles():
    ui_path = getPath(path_to_uiforms)
    ui_files = os.listdir(ui_path)
    py_path = getPath(path_to_pyforms)

    for ui_file in ui_files:
        py_file = ui_file[:-3] # remove .ui
        py_file = u'%s.py' % py_file
        
        py_file = os.path.join(py_path, py_file)
        ui_file = os.path.join(ui_path, ui_file)
        
        cmd = u'pyuic4 %s -o %s' % (ui_file, py_file)
        run(cmd)


if __name__ == '__main__':
    compileUiFiles()
