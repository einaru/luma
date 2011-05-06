# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog
from base.gui.rejects.BaseSelectorDesign import Ui_BaseSelectorDesign
#from base.utils.gui.LumaErrorDialog import LumaErrorDialog


class BaseSelector(QDialog, Ui_BaseSelectorDesign):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self)
        self.setupUi(self)
        self.connection = None
        
    def addBase(self):
        tmpBase = unicode(self.baseDNEdit.text()).strip()
        if tmpBase == u"":
            return      
        self.baseView.addItem(QtGui.QListWidgetItem(tmpBase))
        self.baseDNEdit.clear()
        

    def deleteBase(self):
        for tmpItem in self.baseView.selectedItems():
            if not (None == tmpItem):
                index = self.baseView.indexFromItem(tmpItem)
                d = self.baseView.takeItem(index.row())
                if d != 0:
                    del d
        
    def addServerBase(self):
        print "Not implemented."
        """
        success, serverBaseList, exceptionObject = self.connection.getBaseDNList()
        
        if success:
            for x in serverBaseList:
                if not (x in self.baseList):
                    self.baseList.append(x)
                    self.baseList.sort()
            self.displayBase()
        else:
            #dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not retrieve baseDN.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
        """
        
    def getList(self):
        m = self.baseView.model()
        row = m.rowCount(QtCore.QModelIndex())
        returnList = []
        for i in xrange(row):
            returnList.append(m.data(m.index(i,0)).toPyObject())
        return returnList
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    s = BaseSelector()
    s.show()
    sys.exit(app.exec_())
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
