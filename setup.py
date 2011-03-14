#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
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

import os
import sys
from glob import glob
from distutils.core import setup

import luma.__init__ as appinfo

DISTUTILS_DEBUG = 'f skd'

def fullSplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join)
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
    """
    Custom method to suplement distutils with a setuptools-like way of
    finding all package files
    """
    packages = []
    root_dir = os.path.dirname(__file__)
    if root_dir != '':
        os.chdir(root_dir)
    
    for path, names, files in os.walk(src_dir):
        for i, name in enumerate(names):
            if name.startswith('.'):
                del names[i]
        
        if '__init__.py' in files:
            s = fullSplit(path)
            if s[0] == src_dir:
                s[0] = app_dir
            
            packages.append('.'.join(s))
    return packages


textfiles = [
    'AUTHORS',
    'Changelog',
    'COPYING',
    'INSTALL',
    'README',
    'TODO',
]
desktopfile = 'data/luma.desktop'
extra = {}
src_dir = 'luma'
app_dir = 'luma'

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
_data_files = [
    ('share/luma/icons', glob('data/icons/*.png')),
    ('share/pixmaps', glob('data/icons/luma-48.png')),
    ('share/applications', glob('data/*.desktop')),
    ('share/man/man1', glob('data/man/luma.1.gz'))]

setup(
    name=appinfo.APPNAME,
    version=appinfo.VERSION,
    author='luma devel team',
    author_email='luma@ldap.brows.er',
    url='http://luma.sf.net',
    description=appinfo.DESCRIPTION,
    license='GNU General Public License (GPL) version 2',
    packages=findPackages(),
    package_dir={
        app_dir : src_dir
    },
    data_files=_data_files,
    scripts=['bin/luma'],
    #classifiers=_classifiers,
)


