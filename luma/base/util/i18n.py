# -*- coding: utf-8 -*-
#
# base.util.i18n
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
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
from PyQt4.QtCore import (QDir, QLocale, QString)


class LanguageHandler(object):
    """Helper class providing useful functionality for handling
    available application translations.
    """

    def __init__(self):
        self.__translationPath = QDir(':/i18n')
        self.__availableLanguages = {}
        # Must be put in manually because there exists no translation file
        # UPDATE: well it does now, but we'll keep it this way none the less
        #self.__availableLanguages['en'] = ['English', 'English']
        self.__buildLanguageDictionary()

    def __buildLanguageDictionary(self):
        """Builds the language dictionary used by the application. The
        dictionary is constructed with the locale code as key, and a
        list containing the language name (and possibly the country
        name) as value. The information is based on the ``i18n``entries
        in the ``resources.py`` module, where the alias for a one
        translation file is locale code for the translation.

        If the translation file is named ``luma_nn_NO.ts`` the
        corresponding alias for this file will be ``nb_NO``. Further
        more ``nb`` will map to ``QLocale.NorwegianBokmal``and ``NO``
        will map to ``QLocale.Norway``, resulting in the following entry
        in the dictionary::

            langDict = {
                ...,
                'en' : ['English'], # Default is allways included
                'nb_NO' : ['Norwegian', 'Norway'],
                ...
            }
        """
        for i18n in self.__translationPath:
            if i18n == 'hx':
                self.__availableLanguages[i18n] = ['leet', '10100111001']
            else:
                locale = QLocale(i18n)
                language = QLocale.languageToString(locale.language())
                country = QLocale.countryToString(locale.country())
                self.__availableLanguages[i18n] = [language, country]

    @property
    def availableLanguages(self):
        """Returns a dictionary containing all available language
        translations for the application. The dictionary returned
        is on the form::

            langDict = {
                ...,
                locale : [language[, country]],
                ...
            }
        """
        return self.__availableLanguages

    @property
    def translationPath(self):
        """Returns the full path to the directory containing the
        translation files.
        """
        return self.__translationPath

    def getQmFile(self, locale=''):
        """Returns the ``.qm`` files that matches `locale`. If `locale`
        is empty or ``None``, the ``.qm`` file for ``en`` is returned.

        :param locale: a two-letter lowercase ISO 639 language code,
          with a possible two-letter uppercase ISO 3199 country code,
          that corresponds to one of the ``i18n`` aliases in the
          resource file.
        :type locale: string
        """
        if locale == '' or locale == None:
            locale = 'en'

        return QString(':/i18n/{0}'.format(locale))


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
