# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import ldap
from qt import *
import base64
import re
import os.path

from base.utils.gui.SearchResultViewDesign import SearchResultViewDesign
from base.utils.gui.ObjectWidget import ObjectWidget
from base.backend.ServerList import ServerList
import environment
from base.utils import isBinaryAttribute, encodeBase64


class SearchResultView(SearchResultViewDesign):

    def __init__(self, parent=None, name=None, fl=0):
        SearchResultViewDesign.__init__(self,parent,name,fl)

        self.SERVER = None
        self.RESULT = {}
        self.childWidgets = []
        self.childsToClean = []
        self.FILTER_COLUMN_POS = {}
        self.FILTER_LIST = []
        
        tmpDirObject = os.path.join(environment.lumaInstallationPrefix, "share", "luma", "icons")
        delIconFile = os.path.join(tmpDirObject, "deleteEntry.png")
        exportIconFile = os.path.join(tmpDirObject, "exportLdif.png")
        
        self.popupMenu = QPopupMenu()
        self.popupMenu.insertItem(QIconSet(QPixmap(exportIconFile)), self.trUtf8("Export selected"), self.export_items)
        self.popupMenu.insertSeparator()
        self.popupMenu.insertItem(QIconSet(QPixmap(delIconFile)), self.trUtf8("Delete selected"), self.delete_items)
        
        self.connect(self.resultListView, SIGNAL("rightButtonPressed(QListViewItem*, const QPoint&, int)"), self.show_popup)

###############################################################################

    def show_entry(self, listItem):
        while len(self.childsToClean) > 0:
            number = -1
            for x in range(0, len(self.childWidgets)):
                name1 = self.childWidgets[x].name()
                name2 = self.childsToClean[0]
                if name1 == name2:
                    number = x
            if not(number == -1):
                del self.childWidgets[number]
                del self.childsToClean[0]

        widget = ObjectWidget(None, unicode(listItem.text(0)).encode('utf-8'), 0)
        values = [self.RESULT[unicode(listItem.text(0)).encode('utf-8')]]
        #print values
        widget.initView(self.SERVER, values)
        widget.setMinimumHeight(500)
        widget.show()
        widget.setCaption(listItem.text(0))
        
        # needed if window is closed. gets deletetd from the list
        widget.installEventFilter(self)
        
        # don't loose reference. normally window will disappear if function is completed
        self.childWidgets.append(widget)

###############################################################################

    def set_result(self, server=None, resultData=None, filterList=None):
        self.SERVER = server
        self.process_data(resultData)
        self.FILTER_LIST = filterList
        self.display_results()

###############################################################################

    def process_data(self, data):
        self.RESULT = {}
        if not(data == None):
            for x in data:
                self.RESULT[x[0]] = x

###############################################################################

    def display_results(self):
        self.resultListView.clear()
        while self.resultListView.columns():
            self.resultListView.removeColumn(0)
        self.FILTER_COLUMN_POS = {}
        position = self.resultListView.addColumn("dn")
        self.FILTER_COLUMN_POS["dn"] = position
        for x in self.FILTER_LIST:
            position = self.resultListView.addColumn(x)
            self.FILTER_COLUMN_POS[x] = position
        for x in self.RESULT.keys():
            listItem = QListViewItem(self.resultListView, x)
            listItem.setText(0, x.decode('utf-8'))
            for y in self.RESULT[x][1].keys():
                if (self.FILTER_COLUMN_POS.has_key(y)) and (not (y == 'dn')):
                    showString = []
                    for z in self.RESULT[x][1][y]:
                        if isBinaryAttribute(z) >= 1:
                            showString.append(encodeBase64(z))
                        else:
                            showString.append(z.decode('utf-8'))
                    listItem.setText(self.FILTER_COLUMN_POS[y], ",".join(showString))
            self.resultListView.insertItem(listItem)
        self.resultListView.setColumnWidth(0, 250)
        self.resultListView.triggerUpdate()


###############################################################################

    def eventFilter(self, object, event):
        if (event.type() == QEvent.Close):
            name = object.name()
            self.childsToClean.append(name)
        return 0

###############################################################################

    def delete_items(self):
        warnString = self.trUtf8('Do you really want to delete the item(s) from the server?')
        result = QMessageBox.warning(self, self.trUtf8('Delete entry'), warnString, self.trUtf8('Delete'), self.trUtf8('Cancel'))
        if result == 1:
            return
        
        itemList = self.get_selected_items()
        
        serverList = ServerList()
        serverList.readServerList()
        
        serverMeta = serverList.get_serverobject(self.SERVER)

        # set gui busy
        environment.setBusy(1)
        
        try:
            ldapServerObject = ldap.open(serverMeta.host, serverMeta.port)
            ldapServerObject.protocol_version = ldap.VERSION3
            
            if serverMeta.tls == 1:
                ldapServerObject.start_tls_s()
                
            if len(serverMeta.bindDN) > 0:
                ldapServerObject.simple_bind_s(serverMeta.bindDN,
                                serverMeta.bindPassword)
            for x in itemList:
                # keep UI responsive
                environment.updateUI()
                
                ldapServerObject.delete_s(unicode(x.text(0)))
                
            if len(serverMeta.bindDN) > 0:
                ldapServerObject.unbind()
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + unicode(e)
        
        for x in itemList:
            self.resultListView.takeItem(x)
            
        # set GUI not busy
        environment.setBusy(0)
        
        
###############################################################################
    
    def show_popup(self, tmpItem=None, point=None, itemId=None):
        if not (tmpItem == None):
            self.popupMenu.exec_loop(point)

###############################################################################

    def export_items(self):
        itemList = self.get_selected_items()
        tmpList = []
        for x in itemList:
            tmpList.append(self.RESULT[unicode(x.text(0))])
        exportString = self.convert_to_ldif(tmpList)
        
        fileName = unicode(QFileDialog.getSaveFileName())
        if fileName == '':
            return
        try:
            fileHandler = open(fileName, 'w')
            fileHandler.write(exportString)
            fileHandler.close()
        except IOError, e:
            print "Could not save Data"
            print "Reason: " + unicode(e)
        
###############################################################################

    def get_selected_items(self):
        child = self.resultListView.firstChild()
        tmpList = []
        if child.isSelected():
                tmpList.append(child)
        
        while child.nextSibling():
            child = child.nextSibling()
            if child.isSelected():
                tmpList.append(child)
                
        return tmpList
        
###############################################################################

    def convert_to_ldif(self, data):
        SAFE_STRING_PATTERN = '(^(\000|\n|\r| |:|<)|[\000\n\r\200-\377]+|[ ]+$)'
        safe_string_re = re.compile(SAFE_STRING_PATTERN)

        tmpList = []
        for a in data:
            tmpList.append("dn: " + a[0] + "\n")
            for x in a[1].keys():
                for y in a[1][x]:
                    if not (safe_string_re.search(y) == None):
                        tmpList.append(x + ":: " + base64.encodestring(y))
                    else:
                        tmpList.append(x + ": " + y + "\n")
                    
            tmpList.append("\n")
        return "".join(tmpList)
    
