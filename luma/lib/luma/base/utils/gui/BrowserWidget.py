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
from base.utils.gui.ObjectWidget import ObjectWidget
from base.backend.LumaConnection import LumaConnection
from base.utils import isBinaryAttribute
from base.utils.backend.LdifHelper import LdifHelper

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
        tmpIconFile = os.path.join(tmpDirObject, "share", "luma", "icons", "secure.png")

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
        
        self.blockSignals(True)
        
        if not(item == None):
            fullPath = self.get_full_path(item)
            try:
                server, result = self.getLdapItem(fullPath)
                self.blockSignals(False)
                self.emit(PYSIGNAL("about_to_change"), ())
                self.emit(PYSIGNAL("ldap_result"), (deepcopy(server), deepcopy(result),))
            except TypeError:
                "No result from Server"
                

        self.blockSignals(False)


###############################################################################

    def item_expanded(self, item):
        """ Get all children of the expanded object and display them.
        """
        
        self.blockSignals(True)
        
        fullPath = self.get_full_path(item)
        results = self.getLdapItemChildren(fullPath, 0)
        
        if results == None:
            self.blockSignals(False)
            return None
            item.setExpandable(0)
        if len(results) == 0:
            self.blockSignals(False)
            item.setExpandable(0)
            return None
    
        for x in results:
            tmp = x[0].decode('utf-8')
            tmp = string.split(tmp, ",")
            tmpItem = QListViewItem(item, tmp[0])
            tmpItem.setExpandable(1)
            item.insertItem(tmpItem)

        self.blockSignals(False)
            
###############################################################################

    def item_collapsed(self, item):
        """ Delete all children if a ldap object collapses.
        """
        
        self.blockSignals(True)
        
        fullPath = self.get_full_path(item)
        serverName, ldapObject = self.__split_path(fullPath)
        if len(ldapObject) == 0:
            self.blockSignals(False)
            return None
        while item.childCount() > 0:
            item.takeItem(item.firstChild())
            
        self.blockSignals(False)

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
        conObject.bind()
        searchResult = conObject.search_s(ldapObject, ldap.SCOPE_BASE)
        conObject.unbind()
        
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
        conObject.bind()
        
        # allLevel defines whether the complete subtree is searched or
            # just one level
        searchLevel = None
        if allLevel:
            searchLevel = ldap.SCOPE_SUBTREE
        else:
            searchLevel = ldap.SCOPE_ONELEVEL
                
        searchResult = conObject.search(ldapObject.encode('utf-8'), searchLevel,self.searchObjectClass, None, 0)

        conObject.unbind()
        
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
        serverName = fullPath.split(",")[-1]
        result = self.getLdapItem(fullPath)
        ldifHelper = LdifHelper(serverName)
        self.__save_ldif(ldifHelper.convertToLdif(result[1]))

###############################################################################

    def __export_item_subtree(self):
        """ Export the whole subtree to ldif.
        """
        
        fullPath = self.get_full_path(self.selectedItem())
        serverName = fullPath.split(",")[-1]
        result = self.getLdapItemChildren(fullPath, 1)
        ldifHelper = LdifHelper(serverName)
        self.__save_ldif(ldifHelper.convertToLdif(result))

###############################################################################

    def __export_item_all(self):
        """ Export the whole subtree to ldif, together with all its parents.
        """
        
        currentItem = self.selectedItem()
        fullPath = self.get_full_path(currentItem)
        serverName = fullPath.split(",")[-1]
        ldifHelper = LdifHelper(serverName)
        parents = self.__get_parents(currentItem)
        resultString = ""
        for x in parents:
            tmpResult = self.getLdapItem(x)
            resultString = resultString + ldifHelper.convertToLdif(tmpResult[1])
        subtree = self.getLdapItemChildren(fullPath, 1)
        subtreeString = ldifHelper.convertToLdif(subtree)
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
        data = template.getDataObject()
        
        if template == None:
            return 
            
        fqn = self.get_full_path(self.selectedItem())
        tmpList = fqn.split(",")
        
        server = tmpList[-1]
        del tmpList[-1]
        
        dn = ",".join(tmpList)
        
        fullData = [(dn, data)]
        
        widget = ObjectWidget(None, template.name, 0)
        widget.setMinimumHeight(500)
        widget.setMinimumWidth(600)
        widget.setCaption(self.trUtf8('Add entry'))
        widget.initView(server, fullData, True)
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
        environment.setBusy(1)
        
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
            environment.updateUI()
            self.__delete_ldap_entry(serverName, children[-1][0])
            del children[-1]
        
        parent.setOpen(0)
        parent.setOpen(1)
        
        environment.setBusy(0)
        
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
        
        connectionObject = LumaConnection(serverMeta)
        connectionObject.bind()
        result = connectionObject.delete_s(ldapObject)
        connectionObject.unbind()
        
        if result == 0:
            QMessageBox.critical(None,
                self.trUtf8("Error "),
                self.trUtf8("""Delete operation was not succesful.
See console output for more information."""),
                self.trUtf8("&OK"),
                None,
                None,
                0, -1)


###############################################################################

