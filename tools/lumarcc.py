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
from string import replace
"""
Assumed locations of files:

<top level>
|--luma
|  |--gui
|  |  `--*Design.py
|  `--i18n
|     `--luma_*.ts
|
|--resources
|  |--forms
|  |  `--*Design.ui
|  |--i18n
|  |  `--luma_*.ts
|  `--icons
|
|--tools
|  |--lumarcc.py
|  `--masspyuic4.py
|
|--luma.pro
`--luma.qrc

Purpose:

Compile all project resources in one command
"""

logo = """
   __  __  ______ ___  ____  ___  ____  ____  
  / /\/ /\/ / __ `__ \/___ \/ __\/ ___\/ ___\  lumarcc.py v0.2
 / /_/ /_/ / /\/ /\/ / __  / /\_/ /\__/ /\___\ copyright (c) 2011
 \__/\____/_/ /_/ /_/\____/_/ / \____/\____/\  Einar Uvsløkk
  \_\/\___\_\/\_\/\_\/\___\_\/   \___\/\___\/  <einar.uvslokk@linux.com>
"""

import os
import sys

from optparse import OptionParser, OptionGroup

from PyQt4.QtCore import QProcess, QString

# Filepaths
SOURCE_ICONS = ['resources', 'icons']
SOURCE_TRANS = ['resources', 'i18n']
SOURCE_UI = ['resources', 'forms']
DEST_TRANS = ['luma', 'i18n']
DEST_UI = ['luma', 'base', 'gui']


# Files w/filepaths
LUMA_PRO = ['luma.pro']
LUMA_QRC = ['luma2.qrc']
LUMA_RC = ['luma', 'resources.py']


def run(cmd):
    """
    This method is pretty much pillage from openLP :).
    It executes the provided command, provided it is available on the system.
    
    @param cmd: The wicked command to be executed.
    """
    if verbose:
        print u'\tCommand: %s' % cmd
    if not dryrun:
        proc = QProcess()
        proc.start(cmd)
        while proc.waitForReadyRead():
            if verbose:
                print u'ReadyRead: %s' % QString(proc.readAll())
        if verbose:
            print u'Errors:\n%s' % proc.readAllStandardError()
            print u'Output:\n%s' % proc.readAllStandardOutput()
            print u'------'


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
        if verbose:
            print u'Building command to compile .ui file:'
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


def prepareUiCompiling(compileAll):
    """
    Prepare for compiling.
    Setup up full path to the .ui files, full path to where the 
    generated .py files should end up, and fetches the list of
    available .ui files.
    """
    ui_path = __getPath(SOURCE_UI)
    ui_files = os.listdir(ui_path)
    py_path = __getPath(DEST_UI)

    if not compileAll:
        list = listUiFiles(ui_files)
        num = raw_input(u'\nEnter the number of the file to compile\n' + \
                        u'(use * to compile all files listed): ')
        num = __validateNum(num)
        if num != u'*' and num > 0:
            compileUiFiles([list[int(num)]], ui_path, py_path)
            return

    compileUiFiles(ui_files, ui_path, py_path)


def compileResources():
    """
    Compile resources defined in the project file [luma.pro]
    """
    lumaqrc = __getPath(LUMA_QRC)
    lumarc = __getPath(LUMA_RC)
    cmd = u'pyrcc4 %s -py2 -o %s' % (lumaqrc, lumarc)
    if verbose:
        print u'Building command to compile resources:'
        print u'\tresource collection file: %s' % lumaqrc
        print u'\tpython resource file: %s' % lumarc
    run(cmd)


def createQrcFile(icons=False, i18n=False):
    """
    Create the luma.qrc file based on the content in the resource folder
    
    @param icons: Wheter or not to include icons
    @param i18n: Wheter or not to include translation files
    """
    qrc = __generateQrcFile(icons, i18n)
    __writeToDisk(qrc, __getPath(LUMA_QRC))


def __generateQrcFile(icons=False, i18n=False):
    """
    Scannes the defined icons and/or i18n folders for content to include
    in the luma resource file -> resources.py
    
    @param icons: Wheter or not to include icons
    @param i18n: Wheter or not to include translation files
    """
    qrc = []
    QRC_HEADER_OPEN = u'<!DOCTYPE RCC><RCC version="1.0">'
    QRC_HEADER_CLOSE = u'</RCC>'

    qrc.append(QRC_HEADER_OPEN)

    if i18n:
        i18nPath = __getPath(SOURCE_TRANS)
        qrc.append(u'<qresource prefix="%s">' % os.path.split(i18nPath)[1])
        for file in os.listdir(i18nPath):
            if file[-3:] == u'.qm':
                name = os.path.split(file)[1]
                alias = name[5:-3]
                qrc.append(u'\t<file alias="%s">resources/i18n/%s</file>' % \
                           (alias, name))
        qrc.append(u'</qresources>')

    if icons:
        iconsPath = __getPath(SOURCE_ICONS)
        qrc.append(u'<qresource prefix="%s">' % os.path.split(iconsPath)[1])
        prefix = ''
        for path, dirs, icons in os.walk(iconsPath):
            location = replace(path, iconsPath, u'resources/icons')

            if location[-5:] != u'icons':
                prefix = '%s-' % os.path.split(location)[1]

            for icon in sorted(icons):
                if icon[-4:] == u'.png':
                    (name, alias) = __getIconNameAndAlias(icon)
                    qrc.append(u'\t<file alias="%s%s">%s/%s</file>' % \
                               (prefix, alias, location, name))

        qrc.append(u'</qresource>')

    qrc.append(QRC_HEADER_CLOSE)

    return qrc


def __writeToDisk(list, where):
    """
    Writes a list, item for item, to disk at location where.
    
    @param list: the content to write to disk, should be a list.
    @param where: the path to file we're writing to
    """
    if verbose:
        print u'Writing content to: %s' % where
    if not dryrun:
        file = open(where, 'w')

        for line in list:
            if verbose:
                print line
            file.write(u'%s\n' % line)

        file.close()


def __getIconNameAndAlias(path):
    name = os.path.split(path)[1]
    alias = name[:-4]
    return (name, alias)


def __validateNum(num):
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
        return - 1


def __getPath(pathList):
    """
    Ensures that we get correct paths. That is we change our working 
    directory to the top-level (one step up from tools).
    
    @param pathList: a list of directories to join from cwd
    
    @return: A cross-platform filepath from file system root including
             the last directory in the path list.
    """
    cwd = os.path.abspath(os.path.dirname(__file__))

    if os.path.split(cwd)[1] == u'tools':
        os.chdir(os.path.split(cwd)[0])

    path = os.getcwd()

    for dir in pathList:
        path = os.path.join(path, dir)

    return path


def main():

    global verbose, dryrun

    usage = u'%prog [options]\n'

    # Main Options:
    parser = OptionParser(usage=usage)

    parser.add_option('-c', '--complete', dest='complete', action='store_true',
                      help='Run a complete resource build, ' +
                      'this includes compiling all .ui files before ' +
                      'creating the resource file')
    parser.add_option('-d', '--default', dest='default', action='store_true',
                      help='Compile resources defined in the luma.pro file')
    parser.add_option('-g', '--generate', dest='generate', action='store_true',
                      help='Generate the resource file. Usefull only if ' +
                      'resources are changed.')
    parser.add_option('-q', '--qrc', dest='qrc', action='store_true',
                      help='Create/update the resource.py file. ' +
                      'The luma.qrc must exists for this to succeed.')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      help='Show all output while compiling .ui files')

    # Ui-compiling Options:
    group = OptionGroup(parser, 'Ui-compiling Options',
                        'Use these options to compile .ui files.')
    group.add_option('-a', '--all', dest='all', action='store_true',
                     help='Compile all ui files')
    group.add_option('-l', '--ls', dest='list', action='store_true',
                     help='List all .ui files, and choose the one to compile')
    parser.add_option_group(group)

    # Debug Options:
    group = OptionGroup(parser, 'Debug Options:')
    group.add_option('--dry', dest='dry', action='store_true',
                     help='Dry-run. Must be used together with other options')
    parser.add_option_group(group)

    (opt, args) = parser.parse_args()

    verbose = opt.verbose
    dryrun = opt.dry

    if dryrun:
        print u'!!!!!!!!!!!!!!!\n!!! DRY-RUN !!!\n!!!!!!!!!!!!!!!'

    if len(sys.argv) == 1:
        print logo
        sys.exit(parser.print_usage())
        #"""
        #Default run when no options are given.
        #For convenience when running from a IDE, i.e. Eclipse
        #"""
        #print u'No options given. Will now run with the -lv flags...\n'
        #verbose = True
        #prepareUiCompiling(compileAll=False)
    if opt.generate:
        createQrcFile(icons=True, i18n=True)

    if opt.complete:
        prepareUiCompiling(compileAll=True)
        sys.exit(compileResources())
    if opt.all:
        prepareUiCompiling(compileAll=True)
        if opt.complete:
            sys.exit(compileResources())
    elif opt.list:
        prepareUiCompiling(compileAll=False)

    if opt.default:
        compileResources()


if __name__ == '__main__':
    sys.exit(main())
