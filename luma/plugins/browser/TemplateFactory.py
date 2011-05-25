# -*- coding: utf-8 -*-
#
# Copyright (c) 2011
#     Per Ove Ringdal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
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

class TemplateFactory:
    """Handles loading of html templates.
    """

    def __init__(self, baseDir):
        self.baseDir = baseDir
        self.templateList = None
        self.templateDict = {}

    def getTemplateList(self):
        if self.templateList == None:
            self.templateList = self._createTemplateList()
        return self.templateList[:]

    def _createTemplateList(self):
        """
        templates
        |-- classic.html
        |-- classic-ignore.html
        |-- inetOrgPerson
            |-- person.html
        |-- organization
            |-- address.html
        """
        retlist = []
        for file in os.listdir(self.baseDir):
            path = os.path.join(self.baseDir, file)
            if os.path.isdir(path):
                for dependentFile in os.listdir(path):
                    localPath = os.path.join(file, dependentFile)
                    dependentPath = os.path.join(path, dependentFile)
                    split = dependentFile.rsplit('.')
                    if os.path.isfile(dependentPath) and split[-1] == 'html':
                        retlist.append((file, localPath))
            elif os.path.isfile(path):
                split = file.rsplit('.')
                if split[-1] == 'html':
                    retlist.append(('', file))
        retlist.sort()
        return retlist

    def getTemplateFile(self, fileName):
        if fileName not in self.templateDict:
            self.templateDict[fileName] = self._loadTemplateFile(fileName)
        return self.templateDict[fileName]

    def _loadTemplateFile(self, fileName):
        dir = os.path.join(self.baseDir, fileName)
        file = open(dir, 'r')
        text = file.read()
        file.close()
        return text


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
