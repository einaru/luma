# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004,2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from base.backend.SmartDataObject import SmartDataObject
from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.utils.gui.editors.StandardEditor import StandardEditor
from base.utils.gui.editors.PasswordEditor import PasswordEditor
from base.utils.gui.editors.BinaryEditor import BinaryEditor
from base.utils.gui.editors.RdnEditor import RdnEditor

###############################################################################

# Warning. All attributes listed here must be lowercase
attributeDictionary = {'rdn': RdnEditor}


###############################################################################

def getEditorWidget(parent, dataObject, attributeName, index=0):
    dialog = None
    
    # Do we have a direct mapping from attribute to editor?
    global attributeDictionary
    if attributeDictionary.has_key(attributeName.lower()):
        dialog = attributeDictionary[attributeName.lower()](parent)
        dialog.initValue(dataObject, attributeName, index)
        
    # We don't have a direct mapping
    else:
        # Is attribute password?
        if dataObject.isAttributePassword(attributeName):
            dialog = PasswordEditor(parent)
    
        # Is attribute binary?
        elif dataObject.isAttributeBinary(attributeName):
            dialog = BinaryEditor(parent)
            dialog.initValue(dataObject, attributeName, index)
            
        # Attribute is not binary. Use standard editor.
        else:
            dialog = StandardEditor(parent)
            dialog.initValue(dataObject, attributeName, index)
            
    if dialog == None:
        raise Exception("No suitable editor dialog found")
    
    return dialog
    
