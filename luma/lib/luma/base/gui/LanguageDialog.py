###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <wido.depping@tu-clausthal.de>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from qt import *
from base.gui.LanguageDialogDesign import LanguageDialogDesign
from base.backend.DirUtils import DirUtils
from os import listdir

class LanguageDialog(LanguageDialogDesign):
    """A dialog for choosing the language to use. 
    
    After the dialog is shown, use get_language_file() to get the language
    file which should be used.
    """

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        LanguageDialogDesign.__init__(self,parent,name,modal,fl)
        
        self.trDir = DirUtils().PREFIX + "/share/luma/i18n"
        
        self.languages = []
        for x in listdir(self.trDir):
            if (x[:5] == 'luma_') and (x[-3:] == '.qm'):
                self.languages.append(x[5:-3])
        
        # Since english is the default language, there is no language
        # file and we have to make the entry manually.
        pixmap = QPixmap(self.trDir + "/gb.png")
        self.languageBox.insertItem(pixmap, "English (UK)")
        
        # Insert all languages which have a language file.
        # IMPORTANT: Has to be edited every time a new languaged is
        # added to luma.
        for x in self.languages:
            if x == 'de':
                pixmap = QPixmap(self.trDir + "/" + x + ".png")
                self.languageBox.insertItem(pixmap, "Deutsch")
                continue
            if x == 'br':
                pixmap = QPixmap(self.trDir + "/" + x + ".png")
                self.languageBox.insertItem(pixmap, "Brazil")
                continue
                

###############################################################################

    def get_language_file(self):
        """Returns the language file which should be used (string).
        
        If english is chosen, the string 'NATIVE' is returned. Because there 
        is not translation file for english, all installed translators should 
        be removed.
        
        """
        
        tmpText = str(self.languageBox.currentText())
        
        if tmpText == "Deutsch":
            return self.trDir + "/luma_de.qm"
        elif tmpText == "Brazil":
            return self.trDir + "/luma_br.qm"
        elif tmpText == "English (UK)":
            return 'NATIVE'
        
