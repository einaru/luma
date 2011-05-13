# -*- coding: utf-8 -*-
#
# Copyright (C) 2004
#     Wido Depping, <widod@users.sourceforge.net>
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
import re
import base64


def lumaStringEncode(string):
    string = string.replace("\\", "\\\\")
    string = string.replace(",", r"\\\1")

    return string


def lumaStringDecode(string):
    string = unicode(string)
    string = string.replace(r"\\\1", ",")
    string = string.replace("\\\\", "\\")

    return string


def isBinaryAttribute(attr):
    """Returns ``True`` if `attr` is binary.

    :param attr: the attribute to validate
    :type attr: string
    """
    if attr == None:
        return False

    BINARY_PATTERN = '(^(\000|\n|\r| |:|<)|[\000\n\r\200-\377]+|[ ]+$)'
    binaryPattern = re.compile(BINARY_PATTERN)

    if binaryPattern.search(attr) == None:
        return False
    else:
        return True


def encodeBase64(text):
    """Returns `text` base64 encoded.

    :param text: the text to encode.
    :type text: string
    """
    return base64.encodestring(text)


def encodeUTF8(text, strip=False):
    """Helper method to get text objects in unicode utf-8 encoding.

    Returns the `text` encoded in ``utf-8`` and possibly stripped.

    :param text: the text to encode.
    :type text: string
    :param strip: wether or not to strip `text`.
    :type strip: boolean
    """
    if strip:
        text = text.strip()
    text = unicode(text).encode('utf-8')
    return text


def stripSpecialChars(string):
    """Returns `string` with LDAP special chars stripped back to their
    ascii equivalents. Pretty much the opposite of `escapeSpecialChars`.

    :param string: the string to strip
    :type string: string
    """
    string = string.replace(r'\5C', '\\')
    string = string.replace(r'\2C', ',')
    string = string.replace(r'\3D', '=')
    string = string.replace(r'\2B', '+')
    # string = string.replace(r'\"', '"')
    string = string.replace(r'\22', '"')
    string = string.replace(r'\3C', '<')
    string = string.replace(r'\3E', '>')
    string = string.replace(r'\3B', ';')

    return string


def escapeSpecialChars(string):
    """Returns `string` with all LDAP special chars escaped.

    :param string: the string to escape.
    :type string: string
    """
    tmpList = string.split('=')

    if 2 == len(tmpList):
        attribute = tmpList[0]
        value = "=".join(tmpList[1:])
        value = value.replace('\\', r'\5C')
        value = value.replace(',', r'\2C')
        value = value.replace('=', r'\3D')
        value = value.replace('+', r'\2B')
        # value = value.replace('"', r'\"')
        value = value.replace('"', r'\22')
        value = value.replace('<', r'\3C')
        value = value.replace('>', r'\3E')
        value = value.replace(';', r'\3B')

        tmpString = attribute + '=' + value

    return tmpString


specialCharDict = {
    'NUL': r'\00',
    '"': r'\22',
    '(': r'\28',
    ')': r'\29',
    '*': r'\2A',
    '+': r'\2B',
    ',': r'\2C',
    '/': r'\2F',
    ';': r'\3B',
    '<': r'\3C',
    '=': r'\3D',
    '>': r'\3E',
    '\\': r'\5C',
}


def escapeSpecialChar(char):
    """Returnes the escaped `char`
    """
    return specialCharDict[char]


def explodeDN(dnString):
    """Returns a list of dn tokens. I.e. `dnString` is split into the
    attribute it contains.

    :param dnString: a dnString with attributes seperated by commas.
    :type dnString: string
    """

    dnList = dnString.split(',')

    tokenList = []
    for x in xrange(0, len(dnList)):
        value = dnList[x]
        if "=" in value:
            tokenList.append(value)
        else:
            if len(tokenList) > 0:
                tokenList[-1] = tokenList[-1] + ',' + value

    return tokenList


def getSortedDnList(dnList):
    """Returns a sorted list for distinguished names.

    The higher the object in the tree, the more it will be at the
    beginning of the sorted list. Leaves should be at the end of the
    list.

    :param dnList: a list of distinguised names.
    :type dnList: list
    """
    dnList.sort(__dnCompare)

    return dnList


def escapeDnChars(dn):
    """Returns `dn` with all spesial chars escapes.

    :param dn: the DN to escape.
    :type dn: string
    """
    dn = dn.replace('\,', r'\2C')
    dn = dn.replace('\=', r'\3D')
    dn = dn.replace('\+', r'\2B')

    return dn


def __dnCompare(firstDN, secondDN):
    firstList = explodeDN(firstDN)
    secondList = explodeDN(secondDN)

    return cmp(len(firstList), len(secondList))


def testEscaping():
    assert r"cn=foo" == escapeSpecialChars("cn=foo")
    assert r"cn=foo\2C" == escapeSpecialChars("cn=foo,")
    assert r"cn=foo\5C" == escapeSpecialChars("cn=foo\\")
    assert r"cn=foo\5C\2C" == escapeSpecialChars("cn=foo\\,")
    assert r"cn=\22foo\22" == escapeSpecialChars("cn=\"foo\"")

    assert "cn=foo" == stripSpecialChars(r"cn=foo")
    assert "cn=foo," == stripSpecialChars(r"cn=foo\2C")
    assert "cn=foo\\" == stripSpecialChars(r"cn=foo\5C")
    assert "cn=foo\\," == stripSpecialChars(r"cn=foo\5C\2C")
    assert "cn=\"foo\"" == stripSpecialChars(r"cn=\22foo\22")


if __name__ == "__main__":
    testEscaping()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
