#!/usr/bin/env python
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
import sys

from optparse import OptionParser

from PyQt4 import QtCore

DEBUG = False

PATH_TO_UI = ['resources', 'forms']
PATH_TO_PY = ['base', 'gui']
PATH_TO_TS = ['resources', 'i18n']
PATH_TO_QM = ['i18n']

def getPath(path):
    """
    @param path: a list of directories to join from cwd
    
    @return: A cross-platform filepath from file system root including
             the last directory in the path list.
    """
    if os.path.split(os.path.abspath(u'.'))[1] == u'scripts':
        os.chdir(u'..')
    p = os.getcwd()
    for dir in path:
        p = os.path.join(p, dir)
    return p


def run(cmd):
    """
    This method is pretty much pillage from openLP :).
    
    @param cmd: The wicked command to be executed.
    """
    if verbose:
        print cmd
    if not DEBUG:
        proc = QtCore.QProcess()
        proc.start(cmd)
        while proc.waitForReadyRead():
            if verbose:
                print u'ReadyRead: %s' % QtCore.QString(proc.readAll())
        if verbose:
            print u'Errors:\n%s' % proc.readAllStandardError()
            print u'Output:\n%s' % proc.readAllStandardOutput()


def compileUiFiles(ui_files, src_path, dst_path):
    """
    Iterates through the ui_files and builds the compile command.
    Compiling is done through the run(cmd) method
    
    @param ui_files: a list of ui files to compile
    @param src_path: the source path, where all the .ui files is located
    @param dst_path: the desitination path, where all generated python
                     code is do end up.
    """
    for ui_file in ui_files:
        py_file = ui_file[:-3] # remove .ui
        py_file = u'%s.py' % py_file
        py_file = os.path.join(dst_path, py_file)
        ui_file = os.path.join(src_path, ui_file)
        cmd = u'pyuic4 %s -o %s' % (ui_file, py_file)
        run(cmd)


def listUiFiles(ui_files):
    """
    Create a indexed dictionary for available .ui files.
    The dictionary will be pretty printed.
    
    @param ui_files: a list of all .ui files
    """
    files = {}
    i = 1
    print 'Available .ui files:\n'
    for ui in ui_files:
        files[i] = ui
        print u'%2d  %s' % (i, ui)
        i = i + 1
    return files


def validateNum(num):
    """
    Validates if a variable is numeric. NB! if num == * this will be
    returned as is.
    
    @param num: the variable to validate
    """
    if num == u'*':
        return num
    if num.isdigit():
        return int(num)
    else:
        return -1


def prepareUiCompiling(compileAll):
    """
    Preapare for compiling.
    Setup up full path to the .ui files, full path to where the 
    generated .py files should end up, and fetches the list of
    available .ui files.
    """
    ui_path = getPath(PATH_TO_UI)
    ui_files = os.listdir(ui_path)
    py_path = getPath(PATH_TO_PY)
    
    if not compileAll:
        list = listUiFiles(ui_files)
        num = raw_input(u'\nEnter the number of the file to compile\n' + \
                        u'(use * to compile all files listed): ')
        num = validateNum(num)
        if num != u'*' and num > 0:
            compileUiFiles([list[int(num)]], ui_path, py_path)
            return
    compileUiFiles(ui_files, ui_path, py_path)


def main():
    
    global verbose
    
    usage = u'%prog [options] [files]\n' + \
             'If no options are given the %prog will be run with: -lv'
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
        help='Show all output while compiling .ui files')
    parser.add_option('-a', '--all', dest='all', action='store_true',
        help='Compile all ui files')
    parser.add_option('-l', '--ls', dest='list', action='store_true',
        help='Show a list of all .ui files, and choose the one to compile')

    (opt, args) = parser.parse_args()

    verbose = opt.verbose

    if opt.list:
        prepareUiCompiling(compileAll=False)
    elif opt.all:
        prepareUiCompiling(compileAll=True)
    elif len(sys.argv) == 1:
        """
        Default run when no options are given.
        For convenience when running from a IDE, i.e. Eclipse
        """
        print u'No options given. Will now run with the -lv flags...\n'
        verbose = True
        prepareUiCompiling(compileAll=False)

if __name__ == '__main__':
    sys.exit(main())
