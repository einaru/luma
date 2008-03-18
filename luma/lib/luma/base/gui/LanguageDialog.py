# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from PyQt4 import QtCore
from PyQt4.QtGui import *
from os import listdir
from ConfigParser import *
from base.utils.backend.LogObject import LogObject

import os.path
import environment


class LanguageDialog():
    """A dialog for choosing the language to use. 
    
    After the dialog is shown, use getLanguageFile() to get the language
    file which should be used.
    """

    def __init__(self, configFile):

        # Read configuration file to find default langCode
        self.configFile = configFile
        self.configParser = ConfigParser()
        try:
            self.configParser.readfp(open(self.configFile, 'r'))
        except Exception, errorData:
            tmpString = "Could not read language settings file. Reason:\n"
            tmpString += str(errorData)
            environment.logMessage(LogObject("Debug", tmpString))
            
        if not(self.configParser.has_section("Defaults")):
            self.configParser.add_section("Defaults")
            
        self.selectedLangCode = "NATIVE"
        if self.configParser.has_option("Defaults", "language"):
            languageFile = self.configParser.get("Defaults", "language")
            languageFile = os.path.split(languageFile)[-1]
            if (languageFile[:5] == 'luma_') and (languageFile[-3:] == '.qm'):
                self.selectedLangCode = languageFile[5:-3]
            
        
        # List all language files
        self.trDir = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "i18n")
        self.languages = []
        for x in listdir(self.trDir):
            if (x[:5] == 'luma_') and (x[-3:] == '.qm'):
                self.languages.append(x[5:-3])

###############################################################################

    def getLanguageFile(self):
        """Returns the language file which should be used (string).
        
        If english is chosen, the string 'NATIVE' is returned. Because there 
        is not translation file for english, all installed translators should 
        be removed.
        
        """
        languages = QtCore.QStringList()

        # Since english is the default language, there is no language
        # file and we have to make the entry manually.
        languages.append("English")
        
        # Insert all languages which have a language file.
        # IMPORTANT: Has to be edited every time a new languaged is
        # added to luma.
        for x in self.languages:
            langName = self.getLanguageName(x)
            if not (None == langName):
                languages.append(langName)
        languages.sort()

        selectedIndex = languages.indexOf(self.getLanguageName(self.selectedLangCode))
        language, ok = QInputDialog.getItem(None, \
                self.__tr("Choose Language"), \
                self.__tr("Language:"), \
                languages, selectedIndex, False)

        if ok and not language.isEmpty():
            if language == self.getLanguageName(self.selectedLangCode):
                return None, False
            trFile = self._translageLangueToFile(language)
            self.saveLangSetting(trFile)
            return trFile, ok

        return "NATIVE", False

    def __tr(self,s,c = None):
        return qApp.translate("LanguageDialogDesign",s,c)
                
        
    def _translageLangueToFile(self, langName):
        tmpText = langName
        translationFile = 'NATIVE'
        
        if tmpText == "English":
            translationFile = 'NATIVE'
        elif tmpText == 'Czech':
            translationFile = "luma_cs.qm"
        elif tmpText == "German":
            translationFile = "luma_de.qm"
        elif tmpText == "French":
            translationFile = "luma_fr.qm"
        elif tmpText == "Norwegian":
            translationFile = "luma_no.qm"
        elif tmpText == "Portuguese":
            translationFile = "luma_br.qm"
        elif tmpText == "Russian":
            translationFile = "luma_ru.qm"
        elif tmpText == "Spanish":
            translationFile = "luma_es.qm"
        elif tmpText == "Swedish":
            translationFile = "luma_sv.qm"
        
        return os.path.join(self.trDir, translationFile)
        
###############################################################################

    def setCurrentLanguage(self, languageFile):
        if not ("NATIVE" == languageFile):
            if (languageFile[:5] == 'luma_') and (languageFile[-3:] == '.qm'):
                languageFile = languageFile[5:-3]
        
        self.selectedLangCode = languageFile
        
###############################################################################

    def saveLangSetting(self, trFile):
        self.configParser.set("Defaults", "language", trFile)
        
        try:
            self.configParser.write(open(self.configFile, 'w'))
        except Exception, errorData:
            tmpString = "Could not save language settings file. Reason:\n"
            tmpString += str(errorData)
            environment.logMessage(LogObject("Error", tmpString))

###############################################################################
            
    def getLanguageName(self, languageCode):
        if languageCode == 'cs':
            return "Czech"
        elif languageCode == 'de':
            return "German"
        elif languageCode == 'no':
            return "Norwegian"
        elif languageCode == 'br':
            return "Portuguese"
        elif languageCode == 'ru':
            return "Russian"
        elif languageCode == 'es':
            return "Spanish"
        elif languageCode == 'sv':
            return "Swedish"
        elif languageCode == 'fr':
            return "French"
        elif languageCode == 'NATIVE':
            return "English"
