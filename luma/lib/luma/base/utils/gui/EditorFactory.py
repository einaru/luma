# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2004,2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import string

from base.backend.SmartDataObject import SmartDataObject
from base.utils.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.utils.gui.editors.StandardEditor import StandardEditor
from base.utils.gui.editors.PasswordEditor import PasswordEditor
from base.utils.gui.editors.BinaryEditor import BinaryEditor
from base.utils.gui.editors.RdnEditor import RdnEditor

###############################################################################

# Warning. All attributes listed here must be lowercase
attributeDictionary = {'userpassword': PasswordEditor,
    'rdn': RdnEditor 
    }


###############################################################################

def getEditorWidget(parent, dataObject, attributeName, index=0):
    dialog = None
    
    # Do we have a direct mapping from attribute to editor?
    global attributeDictionary
    if attributeDictionary.has_key(string.lower(attributeName)):
        dialog = attributeDictionary[string.lower(attributeName)](parent)
        dialog.initValue(dataObject, attributeName, index)
        
    # We don't have a direct mapping
    else:
    
        # Is attribute binary?
        if dataObject.isAttributeBinary(attributeName):
        
            # Is attribute password?
            if dataObject.isAttributePassword(attributeName):
                dialog = PasswordEditor(parent)
            
            # Attribute is binary and not password.
            else:
                dialog = BinaryEditor(parent)
                dialog.initValue(dataObject, attributeName, index)
            
        # Attribute is not binary. Use standard editor.
        else:
            dialog = StandardEditor(parent)
            dialog.initValue(dataObject, attributeName, index)
            
    if None == dialog:
        raise Exception("No suitable editor dialog found")
    
    return dialog
    
