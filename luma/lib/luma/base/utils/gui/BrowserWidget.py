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

        self.connect(self, SIGNAL("clicked(QListViewItem*)"), self.itemClicked)
        self.connect(self, SIGNAL("collapsed(QListViewItem*)"), self.itemCollapsed)
        self.connect(self, SIGNAL("expanded(QListViewItem*)"), self.itemExpanded)

        self.setRootIsDecorated(1)
        self.addColumn(self.trUtf8("Entries"))
        self.setResizeMode(QListView.AllColumns)

        self.searchObjectClass = "(objectClass=*)"
        # Example for filtering the entries
        #self.set_search_class(['organizationalUnit', \
        #       'dcObject', 'organization'])

        tmpDirObject = environment.lumaInstallationPrefix
        
        self.secureIcon = QPixmap(os.path.join(tmpDirObject, "share", "luma", "icons", "secure.png"))
        self.aliasIcon = QPixmap(os.path.join(tmpDirObject, "share", "luma", "icons", "alias.png"))
        self.secureAliasIcon = QPixmap(os.path.join(tmpDirObject, "share", "luma", "icons", "secure-alias.png"))

        tmpObject = ServerList()
        tmpObject.readServerList()
        
        self.serverListObject = tmpObject
        
        if (tmpObject.serverList == None):
            self.serverList = []
        else:
            self.serverList = tmpObject.serverList[:]
                
        self.serverDict = {}
        self.aliasDict = {}
            
        for x in self.serverList:
            tmpItem = QListViewItem(self, x.name)
            tmpItem.setExpandable(True)
            self.serverDict[x.name] = tmpItem
            self.aliasDict[x.name] = x.followAliases
            #if x.tls == 1:
            #    tmpItem.setPixmap(0, QPixmap(tmpIconFile))
            #self.insertItem(tmpItem)

        self.displayServerIcons()

        self.addItemWidgets = []

        self.connect(self, SIGNAL("rightButtonPressed(QListViewItem*, const QPoint&, int)"), self.showPopup)
        
        self.widgetList = []
        
        # Item for which a popup menu was openend
        self.popupItem = None
        
        # Menu for adding new objects
        self.addItemMenu = None

###############################################################################

    def displayServerIcons(self):
        for server in self.aliasDict.keys():
            serverMeta = self.serverListObject.getServerObject(server)
            tmpItem = self.serverDict[server]
            if serverMeta.tls and self.aliasDict[server]:
                tmpItem.setPixmap(0, self.secureAliasIcon)
            elif serverMeta.tls:
                tmpItem.setPixmap(0, self.secureIcon)
            elif self.aliasDict[server]:
                tmpItem.setPixmap(0, self.aliasIcon)
            else:
                tmpItem.setPixmap(0, QPixmap())

###############################################################################

    def itemClicked(self, item):
        """ Emit the ldap object and the server if a valid object has been
        clicked.
        """
        
        self.blockSignals(True)
        
        if not(item == None):
            fullPath = self.getFullPath(item)
            try:
                server, result = self.getLdapItem(fullPath)
                self.blockSignals(False)
                self.emit(PYSIGNAL("about_to_change"), ())
                self.emit(PYSIGNAL("ldap_result"), (deepcopy(server), deepcopy(result),))
            except TypeError:
                "No result from Server"
                

        self.blockSignals(False)


###############################################################################

    def itemExpanded(self, item):
        """ Get all children of the expanded object and display them.
        """
        
        self.blockSignals(True)
        
        if item.parent():
            fullPath = self.getFullPath(item)
            
            serverName, dn = self.splitPath(fullPath)
            oldAliasValue = self.aliasDict[serverName]
            self.aliasDict[serverName] = False
            
            results = self.getLdapItemChildren(fullPath, 0, ['dn', 'objectClass'])
        
            if results == None:
                self.aliasDict[serverName] = oldAliasValue
                self.blockSignals(False)
                item.setExpandable(0)
                return None
            if len(results) == 0:
                self.aliasDict[serverName] = oldAliasValue
                self.blockSignals(False)
                item.setExpandable(0)
                return None
    
            for x in results:
                tmp = x[0].decode('utf-8')
                tmp = string.split(tmp, ",")
                tmpItem = QListViewItem(item, tmp[0])
                
                # Add the alias icon if the entry belongs to the 
                # alias objectClass
                values = x[1]
                if values.has_key('objectClass'):
                    for x in values['objectClass']:
                        if 'alias' == string.lower(x):
                            tmpItem.setPixmap(0, self.aliasIcon)
                    
                tmpItem.setExpandable(1)
                item.insertItem(tmpItem)
            
            self.aliasDict[serverName] = oldAliasValue
        else:
            serverList = ServerList()
            serverList.readServerList()
            serverMeta = serverList.getServerObject(self.getFullPath(item))
            tmpList = None
            if serverMeta.autoBase:
                tmpList = LumaConnection(serverMeta).getBaseDNList()
            else:
                tmpList = serverMeta.baseDN
                
            for base in tmpList:
                tmpBase = QListViewItem(item, base)
                tmpBase.setExpandable(1)

        self.blockSignals(False)
            
###############################################################################

    def itemCollapsed(self, item):
        """ Delete all children if a ldap object collapses.
        """
        
        self.blockSignals(True)
        
        fullPath = self.getFullPath(item)
        serverName, ldapObject = self.splitPath(fullPath)
        while item.childCount() > 0:
            item.takeItem(item.firstChild())
            
        self.blockSignals(False)

###############################################################################

    def getFullPath(self, item):
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
        
        serverName, ldapObject = self.splitPath(itemPath)
        if len(ldapObject) == 0:
            return None
        
        serverMeta = self.serverListObject.getServerObject(serverName)
        
        serverMeta.followAliases = self.aliasDict[serverName]
        
        conObject = LumaConnection(serverMeta)
        conObject.bind()
        searchResult = conObject.search(ldapObject, ldap.SCOPE_BASE)
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

    def splitPath(self, itemPath):
        """ Return the server and the DN of an items path.
        """
        
        tmp = string.split(itemPath, ",")
        serverName = tmp[-1]
        ldapObject = itemPath[:-len(serverName)-1]
        return serverName, ldapObject

###############################################################################

    def getLdapItemChildren(self, itemPath, allLevel, noAttributes=None):
        """ Return a list of children a ldap object has.
        
        allLevel == 1:
            get whole subtree
            
        allLevel == 0:
            get only next level
        """
        
        serverName, ldapObject = self.splitPath(itemPath)
        if len(ldapObject) == 0:
            return None
            
        serverMeta = self.serverListObject.getServerObject(serverName)
        searchResult = None
        
        serverMeta.followAliases = self.aliasDict[serverName]
        
        conObject = LumaConnection(serverMeta)
        conObject.bind()
        
        # allLevel defines whether the complete subtree is searched or
        # just one level
        searchLevel = None
        if allLevel:
            searchLevel = ldap.SCOPE_SUBTREE
        else:
            searchLevel = ldap.SCOPE_ONELEVEL
            
                
        searchResult = conObject.search(ldapObject, searchLevel,self.searchObjectClass, noAttributes, 0)

        conObject.unbind()
        
        return searchResult
        



###############################################################################

    def setSearchClass(self, classList):
        """ Display only ldap values which are in classList.
        """
        
        self.searchObjectClass = "(|"
        for x in classList:
            self.searchObjectClass = self.searchObjectClass + \
                    "(objectClass=" + x + ")"
        self.searchObjectClass = self.searchObjectClass + ")"

###############################################################################

    def exportItem(self):
        """ Export the selected item to ldif.
        """
        
        fullPath = self.getFullPath(self.selectedItem())
        serverName = fullPath.split(",")[-1]
        result = self.getLdapItem(fullPath)
        ldifHelper = LdifHelper(serverName)
        self.saveLdif(ldifHelper.convertToLdif(result[1]))

###############################################################################

    def exportItemSubtree(self):
        """ Export the whole subtree to ldif.
        """
        
        fullPath = self.getFullPath(self.selectedItem())
        serverName = fullPath.split(",")[-1]
        result = self.getLdapItemChildren(fullPath, 1)
        ldifHelper = LdifHelper(serverName)
        self.saveLdif(ldifHelper.convertToLdif(result))

###############################################################################

    def exportItemAll(self):
        """ Export the whole subtree to ldif, together with all its parents.
        """
        
        currentItem = self.selectedItem()
        fullPath = self.getFullPath(currentItem)
        serverName = fullPath.split(",")[-1]
        ldifHelper = LdifHelper(serverName)
        parents = self.getParents(currentItem)
        resultString = ""
        for x in parents:
            tmpResult = self.getLdapItem(x)
            resultString = resultString + ldifHelper.convertToLdif(tmpResult[1])
        subtree = self.getLdapItemChildren(fullPath, 1)
        subtreeString = ldifHelper.convertToLdif(subtree)
        self.saveLdif(resultString + subtreeString)


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
        fullPath = self.getFullPath(item)
        serverName, ldapObject = self.splitPath(fullPath)
        if len(ldapObject) == 0:
            return None
            
        self.deleteLdapEntry(serverName, ldapObject)
        
        parent.setOpen(0)
        parent.setOpen(1)
        


###############################################################################

    def showPopup(self, tmpItem=None, point=None, itemId=None):
        """ Display popup menu.
        """
        
        self.popupItem = tmpItem
        
        tmpDirObject = environment.lumaInstallationPrefix
        aliasIconFile = os.path.join(tmpDirObject, "share", "luma", "icons", "alias.png")
        popupMenu = QPopupMenu()
        
        itemPath = self.getFullPath(tmpItem)
        server, dn = self.splitPath(itemPath)
        
        if not (tmpItem == None):
            menuID = popupMenu.insertItem(QIconSet(QPixmap(aliasIconFile)), self.trUtf8("Follow Aliases"), self.enableAliases)
            popupMenu.setItemChecked(menuID, self.aliasDict[server])
                
            if not (tmpItem.parent() == None):
                # different menus for right click
                exportMenu = QPopupMenu()
                self.addItemMenu = QPopupMenu()
                deleteMenu = QPopupMenu()
        
                # Icon files for the menu entries
                addIconFile = os.path.join(tmpDirObject, "share", "luma", "icons", "newEntry.png")
                delIconFile = os.path.join(tmpDirObject, "share", "luma", "icons", "deleteEntry.png")
                exportIconFile = os.path.join(tmpDirObject, "share", "luma", "icons", "exportLdif.png")
        
        
                # Fill export menu
                exportMenu.insertItem(self.trUtf8("Item"), self.exportItem)
                exportMenu.insertItem(self.trUtf8("Subtree"), self.exportItemSubtree)
                exportMenu.insertItem(self.trUtf8("Subtree with Parents"), self.exportItemAll)

        
                # Fill delete menu
                deleteMenu.insertItem(self.trUtf8("Item"), self.deleteItem)
                deleteMenu.insertItem(self.trUtf8("Subtree"), self.deleteItemsRecursive)
                deleteMenu.insertItem(self.trUtf8("Subtree without Node"), self.deleteSubtree)
                
                # Fill add menu
                self.addItemMenu.clear()
                templates = TemplateList()
                for x in templates.templateList:
                    self.addItemMenu.insertItem(x.name, self.addItem)
                    
                popupMenu.insertSeparator()
                popupMenu.insertItem(QIconSet(QPixmap(addIconFile)), self.trUtf8("Add Item"), self.addItemMenu)
                popupMenu.insertSeparator()
                popupMenu.insertItem(QIconSet(QPixmap(exportIconFile)), self.trUtf8("Export to LDIF"), exportMenu)
                popupMenu.insertSeparator()
                popupMenu.insertItem(QIconSet(QPixmap(delIconFile)), self.trUtf8("Delete"), deleteMenu)
                
            popupMenu.exec_loop(point)

###############################################################################

    def saveLdif(self, data):
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

    def getParents(self, item):
        """ Get all parents of an item.
        """
        
        parentList = []
        while (item.parent()):
            item = item.parent()
            parentList.append(self.getFullPath(item))
        parentList.reverse()
        del parentList[0]
        return parentList

###############################################################################

    def addItem(self, id):
        """ Add an item to ldap.
        
        id gives the menu entrie which was clicked and which template was 
        chosen.
        """
        
        templateName = unicode(self.addItemMenu.text(id))
        
        templates = TemplateList()
        template = templates.getTemplate(templateName)
        data = template.getDataObject()
        
        if template == None:
            return 
            
        fqn = self.getFullPath(self.selectedItem())
        tmpList = fqn.split(",")
        
        server = tmpList[-1]
        del tmpList[-1]
        
        dn = ",".join(tmpList)
        
        fullData = [(dn, data)]
        
        floatingWidget = ChildWindow(None)
        self.widgetList.append(floatingWidget)
        widget = ObjectWidget(floatingWidget, template.name.encode("utf-8"), 0)
    
        floatingWidget.setCentralWidget(widget)
        widget.setCaption(self.trUtf8('Add entry'))
        widget.buildToolBar(floatingWidget)
        widget.initView(server, fullData, True)
        
        self.connect(floatingWidget, PYSIGNAL("child_closed"), self.cleanChildren)
        floatingWidget.show()
        
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
        environment.setBusy(True)
        
        currentItem = self.selectedItem()
        
        parent = currentItem.parent()
        fullPath = self.getFullPath(currentItem)
        children = self.getLdapItemChildren(fullPath, 1)
        
        serverName, selectedObject = self.splitPath(fullPath)
        if len(selectedObject) == 0:
            return None
            
        if (not withParent):
            del children[0]
        
        while ((len(children) > 0) and (not(children == None))) :
            environment.updateUI()
            self.deleteLdapEntry(serverName, children[-1][0])
            del children[-1]
        
        parent.setOpen(0)
        parent.setOpen(1)
        
        environment.setBusy(False)
        
###############################################################################

    def deleteSubtree(self):
        """ Delete the subtree of the selected item.
        """
        
        self.deleteItemsRecursive(0)

###############################################################################

    def deleteLdapEntry(self, serverName, ldapObject):
        """ Delete a ldap object from the server given by serverName and
       ldapObject. 
        """
        
        serverMeta = self.serverListObject.getServerObject(serverName)
        
        connectionObject = LumaConnection(serverMeta)
        connectionObject.bind()
        result = connectionObject.delete(ldapObject)
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

    def cleanChildren(self, child):
        index = self.widgetList.index(child)
        del self.widgetList[index]
        

###############################################################################
        
    def enableAliases(self):
        itemPath = self.getFullPath(self.popupItem)
        serverName, dn = self.splitPath(itemPath)
        
        self.aliasDict[serverName] = not self.aliasDict[serverName]
        
        tmpItem = self.serverDict[serverName]
        self.setOpen(tmpItem, False)
        serverMeta = self.serverListObject.getServerObject(serverName)
        serverMeta.followAliases = not serverMeta.followAliases
        self.displayServerIcons()
        
###############################################################################



class ChildWindow(QMainWindow):
    
    def __init__(self, parent = None):
        QMainWindow.__init__(self)
        
        
    def closeEvent(self, event):
        self.emit(PYSIGNAL("child_closed"), (self,))
        self.deleteLater()
        
