import logging
import ldap
from string import replace

from PyQt4 import QtGui, QtCore
from .DeleteDialogDesign import Ui_DeleteDialog
from .ExportDialogDesign import Ui_ExportDialog
from base.util.IconTheme import (pixmapFromTheme, iconFromTheme)
from base.util.Paths import getUserHomeDir
from base.backend.LumaConnectionWrapper import LumaConnectionWrapper

def getRep(serverObject):
    """Returns a representation name for a `serverObject`. This way
    we are able to distinguish between items with identical DNs on
    different servers when exporting or deleting. The representation
    is on the form::

        [serverAlias] distinguishedName 

    Parameters:

    - `serverObject`: the `ServerObject` to get the representation for.
    """
    alias = serverObject.getServerAlias()
    dn = serverObject.getPrettyDN()
    return '[' + alias + '] ' + dn



class DeleteDialog(QtGui.QDialog, Ui_DeleteDialog):
    
    __logger = logging.getLogger(__name__)
    
    def __init__(self, sOList, subTree = True, parent=None):
        """
        subTree: 
            False = only sOList
            True = subtree of SOList
        """
        super(DeleteDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.iconLabel.setPixmap(pixmapFromTheme(
            'document-close', ':/icons/64/document-close'))

        self.model = QtGui.QStandardItemModel()

        self.model.setHorizontalHeaderLabels(["DN","Status"])
        self.items = sOList
        self.deleteDict = {}
        
        self.subTree = subTree        
        self.serverConnections = {}
        
        if not self.subTree: # The nodes only
            for smd in self.items:
                self.addItemToModel(smd)
        else:
            # Load subtrees
            for sO in self.items:
                if not self.serverConnections.has_key(sO.serverMeta.name):
                    self.serverConnections[sO.serverMeta.name] = LumaConnectionWrapper(sO.serverMeta)
                    self.serverConnections[sO.serverMeta.name].bindSync()
                con = self.serverConnections[sO.serverMeta.name]
                # Subtree 
                success, result, e = con.searchSync(base=sO.getDN(), scope=ldap.SCOPE_SUBTREE)
                if success:
                    for i in result:
                        # Subtree only
                        if i.getDN() == sO.getDN():
                            continue
                        self.addItemToModel(i)
                else:
                    continue

        self.deleteItemView.setModel(self.model)
        self.deleteItemView.setAlternatingRowColors(True)
        self.deleteItemView.setUniformRowHeights(True)
        
        self.hasTriedToDelete = False
        self.passedItemsWasDeleted = False
    
    # Made this a module method in order to use it in the ExportDialog aswell
    #
    #def getRep(self, sO):
    #    serverName = sO.getServerAlias()
    #    dn = sO.getPrettyDN()
    #    #return str(dn+" ["+serverName+"]") # This results in a decode error
    #    return dn + ' [' + serverName + ']'

    def addItemToModel(self, smartDataObject):
        # Find a textual representation for the smartobjects
        rep = getRep(smartDataObject)
    
        # Make and item with text rep
        modelItem = QtGui.QStandardItem(rep)
        modelItem.setEditable(False)
        modelItem.setCheckable(True)
        
        # Represents the status of the deletion
        statusItem = QtGui.QStandardItem("")
        statusItem.setEditable(False)
        
        # Dict where one can lookup reps to get smartObjects and modelitems
        self.deleteDict[rep] = [smartDataObject, modelItem, statusItem]
        modelItem.setCheckState(QtCore.Qt.Checked)
        self.model.appendRow([modelItem,statusItem])
            
    def delete(self):
        
        self.deleteButton.setEnabled(False)
        if self.hasTriedToDelete:
            # Should not be called twice
            return
        
        # At his point, we don't "cancel" but say we're done
        self.cancelButton.setText("Done")
        self.hasTriedToDelete = True
        allDeleted = True
        
        # True for now
        self.passedItemsWasDeleted = True
        
        # Iterate through the modelitems and remove unchekced items
        # from the dictionary, which will be used later.
        for i in xrange(self.model.rowCount()):
            item = self.model.itemFromIndex(self.model.index(i, 0))
            if item.checkState() != QtCore.Qt.Checked:
                self.deleteDict.pop(self.__utf8(item.text()))
                # If we unchecked something, can't be sure the passed items was deleted
                self.passedItemsWasDeleted = False
        
        # Map the dictionary keys
        deleteSOList = map(lambda x: self.deleteDict[x][0], self.deleteDict.keys())
        deleteSOList.sort(key=lambda x: len(x.getDN())) #parents first (sorted by length)
        deleteSOList.reverse()
        
        # We now have a list with smartObjects to be deleted, so let's do so
        # TODO Do in thread?
        for sO in deleteSOList:
            # Create a LumaConnection if necessary
            if not self.serverConnections.has_key(sO.serverMeta.name):
                self.serverConnections[sO.serverMeta.name] = LumaConnectionWrapper(sO.serverMeta)
                self.serverConnections[sO.serverMeta.name].bindSync()
            
            # Use it to delete the object on the server
            conn = self.serverConnections[sO.serverMeta.name]
            status, e = conn.delete(sO.getDN())
            
            # Update the status in the dialog
            if not status:
                self.passedItemsWasDeleted = False
                allDeleted = False
                self.deleteDict[getRep(sO)][2].setText(str(e))
            else:
                self.deleteDict[getRep(sO)][2].setText("OK!")
        
        # Remember to unbind all the servers
        for conn in self.serverConnections.values():
            conn.unbind()
            
        # If everything we wanted to delete was deleted -- close
        #if allDeleted:
        #    self.accept()
            
    def cancel(self):
        if self.hasTriedToDelete:
            self.accept() #Let the caller know delete() was run
        else:
            self.reject() #No changes done on the server
        
    def __utf8(self, text):
        return unicode(text).encode('utf-8').strip()

    def accept(self):
        for conn in self.serverConnections.values():
            conn.unbind()
        QDialog.accept(self)

    def reject(self):
        for conn in self.serverConnections.values():
            conn.unbind()
        QDialog.reject(self)

        
import dsml
import StringIO


class ExportDialog(QtGui.QDialog, Ui_ExportDialog):
    """The dialog for exporting ldap entries to disk.
    
    TODO: enable|disable export button when filename|nofilename is defined
    TODO: better feedback if something goes wrong, perhaps not accept(), if
          not all checked items get exported ?
    """
    
    __logger = logging.getLogger(__name__)
    
    def __init__(self, msg='', parent=None):
        """
        @param items:
            The list of items to export.
        @param msg:
            A message to display in the dialog. Might be information
            about problems with fetching all the LDAP entries, etc.
        """
        super(ExportDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.iconLabel.setPixmap(pixmapFromTheme(
            'document-save', ':/icons/64/document-export'))
        self.fileButton.setIcon(iconFromTheme(
            'document-open', ':/icons/32/document-open'))
        self.messageLabel.setText(msg)
        
        self.model = QtGui.QStandardItemModel()
        self.exportItemView.setModel(self.model)
        self.exportItemView.setAlternatingRowColors(True)
        self.exportItemView.setUniformItemSizes(True)
        self.exportDict = {}
        
        # Disabled until path set
        self.exportButton.setEnabled(False)
        # If the users manually edits the path, we'll trust him
        #self.outputEdit.textEdited.connect(self.enableExport)
        # The signal textEdit is not emitted if the text is changed
        # programmatically, we therefore use textChanged instead.
        self.outputEdit.textChanged['QString'].connect(self.onFilenameChanged)

    
    def enableExport(self):
        """Enable the export-button
        """
        self.exportButton.setEnabled(True)
    
    def __utf8(self, text):
        """Helper method for encoding in unicode utf-8, which is
        helpful in particular when working with QStrings.

        Returns a (optionally strpped) unicode utf-8 encoded string.
        
        Parameters:

        - `text`: the text object to encode.
        """
        return unicode(text).encode('utf-8').strip()
    
    def setExportItems(self, data):
        """Sets the items to be exported.
        
        Populates the model.
        """
        self.data = data
        for item in self.data:
            rep = getRep(item)
            modelItem = QtGui.QStandardItem(rep)
            modelItem.setEditable(False)
            modelItem.setCheckable(True)
            
            self.exportDict[rep] = [item, modelItem]
            modelItem.setCheckState(QtCore.Qt.Checked)
            self.model.appendRow(modelItem)
    
    def openFileDialog(self):
        """Slot for the file button.
        
        Opens a File Dialog to let the user choose where to export.
        """
        userdir = getUserHomeDir()
        filter = "LDIF files (*.ldif);;DSML files (*dsml)"
        filename = QtGui.QFileDialog.getSaveFileName(self,
                                                     caption='Select export file',
                                                     directory=userdir,
                                                     filter=filter)
        # Return if the user canceled the dialog
        if filename == "":
            return
        
        filename = self.__utf8(filename)
        filter = self.__utf8(self.formatBox.currentText())
        if filter.startswith('LDIF') and not filename.endswith('.ldif'):
            filename = '%s.ldif' % filename
        elif filter.startswith('DSML') and not filename.endswith('.dsml'):
            filename = '%s.dsml' % filename
 
        self.outputEdit.setText(filename)
        #self.exportButton.setEnabled(True)
    
    def onFormatChanged(self, format):
        """Slot for the format combobox.
        
        Checks if the output file is defined and wether its filending
        matches the choosen export format. If not defined the method
        returns. If the filening doesn't match, it is switched.
        """
        if self.outputEdit.text() == '':
            #self.exportButton.setEnabled(False) #Re-disable if there's nothing there
            return
        format = self.__utf8(format)
        oldname = self.outputEdit.text()
        if format == 'LDIF':
            newname = replace(oldname, '.dsml', '.ldif')
        elif format == 'DSML':
            newname = replace(oldname, '.ldif', '.dsml')
        self.outputEdit.setText(newname)

    def onFilenameChanged(self, filename):
        """Slot for the filename edit.

        Enabels|disables the export button.
        """
        if self.__utf8(filename) ==  '':
            self.exportButton.setEnabled(False)
        else:
            self.exportButton.setEnabled(True)

    def export(self):
        """Slot for the export button.
        
        Exports all checked items to the file defined in the outputEdit
        widget.
        """
        # Iterate through the modelitems and remove unchekced items
        # from the export dictionary, which will be used later.
        for i in xrange(self.model.rowCount()):
            item = self.model.itemFromIndex(self.model.index(i, 0))
            if item.checkState() != QtCore.Qt.Checked:
                del self.exportDict[self.__utf8(item.text())]
        
        # Map the dictionary keys
        #
        itemList = map(lambda x: self.exportDict[x][0], self.exportDict.keys())
        itemList.sort()
        try:
            filename = self.outputEdit.text()
            fileHandler = open(filename, 'w')
            format = self.__utf8(self.formatBox.currentText())
            
            
            # DSML need some header info.
            if format == 'DSML':
                tmp = StringIO.StringIO()
                dsmlWriter = dsml.DSMLWriter(tmp)
                dsmlWriter.writeHeader()
                fileHandler.write(tmp.getvalue())
            
            # Write the LDAP entries to file
            for x in itemList:
                try:
                    if format == 'LDIF':
                        fileHandler.write(x.convertToLdif())
                    
                    elif format == 'DSML':
                        fileHandler.write(x.convertToDsml())
                except IOError, e:
                    msg = 'Could not export %s. Reason\n%s' % (str(x), str(e))
                    self.__logger.error(msg)
            
            # DSML need additional footer info, to close the format
            if format == 'DSML':
                print 'footer'
                tmp = StringIO.StringIO()
                dsmlWriter = dsml.DSMLWriter(tmp)
                dsmlWriter.writeFooter()
                fileHandler.write(tmp.getvalue())
            
            fileHandler.close()
        except IOError, e:
            msg = 'Problems writing to %s. Reason:\n%s' % (filename, str(e))
            self.__logger.error(msg)
        
        self.accept()
    
    def cancel(self):
        """Slot for the cancel button.
        """
        del self.exportDict
        self.reject()

from PyQt4.QtGui import QDialog, QVBoxLayout
from .NewEntryDialogDesign import Ui_Dialog
from ..AdvancedObjectWidget import AdvancedObjectWidget
from base.backend.SmartDataObject import SmartDataObject

class NewEntryDialog(QDialog, Ui_Dialog):

    def __init__(self, parentIndex, templateSmartObject = None, parent=None, entryTemplate = None):
        QDialog.__init__(self)
        self.setupUi(self)
        if templateSmartObject:
            smartObject = templateSmartObject 
        else:
            smartO = parentIndex.internalPointer().smartObject()
            serverMeta = smartO.serverMeta
            baseDN = smartO.getDN()
            data = {}
            smartObject = AdvancedObjectWidget.smartObjectCopy(SmartDataObject((baseDN, data), serverMeta))
        self.objectWidget = AdvancedObjectWidget(None, entryTemplate = entryTemplate)
        self.objectWidget.initModel(smartObject, create=True)
        self.gridLayout.addWidget(self.objectWidget)

    def accept(self):
        if self.objectWidget.saveObject():
            super(NewEntryDialog, self).accept()
        

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
