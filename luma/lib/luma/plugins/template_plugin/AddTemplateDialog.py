# -*- coding: utf-8 -*-

from qt import *
import os.path
from string import strip

from plugins.template_plugin.AddTemplateDialogDesign import AddTemplateDialogDesign
from base.backend.ServerObject import ServerObject
from base.backend.ServerList import ServerList
import environment


class AddTemplateDialog(AddTemplateDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        AddTemplateDialogDesign.__init__(self,parent,name,modal,fl)
        
        self.templateList = []
        
        tmpFile  = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons", "secure.png")
        securePixmap = QPixmap(tmpFile)

        serverListObject = ServerList()
        serverListObject.readServerList()
        serverList = serverListObject.serverList
        
        if not (serverList == None):
            tmpList = []
            for x in serverList:
                tmpList.append(x.name)
            tmpList.sort()
            
            for x in tmpList:
                tmpObject = serverListObject.getServerObject(x)
                if not (x.encryptionMethod == u"None"):
                    self.serverBox.insertItem(securePixmap, tmpObject.name)
                else:
                    self.serverBox.insertItem(tmpObject.name)
                    
###############################################################################

    def valuesChanged(self):
        name = strip(unicode(self.nameEdit.text()))
        if len(name) > 0:
            if name in self.templateList:
                self.statusLabel.setText(self.trUtf8("A template with this name already exists."))
                self.okButton.setEnabled(False)
            else:
                self.okButton.setEnabled(True)
                self.statusLabel.setText(None)
        else:
            self.okButton.setEnabled(False)
            self.statusLabel.setText(self.trUtf8("Please supply a template name."))
            
            
            
            
