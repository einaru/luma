#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# tools.lumaResourceCompiler.py
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einar.uvslokk@linux.com>
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
Assumed locations of files:
.
|-- luma
|   |-- base
|   |   `-- gui
|   |       `design
|   |        `-- *Design.py
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

short_description = """
   __  __  ______ ___  ____  ___  ____  ____  
  / / / / / / __ `__ \/___ \/ __\/ ___\/ ___\  lumarcc.py v0.5
 / /_/ /_/ / / / / / / __  / /  / /___/ /___   copyright (c) 2011
 \__/\____/_/ /_/ /_/\____/_/   \____/\____/   <einar.uvslokk@linux.com>                                               
Luma resource compiler"""

long_description = """
This utility script makes use of the following PyQt commands:

pyrcc4      Used for compiling resources into a python resource file.
            This is a python wrapper for rcc
pyuic4      Used for compiling .ui files and generating py source files.
            This is a python wrapper for uic-qt4
pylupdate4  Used for updating the resources in the project file.
            This is a python wrapper for lupdate-qt4"""


class LumaPRO(object):
    """Object respresenting the ``luma.pro`` project file.

    The sections in the project file is represeneted as a python dict,
    with a string as key, and a list of strings as value::

        pro = {
            section1 : [item, item, ...],
            section2 : [item,  ...],
            ...
        }

    where section can be SOURCES, FORMS, TRANSLATIONS, etc.
    The ``luma.pro`` file will thus be transformed to::

        ...

        section1 += item
        section1 += item
        section1 += ...

        section2 += item
        section2 += ...

        ...
    """
    
    FILE = 'luma.pro'

    def __init__(self):
        self.proDict = {}
        self.proDict['CONFIG'] = ['qt debug']
        self.proDict['RESOURCES'] = ['luma/resources.py']
    
    def __str__(self):
        """Retruns the string representation of the project file.
        """
        return '\n'.join([line for line in self.asList()])

    def addItem(self, section, item):
        """
        """
        if self.proDict.has_key(section):
            self.proDict.get(section).append(item)
        else:
            self.proDict[section] = [item]

    def update(self):
        """
        """
        self.find('SOURCES', getPath(['luma']), '.py', ['__init__.py'])
        self.find('FORMS', getPath(SRC_UI))
        self.find('TRANSLATIONS', getPath(SRC_i18n), '.ts')
        
    def find(self, section, path, ending='', ignore=[]):
        """
        """
        if verbose:
            print '[{0}]'.format(section)
        cwd = os.getcwd() + os.sep
        for p, dirs, files in os.walk(path):
            if p.endswith('rejects'):
                continue

            for file in files:
                relpath = p.replace(cwd, '').replace('\\', '/')
                if not file in ignore and file.endswith(ending):
                    file = os.path.join(relpath, file)
                    self.addItem(section, file)
                    if verbose:
                        print '  {0}'.format(file)

    def save(self):
        with open(self.FILE, 'w') as f:
            f.write(str(self))
            f.write('\n')

    def asList(self):
        """Returns the project file as a list of lines.
        """
        proFile = []
        for section, items in sorted(self.proDict.iteritems()):
            for item in items:
                line = '{0} += {1}'
                proFile.append(line.format(section, item))

            proFile.append('')
                
        return proFile


class LumaQRC(object):
    """Object representing the Luma Resource file (``luma.qrc``).

    The main part of the resource file is represented as a python dict,
    with a string as key, and a tuple containg the accesiable alias and
    the location of the resource::

        qrc = {
            prefix : (alias, location),
            prefix : (alias, location),
            ...,
        }

    which will then be transformed to::

        <!DOCTYPE RCC><RCC version="1.0">
          <qresource prefix="prefix">
            <file alias="alias">location/name</file>
          </qresource>
          <qresource prefix="prefix">
            <file alias="alias">location/name</file>
          </qresource>
          ...
        </RCC>
    """

    FILE = 'luma.qrc'
    header = '<!DOCTYPE RCC><RCC version="1.0">'
    footer = '</RCC>'

    def __init__(self, resourceRoot='resources'):
        """Initializes a `LumaQrc` object.

        Parameters:

        - `resourceRoot`: the resource root location (relative to the
          repository root)
        """
        self.root = resourceRoot
        self.qrcDict = {}
        self.qrcFile = []

    def __str__(self):
        """Returns the .qrc file as a string. The ``newline`` character
        is added after each line.
        """
        return '\n'.join([line for line in self.asList()])

    def getIconPrefix(self, path):
        """All we need to do for the icontheme paths is to look for the
        size folder. This is done by splitting the folder items on 'x' 
        and see if the first item ``isdigit``.
        
        Returns a prefix containing the path folders preceeding the
        size folder, including the size folder (without 'xSize').
        
        Parameters:
        
        - `path`: the path to get the 'prefix' from.
        """
        list = path.split(os.sep)
        i = 0
        for item in list:
            tmp = item.split('x')
            if tmp[0].isdigit():
                return 'icons/{0}'.format(tmp[0])

            # A special case for the ``scalable`` directory
            if item == 'scalable':
                return 'icons/svg/'

            if item == 'plugins':
                return 'icons/plugins'

        # If we end up here we simple return ``icons`` as the prefix
        return 'icons'

    def addResource(self, prefix, path, file):
        """Adds or appends a `resource` to the value for key `prefix`.
        The alias for the resource will be the
        resource filename without hte filending, i.e. *luma.png*
        get the alias *luma*

        Parameters:

        - `resource`: a string containing the path to the resource
          (relative to the repository root).
        """
        if prefix == 'icons':
            prefix = self.getIconPrefix(path)
            alias = file[:-4]
        else:
            alias = file[:-3].replace('luma_', '')

        if self.qrcDict.has_key(prefix):
            self.qrcDict.get(prefix).extend([(alias, path, file)])
        else:
            self.qrcDict[prefix] = [(alias, path, file)]

    def update(self):
        """Scannes the ``resources`` directory for resources to include
        in the ``luma.qrc`` resource file.

        We look for translation files and icons.
        """
        for path, dirs, files in os.walk(self.root):
            for file in sorted(files):
                if path.endswith('i18n') and file[-3:] == '.qm':
                    self.addResource('i18n', path, file)
                elif file[-4:] in ['.png', '.gif']: #, '.svg']:
                    self.addResource('icons', path, file)

    def save(self):
        with open(self.FILE, 'w') as f:
            f.write(str(self))
            f.write('\n')


    def asList(self, indentation=2):
        """Returns the .qrc file as a list of lines. By default the
        lines in the list is indented with 2 spaces.

        Parameters:
        
        - `indentation`: an integer defining how many spaces to use for
          indentation. Use 0 for no indentation (default is 2).
        """
        indent = ''
        for i in xrange(indentation):
            indent = ' {0}'.format(indent)

        self.qrcFile.append(LumaQRC.header)
        for prefix, values in self.qrcDict.iteritems():
            line = '{0}<qresource prefix="{1}">'
            self.qrcFile.append(line.format(indent, prefix))
            for v in values:
                line = '{0}{0}<file alias="{1}">{2}/{3}</file>'
                self.qrcFile.append(line.format(indent, v[0], v[1], v[2]))

            self.qrcFile.append('{0}</qresource>'.format(indent))

        self.qrcFile.append(LumaQRC.footer)
        return self.qrcFile


# ---------------------------------------------------------------------------- #
# Filepaths
SRC_ICONS = ['resources', 'icons']
SRC_i18n = ['resources', 'i18n']
SRC_UI = ['resources', 'forms']
DST_i18n = ['luma', 'i18n']
DST_UI = ['luma', 'base', 'gui', 'design']
PLUGINS = ['luma', 'plugins']

# Files w/filepaths
LUMA_PRO = ['luma.pro']
LUMA_QRC = ['luma.qrc']
LUMA_RC = ['luma', 'resources.py']


def run(cmd, args=[]):
    """Executes the command `cmd` with optional arguments `args`,
    provided it is available on the system.
    
    Parameters:
    
    - `cmd`: The program command.
    - `args`: a list of arguments to pass to `cmd` (default is []).
    """
    if not dryrun:

        proc = QProcess()
        proc.start(cmd, args)
        while proc.waitForReadyRead():
            if verbose:
                print '>>>'
                print 'ReadyRead:\n{0}'.format(proc.readAll())
                print '<<<'
                
        if verbose:
            stderr = proc.readAllStandardError()
            if stderr != '':
                print '>>>'
                print 'Errors:\n{0}'.format(stderr)
                print '<<<'
            stdout = proc.readAllStandardOutput()
            if stdout != '':
                print '>>>'
                print 'Output:{0}\n'.format(proc.readAllStandardOutput())
                print '<<<'


def writeToDisk(list, where):
    """Writes the `list` to disk, item for item.
    
    Parameters:
    
    - `list`: the content to write to disk, should be a list.
    - `where`: the path to file we're writing to.
    """
    if verbose:
        print 'Writing content to {0}'.format(where)

    if not dryrun:
        with open(where, 'w') as f:
            f.write('\n'.join([line for line in list]))


def getPath(dirList):
    """Ensures that we get correct paths. That is we change our
    working directory to the top-level (one step up from tools).
    
    Returns a cross-platform filepath from file system root including
    the last directory in the path list.
    
    Parameters:
    
    - `dirList`: a list of directories to join from cwd.
    """
    cwd = os.path.abspath(os.path.dirname(__file__))

    if os.path.split(cwd)[1] == 'tools':
        os.chdir(os.path.split(cwd)[0])

    path = os.getcwd()

    for dir in dirList:
        path = os.path.join(path, dir)

    return path


def compileResources():
    """Compiles the resources defined in the *luma.qrc* file into the
    ``resources.py`` file.
    """
    lumaqrc = getPath(LUMA_QRC)
    lumarc = getPath(LUMA_RC)

    cmd = 'pyrcc4'
    if sys.platform.lower().startswith('win'):
        cmd = '{0}.exe'.format(cmd)

    args = ['luma.qrc', '-py2', '-o', 'luma/resources.py']

    if verbose:
        print 'Compiling resources:'
        print '  source file: {0}'.format(lumaqrc)
        print '  target file: {0}'.format(lumarc)
        print 'Executing:'
        print '  {0} {1}'.format(cmd, ' '.join([arg for arg in args]))

    run(cmd, args)


def compileUiFiles(all=False):
    """Displayes a list of all *.ui files, and prompts for a index
    based selection. The selected file(s) is then compiled to python
    code.

    Parameters:

    - `all`: a boolean value indicating wether or not we are to compile
      all *.ui files we find or compile a selection. If the script is
      run with the ``-f`` option `all` should be ``True``. We also use
      this value to determine if we print the slection list. (default
      is ``False``)
    """
    selection = {}
    uifiles = []

    # If `all`is True we do not print anything related to the selection
    # list.
    if not all:
        print 'Available *.ui files:'
        print

    index = 1
    for path, dirs, files in os.walk(getPath(SRC_UI)):
        if files != []:
            basename = os.path.basename(path)
            if not all and basename != 'forms':
                print
                print '[{0} plugin]:'.format(basename)

        for file in files:
            selection[index] = os.path.join(path, file)
            if not all:
                print '  {0:2d} {1}'.format(index, file)

            index += 1

    # If all is False we prompt for the index of the file(s) to compile
    compile = []
    if all:
        compile = selection.values()
    else:
        input = raw_input('\nEnter the index of the file(s) to compile\n' +
                          '(use * to compile all files listed):')

        nums = input.split(' ')
        if '*' in nums:
            compile = selection.values()
        else:
            for n in nums:
                if n.isdigit():
                    compile.append(selection[int(n)])
    
    # Iterate through the file(s) marked for compiling, and run 
    # the *pyuic4* command.
    cmd = 'pyuic4'
    if sys.platform.lower().startswith('win'):
        cmd = '{0}.bat'.format(cmd)

    if verbose:
        print 'Compiling ui files:'
    
    for file in compile:
        basename = os.path.basename('{0}.py'.format(file[:-3]))
        dirname = os.path.split(os.path.dirname(file))[1]
        
        # If `dirname` is not `forms` we are dealing with plugins
        # files, and need a different target destination.
        if dirname != 'forms':
            path = os.path.join(getPath(PLUGINS), dirname, 'gui')
        else:
            path = getPath(DST_UI)

        target = os.path.join(path, basename)
        args = [file, '-o', target]

        if verbose:
            print '  Ui file: {0}'.format(file)
            print '  Target file: {0}'.format(target)
            print

        if not dryrun:
            run(cmd, args)


def updateTranslationFiles():
    """Just executes the ``pylupdate4`` command on the ``luma.pro``
    file.
    """
    # FIXME: Might want to extend this utility some more, with options
    #        for generating new translation files (skeletons that is).
    lumapro = 'luma.pro'
    cmd = 'pylupdate4'
    if sys.platform.lower().startswith('win'):
        cmd = '{0}.exe'.format(cmd)

    args = ['-noobsolete']
    
    if verbose:
        args.extend(['-verbose', lumapro])
        print 'Updating translation files...'
        print '  Project file: {0}'.format(lumapro)
        print cmd, ' '.join([a for a in args])
    else:
        args.append(lumapro)

    if not dryrun:
        run(cmd, args)


def updateResourceFile():
    """Updates the resource file and writes the content to disk.
    """
    qrc = LumaQRC()
    if verbose:
        print 'Updating resource file...'
        print '  Target file: {0}'.format(qrc.FILE)
        print '  Scanning for resources...'
    qrc.update()
    if verbose:
        print '  Saving resource file...'
        print
    if not dryrun:
        qrc.save()


def updateProjectFile():
    """Updates the project file and writes the content to disk.
    """
    pro = LumaPRO()
    if verbose:
        print 'Updating project file:'.format(pro.FILE)
        print '  Looking for files to include...'
    pro.update()
    if verbose:
        print '  Saving project file...'
        print
    if not dryrun:
        pro.save()


def main():
    """Sets up the option parser, parsers the commandline for opations
    and arguments, and runs the appropriate methods.
    """
    global verbose, dryrun

    usage = '%prog [options]'
    # Main Options:
    parser = OptionParser(usage=usage)

    parser.add_option(
        '-f', '--full-run',
        dest='full_run', action='store_true',
        help='Do a full run. This involves first compiling all ui files, ' +
        'creating the .qrc file, generate the resource.py file, update ' +
        'translation files, and update the project file.'
    )
    parser.add_option(
        '-u', '--compile-ui-files',
        dest='ui_files', action='store_true',
        help='List all .ui files, and choose the one [or all] files to compile'
    )
    parser.add_option(
        '-q', '--update-qrc',
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
    parser.add_option(
        '-p', '--update-pro',
        dest='pro_file', action='store_true',
        help='Creates or updates the application project file.'
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
        updateResourceFile()
        updateTranslationFiles()
        updateProjectFile()
        compileResources()
        compileUiFiles(all=True)
        sys.exit()

    if opt.qrc_file:
        updateResourceFile()
        compileResources()

    if opt.ui_files:
        compileUiFiles(all=False)

    if opt.ts_files:
        updateTranslationFiles()

    if opt.pro_file:
        updateProjectFile()


if __name__ == '__main__':
    """We first ensures that we change our working directory to the
    repository root. That is, if the script is beeing invoked from the
    ``tools`` folder, we change directory one level up.

    .. warning::
       The script will fail if beeing invoked from a directory deeper
       than the tools folder, i.e. python ../../lumarcc.py
    """
    cwd = os.path.abspath(os.path.dirname(__file__))

    if os.path.split(cwd)[1] == u'tools':
        os.chdir(os.path.split(cwd)[0])

    sys.exit(main())

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
