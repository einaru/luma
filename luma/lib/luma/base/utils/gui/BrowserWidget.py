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
from base.utils.gui.AdvancedObjectWidget import AdvancedObjectWidget
from base.backend.LumaConnection import LumaConnection
from base.utils import isBinaryAttribute
from base.utils import escapeSpecialChars
from base.utils.gui.LumaErrorDialog import LumaErrorDialog
from base.utils.gui.DeleteDialog import DeleteDialog
from base.utils.gui.ExportDialog import ExportDialog

class BrowserWidget(QListView):
    """ Widget for browsing ldap trees. 
    
    It gets all server information from the Luma config file.
    """

    def __init__(self,parent = None,name = None,fl = 0):
        QListView.__init__(self,parent,name,fl)

        self.connect(self, SIGNAL("clicked(QListViewItem*)"), self.itemClicked)
        self.connect(self, SIGNAL("collapsed(QListViewItem*)"), self.itemCollapsed)
        self.connect(self, SIGNAL("expanded(QListViewItem*)"), self.itemExpanded)
        #self.connect(self, SIGNAL("doubleClicked(QListViewItem*)"), self.itemExpanded)

        self.setRootIsDecorated(1)
        self.addColumn(self.trUtf8("Entries"))
        self.setResizeMode(QListView.AllColumns)

        self.searchObjectClass = "(objectClass=*)"
        # Example for filtering the entries
        # self.setSearchClass(['organizationalUnit', 'dcObject', 'organization'])

        tmpDirObject = environment.lumaInstallationPrefix
        
        self.iconPath = os.path.join(tmpDirObject, "share", "luma", "icons")
        self.secureIcon = QPixmap(os.path.join(self.iconPath, "secure.png"))
        self.aliasIcon = QPixmap(os.path.join(self.iconPath, "alias.png"))
        self.secureAliasIcon = QPixmap(os.path.join(self.iconPath, "secure-alias.png"))

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

        self.displayServerIcons()

        self.addItemWidgets = []

        self.connect(self, SIGNAL("rightButtonPressed(QListViewItem*, const QPoint&, int)"), self.showPopup)
        
        self.widgetList = []
        
        # Item for which a popup menu was openend
        self.popupItem = None
        
        # Menu for adding new objects
        self.addItemMenu = None
        
        # The baseDN of the currently selected item
        self.currentBase = None

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
        
        if not (item == None):
            fullPath = self.getFullPath(item)

            success, resultList, exceptionObject = self.getLdapItem(fullPath)
            
            if not (None == success):
                if success:
                    if len(resultList) > 0:
                        result = resultList[0]
                        result.serverMeta.currentBase = self.currentBase
                        self.emit(PYSIGNAL("about_to_change"), ())
                        self.emit(PYSIGNAL("ldap_result"), (deepcopy(result),))
                else:
                    dialog = LumaErrorDialog()
                    errorMsg = self.trUtf8("Could not access entry.<br><br>Reason: ")
                    errorMsg.append(str(exceptionObject))
                    dialog.setErrorMessage(errorMsg)
                    dialog.exec_loop()

###############################################################################

    def itemExpanded(self, item):
        """ Get all children of the expanded object and display them.
        """
        
        if item.parent():
            fullPath = self.getFullPath(item)
            
            serverName, dn = self.splitPath(fullPath)
            oldAliasValue = self.aliasDict[serverName]
            self.aliasDict[serverName] = False
            
            success, resultList, exceptionObject = self.getLdapItemChildren(fullPath, 0, ['dn', 'objectClass'])
        
            if success:
                if len(resultList) == 0:
                    self.aliasDict[serverName] = oldAliasValue
                    item.setExpandable(0)
                else:
                    for x in resultList:
                        tmp = x.getPrettyRDN()
                        tmpItem = QListViewItem(item, tmp)
                
                        # Add the alias icon if the entry belongs to the 
                        # alias objectClass
                        if x.isAliasObject():
                            tmpItem.setPixmap(0, self.aliasIcon)
                    
                        tmpItem.setExpandable(1)
                        item.insertItem(tmpItem)
                        
                    self.aliasDict[serverName] = oldAliasValue
                    
            else:
                self.aliasDict[serverName] = oldAliasValue
                item.setExpandable(0)
                
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not expand entry.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                
        else:
            serverList = ServerList()
            serverList.readServerList()
            serverMeta = serverList.getServerObject(self.getFullPath(item))
            tmpList = []
            if serverMeta.autoBase:
                success, tmpList, exceptionObject = LumaConnection(serverMeta).getBaseDNList()
                
                if not success:
                    dialog = LumaErrorDialog()
                    errorMsg = self.trUtf8("Could not retrieve baseDN.<br><br>Reason: ")
                    errorMsg.append(str(exceptionObject))
                    dialog.setErrorMessage(errorMsg)
                    dialog.exec_loop()
                    
            else:
                tmpList = serverMeta.baseDN
                
            if None == tmpList:
                tmpList = []
                
            for base in tmpList:
                tmpBase = QListViewItem(item, base)
                tmpBase.setExpandable(1)
            
###############################################################################

    def itemCollapsed(self, item):
        """ Delete all children if a ldap object collapses.
        """
        
        fullPath = self.getFullPath(item)
        serverName, ldapObject = self.splitPath(fullPath)
        while item.childCount() > 0:
            item.takeItem(item.firstChild())

###############################################################################

    def getFullPath(self, item):
        """ Return the full dn of an object, including its server.
        """
        
        try:
            tmpList = []
            
            pathItem = unicode(item.text(0)).encode('utf-8')
            pathItem = escapeSpecialChars(pathItem)
            tmpList.append(pathItem)
            
            while item.parent():
                oldItem = item
                item = item.parent()
                
                # Try to get the currently used baseDN
                if not (None == item):
                    tmpItem = item.parent()
                    if None == tmpItem:
                        self.currentBase = unicode(oldItem.text(0)).encode('utf-8')
                    
                pathItem = unicode(item.text(0)).encode('utf-8')
                pathItem = escapeSpecialChars(pathItem)
                tmpList.append(pathItem)

            return ",".join(tmpList)
        except AttributeError, e:
            print "Attribute Error in function 'BrowserWidget.getFullPath()'. Reason:"
            print e

###############################################################################

    def getLdapItem(self, itemPath):
        """ Get all data of a ldap object given by its path.
        """
        
        serverName, ldapObject = self.splitPath(itemPath)
        if len(ldapObject) == 0:
            return (None, None, None)
        
        serverMeta = self.serverListObject.getServerObject(serverName)
        
        serverMeta.followAliases = self.aliasDict[serverName]
        
        conObject = LumaConnection(serverMeta)
        bindSuccess, exceptionObject = conObject.bind()
        
        if not bindSuccess:
                return (False, None, exceptionObject)
                
        success, resultList, exceptionObject = conObject.search(ldapObject, ldap.SCOPE_BASE)
        conObject.unbind()
    
        return (success, resultList, exceptionObject)
        
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
        bindSuccess, exceptionObject = conObject.bind()
        
        if not bindSuccess:
            return (False, None, exceptionObject)
        
        # allLevel defines whether the complete subtree is searched or
        # just one level
        searchLevel = None
        if allLevel:
            searchLevel = ldap.SCOPE_SUBTREE
        else:
            searchLevel = ldap.SCOPE_ONELEVEL
            
                
        success, resultList, exceptionObject = conObject.search(ldapObject, searchLevel,self.searchObjectClass, noAttributes, 0)

        conObject.unbind()
        
        return (success, resultList, exceptionObject)
        



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
        success, resultList, exceptionObject = self.getLdapItem(fullPath)
        
        if success and (len(resultList) > 0):
                exportDialog = ExportDialog()
                exportDialog.initData(resultList)
                exportDialog.exec_loop()
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not export item.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()

###############################################################################

    def exportItemSubtree(self):
        """ Export the whole subtree to ldif.
        """
        
        fullPath = self.getFullPath(self.selectedItem())
        success, resultList, exceptionObject = self.getLdapItemChildren(fullPath, 1)
        
        if success and (len(resultList) > 0):
            exportDialog = ExportDialog()
            exportDialog.initData(resultList)
            exportDialog.exec_loop()
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not export items.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
        

###############################################################################

    def exportItemAll(self):
        """ Export the whole subtree to ldif, together with all its parents.
        """
        
        
        itemList = []
        stringList = []
        searchError = False
        
        currentItem = self.selectedItem()
        fullPath = self.getFullPath(currentItem)
        exceptionObject = None
        
        parentDNList = self.getParents(currentItem)
        for x in parentDNList:
            success, resultList, exceptionObject = self.getLdapItem(x)
            if success:
                itemList.extend(resultList)
            else:
                searchError = True
                break
                
        if not searchError:
            success, subtreeList, exceptionObject = self.getLdapItemChildren(fullPath, 1)
            
            if success:
                itemList.extend(subtreeList)
                if len(itemList) > 0:
                    exportDialog = ExportDialog()
                    exportDialog.initData(itemList)
                    exportDialog.exec_loop()
            else:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not export items.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not export items.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()

###############################################################################

    def deleteItem(self):
        """ Delete selected item from the server.
        """
        
        item = self.selectedItem()
        parent = item.parent()
        fullPath = self.getFullPath(item)
        serverName, ldapObject = self.splitPath(fullPath)
        if len(ldapObject) == 0:
            return None
            
        success, resultList, exceptionObject = self.getLdapItem(fullPath)
        
        if success:
            if len(resultList) > 0:
                deleteDialog = DeleteDialog()
                deleteDialog.initData(resultList)
                deleteDialog.exec_loop()
                parent.setOpen(0)
                parent.setOpen(1)
                self.setSelected(parent, True)
                self.itemClicked(parent)
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not retrieve entry for deletion.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()


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
                popupMenu.insertItem(QIconSet(QPixmap(exportIconFile)), self.trUtf8("Export"), exportMenu)
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
        
        # get the template object for the selected template name
        templateName = unicode(self.addItemMenu.text(id))
        templates = TemplateList()
        template = templates.getTemplate(templateName)
        
        # get server name and basedn from where to add
        fqn = self.getFullPath(self.selectedItem())
        tmpList = fqn.split(",")
                
        serverName = tmpList[-1]
        del tmpList[-1]
        
        baseDN = ",".join(tmpList)
        
        tmpObject = ServerList()
        tmpObject.readServerList()
        serverMeta = tmpObject.getServerObject(serverName)
        
        smartObject = template.getDataObject(serverMeta, baseDN)
        
        floatingWidget = ChildWindow(None)
        self.widgetList.append(floatingWidget)
        widget = AdvancedObjectWidget(floatingWidget, template.name.encode("utf-8"), 0)
        widget.baseDN = baseDN
    
        floatingWidget.setCentralWidget(widget)
        widget.setCaption(self.trUtf8('Add entry'))
        widget.buildToolBar(floatingWidget)
        widget.initView(smartObject, True)
        
        self.connect(floatingWidget, PYSIGNAL("child_closed"), self.cleanChildren)
        floatingWidget.resize(500, 400)
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
        
        currentItem = self.selectedItem()
        
        parent = currentItem.parent()
        fullPath = self.getFullPath(currentItem)
        success, childrenList, exceptionObject = self.getLdapItemChildren(fullPath, 1)
        
        if success:
            if len(childrenList) > 0:
                if (not withParent):
                    del childrenList[0]
                
                childrenList.sort()
                #print map(lambda x: x.getDN(), childrenList)
                deleteDialog = DeleteDialog()
                deleteDialog.initData(childrenList)
                deleteDialog.exec_loop()
                parent.setOpen(0)
                parent.setOpen(1)
                self.setSelected(parent, True)
                self.itemClicked(parent)
            else:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not retrieve entry for deletion.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
            
            
            
            #serverName, selectedObject = self.splitPath(fullPath)
            #if len(selectedObject) == 0:
            #    return
            
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
        bindSuccess, exceptionObject = connectionObject.bind()
        
        if not bindSuccess:
            return (False, exceptionObject)
            
        success, exceptionObject = connectionObject.delete(ldapObject)
        connectionObject.unbind()
        
        return (success, exceptionObject)

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

    def reopenDN(self, dnString):
        """ Reopens the listitem for the given dnString.
        
        The dnString consits of the actuacl dn and its server alias appended. Example:
        ou=foo,o=bar,MyServerAlias
        """
        
        listIterator = QListViewItemIterator(self)
        while listIterator.current():
            item = listIterator.current()
            itemDN = self.getFullPath(item)
            
            if dnString == itemDN:
                item.setOpen(0)
                item.setOpen(1)
                break
                
            listIterator += 1
        
###############################################################################



class ChildWindow(QMainWindow):
    
    def __init__(self, parent = None):
        QMainWindow.__init__(self)
        
        
    def closeEvent(self, event):
        self.emit(PYSIGNAL("child_closed"), (self,))
        self.deleteLater()
        
