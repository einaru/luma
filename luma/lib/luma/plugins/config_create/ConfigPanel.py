# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


import re
from os import listdir
import os.path

from qt import *

from plugins.config_create.ConfigPanelDesign import ConfigPanelDesign
from plugins.config_create.ConfigError import ConfigError
from plugins.config_create.ConfigFileObject import ConfigFileObject
import environment

class ConfigPanel(ConfigPanelDesign):
    def __init__(self, parent=None):
        ConfigPanelDesign.__init__(self, parent)

        self.setName("PLUGIN_CONFIG_CREATOR")

        self.prefix = os.path.join( environment.lumaInstallationPrefix, "lib", "luma", "plugins", "config_create")
        iconPrefix = os.path.join( environment.lumaInstallationPrefix, "share", "luma", "icons", "plugins", "config_create")

        helpIcon = QPixmap(os.path.join(iconPrefix, "help.png"))
        
        self.helpSuffix = ConfigError(self)
        self.helpSuffix.suffixIcon.setPixmap(helpIcon)
        self.helpSuffix.errorLabel.setText(self.trUtf8("Help for Suffix:"))

        self.helpAdmin = ConfigError(self)
        self.helpAdmin.suffixIcon.setPixmap(helpIcon)
        self.helpAdmin.errorLabel.setText(self.trUtf8("Help for Admin Name:"))

        self.helpDistribution = ConfigError(self)
        self.helpDistribution.suffixIcon.setPixmap(helpIcon)
        self.helpDistribution.errorLabel.setText(self.trUtf8("Help for Distribution:"))

        self.helpPassword = ConfigError(self)
        self.helpPassword.suffixIcon.setPixmap(helpIcon)
        self.helpPassword.errorLabel.setText(self.trUtf8("Help for Password:"))

        errorIcon = QPixmap(os.path.join(iconPrefix, "error.png"))
        
        self.warningSuffix = ConfigError(self)
        self.warningSuffix.suffixIcon.setPixmap(errorIcon)
        self.warningSuffix.errorLabel.setText(self.trUtf8("Bad Suffix!"))

        self.warningAdmin = ConfigError(self)
        self.warningAdmin.suffixIcon.setPixmap(errorIcon)
        self.warningAdmin.errorLabel.setText(self.trUtf8("Bad Admin Name!"))

        self.warningPassword = ConfigError(self)
        self.warningPassword.suffixIcon.setPixmap(errorIcon)
        self.warningPassword.errorLabel.setText(self.trUtf8("Bad Password!"))

        self.warningFile = ConfigError(self)
        self.warningFile.suffixIcon.setPixmap(errorIcon)
        self.warningFile.errorLabel.setText(self.trUtf8("Bad File Name!"))

        self.dataInformation = ConfigError(self)
        self.dataInformation.suffixIcon.setPixmap(QPixmap(os.path.join(iconPrefix, "final.png")))

        self.distributionList = {}
        self.readDistributionPreferences()



    def displaySuffixHelp(self):
        self.helpSuffix.show()

    def displayAdminNameHelp(self):
        self.helpAdmin.show()

    def displayPasswordHelp(self):
        self.helpPassword.show()

    def displayDistributionHelp(self):
        self.helpDistribution.show()

    def displayFileChooser(self):
        saveFileName = QFileDialog.getSaveFileName("", "*", self, "FileDialog")
        self.saveFile.setText(saveFileName)

    def createConfig(self):
        configObject = ConfigFileObject(self)

    def suffixWarning(self):
        self.warningSuffix.show()

    def adminWarning(self):
        self.warningAdmin.show()

    def passwordWarning(self):
        self.warningPassword.show()

    def fileWarning(self):
        self.warningFile.show()

    def readDistributionPreferences(self):
        templatePattern = re.compile('.template$')

        distributionDir = os.path.join(self.prefix, "distributions")

        fileList = listdir(distributionDir)

        for x in fileList:
            if templatePattern.search(x):
                datei = open(os.path.join(distributionDir, x), 'r')
                firstLine = datei.readline()
                key = firstLine[:6]
                if key == "TITLE=":
                    value = firstLine[6:-1]
                    self.distributionBox.insertItem(value)
                    self.distributionList[value] = os.path.join(distributionDir, x)
                datei.close()

    def displayVariables(self, suffix, rootDN, password):
        infoString = "<b><u>Server Information</u></b><br><br><b>REMEMBER THESE INFORMATIONS!!!</b><br>"
        infoString = infoString + "<u>Suffix:</u> " + suffix + "<br>"
        infoString = infoString + "<u>Admin Name:</u> " + rootDN + "<br>"
        infoString = infoString + "<u>Password:</u> " + password + "<br>"
        self.dataInformation.errorLabel.setText(infoString)
        self.dataInformation.adjustSize()
        self.dataInformation.show()
