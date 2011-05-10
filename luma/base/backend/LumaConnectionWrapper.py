from __future__ import with_statement
import threading
from threading import RLock

from PyQt4.QtCore import QObject, QThread, Qt
from PyQt4.QtCore import pyqtSlot, pyqtSignal

from PyQt4.QtGui import qApp

from LumaConnection import LumaConnection
import ldap, time, types, logging

class LumaConnectionWrapper(QObject):
    """
    Wrapper for LumaConnection providing
    async-versions of time-consuming methods
    which use signals to return the result
    and also sync-versions which use 
    qApp.processEvents() to avoid
    blocking the GUI.

    If your method can work with signals to
    get the result, please use the async-methods.
    That way we avoid calling qApp.processEvents()
    which leads to recursion if other methods
    are called while waiting for the result which
    again mens your results will be delayed until
    that method is finished.


    The xAsync-methods takes an identStr which
    is signaled along with the result of the operation
    for identifying purposes.
    """
    
    # The signals the user should bind to
    # to recive the result og xAsync-methods
    bindFinished = pyqtSignal(bool, Exception, str)
    searchFinished = pyqtSignal(bool, list, Exception, str)

    def __init__(self, serverObject, parent = None):
        """
        To use the async-methods YOU NEED TO SPECIFY A PARENT QOBJECT!
        If you promise to only use the sync-methods, you don't need
        to spesify a parent.
        """
        QObject.__init__(self, parent)
        self.lumaConnection = LumaConnection(serverObject)
        self.logger = logging.getLogger(__name__)

    ###########
    # BIND
    ###########
    def bindSync(self):
        """
        Equivalent to LumaConnection.bind()
        but doesn't block the GUI through calling
        qApp.processEvents() while the bind
        is in progress.
        """
        bindWorker = BindWorker(self.lumaConnection)
        thread = self.__createThread(bindWorker)
        thread.start()
        
        while not thread.isFinished():
            self.__whileWaiting()

        return (bindWorker.success, bindWorker.exception)

    def bindAsync(self, identStr = ""):
        """
        Non-blocking. Listen to LumaConnectionWrapper.bindFinished
        for the result.

        Only use the exception passed if "success" is False.
        """
        bindWorker = BindWorker(self.lumaConnection, identStr)
        bindWorker.workDone.connect(self.__bindThreadFinished)
        thread = self.__createThread(bindWorker)
        thread.start()

    @pyqtSlot(bool, Exception, str)
    def __bindThreadFinished(self, success, exception, identStr):
        self.bindFinished.emit(success, exception, identStr)

    ###########
    # SEARCH
    ###########
    def searchSync(
            self,
            base="",
            scope=ldap.SCOPE_BASE,
            filter="(objectClass=*)",
            attrList=None,
            attrsonly=0,
            sizelimit=0
            ):
        """
        Equivalent to LumaConnection.search().
        See bindSync() for details.
        """
        searchWorker = SearchWorker(self.lumaConnection, base, scope, filter, attrList, attrsonly, sizelimit)
        thread = self.__createThread(searchWorker)
        thread.start()
        
        while not thread.isFinished():
            self.__whileWaiting()

        return (searchWorker.success, searchWorker.resultList, searchWorker.exception)


    def searchAsync(
            self, 
            base="",
            scope=ldap.SCOPE_BASE,
            filter="(objectClass=*)",
            attrList=None, 
            attrsonly=0,
            sizelimit=0,
            identStr=""
            ):
        """
        Non-blocking. Listen to LumaConnectionWrapper.searchFinished
        for the result.

        Only use the exception passed if "success" is False.
        """
        searchWorker = SearchWorker(self.lumaConnection, base, scope, filter, attrList, attrsonly, sizelimit, identStr)
        searchWorker.workDone.connect(self.__searchThreadFinished)
        thread = self.__createThread(searchWorker)
        thread.start()

    @pyqtSlot(bool, list, Exception, str)
    def __searchThreadFinished(self, success, resultList, exception, identStr):
            self.searchFinished.emit(success, resultList, exception, identStr)
    
    def getBaseDNListSync(self):
        # TODO MAKE ASYNC VERSION
        return self.lumaConnection.getBaseDNList()

    ###########
    # Sync-only-methods (resonably quick, so no immediate need for async-versions.
    ###########
    def delete(self, dnDelete=None):
        return self.lumaConnection.delete(dnDelete)
    def modify(self, dn, modlist=None):
        return self.lumaConnection.modify(dn, modlist)
    def add(self, dn, modlist):
        return self.lumaConnection.add(dn, modlist)
    def updateDataObject(self, smartDataObject):
        return self.lumaConnection.updateDataObject(smartDataObject)
    def addDataObject(self, dataObject):
        return self.lumaConnection.addDataObject(dataObject)
    def unbind(self):
        self.lumaConnection.unbind()

    ###########
    # Internal methods
    ###########
    def __whileWaiting(self):
        """
        When using sync-methods we runs this
        while waiting for LumaConnection to return
        data. This keeps the GUI responsive.
        """
        qApp.processEvents()
        time.sleep(0.05)
    
    def __createThread(self, worker): 
        # Create the thread
        workerThread = WorkerThread()
        # Move worker to thread
        workerThread.setWorker(worker)
        return workerThread



###########
# Worker-classes used by LumaConnectionWrapper
# to run code in it's own thread (WorkerThread).
###########
class BindWorker(QObject):
    """
    Runs LumaConnection.bind()
    """
    workDone = pyqtSignal(bool, Exception, str)
    def __init__(self, lumaConnection, identStr = ""):
        QObject.__init__(self)
        self.lumaConnection = lumaConnection
        self.logger = logging.getLogger(__name__)
        self.identStr = identStr
    def doWork(self):
        self.success, self.exception = self.lumaConnection.bind()
        if self.success:
            self.workDone.emit(self.success, Exception(), self.identStr)
        else:
            self.workDone.emit(self.success, self.exception, self.identStr)
        self.logger.debug("BindWorker finished.")

class SearchWorker(QObject):
    """
    Runs LumaConnection.search()
    """
    workDone = pyqtSignal(bool, list, Exception, str)
    def __init__(self, lumaConnection, base, scope, filter, attrList, attrsonly, sizelimit, identStr = ""):
        QObject.__init__(self)
        self.lumaConnection = lumaConnection
        self.logger = logging.getLogger(__name__)
        self.base = base
        self.scope = scope
        self.filter = filter
        self.attrList = attrList
        self.attrsonly = attrsonly
        self.sizelimit = sizelimit
        self.identStr = identStr
    def doWork(self):
        self.success, self.resultList, self.exception = self.lumaConnection.search(self.base, self.scope, self.filter, self.attrList, self.attrsonly, self.sizelimit)
        if self.success:
            self.workDone.emit(self.success, self.resultList, Exception(), self.identStr)
        else:
            self.workDone.emit(self.success, self.resultList, self.exception, self.identStr)
        self.logger.debug("SearchWorker finished")

###########
# Used by LumaConnectionWrapper to run the worker-classes in it's own thread
###########
class WorkerThread(QThread):
    """
    Used to run code in it's own thread.
    The worker must have a doWork() method
    with the work to be done and a workDone-signal
    which is emitted when doWork() is finished.
    """

    __threadPool = []
    __Lock = RLock()
    
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.logger = logging.getLogger(__name__)

        # Add to the threadpool so the thread is not GCed
        # while running.
        with WorkerThread.__Lock:
            WorkerThread.__threadPool.append(self)

        # Cleanup on finish
        self.finished.connect(self.cleanup)
        self.terminated.connect(self.cleanup)
        
        self.worker = None

    def run(self):
        self.exec_()

    def quit(self):
        QThread.quit(self)
        self.cleanup()
    
    def cleanup(self):
        """
        Removed this thread from the threadpool
        so that it is GCed.
        """
        self.logger.debug("Cleanup called.")
        # Remove from threadpool on finish
        print "Debug -- before cleanup of threadpool:"
        print WorkerThread.__threadPool
        with WorkerThread.__Lock:
            WorkerThread.__threadPool.remove(self)
        print "Debug -- after cleanup of threadpool:"
        print WorkerThread.__threadPool

    def setWorker(self, worker):
        """
        Sets worker to be executed in this thread.
        """
        worker.moveToThread(self)
        self.worker = worker
        # Start worker on thread start
        self.started.connect(worker.doWork)
        # Stop thread on worker finish
        self.worker.workDone.connect(self.quit)

