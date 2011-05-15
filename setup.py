# -*- coding: utf-8 -*-
#
# setup
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

import os
import shutil
import sys
from glob import glob
from distutils.core import setup

import luma.__init__ as appinfo


def fullSplit(path, result=None):
    """Split a pathname into components (the opposite of os.path.join)
    in a platform-neutral way.
    """
    if result is None:
        result = []

    head, tail = os.path.split(path)

    if head == '':
        return [tail] + result

    if head == path:
        return result

    return fullSplit(head, [tail] + result)


def findPackages():
    """Custom method to suplement distutils with a setuptools-like way
    of finding all package files
    """
    skipDirs = ['rejects', 'test']
    packages = []
    root_dir = os.path.dirname(__file__)
    if root_dir != '':
        os.chdir(root_dir)

    for path, names, files in os.walk(src_dir):
        top = os.path.split(path)[1]
        # Skip directories defined in `skipDirs`
        if top in skipDirs:
            continue

        for i, name in enumerate(names):
            if name.startswith('.'):
                del names[i]

        if '__init__.py' in files:
            s = fullSplit(path)
            if s[0] == src_dir:
                s[0] = app_dir

            packages.append('.'.join(s))
    return packages

# Some default values shared among platforms
src_dir = 'luma'
app_dir = 'luma'
_author = 'Luma devel team'
_author_email = 'luma-devel@luma.sf.net'
_data_files = []

textfiles = [
    'AUTHORS',
    'Changelog',
    'COPYING',
    'HACKING',
    'INSTALL',
    'README',
    'TODO',
]

# For a complete list of available classifiers, see:
# http://pypi.python.org/pypi?%3Aaction=list_classifiers
_classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Environment :: MacOS X',
    'Environment :: Win32 (MS Windows)',
    'Environment :: X11 Applications :: Qt',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Topic :: Utilities',
]

# First we setup some platform spesific includes
# Winsows
if sys.platform.lower().startswith('win'):
    # TODO: add Windows spesifics. (py2exe?)
    _extras = dict(
        scripts=['luma/luma.py']
    )
# Mac OS X
elif sys.platform.lower().startswith('darwin'):
    # TODO: add Mac OS X spesifics. (py2app?)
    _extras = dict(
        scripts=['bin/luma'],
        data_files=[('share/man/man1', glob('data/man/luma.1.gz'))]
    )
# Linux
elif sys.platform.lower().startswith('linux'):
    # Include the application icon in various sizes, so that icon themers
    # can change this as per the iconthemeing standards defined by
    # freedesktop.org
    for size in [16, 22, 32, 48, 64, 128, 256]:
        dst = 'share/icons/hicolor/{0}x{0}/apps'.format(size)
        src = glob('data/icons/{0}x{0}/luma.png'.format(size))
        _data_files.append((dst, src))

    # Include the scalable application icon aswell
    _data_files.append(('share/icons/hicolor/scalable/apps',
                       glob('data/icons/scalable/luma.svg')))
    _data_files.append(('share/pixmaps',
                        glob('data/icons/scalable/luma.svg')))

    # Include the desktop and manpage files
    _data_files.append(('share/applications', glob('data/luma.desktop')))
    _data_files.append(('share/man/man1', glob('data/man/luma.1.gz')))

    _extras = dict(
        data_files=_data_files,
        scripts=['bin/luma']
    )

if __name__ == '__main__':

    error = sys.stderr.write
    write = sys.stdout.write

    # Then it's time for the general setup
    success = setup(
        name=appinfo.APPNAME,
        version=appinfo.VERSION,
        author=_author,
        author_email=_author_email,
        url='http://luma.sf.net',
        description=appinfo.DESCRIPTION,
        license='GNU General Public License (GPL) version 2',
        packages=findPackages(),
        package_dir={
            app_dir : src_dir
        },
        classifiers=_classifiers,
        **_extras
    )

    # This section is commented out because it currently is not
    # needed. It was created in an attempt to solve the issue with
    # including none python files in site-packages. This is currently
    # done for the html files shipped with the browser plugin.
    #
    #if success and 'install' in sys.argv:
    #    """If ``setup`` was successfully executed with the install
    #    argument we need to do some additional post processing work.

    #    This includes copying ``luma/plugins/browser/templates`` into
    #    path returned by ``luma.base.util.Paths.getConfigPrefix``.
    #    """
    #    from luma.base.util.Paths import getConfigPrefix

    #    src = os.path.join('luma', 'plugins','browser_plugin', 'templates')
    #    configPrefix = getConfigPrefix()

    #    if not configPrefix[0]:
    #        error('Unable to create user config folder:')
    #        msg = 'Additional none-python files will be copied to: {0}'
    #        error(msg.format(configPrefix[1]))

    #    dst = os.path.join(configPrefix[1], 'browser-templates')
    #    try:
    #        shutil.copytree(src, dst)
    #    except OSError:
    #        sys.stderr.write('Unable to copy files.')
    #        msg = 'Destination allready exists: {0}'
    #        sys.stderr.write(msg.format(dst))


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
