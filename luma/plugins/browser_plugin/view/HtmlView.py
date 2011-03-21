# -*- coding: utf-8 -*-
import os
import PyQt4
from PyQt4.QtCore import SIGNAL, QUrl, QString
from PyQt4.QtGui import QTextBrowser, QTextDocument
from plugins.browser_plugin.view.AbstractEntryView import AbstractEntryView

class HtmlView(AbstractEntryView):

    def __init__(self, entryModel, filepath, objectClass):
        AbstractEntryView.__init__(self)
        self.entryModel = entryModel
        self.filepath = filepath
        self.currentDocument = ""
        self.objectWidget = None

    @staticmethod
    def listfiles():
        retlist = []
        for dir in os.listdir("."):
            if dir == "templates" and os.path.isdir(dir):
                for subdir in os.listdir(dir):
                    objectClassDir = os.path.join(dir, subdir)
                    if os.path.isdir(objectClassDir):
                        for file in os.listdir(objectClassDir):
                            templateFile = os.path.join(objectClassDir, file)
                            split = str(file).rsplit(".")
                            if os.path.isfile(templateFile) and split[-1] == 'html':
                                retlist.append((templateFile, subdir))
        return retlist


    @staticmethod
    def supportedViews(entryModel):
        """
        """
        retlist = []
        smartObject = entryModel.getSmartObject()
        objectClasses = smartObject.getObjectClasses()
        for filepath, objectClass in HtmlView.listfiles():
            if objectClass in objectClasses:
                retlist.append(HtmlView(entryModel, filepath, objectClass))
        return retlist
        
    def getName(self):
        """
        returns the name that will be displayed in the QComboBox
        """
        return self.filepath

    def initWidget(self, parent=None):
        self.objectWidget = QTextBrowser(parent)
        self.objectWidget.setOpenLinks(False)
        self.objectWidget.connect(self.objectWidget, SIGNAL("anchorClicked(const QUrl&)"), self.anchorClicked)

    def refreshView(self):
        #TODO static file
        self.currentDocument = self.createDocument()
        self.objectWidget.setHtml(self.currentDocument)

    def modelChanged(self):
        """
        called when the model is changed
        """
        pass
    def getWidget(self):
        """
        returns the widget that displays the view
        """
        return self.objectWidget

    def createDocument(self):
        smartObject = self.entryModel.getSmartObject()
        text = open(self.filepath, "r").read()
        for attribute in smartObject.getAttributeList():
            i = 0
            for attributeValue in smartObject.getAttributeValueList(attribute):
                attribute_html = attribute + "__value"
                text = text.replace(attribute_html, attributeValue)
                i += 1


        return text

    def anchorClicked(self, url):
        print url
