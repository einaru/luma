
class AbstractEntryView:

    def __init__(self):
        pass

    def supportsSmartObject(self, smartObject):
        """
        returns True if it supports view for the smartObject
        """
        pass
    def getName(self):
        """
        returns the name that will be displayed in the QComboBox
        """
        pass
    def getCurrentDocument(self):
        """
        returns the current document
        """
        pass
