#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# dictgen
#
# Copyright (C) 2011
#     Einar Uvsløkk, <einar.uvslokk@linux.com>
# 
# dictgen is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# oya-invitationals is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
import os

from PyQt4.QtCore import QLocale

def write(file, lines):

    with open(file, 'w') as f:
        for line in lines:
            f.write(line)

def transform(inputfile, dictname):

    output = []
    with open(inputfile, 'r') as input:

        output.append(dictname + '= {\n')
        for line in input:
            tmp = line.strip().split(' ', 1)

            code = tmp[0]
            lang = tmp[1]
            
            abrivations = lang.split(';')
            if len(abrivations) == 1:
                out = '    "{0}" : "{1}",\n'.format(abrivations[0], code)
                output.append(out)
            else:
                for abr in abrivations:
                    out = '    "{0}" : "{1}",\n'.format(abr.strip(), code)
                    output.append(out)

        output.append('}\n\n')

    return output


def generateDict(verbose=False):
    # As per the Qt4.7 documentation the QLocale.Language enumeration
    # ranges from 1 to 214:
    # http://doc.trolltech.com/4.7/qlocale.html#Language-enum
    lines = ['locales = {\n']
    for l in xrange(1, 214):
        lang = QLocale.languageToString(l)
        for c in QLocale.countriesForLanguage(l):
            code = QLocale(l, c).name()
            country = QLocale.countryToString(c)
            if verbose:
                print code, lang, country
            line = "    '{0}' : ['{1}', '{2}'],\n"
            lines.append(line.format(code, lang, country))

    lines.append('}\n\n')
    return lines




if __name__ == '__main__':
    ## ISO 639 - language codes
    #lines = transform(os.path.join('files', 'ISO-639.txt'), 'languages')
    ## ISO 3166 - country codes
    #lines.extend(transform(os.path.join('files', 'ISO-3166.txt'), 'countries'))
    #write(file='isocodes.py', lines=lines)
    write(file='locale.py', lines=generateDict())


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
