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
This script uses Google Translate to generate native names for languages
we uses and might use in our application.

Predefined is a dictionary containing 2 char language codes defined in the
ISO 638-1 standard [1], as well as the english name of the language.
The english name is used to get the native name.

NB! don't blindly trust the returned translation from Google,
    some post-adjustment might be necessary for some languages,
    (i.e 'Norwegian' is translated to 'Norske' but should be 'Norsk')

[1] http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
"""
import os
import json
from urllib2 import urlopen
from urllib import urlencode

# Google Translate supported languages
iso = {
    u'af' : u'Afrikaans',
    u'sq' : u'Albanian',
    u'ar' : u'Arabic',
    u'be' : u'Belarusian',
    u'bg' : u'Bulgarian',
    u'ca' : u'Catalan',
    u'zh' : u'Chinese',
    u'hr' : u'Croatian',
    u'cs' : u'Czech',
    u'da' : u'Danish',
    u'nl' : u'Dutch',
    u'en' : u'English',
    u'et' : u'Estonian',
    u'tl' : u'Filipino',
    u'fi' : u'Finnish',
    u'fr' : u'French',
    u'gl' : u'Galician',
    u'de' : u'German',
    u'el' : u'Greek',
    u'he' : u'Hebrew',
    u'hi' : u'Hindi',
    u'hu' : u'Hungarian',
    u'is' : u'Icelandic',
    u'id' : u'Indonesian',
    u'ga' : u'Irish',
    u'it' : u'Italian',
    u'ja' : u'Japanese',
    u'ko' : u'Korean',
    u'lv' : u'Latvian',
    u'lt' : u'Lithuanian',
    u'mk' : u'Macedonian',
    u'ms' : u'Malay',
    u'mt' : u'Maltese',
    u'no' : u'Norwegian',
    u'fa' : u'Persian',
    u'pl' : u'Polish',
    u'pt' : u'Portuguese',
    u'ro' : u'Romanian',
    u'ru' : u'Russian',
    u'sr' : u'Serbian',
    u'sk' : u'Slovak',
    u'sl' : u'Slovenian',
    u'es' : u'Spanish',
    u'sw' : u'Swahili',
    u'sv' : u'Swedish',
    u'th' : u'Thai',
    u'tr' : u'Turkish',
    u'uk' : u'Ukrainian',
    u'vi' : u'Vietnamese',
    u'cy' : u'Welsh',
    u'yi' : u'Yiddish'
}

base_url='http://ajax.googleapis.com/ajax/services/language/translate?'

def getNativeLanguageNamesFromGoogleTranslate(param='haha'):
    """
    The google translate API can be found here: 
    http://code.google.com/apis/ajaxlanguage/documentation/#Examples
    """
    result = []
    result.append('iso_native = {\n')
    for target, text in iso.iteritems():
        langpair='en|%s' % target
        params = urlencode((('v', 1.0), ('q', text), ('langpair', langpair),))
        url = base_url + params
        content = urlopen(url).read()
        try:
            trans_dict=json.loads(content)
            print(trans_dict['responseData']['translatedText'])
            native = (trans_dict['responseData']['translatedText'])
            result.append("u'%s' : u'%s', # %s\n" % (target, native, text))
        except AttributeError:
            print('Unable to translate to %s' % target)
    result.append('}')
    writeToDisk(result)

def writeToDisk(list):
    #list = ['sdsd', 'asfsdf', 'dsf', 'lkop', 'qweqwr']
    outputFile = u'translate-output-iso.py'
    path = os.path.join(os.getcwd(), outputFile)
    file = open(path, 'w')
    print u'Generated iso dictionary will be written to:\n' + \
          u'\t%s' % (outputFile) 
    for i in sorted(list):
        print i
        file.write(i)
    file.close()

if __name__ == '__main__':
    getNativeLanguageNamesFromGoogleTranslate()