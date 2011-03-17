from AbstractLDAPTreeItem import AbstractLDAPTreeItem
from PyQt4.QtGui import qApp, QCursor
from PyQt4.QtCore import Qt
import logging

class RootTreeItem(AbstractLDAPTreeItem):
    """
    Represent the (invisible) root item of the model.
    """
    
    def __init__(self, title, parent = None):
        AbstractLDAPTreeItem.__init__(self, parent)
        self.title = title
        self.logger = logging.getLogger(__name__)
        
    def data(self, column):
        return self.title
    
    def columnCount(self):
        return 1
    
    def fetchChildList(self):
        return None
    
    def smartObject(self):
        return None
