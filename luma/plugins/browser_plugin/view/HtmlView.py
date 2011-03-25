# -*- coding: utf-8 -*-
import os
import copy
import PyQt4
from PyQt4.QtCore import SIGNAL, QUrl, QString, QXmlStreamReader, QString
from PyQt4.QtGui import QTextBrowser, QTextDocument, QInputDialog, QLineEdit
from plugins.browser_plugin.view.AbstractEntryView import AbstractEntryView

class HtmlView(QTextBrowser):

    def __init__(self, entryModel, parent=None):
        QTextBrowser.__init__(self, parent)
        self.entryModel = entryModel
        self.currentDocument = ""
        self.htmlTemplate = ""

        self.setOpenLinks(False)
        self.connect(self, SIGNAL("anchorClicked(const QUrl&)"), self.anchorClicked)



###############################################################################
###############################################################################
###############################################################################

    def anchorClicked(self, url):
        nameString = unicode(url.toString())
        tmpList = nameString.split("__")
        
        if tmpList[0] in self.entryModel.getSmartObject().getObjectClasses():
            self.entryModel.deleteObjectClass(tmpList[0])
            #self.refreshView()
        else:
            if not len(tmpList) == 3:
                return
            attributeName, index, operation = tmpList[0], int(tmpList[1]), tmpList[2]
            if operation == "edit":
                self.editAttribute(attributeName, index)
            elif operation == "delete":
                self.deleteAttribute(attributeName, index)
            elif operation == "export":
                self.exportAttribute(attributeName, index)

###############################################################################

    def editAttribute(self, attributeName, index):
        smartObject = self.entryModel.getSmartObject()
        oldDN = smartObject.getDN()
        
        if attributeName == 'RDN':
            # TODO correct this, used on creation?
            smartObject.setDN(self.baseDN)

        attributeValue = smartObject.getAttributeValue(attributeName, index)
        newValue, ok = QInputDialog.getText(self.objectWidget, 
                            self.trUtf8('Input dialog'), 
                            self.trUtf8('Attribute value:'), 
                            QLineEdit.Normal, 
                            attributeValue)
        if ok:
            newValue = unicode(newValue)
            if not newValue == None:
                self.entryModel.editAttribute(attributeName, index, newValue)
        else:
            if attributeName == 'RDN':
                # TODO correct this
                smartObject.setDN(oldDN)

###############################################################################

    def deleteAttribute(self, attributeName, index):
        self.entryModel.deleteAttribute(attributeName, index)

###############################################################################

    # TODO: not used yet
    def exportAttribute(self, attributeName, index):
        return
        """ Show the dialog for exporting binary attribute data.
        """
        '''
        value = self.ldapDataObject.getAttributeValue(attributeName, index)


        #filename = unicode(QFileDialog.getSaveFileName(
        #                    self,
        #fileName = unicode(QFileDialog.getSaveFileName(\
        #                    QString.null,
        #                    "All files (*)",
        #                    self, None,
        #                    self.trUtf8("Export binary attribute to file"),
        #                    None, 1))

        if unicode(fileName) == "":
            return
            
        try:
            fileHandler = open(fileName, "w")
            fileHandler.write(value)
            fileHandler.close()
            SAVED = True
        except IOError, e:
            result = QMessageBox.warning(None,
                self.trUtf8("Export binary attribute"),
                self.trUtf8("""Could not export binary data to file. Reason:
""" + str(e) + """\n\nPlease select another filename."""),
                self.trUtf8("&Cancel"),
                self.trUtf8("&OK"),
                None,
                1, -1)
        '''
