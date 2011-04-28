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
from .StandardEditor import StandardEditor
from .PasswordEditor import PasswordEditor
from .BinaryEditor import BinaryEditor
from .RdnEditor import RdnEditor

###############################################################################

# Warning. All attributes listed here must be lowercase
attributeDictionary = {'rdn': RdnEditor}


###############################################################################

def getEditorWidget(parent, smartObject, attributeName, index=0):
    dialog = None
    
    # Do we have a direct mapping from attribute to editor?
    global attributeDictionary
    if attributeDictionary.has_key(attributeName.lower()):
        dialog = attributeDictionary[attributeName.lower()](parent)
        dialog.initValue(smartObject, attributeName, index)
        
    # We don't have a direct mapping
    else:
        # Is attribute password?
        if smartObject.isAttributePassword(attributeName):
            dialog = PasswordEditor(parent)
    
        # Is attribute binary?
        elif smartObject.isAttributeBinary(attributeName):
            dialog = BinaryEditor(parent)
            dialog.initValue(smartObject, attributeName, index)
            
        # Attribute is not binary. Use standard editor.
        else:
            dialog = StandardEditor(parent)
            dialog.initValue(smartObject, attributeName, index)
            
    if dialog == None:
        raise Exception("No suitable editor dialog found")
    
    return dialog
    
