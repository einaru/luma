# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *
from os import listdir
import os.path

from base.gui.LanguageDialogDesign import LanguageDialogDesign
import environment


class LanguageDialog(LanguageDialogDesign):
    """A dialog for choosing the language to use. 
    
    After the dialog is shown, use get_language_file() to get the language
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
        pixmap = QPixmap(os.path.join(self.trDir, "gb.png"))
        self.languageBox.insertItem(pixmap, "English (UK)")
        
        # Insert all languages which have a language file.
        # IMPORTANT: Has to be edited every time a new languaged is
        # added to luma.
        for x in self.languages:
            pixmap = QPixmap(os.path.join(self.trDir, x + ".png"))
            
            
            if x == 'br':
                self.languageBox.insertItem(pixmap, "Brazilian")
                continue
            elif x == 'de':
                self.languageBox.insertItem(pixmap, "German")
                continue
            elif x == 'no':
                self.languageBox.insertItem(pixmap, "Norwegian")
                continue
            elif x == 'ru':
                self.languageBox.insertItem(pixmap, "Russian")
                continue
            elif x == 'es':
                self.languageBox.insertItem(pixmap, "Spanish")
                continue
            elif x == 'sv':
                self.languageBox.insertItem(pixmap, "Swedish")
                continue
                

###############################################################################

    def get_language_file(self):
        """Returns the language file which should be used (string).
        
        If english is chosen, the string 'NATIVE' is returned. Because there 
        is not translation file for english, all installed translators should 
        be removed.
        
        """
        
        tmpText = str(self.languageBox.currentText())
        translationFile = 'NATIVE'
        
        if tmpText == "Germany":
            translationFile = "luma_de.qm"
        elif tmpText == "Brazil":
            translationFile = "luma_br.qm"
        elif tmpText == "English (UK)":
            translationFile = 'NATIVE'
        elif tmpText == "Spain":
            translationFile = "luma_es.qm"
        elif tmpText == "Norway":
            translationFile = "luma_no.qm"
        elif tmpText == "Russia":
            translationFile = "luma_ru.qm"
        elif tmpText == "Sweden":
            translationFile = "luma_sv.qm"
        
        return os.path.join(self.trDir, translationFile)
        
