#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2008 by Vegar Westerlund
#    <vegarwe@users.sourceforge.net>
###########################################################################

from plugins.browser_plugin.item.ServerTreeItem import ServerTreeItem
from plugins.browser_plugin.item.RootTreeItem import RootTreeItem
from plugins.browser_plugin.item.LDAPErrorItem import LDAPErrorItem
from base.backend.LumaConnection import LumaConnection

from PyQt4.QtCore import QAbstractItemModel, pyqtSlot, pyqtSignal, Qt
from PyQt4.QtCore import QModelIndex, QVariant, QCoreApplication, QRunnable
from PyQt4.QtCore import QPersistentModelIndex
from PyQt4.QtCore import QThreadPool, QThread

from PyQt4.QtGui import QMessageBox

class LDAPTreeItemModel(QAbstractItemModel):
    """
    The model used by the QTreeView in the BrowserPlugin.
    """
    
    # Callers can listed to this signal and display busy-messages as they see fit
    workingSignal = pyqtSignal(bool)
    # Emitted by the QRunnableWorker when finished
    listFetched = pyqtSignal(QModelIndex, tuple)

    def __init__(self, serverList, parent=None):
        super(LDAPTreeItemModel, self).__init__(parent)
        self.verified = []
        self.threadPool = []
        self.listFetched.connect(self.workerFinished)
        self.populateModel(serverList)

    """ These are called internally in order to signal when busy
    """
    def isWorking(self):
        self.workingSignal.emit(True)
    def doneWorking(self):
        self.workingSignal.emit(False)

    def columnCount(self, parent):
        """
        Given a parent, how many children.
        """
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role=Qt.DisplayRole):
        """
        Returns data given an index and role.
        """

        if not index.isValid():
            return QVariant()

        #Is also (should also be) checked in the items themselves
        #if role != Qt.DisplayRole and role != Qt.DecorationRole:
        #    return QtCore.QVariant()

        item = index.internalPointer()

        return QVariant(item.data(index.column(), role))

    def flags(self, index):
        """
        Items are enabled and selectable.
        """

        if not index.isValid():
            return Qt.ItemIsEnabled

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        """
        The root defines the header.
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return QVariant()

    def index(self, row, column, parent):
        """
        Creates and index given a row, column and parent.
        If the parent is invalid, use the root-item.
        """

        # Really needed? Should avoid calls to rowCount() where possible
        if row < 0 or column < 0: #or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        # Probably not needed
        if parentItem.populated == 1 and row >= parentItem.childCount():
            return QModelIndex()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        """
        Returns the parent of the model item with the given index. 
        """

        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            # Invalid indexes reffer to the root
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        """
        Returns the number of rows under the given parent (i.e. children)
        This should not be called to determine IF a parent has children, and
        it has to look up the exact number, that's what hasChildren() is for.
        """

        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        if not parentItem.populated:
            parentItem.loading = True
            parentItem.populated = True

            # -- New solution --
            self.layoutChanged.emit()
            self.fetchInThread(parent, parentItem)

            # -- Old solution --
            #self.populateItem(parentItem)
            # Updates the |>-icon to show if the item has children
            #self.layoutChanged.emit()

        return parentItem.childCount()

    def hasChildren(self, parent):
        """
        Used to avoid (expensive) calls to rowCount()
        to find out it an item has children.
        
        Return True unless it's known to not have children
        (ie. it has already been loaded).
        """

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        if parentItem.populated:
            return parentItem.childCount() > 0

        # True
        return 1

    def populateModel(self, serverList):
        """
        Called after the model is initialized. Adds the servers to the root.
        """

        self.rootItem = RootTreeItem("Servere", None) # Also provides the header

        if not len(serverList.getTable()) > 0:
            # If there's no servers :(
            self.rootItem.appendChild(LDAPErrorItem(QCoreApplication.translate("LDAPTreeItemModel", "No servers defined"), None, self.rootItem))
            return

        for server in serverList.getTable():
            tmp = ServerTreeItem([server.name], server, self.rootItem)
            self.rootItem.appendChild(tmp)

# Not currently used -- see rowCount()
#    def populateItem(self, parentItem):
#        """
#        Populates the list of children for the current parent-item.
#        This is called from rowCount() when the list is actually 
#        needed (lazy loading).
#        """
#
#        self.isWorking()
#        
#        # Don't try to fetch again
#        parentItem.populated = 1
#
#        # Ask the item to fetch the list for us
#        (success, list, exception) = parentItem.fetchChildList()
#        
#        if not success:
#            self.displayError(exception)
#            self.doneWorking()
#            return
#        
#        # Workaround:
#        # if someone opens a long list, the user could
#        # set a limit and have the childList be populated by that function
#        # before this method runs.
#        # To make sure the list aquired here isn't appended to that list
#        # we clear the list of children even though in most cases
#        # it won't be populated.
#        
#        # Normally (and prefferably)
#        # this method should be called and return before anything else is done to the model.
#        parentItem.emptyChildren()
#        for x in list:
#            parentItem.appendChild(x)
#
#        self.doneWorking()

    def displayError(self, exceptionObject):
        """
        Displays an error-message if populateItem fails.
        """
        QMessageBox.critical(None,"Error","Couldn't (re)populate list.\nError was: "+str(exceptionObject))

    @pyqtSlot(QModelIndex)
    def reloadItem(self, parentIndex):
        """
        Re-populates an already populated item, e.g. when a filter or limit it set.
        """
        #self.isWorking()

        parentItem = parentIndex.internalPointer()
        parentItem.populated = True
        self.fetchInThread(parentIndex, parentItem)
        #(success, newList, exception) = parentItem.fetchChildList()

        #if not success:
            # Basically, do nothing (can maybe use the existing list)
            #self.displayError(exception) #Let the user know we failed though
            #self.doneWorking()
            #return

        # Clear old list and insert new
        #self.clearItem(parentIndex)

        #self.beginInsertRows(parentIndex, 0, len(newList) - 1)
        #for x in newList:
            #parentItem.appendChild(x)
        #parentItem.populated = 1 #If the list is empty, this isn't set (appendChild isn't called)
        #self.endInsertRows()     
        
        #self.doneWorking()

    @pyqtSlot(QModelIndex)
    def clearItem(self, parentIndex):
        """
        Removes all children for this item.
        Used by reloadItem()
        """
        #self.isWorking()
        parentItem = parentIndex.internalPointer()
        if parentItem.childCount() > 0:
            self.beginRemoveRows(parentIndex, 0, parentItem.childCount() - 1)
            parentItem.emptyChildren()
            self.endRemoveRows()
        #self.doneWorking()
    
    def deleteItem(self, index):
        """ Tries to delete the item referenced by the passed index on the server
        """
        item = index.internalPointer()
        success, message, exceptionObject = item.delete()
        if success:
            # Remove from model
            parentIndex = self.parent(index)
            self.beginRemoveRows(parentIndex, index.row(), index.row())
            parentItem = parentIndex.internalPointer()
            parentItem.removeChild(item)
            self.endRemoveRows()
            # Return success
            return (True, message)
        else:
            # Return fail
            return (False, message)
        
    def deleteSubtree(self, index, withNode = 0):
        pass
    
    def removeRows(self, row, count, parent = QModelIndex()):
        """ Removew rows from the model
        """
        if parent.isValid():
            self.beginRemoveRows(parent, row, row+count-1)
            parent = parent.internalPointer()
            item = parent.child(row)
            parent.removeChild(item)
            item.emptyChildren() #Not strictly necessary
            self.endRemoveRows()
            return True
        else:
            return False
    
    def unverified(self, serverObject):
        if serverObject.name in self.verified:
            return False
        return True

    def fetchInThread(self, parentIndex, parentItem):
       
        # Find associated ServerItem
        serverItem = parentItem.getParentServerItem()

        if serverItem != None and self.unverified(serverItem.serverMeta):
            # Verifies the connection to the server, and asks for password if it's invalid
            # (Needs to be done in the GUI-thread (bacause of the password-dialog), which this should be)
            conn = LumaConnection(serverItem.serverMeta)
            success, exception = conn.bind(askForPw = True)
            if success:
                self.verified.append(serverItem.serverMeta.name)

        # Do the search (in another thread)
        # Two different solutions, each with it's own problems

        """ QThreadWorker """
        ## Read below before uncommenting, and also remember
        ## to uncomment the __del__-method if you don't like crashes.
        
        # Create the thread
        workerThread = WorkerThread()
        # Set up threadpool
        workerThread.finished.connect(self.removeThreadFromPool)
        self.threadPool.append(workerThread)
        
        # Create the worker
        worker = Worker(parentIndex, parentItem)
        worker.listFetched.connect(self.workerFinished)
        worker.listFetched.connect(workerThread.quit)
        # Move worker to thread
        workerThread.setWorker(worker)
    
        # Start thread
        workerThread.start()

        """ QThreadPool + QRunnable """
        #thread = QRunnableWorker(self, parentIndex, parentItem)
        #QThreadPool.globalInstance().start(thread)

        parentItem.loading = True

    @pyqtSlot()
    def removeThreadFromPool(self):
        self.threadPool.remove(self.sender())
        print "Number of currently running threads: "+str(len(self.threadPool))

    @pyqtSlot(QModelIndex, tuple)
    def workerFinished(self, parentIndex, tupel):
        if parentIndex.isValid():

            parentItem = parentIndex.internalPointer()
            parentItem.loading = False

            (success, newList, exception) = tupel
            if not success:
                # Basically, do nothing (can maybe use the existing list)
                self.displayError(exception) #Let the user know we failed though
                parentItem.error = True
                return
            # Clear old list and insert new
            self.clearItem(parentIndex)
            
            self.beginInsertRows(parentIndex, 0, len(newList) - 1)
            for x in newList:
                parentItem.appendChild(x)
            parentItem.populated = 1 #If the list is empty, this isn't set (appendChild isn't called)
            self.endInsertRows()     

            self.layoutChanged.emit()


class WorkerThread(QThread):
	
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.worker = None

    def run(self):
        self.exec_()

    def setWorker(self, worker):
        worker.moveToThread(self)
        self.worker = worker
        self.started.connect(worker.start)


from PyQt4.QtCore import QObject
class Worker(QObject):
    """ 
    Problems/issues:
        - None major?
        - Minor: reload when in progress aborts the currently running one
                 resulting in a timeout in 60 sec. which overwrites the data.
                 Fixed by removing self.cancelSearch() in LDAPTreeItem
                 but should be properly fixed instead. (Removing cancel?)
    """
    
    # Emitted by the workerThread when finished
    listFetched = pyqtSignal(QModelIndex, tuple)

    def __init__(self, parentIndex, parentItem):
        super(Worker, self).__init__()
        self.parentIndex = parentIndex
        self.persistent = QPersistentModelIndex(parentIndex)

        self.parentItem = parentItem
        self.parentItem.loading = True

    @pyqtSlot()
    def start(self):
        tupel = self.parentItem.fetchChildList()

        if self.persistent.isValid():
            # QPersistenModelIndex -> QModelIndex
            # Should prefferably not be done here (changes can happend until the receiver-thread process the event)
            # but Qt can't send QPersistentModelIndexes (yet?)
            # Also, using QModelIndex through the whole process also works for some reason.
            # The new items are placed right even though QModelIndex.row() is wrong (e.g. because
            index = QModelIndex(self.persistent)
            self.listFetched.emit(index, tupel)
            #self.model.threads.remove(self)

class QRunnableWorker(QRunnable):
    """
    Problems/issues:
        - If Luma is closed while this is running
          the Luma-process will not close before this
          finishes.
    """

    def __init__(self, target, parentIndex, parentItem):
        super(QRunnableWorker, self).__init__()
        self.target = target
        self.parentIndex = parentIndex
        self.persistent = QPersistentModelIndex(parentIndex)
        self.parentItem = parentItem

    def run(self):
        tupel = self.parentItem.fetchChildList()
        from PyQt4.QtGui import qApp
        if qApp.closingDown():
            return
        if self.persistent.isValid():
            # QPersistenModelIndex -> QModelIndex
            # Should prefferably not be done here (changes can happend until the receiver-thread process the event)
            # but Qt can't send QPersistentModelIndexes (yet?)
            # Also, using QModelIndex through the whole process also works for some reason.
            # The new items are placed right even though QModelIndex.row() is wrong (e.g. because
            # an item was deleted above it). 
            index = QModelIndex(self.persistent)
            self.target.listFetched.emit(index, tupel)
