# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import os.path

from plugins.template_plugin.AddAttributeDialogDesign import AddAttributeDialogDesign
import environment


class AddAttributeDialog(AddAttributeDialogDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        AddAttributeDialogDesign.__init__(self,parent,name,modal,fl)
        
        self.mustLabel.setText("")
        self.singleLabel.setText("")
        self.binaryLabel.setText("")
        
        iconPrefix = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        self.okIcon = QPixmap(os.path.join(iconPrefix, "ok.png"))
        self.noIcon = QPixmap(os.path.join(iconPrefix, "no.png"))
        
        # This is a set of the attributes. Set up by the calling parent after
        # initalisation.
        self.attributes = None
        
        # Server meta information. Set up by the caller.
        self.metaInfo = None
        
        # The current objectclasses for the template.
        self.objectClasses = None
        
        # Dictionary with all attributes having a default value
        self.defaultValues = {}
        
###############################################################################

    def attributeChanged(self, item):
        name = str(item.text(0))
        must = self.metaInfo.isMust(name, self.objectClasses)
        single = self.metaInfo.isSingle(name)
        binary = self.metaInfo.isBinary(name)
        
        self.defaultEdit.blockSignals(True)
        self.defaultEdit.clear()
        
        if must:
            self.mustLabel.setPixmap(self.okIcon)
        else:
            self.mustLabel.setPixmap(self.noIcon)

        if single:
            self.singleLabel.setPixmap(self.okIcon)
        else:
            self.singleLabel.setPixmap(self.noIcon)

        if binary:
            self.binaryLabel.setPixmap(self.okIcon)
            self.defaultEdit.setEnabled(False)
        else:
            self.binaryLabel.setPixmap(self.noIcon)
            self.defaultEdit.setEnabled(True)
            if name in self.defaultValues.keys():
                self.defaultEdit.setText(self.defaultValues[name])
                
        self.defaultEdit.blockSignals(False)
            
###############################################################################

    def defaultChanged(self, defaultValue):
        attribute = str(self.attributeView.currentItem().text(0))
        self.defaultValues[attribute] = unicode(defaultValue)
    
