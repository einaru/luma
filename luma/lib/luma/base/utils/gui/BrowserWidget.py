###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <wido.depping@tu-clausthal.de>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
import string
import ldap
import time

from base.backend.ServerList import ServerList
from base.backend.DirUtils import DirUtils
from base.utils.backend.templateutils import *
from base.utils.gui.TemplateObjectWidget import TemplateObjectWidget

class BrowserWidget(QListView):

    def __init__(self,parent = None,name = None,fl = 0):
        QListView.__init__(self,parent,name,fl)

        self.connect(self, SIGNAL("clicked(QListViewItem*)"), self.item_clicked)
        self.connect(self, SIGNAL("collapsed(QListViewItem*)"), self.item_collapsed)
        self.connect(self, SIGNAL("expanded(QListViewItem*)"), self.item_expanded)

        self.setRootIsDecorated(1)
        self.addColumn(self.trUtf8("Entries"))
        self.setResizeMode(QListView.AllColumns)

        self.searchObjectClass = "(objectClass=*)"
        # Example for filtering the entries
        #self.set_search_class(['organizationalUnit', \
        #       'dcObject', 'organization'])

        tmpDirObject = DirUtils()
        tmpIconFile = tmpDirObject.PREFIX + "/lib/luma/base/utils/icons/secure.png"

        tmpObject = ServerList()
        tmpObject.readServerList()
        
        self.serverListObject = tmpObject
        
        if (tmpObject.SERVERLIST == None):
            self.SERVERLIST = []
        else:
            self.SERVERLIST = tmpObject.SERVERLIST[:]
            
        for x in self.SERVERLIST:
            tmpItem = QListViewItem(self, x.name)
            if int(x.tls):
                tmpItem.setPixmap(0, QPixmap(tmpIconFile))
            self.insertItem(tmpItem)
            tmpBase = QListViewItem(tmpItem, x.baseDN)
            tmpBase.setExpandable(1)
            tmpItem.insertItem(tmpBase)

            
        # different menus for right click
        self.popupMenu = QPopupMenu()
        self.exportMenu = QPopupMenu()
        self.addItemMenu = QPopupMenu()
        
        # icon files for the menu entries
        addIconFile = tmpDirObject.PREFIX + "/share/luma/icons/newEntry.png"
        delIconFile = tmpDirObject.PREFIX + "/share/luma/icons/deleteEntry.png"
        exportIconFile = tmpDirObject.PREFIX + "/share/luma/icons/exportLdif.png"
        
        self.exportMenu.insertItem(self.trUtf8("Item"), self.__export_item)
        self.exportMenu.insertItem(self.trUtf8("Item+Subtree"), self.__export_item_subtree)
        self.exportMenu.insertItem(self.trUtf8("Item+Subtree+Parents"), self.__export_item_all)

        self.popupMenu.insertItem(QIconSet(QPixmap(addIconFile)), self.trUtf8("Add Item"), self.addItemMenu)
        self.popupMenu.insertSeparator()
        self.popupMenu.insertItem(QIconSet(QPixmap(exportIconFile)), self.trUtf8("Export to LDIF"), self.exportMenu)
        self.popupMenu.insertSeparator()
        #self.popupMenu.insertItem
        self.popupMenu.insertItem(QIconSet(QPixmap(delIconFile)), self.trUtf8("Delete Item"), self.__delete_item)
        self.popupMenu.insertItem(QIconSet(QPixmap(delIconFile)), self.trUtf8("Delete Items recursive"), self.__delete_items_recursive)
        
        self.connect(self.addItemMenu, SIGNAL("aboutToShow()"), self.create_add_menu)

        self.addItemWidgets = []

        self.connect(self, SIGNAL("rightButtonPressed(QListViewItem*, const QPoint&, int)"), self.__show_popup)

###############################################################################

    def item_clicked(self, item):
        if not(item == None):
            fullPath = self.get_full_path(item)
            try:
                server, result = self.getLdapItem(fullPath)
                self.emit(PYSIGNAL("ldap_result"), (server, result[:],))
            except TypeError:
                "No result from Server"


###############################################################################

    def item_expanded(self, item):
        fullPath = self.get_full_path(item)
        results = self.getLdapItemChildren(fullPath, 0)
        if results == None:
            return None
        if len(results) == 0:
            item.setExpandable(0)
            return None
        for x in results:
            tmp = x[0]
            tmp = string.split(tmp, ",")
            tmpItem = QListViewItem(item, tmp[0])
            tmpItem.setExpandable(1)
            item.insertItem(tmpItem)



###############################################################################

    def item_collapsed(self, item):
        fullPath = self.get_full_path(item)
        serverName, ldapObject = self.__split_path(fullPath)
        if len(ldapObject) == 0:
            return None
        while item.childCount() > 0:
            item.takeItem(item.firstChild())

###############################################################################

    def get_full_path(self, item):
        try:
            fullPath = str(item.text(0))
            while item.parent():
                item = item.parent()
                fullPath = fullPath + "," + str(item.text(0))
            return fullPath
        except AttributeError:
            pass

###############################################################################

    def getLdapItem(self, itemPath):
        serverName, ldapObject = self.__split_path(itemPath)
        if len(ldapObject) == 0:
            return None
        
        serverMeta = self.serverListObject.get_serverobject(serverName)
                
        mainWin = qApp.mainWidget()
        # set gui busy
        mainWin.set_busy()
        
        try:
            ldapServerObject = ldap.open(serverMeta.host)
            ldapServerObject.protocol_version = ldap.VERSION3
            if serverMeta.tls == "1":
                ldapServerObject.start_tls_s()
            if len(serverMeta.bindDN) > 0:
                ldapServerObject.simple_bind_s(serverMeta.bindDN,
                                    serverMeta.bindPassword)
            searchResult = ldapServerObject.search_s(ldapObject, ldap.SCOPE_BASE)
            if len(serverMeta.bindDN) > 0:
                ldapServerObject.unbind()
            mainWin.set_busy(0)
            return serverName, searchResult[:]
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)
            mainWin.set_busy(0)

###############################################################################

    def __split_path(self, itemPath):
        tmp = string.split(itemPath, ",")
        serverName = tmp[-1]
        ldapObject = itemPath[:-len(serverName)-1]
        return serverName, ldapObject

###############################################################################

    def getLdapItemChildren(self, itemPath, allLevel):
        serverName, ldapObject = self.__split_path(itemPath)
        if len(ldapObject) == 0:
            return None
            
        serverMeta = self.serverListObject.get_serverobject(serverName)
        searchResult = []

        mainWin = qApp.mainWidget()
        # set gui busy
        mainWin.set_busy()

        try:
            ldapServerObject = ldap.open(serverMeta.host)
            ldapServerObject.protocol_version = ldap.VERSION3
            if serverMeta.tls == "1":
                ldapServerObject.start_tls_s()
            if len(serverMeta.bindDN) > 0:
                ldapServerObject.simple_bind_s(serverMeta.bindDN,
                                serverMeta.bindPassword)

            # allLevel defines whether the complete subtree is searched or
            # just one level
            searchLevel = None
            if allLevel:
                searchLevel = ldap.SCOPE_SUBTREE
            else:
                searchLevel = ldap.SCOPE_ONELEVEL

            resultId = ldapServerObject.search(ldapObject, searchLevel,
                self.searchObjectClass, None, 0)

            while 1:
                # keep UI responsive
                mainWin.update_ui()

                result_type, result_data = ldapServerObject.result(resultId, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        for x in result_data:
                            searchResult.append(x)

            if len(serverMeta.bindDN) > 0:
                ldapServerObject.unbind()
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)

        # set GUI not busy
        mainWin.set_busy(0)
        return searchResult[:]

###############################################################################

    def set_search_class(self, classList):
        self.searchObjectClass = "(|"
        for x in classList:
            self.searchObjectClass = self.searchObjectClass + \
                    "(objectClass=" + x + ")"
        self.searchObjectClass = self.searchObjectClass + ")"

###############################################################################

    def __export_item(self):
        fullPath = self.get_full_path(self.selectedItem())
        result = self.getLdapItem(fullPath)
        ldifString = self.__convert_to_ldif(result[1])
        self.__save_ldif(ldifString)

###############################################################################

    def __export_item_subtree(self):
        fullPath = self.get_full_path(self.selectedItem())
        results = self.getLdapItemChildren(fullPath, 1)
        resultString = self.__convert_to_ldif(results)
        self.__save_ldif(resultString)

###############################################################################

    def __export_item_all(self):
        currentItem = self.selectedItem()
        fullPath = self.get_full_path(currentItem)
        parents = self.__get_parents(currentItem)
        resultString = ""
        for x in parents:
            tmpResult = self.getLdapItem(x)
            resultString = resultString + self.__convert_to_ldif(tmpResult[1])
        subtree = self.getLdapItemChildren(fullPath, 1)
        subtreeString = self.__convert_to_ldif(subtree)
        self.__save_ldif(resultString + subtreeString)


###############################################################################

    def __delete_item(self):
        warnString = self.trUtf8('Do you really want to delete the item from the server?')
        result = QMessageBox.warning(self, self.trUtf8('Delete entry'), warnString, self.trUtf8('Delete'), self.trUtf8('Cancel'))
        if result == 1:
            return
        item = self.selectedItem()
        parent = item.parent()
        fullPath = self.get_full_path(item)
        serverName, ldapObject = self.__split_path(fullPath)
        if len(ldapObject) == 0:
            return None
            
        self.__delete_ldap_entry(serverName, ldapObject)
        
        parent.setOpen(0)
        parent.setOpen(1)
        


###############################################################################

    def __show_popup(self, tmpItem=None, point=None, itemId=None):
        if not (tmpItem == None):
            if not (tmpItem.parent() == None):
                self.popupMenu.exec_loop(point)

###############################################################################

    def __convert_to_ldif(self, data):
        tmpListe = []
        for a in data:
            tmpListe.append("dn: " + a[0] + "\n")
            for x in a[1].keys():
                for y in a[1][x]:
                    tmpListe.append(x + ": " + y + "\n")
            tmpListe.append("\n")
        return string.join(tmpListe, "")

###############################################################################

    def __save_ldif(self, data):
        fileName = str(QFileDialog.getSaveFileName())
        if fileName == '':
            return
        try:
            fileHandler = open(fileName, 'w')
            fileHandler.write(data)
            fileHandler.close()
        except IOError, e:
            print "Could not save Data"
            print "Reason: " + str(e)

###############################################################################

    def __get_parents(self, item):
        parentList = []
        while (item.parent()):
            item = item.parent()
            parentList.append(self.get_full_path(item))
        parentList.reverse()
        del parentList[0]
        return parentList

###############################################################################

    def create_add_menu(self):
        self.addItemMenu.clear()
        tFile = TemplateFile()
        for x in tFile.tplList:
            self.addItemMenu.insertItem(x.name, self.add_item)
            
###############################################################################

    def add_item(self, id):
        templateName = str(self.addItemMenu.text(id))
        
        tFile = TemplateFile()
        template = tFile.get_templateobject(templateName)
        
        if template == None:
            return 
            
        fqn = self.get_full_path(self.selectedItem())
        widget = TemplateObjectWidget(None, template.name, 0)
        widget.setMinimumHeight(350)
        widget.setCaption(self.trUtf8('Add entry'))
        widget.init_view(fqn, template)
        widget.show()
        
        # don't loose reference. normally window will disappear if function is completed
        self.addItemWidgets.append(widget)
        
###############################################################################
        
    def __delete_items_recursive(self):
        warnString = self.trUtf8('Do you really want to delete the items recursively from the server?')
        result = QMessageBox.warning(self, self.trUtf8('Delete entry'), warnString, self.trUtf8('Delete'), self.trUtf8('Cancel'))
        if result == 1:
            return
            
        mainWin = qApp.mainWidget()
        # set gui busy
        mainWin.set_busy(1)
        
        currentItem = self.selectedItem()
        
        parent = currentItem.parent()
        fullPath = self.get_full_path(currentItem)
        children = self.getLdapItemChildren(fullPath, 1)
        
        serverName, selectedObject = self.__split_path(fullPath)
        if len(selectedObject) == 0:
            return None
        
        while ((len(children) > 0) and (not(children == None))) :
            mainWin.update_ui()
            print children[-1][0]
            self.__delete_ldap_entry(serverName, children[-1][0])
            del children[-1]
        
        currentItem.setOpen(0)
        currentItem.setOpen(1)
        parent.setOpen(0)
        parent.setOpen(1)
        
        mainWin.set_busy(0)

###############################################################################

    def __delete_ldap_entry(self, serverName, ldapObject):
        serverMeta = self.serverListObject.get_serverobject(serverName)
        try:
            ldapServerObject = ldap.open(serverMeta.host)
            ldapServerObject.protocol_version = ldap.VERSION3
            if serverMeta.tls == "1":
                ldapServerObject.start_tls_s()
            if len(serverMeta.bindDN) > 0:
                ldapServerObject.simple_bind_s(serverMeta.bindDN,
                                serverMeta.bindPassword)
            ldapServerObject.delete_s(ldapObject)
            if len(serverMeta.bindDN) > 0:
                ldapServerObject.unbind()
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + str(e)

###############################################################################

