import re
import string

class ConfigFileObject:
    def __init__(self, configPanelTmp=None):
        self.configPanel = configPanelTmp

        self.suffix = str(self.configPanel.suffix.text())
        self.admin = str(self.configPanel.adminName.text())
        self.password = str(self.configPanel.adminPassword.text())
        self.passwordVerify = str(self.configPanel.adminPasswordVerify.text())
        self.fileName = str(self.configPanel.saveFile.text())

        self.suffixDN = ""
        self.adminDN= ""

        self.configPanel.finishConfig.setDisabled(True)

        if self.checkInput():
            templateName = self.configPanel.distributionBox.currentText()
            fileValue = self.configPanel.distributionList[str(templateName)]
            templateFile = open(fileValue, 'r')
            templateList = templateFile.readlines()

            del templateList[0:2]

            confFile = open(self.fileName, 'w')
            for x in templateList:
                confFile.write(x)
            confFile.write(self.appendSuffix())
            confFile.write(self.appendRootDN())
            confFile.write(self.appendRootPW())

            confFile.close()

            self.configPanel.displayVariables(self.suffixDN, self.adminDN, self.password)

        self.configPanel.finishConfig.setDisabled(False)

    def appendSuffix(self):
        dnValues = string.split(self.suffix, '.')
        dnName = ""
        for x in dnValues:
            dnName = dnName + "dc=" + x + ","
        dnName = dnName[:-1]
        self.suffixDN = dnName
        returnValue = "\nsuffix\t" + dnName + "\n"
        return returnValue


    def appendRootDN(self):
        self.adminDN = "cn=" + self.admin + "," + self.suffixDN
        returnValue = "\nrootdn\t" + self.adminDN + "\n"
        return returnValue


    def appendRootPW(self):
        returnValue = "\nrootpw\t" + self.password + "\n"
        return returnValue


    def checkInput(self):
        if self.validSuffix():
            if self.validAdmin():
                if self.validPassword():
                    if self.validFile():
                        return 1
                    else:
                        self.configPanel.fileWarning()
                        return 0
                else:
                    self.configPanel.passwordWarning()
                    return 0
            else:
                self.configPanel.adminWarning()
                return 0
        else:
            self.configPanel.suffixWarning()
            return 0


    def validSuffix(self):
        suffixPattern = re.compile('^\w[\w.-]*\w$')
        suffixPattern2 = re.compile('.*[.-][.-].*')
        if suffixPattern.search(self.suffix):
            if suffixPattern2.search(self.suffix):
                return 0
            else:
                return 1
        else:
            return 0


    def validAdmin(self):
        adminPattern = re.compile('^[a-zA-Z]+$')
        if adminPattern.search(self.admin):
            return 1
        else:
            return 0


    def validPassword(self):
        if len(self.password) >= 6:
            if self.password == self.passwordVerify:
                return 1
            else:
                return 0
        else:
            return 0

    def validFile(self):
        if self.fileName == "":
            return 0
        else:
            return 1
