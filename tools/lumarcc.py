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
Assumed locations of files:
.
|-- luma
|   |-- base
|   |   `-- gui
|   |       `-- *Design.py
|   `-- plugins
|       `-- <plugin-name>
|           `-- gui
|               `-- *Design.py
|-- resources
|   |-- forms
|   |   |-- plugins
|   |   |   `-- search
|   |   |       `-- *Design.ui
|   |   `-- *Design.ui
|   |--i18n
|   |  `--luma_*.ts
|   `--icons
|-- tools
|   `--lumarcc.py
|
|-- luma.pro
`-- luma.qrc

Purpose:

Compile all project resources in one command
"""
import os
import sys
from string import replace
import subprocess

from optparse import OptionParser, OptionGroup

from PyQt4.QtCore import QProcess, QString

# Filepaths
SOURCE_ICONS = ['resources', 'icons']
SOURCE_TRANS = ['resources', 'i18n']
SOURCE_UI = ['resources', 'forms']
DEST_TRANS = ['luma', 'i18n']
DEST_UI = ['luma', 'base', 'gui']
PLUGINS = ['luma', 'plugins']

# Files w/filepaths
LUMA_PRO = ['luma.pro']
LUMA_QRC = ['luma.qrc']
LUMA_RC = ['luma', 'resources.py']
LUMA_RC_ICONS = ['luma', 'iconsrc.py']
LUMA_RC_I18N = ['luma', 'i18nrc.py']

short_description = """
   __  __  ______ ___  ____  ___  ____  ____  
  / /\/ /\/ / __ `__ \/___ \/ __\/ ___\/ ___\  lumarcc.py v0.5
 / /_/ /_/ / /\/ /\/ / __  / /\_/ /\__/ /\___\ copyright (c) 2011
 \__/\____/_/ /_/ /_/\____/_/ / \____/\____/\  Einar Uvsløkk
  \_\/\___\_\/\_\/\_\/\___\_\/   \___\/\___\/  <einar.uvslokk@linux.com>

Luma resource compiler"""

long_description = """
This utility script makes use of the following PyQt commands:

pyrcc4      Used for compiling resources into a python resource file.
            This is a python wrapper for rcc
pyuic4      Used for compiling .ui files and generating py source files.
            This is a python wrapper for uic-qt4
pylupdate4  Used for updating the resources in the project file.
            This is a python wrapper for lupdate-qt4"""


def __run(cmd, args=[]):
    """
    This method is pretty much pillage from openLP :).
    It executes the provided command, provided it is available on the system.
    
    @param cmd: The wicked command to be executed.
    """
    if not dryrun:

        proc = QProcess()
        proc.start(cmd, args)
        while proc.waitForReadyRead():
            if verbose:
                print u'  ReadyRead: %s' % proc.readAll()
        if verbose:
            stderr = proc.readAllStandardError()
            if stderr != '':
                print u'  Errors: %s' % stderr
            stdout = proc.readAllStandardOutput()
            if stdout != '':
                print u'  Output: %s' % proc.readAllStandardOutput()

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
            file.write(u'%s\n' % line)

        file.close()


def _getIconNameAndAlias(path):
    name = os.path.split(path)[1]
    alias = name[:-4]
    return (name, alias)


def _validateNum(num):
    """ Validates if a variable is numeric. NB! if num == * this will
    be returned as is.
    
    @param num:
        the variable to validate
    
    @return:
        * indicates the wildcard to apply, else a number is returned.
        The parameter if it was a number, -1 if not.
    """
    if num == u'*':
        return num
    if num.isdigit():
        return int(num)
    else:
        return - 1


def _getPath(pathList):
    """ Ensures that we get correct paths. That is we change our
    working directory to the top-level (one step up from tools).
    
    @param pathList:
        a list of directories to join from cwd
    
    @return:
        A cross-platform filepath from file system root including the
        last directory in the path list.
    """
    cwd = os.path.abspath(os.path.dirname(__file__))

    if os.path.split(cwd)[1] == u'tools':
        os.chdir(os.path.split(cwd)[0])

    path = os.getcwd()

    for dir in pathList:
        path = os.path.join(path, dir)

    return path


def _listUiFiles(noprint=False):
    """ List all available .ui files
    """
    uipath = _getPath(SOURCE_UI)

    uifiles = {}
    index = 1
    if not noprint:
        print 'Available .ui files:\n'

    for path, dir, files in os.walk(uipath):
        if files != []:
            basename = os.path.basename(path)
            if not noprint and basename != 'forms':
                print '\n[%s plugin]:' % basename
        for file in files:
            uifiles[index] = os.path.join(path, file)
            if not noprint:
                print '%2d  %s' % (index, file)
            index = index + 1

    return uifiles


def _prepareUiFiles(all=False):
    """ Prepares the .ui files for compiling. A list of available .ui
    files will be printed, and the user will be prompted for the index
    of the file to be compiled. The index must be an valid integer, or
    * to compile all files.
    
    @param all: boolean value;
        whether or not to prepare all files
    """

    if all:
        return _listUiFiles(noprint=True).values()

    uifiles = _listUiFiles()
    files = []

    input = raw_input('\nEnter the number of the file(s) to compile\n' +
                     '(use * to compile all files listed):')

    nums = input.split(' ')
    for num in nums:
        num = _validateNum(num)
        if num == '*':
            return uifiles.values()
        elif num > 0:
            files.append(uifiles[num])

    return files


def _generateQrcFile(icons=False, i18n=False):
    """ Scannes the defined icons and/or i18n folders for content to
    include in the luma resource file -> resources.py
    
    @param icons:
        Wheter or not to include icons
    @param i18n:
        Wheter or not to include translation files
    """
    qrc = []
    QRC_HEADER_OPEN = u'<!DOCTYPE RCC><RCC version="1.0">'
    QRC_HEADER_CLOSE = u'</RCC>'

    qrc.append(QRC_HEADER_OPEN)

    if i18n:
        i18nPath = _getPath(SOURCE_TRANS)
        qrc.append(u'  <qresource prefix="%s">' % os.path.split(i18nPath)[1])
        for file in os.listdir(i18nPath):
            if file[-3:] == u'.qm':
                name = os.path.split(file)[1]
                alias = name[5:-3]
                qrc.append(u'    <file alias="%s">resources/i18n/%s</file>' % \
                           (alias, name))
        qrc.append(u'  </qresource>')

    if icons:
        iconsPath = _getPath(SOURCE_ICONS)
        qrc.append(u'  <qresource prefix="%s">' % os.path.split(iconsPath)[1])
        prefix = ''
        for path, dirs, icons in os.walk(iconsPath):
            location = replace(path, iconsPath, u'resources/icons')

            if location[-5:] != u'icons':
                prefix = '%s-' % os.path.split(location)[1]

            for icon in sorted(icons):
                if icon[-4:] == u'.png':
                    (name, alias) = _getIconNameAndAlias(icon)
                    qrc.append(u'    <file alias="%s%s">%s/%s</file>' % \
                               (prefix, alias, location, name))

        qrc.append(u'  </qresource>')

    qrc.append(QRC_HEADER_CLOSE)

    if verbose:
        print '\nGenerated .qrc file:'
        for line in qrc:
            print line

    return qrc


def compileUiFiles(compileAll=False):
    """ Find and list all available .ui files, and prepare the selected
    files for compiling.
    
    @param compileAll: boolean value;
        wheter or not to compile all files
    """

    uifiles = _prepareUiFiles(compileAll)
    pypath = _getPath(DEST_UI)

    cmd = 'pyuic4'
    if sys.platform == 'win32':
        cmd = '%s.exe' % cmd

    for uifile in uifiles:

        pyfile = '%s.py' % uifile[:-3]
        basename = os.path.basename(pyfile)
        dirname = os.path.split(os.path.dirname(uifile))[1]

        if dirname != 'forms':
            # We are dealing with plugin forms
            # and need to use a different destination path
            pluginpath = os.path.join(_getPath(PLUGINS), dirname, 'gui')
            pyfile = os.path.join(pluginpath, basename)
        else:
            # We are dealing with regular .ui forms,
            # and can use the default location 
            pyfile = os.path.join(pypath, basename)

        args = [uifile, '-o', pyfile]
        if verbose:
            print 'Executing: ', cmd, uifile, '-o', pyfile
        __run(cmd, args)


def createQrcFile(icons=False, i18n=False):
    """ Create the luma.qrc file based on the content in the resource
    folder
    
    @param icons:
        Wheter or not to include icons
    @param i18n:
        Wheter or not to include translation files
    """
    qrc = _generateQrcFile(icons, i18n)
    __writeToDisk(qrc, _getPath(LUMA_QRC))


def compileResources():
    """ Compile resources defined in the project file [luma.pro]
    """
    lumaqrc = _getPath(LUMA_QRC)
    lumarc = _getPath(LUMA_RC)

    cmd = 'pyrcc4'
    if sys.platform == 'win32':
        cmd = '%s.exe' % cmd

    args = [lumaqrc, '-py2', '-o', lumarc]

    if verbose:
        print '\nBuilding command to compile resources:'
        print '  resource file: %s' % lumaqrc
        print '  python resource file: %s' % lumarc
        print 'Executing: ', cmd, lumaqrc, '-py2', '-o', lumarc

    __run(cmd, args)


def updateTranslationFiles():
    """ Just executes the pylupdate4 command on the project file.
    """
    lumapro = _getPath(LUMA_PRO)

    cmd = 'pylupdate4'
    if sys.platform == 'win32':
        cmd = '%s.exe' % cmd

    args = ['-noobsolete']

    if verbose:
        args.append('-verbose')
        print '\nBuilding command to update translation files:'
        print '  project file: %s' % lumapro
        print 'Executing: ', cmd, '-noobsolete -verbose', lumapro

    args.append(lumapro)
    __run(cmd, [lumapro])


def main():

    global verbose, dryrun

    usage = '%prog [options]'
    # Main Options:
    parser = OptionParser(usage=usage)

    parser.add_option(
        '-f', '--full-run',
        dest='full_run', action='store_true',
        help='Do a full run. This involves first compiling all ui files, ' +
        'creating the .qrc file, and generate the resource.py file'
    )
    parser.add_option(
        '-u', '--compile-ui-files',
        dest='ui_files', action='store_true',
        help='List all .ui files, and choose the one [or all] files to compile'
    )
    parser.add_option(
        '-q', '--create-qrc-file',
        dest='qrc_file', action='store_true',
        help='Create and write the .qrc file to disk'
    )
    parser.add_option(
        '-t', '--update-ts',
        dest='ts_files', action='store_true',
        help='Creates or updates the application translations files. ' +
        'This is done by reading the project file. (NOTE: the .ts files, ' +
        'obviously, needs to be updated manually with QLinguist afterwards).'
    )
    # Debug Options:
    group = OptionGroup(parser, 'Debug Options')
    group.add_option(
        '-d', '--dry',
        dest='dry', action='store_true',
        help='Do a dry-run to see what will be done, without doing anything ' +
        '(NOTE: verbose will be set to True when this option is enabled.'
    )
    group.add_option(
        '-v', '--verbose',
        dest='verbose', action='store_true',
        help='Show output and information on whats going on'
    )
    group.add_option(
        '-i', '--info',
        dest='info', action='store_true',
        help='Show script information'
    )
    parser.add_option_group(group)

    (opt, args) = parser.parse_args()

    verbose = opt.verbose
    dryrun = opt.dry

    if dryrun:
        verbose = True

    if opt.info:
        print short_description
        parser.print_usage()
        print long_description
        sys.exit()

    if dryrun:
        print u'!!!!!!!!!!!!!!!\n!!! DRY-RUN !!!\n!!!!!!!!!!!!!!!'

    if len(sys.argv) == 1:
        print short_description
        parser.print_help()

    if opt.full_run:
        compileUiFiles(compileAll=True)
        createQrcFile(icons=True, i18n=True)
        compileResources()
        updateTranslationFiles()
        sys.exit()

    if opt.qrc_file:
        createQrcFile(icons=True, i18n=True)

    if opt.ui_files:
        compileUiFiles(compileAll=False)

    if opt.ts_files:
        updateTranslationFiles()


if __name__ == '__main__':
    sys.exit(main())
