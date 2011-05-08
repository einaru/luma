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
    blocking the GUI
    """
    
    # The signals the user should bind to
    # to recive the result og xAsync-methods
    bindFinished = pyqtSignal(bool, Exception)
    searchFinished = pyqtSignal(bool, list, Exception)

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

    def bindAsync(self):
        """
        Non-blocking. Listen to QLuma.bindFinished
        for the result.

        Only use the exception is success is False.
        """
        bindWorker = BindWorker(self.lumaConnection)
        bindWorker.workDone.connect(self.__bindThreadFinished)
        thread = self.__createThread(bindWorker)
        thread.start()

    @pyqtSlot(bool, Exception)
    def __bindThreadFinished(self, success, exception):
        self.bindFinished.emit(success, exception)

    ###########
    # SEARCH
    ###########
    def searchSync(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None, attrsonly=0, sizelimit=0):
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


    def searchAsync(self, base="", scope=ldap.SCOPE_BASE, filter="(objectClass=*)", attrList=None, attrsonly=0, sizelimit=0):
        searchWorker = SearchWorker(self.lumaConnection, base, scope, filter, attrList, attrsonly, sizelimit)
        searchWorker.workDone.connect(self.__searchThreadFinished)
        thread = self.__createThread(searchWorker)
        thread.start()

    @pyqtSlot(bool, list, Exception)
    def __searchThreadFinished(self, success, resultList, exceptionList):
        if success:
            # Can't send None so we send a generic Exception
            # Listeners should use success to know if there's
            # an exception or not.
            self.bindFinished.emit(success, resultList, Exception())
        else:
            self.bindFinished.emit(success, resultList, exceptionList[0])
    
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
###########
class BindWorker(QObject):
    workDone = pyqtSignal(bool, Exception)
    def __init__(self, lumaConnection):
        QObject.__init__(self)
        self.lumaConnection = lumaConnection
        self.logger = logging.getLogger(__name__)
    def doWork(self):
        self.success, self.exception = self.lumaConnection.bind()
        if self.success:
            self.workDone.emit(self.success, Exception())
        else:
            self.workDone.emit(self.success, self.exception)
        self.logger.debug("BindWorker finished.")

class SearchWorker(QObject):
    workDone = pyqtSignal(bool, list, Exception)
    def __init__(self, lumaConnection, base, scope, filter, attrList, attrsonly, sizelimit):
        QObject.__init__(self)
        self.lumaConnection = lumaConnection
        self.logger = logging.getLogger(__name__)
        self.base = base
        self.scope = scope
        self.filter = filter
        self.attrList = attrList
        self.attrsonly = attrsonly
        self.sizelimit = sizelimit
    def doWork(self):
        self.success, self.resultList, self.exception = self.lumaConnection.search(self.base, self.scope, self.filter, self.attrList, self.attrsonly, self.sizelimit)
        if self.success:
            self.workDone.emit(self.success, self.resultList, Exception())
        else:
            print self.success, self.resultList, self.exception
            self.workDone.emit(self.success, self.resultList, self.exception)
        self.logger.debug("SearchWorker finished")

###########
# Used by LumaConnectionWrapper to run the worker-classes in it's own thread
###########
class WorkerThread(QThread):

    __threadPool = []
    __Lock = RLock()
    
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.logger = logging.getLogger(__name__)

        # Add to the threadpool
        with WorkerThread.__Lock:
            WorkerThread.__threadPool.append(self)

        # Cleanup on finish
        self.finished.connect(self.cleanup)
        self.terminated.connect(self.cleanup)

        self.worker = None

    def run(self):
        self.logger.debug("Run started")
        self.exec_()

    def cleanup(self):
        self.logger.debug("Cleanup called.")
        # Remove from threadpool on finish
        print "Debug -- before cleanup of threadpool:"
        print WorkerThread.__threadPool
        with WorkerThread.__Lock:
            WorkerThread.__threadPool.remove(self)
        print "Debug -- after cleanup of threadpool:"
        print WorkerThread.__threadPool

    def setWorker(self, worker):
        worker.moveToThread(self)
        self.worker = worker
        # Start worker on thread start
        self.started.connect(worker.doWork)
        # Stop thread on worker finish
        self.worker.workDone.connect(self.quit)

"""
            # Prompt for password on _invalid_pwd or _blank_pwd
            if self._cert_error(exception, self.serverObject):
                svarFraBruker = False
                if svarFraBruker == QMessageBox.Yes:
                    self.serverObject.checkServerCertificate = ServerCheckCertificate.Never
                    LumaConnection.__certMap[self.serverObject.name] = ServerCheckCertificate.Never
                    success, exception, ldapServerObject = self.__bind()
            
            # Prompt for password on _invalid_pwd or _blank_pwd
            if self._invalid_pwd(exception) or self._blank_pwd(exception, self.serverObject):
                hasNewPassword = False
                if hasNewPassword:
                    self.serverObject.bindPassword = unicode(pw)
                    LumaConnection.__passwordMap[self.serverObject.name] = self.serverObject.bindPassword
                    success, exception, ldapServerObject = self.__bind()
"""


