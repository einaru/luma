# -*- coding: utf-8 -*-

class AbstractEntryView:

    def __init__(self):
        pass

    @staticmethod
    def supportedViews(entryModel):
        """
        """
        pass
    def getName(self):
        """
        returns the name that will be displayed in the QComboBox
        """
        pass

    def initView(self, parent=None):
        pass

    def refreshView(self):
        pass

    def modelChanged(self):
        """
        called when the model is changed
        """
        pass
    def getWidget(self):
        """
        returns the widget that displays the view
        """
