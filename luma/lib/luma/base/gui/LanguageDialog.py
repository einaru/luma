# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from PyQt4.QtGui import *
from os import listdir
import os.path

from base.gui.LanguageDialogDesign import LanguageDialogDesign
import environment


class LanguageDialog(LanguageDialogDesign):
    """A dialog for choosing the language to use. 
    
    After the dialog is shown, use getLanguageFile() to get the language
    file which should be used.
    """

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        LanguageDialogDesign.__init__(self,parent,name,modal,fl)
        
        self.trDir = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "i18n")
        
        self.languages = []
        for x in listdir(self.trDir):
            if (x[:5] == 'luma_') and (x[-3:] == '.qm'):
                self.languages.append(x[5:-3])
        
        # Since english is the default language, there is no language
        # file and we have to make the entry manually.
        self.languageBox.insertItem("English")
        
        # Insert all languages which have a language file.
        # IMPORTANT: Has to be edited every time a new languaged is
        # added to luma.
        stringList = []
        for x in self.languages:
            langName = self.getLanguageName(x)
            if not (None == langName):
                stringList.append(langName)
                
        stringList.sort()
        map(self.languageBox.insertItem, stringList)
                

###############################################################################

    def getLanguageFile(self):
        """Returns the language file which should be used (string).
        
        If english is chosen, the string 'NATIVE' is returned. Because there 
        is not translation file for english, all installed translators should 
        be removed.
        
        """
        
        tmpText = str(self.languageBox.currentText())
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
        
        self.languageBox.setCurrentText(self.getLanguageName(languageFile))
        
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
