# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

from qt import *
from copy import deepcopy
import string
import ldap
import os.path
import re
import base64

from base.backend.ServerList import ServerList
import environment
from base.utils.backend.templateutils import *
from base.utils.gui.TemplateObjectWidget import TemplateObjectWidget
from base.backend.LumaConnection import LumaConnection
#from base.utils import lumaStringDecode, lumaStringEncode

class BrowserWidget(QListView):
    """ Widget for browsing ldap trees. 
    
    It gets all server information from the Luma config file.
    """

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

        tmpDirObject = environment.lumaInstallationPrefix
        tmpIconFile = os.path.join(tmpDirObject, "lib", "luma", "base", "utils", "icons", "secure.png")

        tmpObject = ServerList()
        tmpObject.readServerList()
        
        self.serverListObject = tmpObject
        
        if (tmpObject.SERVERLIST == None):
            self.SERVERLIST = []
        else:
            self.SERVERLIST = tmpObject.SERVERLIST[:]
            
        for x in self.SERVERLIST:
            tmpItem = QListViewItem(self, x.name)
            if x.tls == 1:
                tmpItem.setPixmap(0, QPixmap(tmpIconFile))
            self.insertItem(tmpItem)
            tmpBase = QListViewItem(tmpItem, x.baseDN)
            tmpBase.setExpandable(1)
            tmpItem.insertItem(tmpBase)

            
        # different menus for right click
        self.popupMenu = QPopupMenu()
        self.exportMenu = QPopupMenu()
        self.addItemMenu = QPopupMenu()
        self.deleteMenu = QPopupMenu()
        
        # Icon files for the menu entries
        addIconFile = os.path.join(tmpDirObject, "share", "luma", "icons", "newEntry.png")
        delIconFile = os.path.join(tmpDirObject, "share", "luma", "icons", "deleteEntry.png")
        exportIconFile = os.path.join(tmpDirObject, "share", "luma", "icons", "exportLdif.png")
        
        
        # Fill export menu
        self.exportMenu.insertItem(self.trUtf8("Item"), self.__export_item)
        self.exportMenu.insertItem(self.trUtf8("Subtree"), self.__export_item_subtree)
        self.exportMenu.insertItem(self.trUtf8("Subtree with Parents"), self.__export_item_all)

        
        # Fill delete menu
        self.deleteMenu.insertItem(self.trUtf8("Item"), self.deleteItem)
        self.deleteMenu.insertItem(self.trUtf8("Subtree"), self.deleteItemsRecursive)
        self.deleteMenu.insertItem(self.trUtf8("Subtree without Node"), self.deleteSubtree)
        
        
        self.popupMenu.insertItem(QIconSet(QPixmap(addIconFile)), self.trUtf8("Add Item"), self.addItemMenu)
        self.popupMenu.insertSeparator()
        self.popupMenu.insertItem(QIconSet(QPixmap(exportIconFile)), self.trUtf8("Export to LDIF"), self.exportMenu)
        self.popupMenu.insertSeparator()
        self.popupMenu.insertItem(QIconSet(QPixmap(delIconFile)), self.trUtf8("Delete"), self.deleteMenu)
        
        
        self.connect(self.addItemMenu, SIGNAL("aboutToShow()"), self.create_add_menu)

        self.addItemWidgets = []

        self.connect(self, SIGNAL("rightButtonPressed(QListViewItem*, const QPoint&, int)"), self.__show_popup)

###############################################################################

    def item_clicked(self, item):
        """ Emit the ldap object and the server if a valid object has been
        clicked.
        """
        
        if not(item == None):
            fullPath = self.get_full_path(item)
            try:
                server, result = self.getLdapItem(fullPath)
                self.emit(PYSIGNAL("ldap_result"), (deepcopy(server), deepcopy(result),))
            except TypeError:
                "No result from Server"


###############################################################################

    def item_expanded(self, item):
        """ Get all children of the expanded object and display them.
        """
        
        fullPath = self.get_full_path(item)
        results = self.getLdapItemChildren(fullPath, 0)
        if results == None:
            return None
            item.setExpandable(0)
        if len(results) == 0:
            item.setExpandable(0)
            return None
        for x in results:
            tmp = x[0].decode('utf-8')
            tmp = string.split(tmp, ",")
            tmpItem = QListViewItem(item, tmp[0])
            tmpItem.setExpandable(1)
            item.insertItem(tmpItem)


###############################################################################

    def item_collapsed(self, item):
        """ Delete all children if a ldap object collapses.
        """
        
        fullPath = self.get_full_path(item)
        serverName, ldapObject = self.__split_path(fullPath)
        if len(ldapObject) == 0:
            return None
        while item.childCount() > 0:
            item.takeItem(item.firstChild())

###############################################################################

    def get_full_path(self, item):
        """ Return the full dn of an object, including its server.
        """
        
        try:
            fullPath = unicode(item.text(0)).encode('utf-8')
            while item.parent():
                item = item.parent()
                fullPath = fullPath + "," + unicode(item.text(0)).encode('utf-8')
            return fullPath
        except AttributeError:
            pass

###############################################################################

    def getLdapItem(self, itemPath):
        """ Get all data of a ldap object given by its path.
        """
        
        serverName, ldapObject = self.__split_path(itemPath)
        if len(ldapObject) == 0:
            return None
        
        serverMeta = self.serverListObject.get_serverobject(serverName)
        
        conObject = LumaConnection(serverMeta)
        searchResult = conObject.search_s(ldapObject.encode('utf-8'), ldap.SCOPE_BASE)
        if searchResult == None:
            QMessageBox.critical(None,
                self.trUtf8("Error"),
                self.trUtf8("""Could not access entry.
See console output for more information."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)
            
        return serverName, searchResult
        
###############################################################################

    def __split_path(self, itemPath):
        """ Return the server and the DN of an items path.
        """
        
        tmp = string.split(itemPath, ",")
        serverName = tmp[-1]
        ldapObject = itemPath[:-len(serverName)-1]
        return serverName, ldapObject

###############################################################################

    def getLdapItemChildren(self, itemPath, allLevel):
        """ Return a list of children a ldap object has.
        
        allLevel == 1:
            get whole subtree
            
        allLevel == 0:
            get only next level
        """
        
        serverName, ldapObject = self.__split_path(itemPath)
        if len(ldapObject) == 0:
            return None
            
        serverMeta = self.serverListObject.get_serverobject(serverName)
        searchResult = None
        
        conObject = LumaConnection(serverMeta)
        
        # allLevel defines whether the complete subtree is searched or
            # just one level
        searchLevel = None
        if allLevel:
            searchLevel = ldap.SCOPE_SUBTREE
        else:
            searchLevel = ldap.SCOPE_ONELEVEL
                
        searchResult = conObject.search(ldapObject.encode('utf-8'), searchLevel,self.searchObjectClass, None, 0)

        return searchResult
        



###############################################################################

    def set_search_class(self, classList):
        """ Display only ldap values which are in classList.
        """
        
        self.searchObjectClass = "(|"
        for x in classList:
            self.searchObjectClass = self.searchObjectClass + \
                    "(objectClass=" + x + ")"
        self.searchObjectClass = self.searchObjectClass + ")"

###############################################################################

    def __export_item(self):
        """ Export the selected item to ldif.
        """
        
        fullPath = self.get_full_path(self.selectedItem())
        result = self.getLdapItem(fullPath)
        ldifString = self.__convert_to_ldif(result[1])
        self.__save_ldif(ldifString)

###############################################################################

    def __export_item_subtree(self):
        """ Export the whole subtree to ldif.
        """
        
        fullPath = self.get_full_path(self.selectedItem())
        results = self.getLdapItemChildren(fullPath, 1)
        resultString = self.__convert_to_ldif(results)
        self.__save_ldif(resultString)

###############################################################################

    def __export_item_all(self):
        """ Export the whole subtree to ldif, together with all its parents.
        """
        
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

    def deleteItem(self):
        """ Delete selected item from the server.
        """
        
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
        """ Display popup menu.
        """
        
        if not (tmpItem == None):
            if not (tmpItem.parent() == None):
                self.popupMenu.exec_loop(point)

###############################################################################

    def __convert_to_ldif(self, data):
        """ Convert data of a ldap object to ldif format.
        """
        
        SAFE_STRING_PATTERN = '(^(\000|\n|\r| |:|<)|[\000\n\r\200-\377]+|[ ]+$)'
        safe_string_re = re.compile(SAFE_STRING_PATTERN)

        
        tmpListe = []
        if data == None:
            data = []
        for a in data:
            tmpListe.append("dn: " + a[0] + "\n")
            for x in a[1].keys():
                for y in a[1][x]:
                    if not (safe_string_re.search(y) == None):
                        tmpListe.append(x + ":: " + base64.encodestring(y))
                    else:
                        tmpListe.append(x + ": " + y + "\n")

            tmpListe.append("\n")
        return string.join(tmpListe, "")

###############################################################################

    def __save_ldif(self, data):
        """ Save ldif data to file.
        """
        
        if not (len(data) == 0):
            fileName = unicode(QFileDialog.getSaveFileName())
            if fileName == '':
                return
            try:
                fileHandler = open(fileName, 'w')
                fileHandler.write(data)
                fileHandler.close()
            except IOError, e:
                print "Could not save Data"
                print "Reason: " + unicode(e)

###############################################################################

    def __get_parents(self, item):
        """ Get all parents of an item.
        """
        
        parentList = []
        while (item.parent()):
            item = item.parent()
            parentList.append(self.get_full_path(item))
        parentList.reverse()
        del parentList[0]
        return parentList

###############################################################################

    def create_add_menu(self):
        """ Fill the 'add'-menu with entries from the templates.
        """
        
        self.addItemMenu.clear()
        tFile = TemplateFile()
        for x in tFile.tplList:
            self.addItemMenu.insertItem(x.name, self.add_item)
            
###############################################################################

    def add_item(self, id):
        """ Add an item to ldap.
        
        id gives the menu entrie which was clicked and which template was 
        chosen.
        """
        
        templateName = unicode(self.addItemMenu.text(id))
        
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
        
    def deleteItemsRecursive(self, withParent=1):
        """ Delete the subtree of the selected item.
        
        withParent == 1:
            delete the selected item, too
            
        withParent == 0:
            do not delete the selected item
        """
        
        warnString = self.trUtf8('Do you really want to delete the items recursively from the server?')
        result = QMessageBox.warning(self, self.trUtf8('Delete entries'), warnString, self.trUtf8('Delete'), self.trUtf8('Cancel'))
        if result == 1:
            return
            
        # set gui busy
        environment.set_busy(1)
        
        currentItem = self.selectedItem()
        
        parent = currentItem.parent()
        fullPath = self.get_full_path(currentItem)
        children = self.getLdapItemChildren(fullPath, 1)
        
        serverName, selectedObject = self.__split_path(fullPath)
        if len(selectedObject) == 0:
            return None
            
        if (not withParent):
            del children[0]
        
        while ((len(children) > 0) and (not(children == None))) :
            environment.update_ui()
            self.__delete_ldap_entry(serverName, children[-1][0])
            del children[-1]
        
        parent.setOpen(0)
        parent.setOpen(1)
        
        environment.set_busy(0)
        
###############################################################################

    def deleteSubtree(self):
        """ Delete the subtree of the selected item.
        """
        
        self.deleteItemsRecursive(0)

###############################################################################

    def __delete_ldap_entry(self, serverName, ldapObject):
        """ Delete a ldap object from the server given by serverName and
       ldapObject. 
        """
        
        serverMeta = self.serverListObject.get_serverobject(serverName)
        
        try:
            ldapServerObject = ldap.open(serverMeta.host)
            ldapServerObject.protocol_version = ldap.VERSION3
            if serverMeta.tls == 1:
                ldapServerObject.start_tls_s()
            if len(serverMeta.bindDN) > 0:
                ldapServerObject.simple_bind_s(serverMeta.bindDN,
                                serverMeta.bindPassword)
            ldapServerObject.delete_s(ldapObject)
            if len(serverMeta.bindDN) > 0:
                ldapServerObject.unbind()
        except ldap.LDAPError, e:
            print "Error during LDAP request"
            print "Reason: " + unicode(e)
            QMessageBox.critical(None,
                self.trUtf8("Error "),
                self.trUtf8("""Delete operation was not succesful.
See console output for more information."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)


###############################################################################

