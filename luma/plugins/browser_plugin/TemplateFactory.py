import os

class TemplateFactory:
    """
    Handles loading of html templates
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
                    split = str(dependentFile).rsplit('.')
                    if os.path.isfile(dependentPath) and split[-1] == 'html':
                        retlist.append((str(file), str(localPath)))
            elif os.path.isfile(path):
                split = str(file).rsplit('.')
                if split[-1] == 'html':
                    retlist.append(('', str(file)))
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



