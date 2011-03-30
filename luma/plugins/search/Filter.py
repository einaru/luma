# -*- coding: utf-8 -*-
#
# plugins.search.Filter
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
"""
This module contains methods for validating and parsing LDAP search
filters, and follows the 'LDAP String Representation of Search Filters'
specifications defined in RFC4514 [1].

Short form definition summary in EBNF:

    <filter>         := `(` <filterComp> `)`
    <filerComp>      :=  <boolComp> | <item>
    <boolComp>       := <boolOp> { <filter> }*
    <boolOp>         := `&` | `|` | `!`
    <item>           := <simple> | <exstensible>
    <simple>         := `(` <attr> <equalOp> <assertionValue> `)`
    <attr>           := (* a valid LDAP attribute *)
    <equalOp>        := `=` | `~=` | `>=` | `<=`
    <assertionValue> := <normal> | <escaped> | `*`
    <normal>         := (* all alphabetic and digit characters *)
    <escaped>        := `\`(* HEX representation of special chars *)
    <extensible>     := `(` (* TODO: learng the exstensible syntax :) *) `)`


[1] http://tools.ietf.org/html/rfc4515
"""
import re

SPECIAL_CHARS = {
    'NUL' : r'\00',
    '"' : r'\22',
    '(' : r'\28',
    ')' : r'\29',
    '*' : r'\2A',
    '+' : r'\2B',
    ',' : r'\2C',
    '/' : r'\2F',
    ';' : r'\3B',
    '<' : r'\3C',
    '=' : r'\3D',
    '>' : r'\3E',
    '\\' : r'\5C',
}
BOOLEAN_OPERATORS = {
    '&' : 'AND',
    '|' : 'OR',
    '!' : 'NOT'
}
EQUALITY_OPERATORS = {
    '=' : 'equals',
    '~=' : 'approximatly',
    '>=' : 'greater than or equals',
    '<=' : 'less than or equals'
}
LOWER = 'abcdefghijklmnopqrstuvwxyz'
UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGITS = '0123456789'
HEXDIGITS = '{0}{1}{2}'.format(DIGITS, LOWER[:6], UPPER[:6])
LETTERS = '{0}{1}'.format(LOWER, UPPER)
LPARENT = ')'
RPARENT = '('

# Regular expressions for various filter items
_filterRegex = ''
_filterCompRegex = '\(.*\)'
_attributeRegex = '\w*'
_assertionRegex = '=\w*[^=]'
_boolOpRegex = ''
_equalityOpRegex = ''

class UnmatchingParenthesesError(Exception):
    pass

def getAttributes(filter):
    """Finds all attributes present in an LDAP search filter.
    
    For example, the filter: 
    
        (&(objectClass=Person)(|(sn=Jensen)(cn=Babs J*))
    
    will return:
    
        ['sn', 'cn']
    
    @return: list;
        A list containing all attributes, might be the empty list.
    """
    regex = re.compile(_attributeRegex)
    raise NotImplementedError

def getAssertionValues(filter):
    """Finds all assertion values in an LDAP search filter.
    
    The filter:
    
        (&(objectClass=Person)(|(sn=Jensen)(cn=Babs J*))
    
    will return:
        
        ['Jensen', 'Babs J*']
    
    @return: list;
         list containing all assertion values, might be the empty list.
    """
    regex = re.compile(_assertionRegex)
    raise NotImplementedError

def getFilterComponents(filter):
    """Find all filter components in an LDAP search filter.
    
    The filter:
    
        (&(objectClass=Person)(|(sn=Jensen)(cn=Babs J*))
    
    will return:
        { '&' : ['objectClass=Person', {'|' : ['sn=Jensen', 'cn=Babs J*']}]}
    or
        [ '&', ['objectClass=Person', '|', ['sn=Jensen', 'cn=Babs J*']]]
    """
    regex = re.compile(_filterCompRegex)
    _ret = []
    _filter = regex.findall(filter)
    l = _filter[0]
    r = _filter[-1:]
    if l == LPARENT:
        if r == RPARENT:
            pass
        else:
            raise UnmatchingParenthesesError
    elif l in BOOLEAN_OPERATORS.keys():
        _ret.append(l)

i = 0
def test(filter):
    global i
    _r = re.compile(_filterCompRegex)
    _tmp = _r.findall(filter)
    print _tmp
    if i < 10:
        i += 1
        test(filter[1:-1])

complex = r"""
(?P<attr>[a-zA-Z_][a-zA-Z0-9_]*)
|(?P<equality_op>[=])
|(?P<bool_op>[&][|][!])
|(?P<lparent>[(])
|(?P<rparent>[)])
|(?P<equals>[=])
"""

complex2 = r"""
(?P<identifier>[a-zA-Z_][a-zA-Z0-9_]*)
|(?P<integer>[0-9]+)
|(?P<dot>\.)
|(?P<open_variable>[$][{])
|(?P<open_curly>[{])
|(?P<close_curly>[}])
|(?P<newline>\n)
|(?P<whitespace>\s+)
|(?P<equals>[=])
|(?P<slash>[/])
"""

token_re = re.compile(complex, re.VERBOSE)

class TokenizerException(Exception):
    pass

def tokenize(text):
    pos = 0
    while True:
        m = token_re.match(text, pos)
        if not m: break
        pos = m.end()
        tokname = m.lastgroup
        tokvalue = m.group(tokname)
        yield tokname, tokvalue
    if pos != len(text):
        raise TokenizerException('tokenizer stopped at pos %r of %r' % (pos, len(text)))

# Various test strings
filter = r'(!(objectClass=*)(&(objectGroup=group1)(dn=OLIVER)(!(posixShell~=zsh))))'
booleanOps = ['!', '&', '!']
equalityOps = ['=', '=', '=', '-=']
criterias = ['objectClass=*', 'objectGroup=group1', 'dn=OLIVER', 'posixShell~=zsh']
attributes = ['objectClass', 'objectGroup', 'dn', 'posixShell']


for tok in tokenize(filter):
    print tok

#test(filter)
#test('(test)(test)')
