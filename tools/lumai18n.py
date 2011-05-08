#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# lumai18n

# Copyright (C) 2011
#     Einar Uvsløkk, <einar.uvslokk@gmail.com>
# 
# program is free software: you can redistribute it and/or modify it
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
import sys

from optparse import (OptionParser, OptionGroup)

from lumarcc import (updateTranslationFiles, updateProjectFile)
from util.isocodes import (languages, countries)

short_description = """lumai18n.py - Luma Internationalization tool
copyright (c) Einar Uvsløkk 2011 einar.uvslokk@linux.com
"""
long_description="""
lumai18n.py is part of the Luma tool chain.

It creates a new translation source file following the Luma
internationalization naming conventions::

    luma_ll_CC.ts

where ``ll`` is a two-letter lowercase ISO 639 [1]_ language code,
and   ``CC`` is a two-letter uppercase ISO 3166 [2]_ country code.

.. [1] http://www.gnu.org/software/gettext/manual/gettext.html#Language-Codes
.. [2] http://www.gnu.org/software/gettext/manual/gettext.html#Country-Codes
"""

def listPossibleLanguageTranslations():
    """Displayes a list of possible new language translations to choose
    from.
    """
    # FIXME: This method should return a list of languages and
    #        countries. However, with what we go at this point,
    #        (see: util.isocodes) we have no way to dynamically map
    #        languages to countries in order to create the desired
    #        translation file name.
    raise NotImplementedError


def __getOptions(dictionary, criteria):
    """Helper method for `getLanguageCode` and `getCountryCode`.

    Returns a list of tuples where a match between `criteria` and a key
    in `dictionary` is found. A tuple in the returned list is on the
    form::

        (dictionary[key], key)
    
    Parameters:

    - `dictionary`: a dictionary to match keys against `criteria`.
    - `criteria`: the criteria to match against keys against.
    """
    options = []
    for key in dictionary.keys():
        if key.lower().find(criteria.lower()) != -1:
            options.append((dictionary[key], key))

    return options


def __getChoice(options, criteria, forwhat):
    """Helper method for `getLanguageCode` and `getCountryCode`.

    Called when `__getOptions` returns multiple options. The method
    displays the list of `options` and prompts the user for a choice.

    Returns the value in `options` that corresponds to the choice.

    Parameters:

    - `options`: a list of tuples to choose from.
    - `criteria`: the criteria that genreated `options`.
    - `forwhat`: the category for the criteria.
    """
    choice = None

    msg = 'More than one match was found for {0}: {1}\n'
    print msg.format(forwhat, criteria)

    for i, opt in enumerate(options):
        print '  ({0}) {1}'.format(i, opt[1])
    
    try:
        msg = '\nPlease choose a {0}: '
        input = raw_input(msg.format(forwhat))
        return options[int(input)][0]
    except KeyboardInterrupt:
        print '\nAborting on keyboard interrupt ...'
        sys.exit(1)


def getLanguageCode(language):
    """Returns the a two-letter lowercase ISO 639 language code for
    `language`. If no language code is found ``None`` is returned.
    """
    options = __getOptions(languages, language)

    if len(options) == 1:
        return options[0][0]
    elif len(options) > 1:
        return __getChoice(options, language, 'language')
    else:
        return None


def getCountryCode(country):
    """Returns the a two-letter uppercase ISO 3166 country code for
    `country`. If no country code is found ``None`` is returned.
    """
    options = __getOptions(countries, country)
    if len(options) == 1:
        return options[0][0]
    elif len(options) > 1:
        return __getChoice(options, country, 'country')
    else:
        return None


def createTranslationFile(langCode, countryCode=''):
    """Creates a new Luma translation file.

    The name of the translation file will be on the form::

        luma_`langCode`[_`countryCode`].ts

    I.e is `country` is not mandatory, and is only appended if it is
    provided. If a translation file with the same name already exists,
    file is not created.

    Parameters:
    
    - `langCode`: a two-letter lowletter ISO 639 language code.
    - `countryCode`: a two-letter uppercase ISO 3199 country code.
    """
    name = 'luma_{0}'.format(langCode)
    if countryCode != '':
        name = '{0}_{1}'.format(name, countryCode)
    name = '{0}.ts'.format(name)
    filepath = os.path.join('resources', 'i18n', name)

    if os.path.isfile(filepath):
        msg = 'A Luma translation file already exists with name: {0}'
        print msg.format(name)
        print 'The file will therefore _not_ be created...'
    else:
        print 'Luma translation file will be created:'
        print '  Destination: {0}'.format(filepath)
        try:
            file = open(filepath, 'w')
            file.close()
            ## Update the translation files with lumarcc.py
            ## FIXME: Figure out if we are able to easily fo this for
            ##        only spesific files.
            #updateProjectFile()
            #updateTranslationFiles()
            print 'Translation file succesfully created...'
        except IOError, e:
            print 'Unable to create translation file...'
            print str(e)


def main():
    global verbose, dryrun

    usage = '%prog [options] -l LANG -c COUNTRY'

    parser = OptionParser(usage=usage)

    # Main Options
    parser.add_option(
        '--list',
        dest='list', action='store_true',
        help='Display a list containing valid names for translation files ' +
        'that can be created by this script.'
    )
    parser.add_option(
        '-l', '--language',
        dest='lang', action='store', type='string', metavar='LANG',
        help='The name of the language to create translation file for. ' +
        'The script will try to look up the correct ISO 639 code to use.'
    )
    parser.add_option(
        '-L', '--LANG',
        dest='lang_code', action='store', type='string', metavar='CODE',
        help='A twoletter lowercase ISO 639 language code to create a ' +
        'translation file for.'
    )
    parser.add_option(
        '-c', '--country',
        dest='country', action='store', type='string', metavar='COUNTRY',
        help='The name of the country to create translation file for.' +
        'The script will try to look up the correct ISO 3166 code to use.'
    )
    parser.add_option(
        '-C', '--COUNTRY',
        dest='country_code', action='store', type='string', metavar='CODE',
        help='A twoletter lowercase ISO 3166 language code to create a' +
        'translation file for.'
    )
    # Debug Options
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

    if len(sys.argv) == 1:
        print short_description
        parser.print_help()
        sys.exit()

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

    if opt.list:
        listPossibleLanguageTranslations()
        sys.exit()

    if dryrun:
        print u'!!!!!!!!!!!!!!!\n!!! DRY-RUN !!!\n!!!!!!!!!!!!!!!'

    # The language is mandatory. If neither a language code or a
    # language name is given, or no match is returned for a given
    # language name, we abort the script.
    if opt.lang_code:
        lang = opt.lang_code
    elif opt.lang:
        lang = getLanguageCode(opt.lang)
        if lang is None:
            print 'No match was found for language: {0}'.format(language)
            print 'Aborting...'
            sys.exit(1)
    else:
        print "You need to provide either a language name or a language code!"
        print "Aborting ..."
        sys.exit(1)

    # The country is _not_ mandatory. It neither a country code or a
    # country name is given we simply assign country a empty string.
    if opt.country_code:
        country = opt.country_code
    elif opt.country:
        country = getCountryCode(opt.country)
    else:
        country = None

    createTranslationFile(lang, country)


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
