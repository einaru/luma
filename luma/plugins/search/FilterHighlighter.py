# -*- coding: utf-8 -*-
#
# plugins.search.FilterHighlighter
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

from PyQt4.QtCore import QRegExp
from PyQt4.QtGui import (QColor, QTextCharFormat, QSyntaxHighlighter)

def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    c = QColor(color)
    #c.setNamedColor(color)

    f = QTextCharFormat()
    f.setForeground(c)
    return f

STYLES = {
    'keyword' : format('magenta'),
    'brace' : format('blue'),
    'operator' : format('red'),
}

class LumaFilterHighlighter(QSyntaxHighlighter):
    """Enables highlighting of LDAP search filters.
    """
    keywords = ['objectClass']
    braces = [ '\(', '\)']
    operators = [
        '\&', '\|' '\!',
        '=', '\~=', '>=', '<=',
    ]
    
    def __init__(self, filter, attributes=[]):
        """
        @param attributes: list;
            a list of attributes to give
        TODO: the given attributes list doesn't register as keywords.
        """
        super(LumaFilterHighlighter, self).__init__(filter)
        
        self.keywords.extend(attributes)
        
        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
            for w in self.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
            for o in self.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
            for b in self.braces]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
            for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = expression.cap(nth).length()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
