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
from base.utils.backend.LogObject import LogObject
from base.gui.ImprovedServerDialog import ImprovedServerDialog

class BrowserWidget(QListView):
    """ Widget for browsing ldap trees. 
    
    It gets all server information from the Luma config file.
    """

    def __init__(self,parent = None,name = None,fl = 0):
        QListView.__init__(self,parent,name,fl)
        self.setSelectionMode(QListView.Extended)

        self.connect(self, SIGNAL("mouseButtonPressed(int, QListViewItem*, const QPoint&, int)"), self.itemClicked)
        self.connect(self, SIGNAL("collapsed(QListViewItem*)"), self.itemCollapsed)
        self.connect(self, SIGNAL("expanded(QListViewItem*)"), self.itemExpanded)
        self.connect(self, SIGNAL("rightButtonPressed(QListViewItem*, const QPoint&, int)"), self.showPopup)


        self.setRootIsDecorated(True)
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
            tmpItem = BrowserItem(self, x.name)
            tmpItem.serverType = True
            tmpItem.setServerName(x.name)
            tmpItem.setExpandable(True)
            self.serverDict[x.name] = tmpItem
            self.aliasDict[x.name] = x.followAliases

        self.displayServerIcons()

        self.addItemWidgets = []
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
            
            encryption = False
            if not (serverMeta.encryptionMethod == u"None"):
                encryption = True
                
            if encryption and self.aliasDict[server]:
                tmpItem.setPixmap(0, self.secureAliasIcon)
            elif encryption:
                tmpItem.setPixmap(0, self.secureIcon)
            elif self.aliasDict[server]:
                tmpItem.setPixmap(0, self.aliasIcon)
            else:
                tmpItem.setPixmap(0, QPixmap())

###############################################################################

    def itemClicked(self, buttonNumber, item):
        """ Emit the ldap object and the server if a valid object has been
        clicked.
        """
        
        if not (buttonNumber ==1):
            return
            
        if item == None:
            return
            
        if item.isLdapType():
            name = item.getServerName()
            dn = item.getDn()
            
            # Update under which base we are working now
            tmpItem = item
            while tmpItem.parent():
                if tmpItem.isBaseType():
                    self.currentBase = tmpItem.getDn()
                    break
                tmpItem = tmpItem.parent() 
                
            success, resultList, exceptionObject = self.getLdapItem(name, dn)
            if not (success == None):
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
        
        # We have a ldap entry clicked
        if item.parent():
            serverName = item.getServerName()
            dn = item.getDn()
            oldAliasValue = self.aliasDict[serverName]
            self.aliasDict[serverName] = False
            
            success, resultList, exceptionObject = self.getLdapItemChildren(serverName, dn, 0, ['dn', 'objectClass'])
        
            if success:
                if len(resultList) == 0:
                    self.aliasDict[serverName] = oldAliasValue
                    item.setExpandable(0)
                else:
                    for x in resultList:
                        tmp = x.getPrettyRDN()
                        tmpItem = BrowserItem(item, tmp)
                        tmpItem.ldapType = True
                        tmpItem.setServerName(item.getServerName())
                        tmpItem.setDn(x.getDN())
                
                        # Add the alias icon if the entry belongs to the 
                        # alias objectClass
                        if x.isAliasObject():
                            tmpItem.setPixmap(0, self.aliasIcon)
                    
                        tmpItem.setExpandable(1)
                        item.insertItem(tmpItem)
                        
                    self.aliasDict[serverName] = oldAliasValue
                    
            else:
                self.aliasDict[serverName] = oldAliasValue
                #item.setExpandable(0)
                
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not expand entry.<br><br>Reason: ")
                if isinstance(exceptionObject, ldap.INVALID_CREDENTIALS):
                    errorMsg.append(self.trUtf8("Invalid username or wrong password"))
                else:
                    errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
        
        # We have a server item clicked
        else:
            serverList = ServerList()
            serverList.readServerList()
            serverMeta = serverList.getServerObject(item.getServerName())
            tmpList = []
            if serverMeta.autoBase:
                success, tmpList, exceptionObject = LumaConnection(serverMeta).getBaseDNList()
                
                if not success:
                    item.setOpen(0)
                    dialog = LumaErrorDialog()
                    errorMsg = self.trUtf8("Could not retrieve baseDN.<br><br>Reason: ")
                    if isinstance(exceptionObject, ldap.INVALID_CREDENTIALS):
                        errorMsg.append(self.trUtf8("Invalid username or wrong password"))
                    else:
                        errorMsg.append(str(exceptionObject))
                    dialog.setErrorMessage(errorMsg)
                    dialog.exec_loop()
                    
            else:
                tmpList = serverMeta.baseDN
                
            if tmpList == None:
                tmpList = []
                
            for base in tmpList:
                tmpBase = BrowserItem(item, base)
                tmpBase.baseType = True
                tmpBase.ldapType = True
                tmpBase.setDn(base)
                tmpBase.setServerName(item.getServerName())
                tmpBase.setExpandable(1)
            
###############################################################################

    def itemCollapsed(self, item):
        """ Delete all children if a ldap object collapses.
        """
        
        while item.childCount() > 0:
            item.takeItem(item.firstChild())

###############################################################################

    def getLdapItem(self, serverName, dn):
        """ Get all data of a ldap object given by its path.
        """
        
        serverMeta = self.serverListObject.getServerObject(serverName)
        
        serverMeta.followAliases = self.aliasDict[serverName]
        
        conObject = LumaConnection(serverMeta)
        bindSuccess, exceptionObject = conObject.bind()
        
        if not bindSuccess:
                return (False, None, exceptionObject)
                
        success, resultList, exceptionObject = conObject.search(dn, ldap.SCOPE_BASE)
        conObject.unbind()
    
        return (success, resultList, exceptionObject)

###############################################################################

    def getLdapItemChildren(self, serverName, dn, allLevel, noAttributes=None):
        """ Return a list of children a ldap object has.
        
        allLevel == 1:
            get whole subtree
            
        allLevel == 0:
            get only next level
        """
        
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
            
                
        success, resultList, exceptionObject = conObject.search(dn, searchLevel,self.searchObjectClass, noAttributes, 0)

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
        
        selectedItems = []
        listIterator = QListViewItemIterator(self)
        while listIterator.current():
            item = listIterator.current()
            
            if item.isSelected():
                selectedItems.append(item)
                
            listIterator += 1
            
        if len(selectedItems) == 0:
            return
            
        entryList = []
        partialResults = False
        for x in selectedItems:
            # check if we selected a server name
            if x.isServerType():
                continue
              
            serverName = x.getServerName()
            dn = x.getDn()
            success, resultList, exceptionObject = self.getLdapItem(serverName, dn)
            
            if success:
                entryList.extend(resultList)
            else:
                errorMsg = self.trUtf8("Could not retrieve entry with DN %1 on server %2 for exporting.<br><br>Reason: ")
                errorMsg = errorMsg.text().arg(ldapObject).arg(serverName)
                errorMsg.append(str(exceptionObject))
                environment.logMessage(LogObject("Error", errorMsg))
                partialResults = True
               
        if partialResults:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not retrieve all entries for exporting. More information in the logger.")
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            return
            
        if len(entryList) == 0:
            return
            
        exportDialog = ExportDialog()
        exportDialog.initData(entryList)
        exportDialog.exec_loop()

###############################################################################

    def exportItemSubtree(self):
        """ Export the whole subtree to ldif.
        """
        
        selectedItems = []
        listIterator = QListViewItemIterator(self)
        while listIterator.current():
            item = listIterator.current()
            
            if item.isSelected():
                selectedItems.append(item)
                
            listIterator += 1
            
        if len(selectedItems) == 0:
            return
            
        entryList = []
        partialResults = False
        for x in selectedItems:
            # check if we selected a server name
            if x.isServerType():
                continue
            
            serverName = x.getServerName()
            dn = x.getDn()
            success, resultList, exceptionObject = self.getLdapItemChildren(serverName, dn, 1)
            
            if success:
                entryList.extend(resultList)
            else:
                errorMsg = self.trUtf8("Could not retrieve entry with DN %1 on server %2 for exporting.<br><br>Reason: ")
                errorMsg = errorMsg.text().arg(ldapObject).arg(serverName)
                errorMsg.append(str(exceptionObject))
                environment.logMessage(LogObject("Error", errorMsg))
                partialResults = True
               
        if partialResults:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not retrieve all entries for exporting. More information in the logger.")
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            return
            
        if len(entryList) == 0:
            return
            
        exportDialog = ExportDialog()
        exportDialog.initData(entryList)
        exportDialog.exec_loop()

###############################################################################

    def exportItemAll(self):
        """ Export the whole subtree to ldif, together with all its parents.
        
        TODO: The code produces multiple exports of some entries if the 
        selections are on different levels in the same subtree.
        """
        
        selectedItems = []
        listIterator = QListViewItemIterator(self)
        while listIterator.current():
            item = listIterator.current()
            
            if item.isSelected():
                selectedItems.append(item)
                
            listIterator += 1
            
        if len(selectedItems) == 0:
            return
            
        # remove duplicated items
        tmpDict = {}
        for x in selectedItems:
            tmpDict[x] = None
        selectedItems = tmpDict.keys()
        
        
            
        parentDNList = []
        for x in selectedItems:
            parentDNList.extend(self.getParents(x))
            
        # remove duplicated items for parents
        tmpDict = {}
        for x in parentDNList:
            tmpDict[x] = None
        parentDNList = tmpDict.keys()
        
        # get ldap entries for the parentsa of the entries to be exported
        parentEntries = []
        partialResults = False
        for x in parentDNList:
            # check if we selected a server name
            if x.isServerType():
                continue
    
            serverName = x.getServerName()
            dn = x.getDn()
            success, resultList, exceptionObject = self.getLdapItem(serverName, dn)
            
            if success:
                parentEntries.extend(resultList)
            else:
                errorMsg = self.trUtf8("Could not retrieve entry with DN %1 on server %2 for exporting.<br><br>Reason: ")
                errorMsg = errorMsg.text().arg(ldapObject).arg(serverName)
                errorMsg.append(str(exceptionObject))
                environment.logMessage(LogObject("Error", errorMsg))
                partialResults = True
        
        # get ldap entries for the selected items
        entryList = []
        for x in selectedItems:
            # check if we selected a server name
            if x.isServerType():
                continue
            
            serverName = x.getServerName()
            dn = x.getDn()
            success, resultList, exceptionObject = self.getLdapItemChildren(serverName, dn, 1)
            
            if success:
                entryList.extend(resultList)
            else:
                errorMsg = self.trUtf8("Could not retrieve entry with DN %1 on server %2 for exporting.<br><br>Reason: ")
                errorMsg = errorMsg.text().arg(ldapObject).arg(serverName)
                errorMsg.append(str(exceptionObject))
                environment.logMessage(LogObject("Error", errorMsg))
                partialResults = True
               
        if partialResults:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not retrieve all entries for exporting. More information in the logger.")
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            return
            
        if len(entryList) == 0:
            return
           
        entryList.extend(parentEntries)
        entryList.sort()
        exportDialog = ExportDialog()
        exportDialog.initData(entryList)
        exportDialog.exec_loop()

###############################################################################

    def deleteItem(self):
        """ Delete selected item from the server.
        """
        
        selectedItems = []
        listIterator = QListViewItemIterator(self)
        while listIterator.current():
            item = listIterator.current()
            
            if item.isSelected():
                selectedItems.append(item)
                
            listIterator += 1
            
        if len(selectedItems) == 0:
            return
            
        entryList = []
        partialResults = False
        for x in selectedItems:
            # check if we selected a server name
            if x.isServerType():
                continue
            
            serverName = x.getServerName()
            dn = x.getDn()
            success, resultList, exceptionObject = self.getLdapItem(serverName, dn)
            
            if success:
                entryList.extend(resultList)
            else:
                errorMsg = self.trUtf8("Could not retrieve entry with DN %1 on server %2 for deletion.<br><br>Reason: ")
                errorMsg = errorMsg.text().arg(ldapObject).arg(serverName)
                errorMsg.append(str(exceptionObject))
                environment.logMessage(LogObject("Error", errorMsg))
                partialResults = True
               
        if partialResults:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not retrieve all entries for deletion. More information in the logger.")
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            return
            
        if len(entryList) == 0:
            return
            
        
        deleteDialog = DeleteDialog()
        deleteDialog.initData(entryList)
        deleteDialog.exec_loop()

###############################################################################

    def showPopup(self, tmpItem=None, point=None, itemId=None):
        """ Display popup menu.
        """
        
        if tmpItem == None:
            return
            
        #self.itemClicked(tmpItem)
        #self.emit(SIGNAL("clicked(QListViewItem*)"), (tmpItem,))
        self.popupItem = tmpItem
        
        tmpDirObject = environment.lumaInstallationPrefix
        aliasIconFile = os.path.join(tmpDirObject, "share", "luma", "icons", "alias.png")
        popupMenu = QPopupMenu()
        
        server = tmpItem.getServerName()
        dn = tmpItem.getDn()
        
        # try to find how many items are selected
        multipleSelected = False
        listIterator = QListViewItemIterator(self)
        tmpInt = 0
        while listIterator.current():
            item = listIterator.current()
            
            if item.isSelected():
                tmpInt += 1
                    
            if tmpInt >= 2:
                multipleSelected = True
                break 
                
            listIterator += 1
        
        popupMenu.insertItem(self.trUtf8("Edit server settings"), self.editServerSettings)
        
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
            if multipleSelected:
                exportMenu.insertItem(self.trUtf8("Items"), self.exportItem)
                exportMenu.insertItem(self.trUtf8("Subtrees"), self.exportItemSubtree)
                exportMenu.insertItem(self.trUtf8("Subtrees with Parents"), self.exportItemAll)
            else:
                exportMenu.insertItem(self.trUtf8("Item"), self.exportItem)
                exportMenu.insertItem(self.trUtf8("Subtree"), self.exportItemSubtree)
                exportMenu.insertItem(self.trUtf8("Subtree with Parents"), self.exportItemAll)

        
            # Fill delete menu
            if multipleSelected:
                deleteMenu.insertItem(self.trUtf8("Items"), self.deleteItem)
                deleteMenu.insertItem(self.trUtf8("Subtrees"), self.deleteItemsRecursive)
                deleteMenu.insertItem(self.trUtf8("Subtrees without Node"), self.deleteSubtree)
            else:
                deleteMenu.insertItem(self.trUtf8("Item"), self.deleteItem)
                deleteMenu.insertItem(self.trUtf8("Subtree"), self.deleteItemsRecursive)
                deleteMenu.insertItem(self.trUtf8("Subtree without Node"), self.deleteSubtree)
                
            # Fill add menu
            self.addItemMenu.clear()
            self.addItemMenu.insertItem(self.trUtf8("Attribute"), self.addAttribute)
            self.addItemMenu.insertSeparator()
            templates = TemplateList()
            for x in templates.templateList:
                self.addItemMenu.insertItem(x.name, self.addItem)
                    
            popupMenu.insertSeparator()
            popupMenu.insertItem(QIconSet(QPixmap(addIconFile)), self.trUtf8("Add"), self.addItemMenu)
            popupMenu.insertSeparator()
            popupMenu.insertItem(QIconSet(QPixmap(exportIconFile)), self.trUtf8("Export"), exportMenu)
            popupMenu.insertSeparator()
            popupMenu.insertItem(QIconSet(QPixmap(delIconFile)), self.trUtf8("Delete"), deleteMenu)
             
        self.itemClicked(1, tmpItem)
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
            parentList.append(item)
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
        selectedItems = []
        listIterator = QListViewItemIterator(self)
        while listIterator.current():
            item = listIterator.current()
            
            if item.isSelected():
                selectedItems.append(item)
                
            listIterator += 1
            
        if len(selectedItems) == 0:
            return
        
        firstItem = selectedItems[0]
        serverName = firstItem.getServerName()
        baseDN = firstItem.getDn()
        
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
        
        selectedItems = []
        listIterator = QListViewItemIterator(self)
        while listIterator.current():
            item = listIterator.current()
            
            if item.isSelected():
                selectedItems.append(item)
                
            listIterator += 1
            
        if len(selectedItems) == 0:
            return
            
        entryList = []
        partialResults = False
        for x in selectedItems:
            # check if we selected a server name
            if x.isServerType():
                continue
                
            serverName = x.getServerName()
            dn = x.getDn()
                
            success, resultList, exceptionObject = self.getLdapItemChildren(serverName, dn, withParent)
            
            if success:
                entryList.extend(resultList)
            else:
                errorMsg = self.trUtf8("Could not retrieve entry with DN %1 on server %2 for deletion.<br><br>Reason: ")
                errorMsg = errorMsg.text().arg(ldapObject).arg(serverName)
                errorMsg.append(str(exceptionObject))
                environment.logMessage(LogObject("Error", errorMsg))
                partialResults = True
            
        if partialResults:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Could not retrieve all entries for deletion. More information in the logger.")
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
            return
            
        if len(entryList) == 0:
            return
            
        entryList.sort()
        deleteDialog = DeleteDialog()
        deleteDialog.initData(entryList)
        deleteDialog.exec_loop()
            
###############################################################################

    def deleteSubtree(self):
        """ Delete the subtree of the selected item.
        """
        
        self.deleteItemsRecursive(0)

###############################################################################

    def keyPressEvent(self, keyEvent):
        self.setEnabled(False)
        keyText = unicode(keyEvent.text()).lower()
        if len(keyText) == 0:
            keyEvent.ignore()
            self.setEnabled(True)
            return
        
        # find the first item below the currently selected item
        selectedItem = self.selectedItem()
        currentItem = None
        
        # Either no item is selected of the can select multiple items.
        if selectedItem == None:
            listIterator = QListViewItemIterator(self)
            while listIterator.current():
                item = listIterator.current()
            
                if item.isSelected():
                    currentItem = item.itemBelow()
                    break
                
                listIterator += 1
                
        # We have one selected item
        else:
            currentItem = selectedItem.itemBelow()
        
        # Small error prevention
        if currentItem == None:
            currentItem = self.firstChild()
            if currentItem == None:
                self.setEnabled(True)
                return
        
        # Now we try to find the next item matching our search key.
        listIterator = QListViewItemIterator(currentItem)
        item = None
        while listIterator.current():
            item = listIterator.current()
            
            nodeString = unicode(item.text(0))
            tmpList = nodeString.split("=")
            if len(tmpList) < 2:
                listIterator +=1
                continue
                    
            tmpString = tmpList[1]
            if len(tmpString) == 0:
                listIterator +=1
                continue
                    
            if keyTex == tmpString[0].lower():
                self.ensureItemVisible(item)
                self.setSelected(item, True)
                self.itemClicked(item)
                break
                
            listIterator += 1
            
        # When re-enabled, we need to get the focus again. Otherwise further 
        # key presses will be ignored.
        self.setEnabled(True)
        self.setFocus()
        
        
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
        serverName = self.popupItem.getServerName()
        dn = self.popupItem.getDn()
        
        self.aliasDict[serverName] = not self.aliasDict[serverName]
        
        tmpItem = self.serverDict[serverName]
        self.setOpen(tmpItem, False)
        serverMeta = self.serverListObject.getServerObject(serverName)
        serverMeta.followAliases = not serverMeta.followAliases
        self.displayServerIcons()
        
###############################################################################

    def editServerSettings(self):
        serverName = self.popupItem.getServerName()
        
        dialog = ImprovedServerDialog()
        dialog.selectServer(serverName)
        dialog.exec_loop()
        if (dialog.result() == QDialog.Accepted) or dialog.SAVED:
            environment.reloadPlugins()
    
###############################################################################

    def reopenDN(self, serverString, dnString):
        """ Reopens the listitem for the given dnString.
        
        The dnString consits of the actuacl dn and its server alias appended. Example:
        ou=foo,o=bar,MyServerAlias
        """
        
        listIterator = QListViewItemIterator(self)
        while listIterator.current():
            item = listIterator.current()
            itemDN = item.getDn()
            serverName = item.getServerName()
            
            if (itemDN == dnString) and (serverName == serverString): 
                item.setOpen(0)
                item.setOpen(1)
                break
                
            listIterator += 1
        
###############################################################################

    def addAttribute(self):
        """ Emits a signal that an attribute is to be added to the current
        entry.
        """
        
        self.emit(PYSIGNAL("ADD_ATTRIBUTE"), ())
        
###############################################################################

class ChildWindow(QMainWindow):
    
    def __init__(self, parent = None):
        QMainWindow.__init__(self)
        
        
    def closeEvent(self, event):
        self.emit(PYSIGNAL("child_closed"), (self,))
        self.deleteLater()
        
###############################################################################

class BrowserItem(QListViewItem):

    def __init__(self, parent, text):
        QListViewItem.__init__(self, parent, text)
        
        self.serverType = False
        self.baseType = False
        self.ldapType = False
        
        # DN of the entry if it is not a server item
        self.dn = None
        
        # name of the server the item belongs to
        self.serverName = None

    def isServerType(self):
        return self.serverType
            
    def isBaseType(self):
        return self.baseType
            
    def isLdapType(self):
        return self.ldapType
            
    def setServerName(self, serverString):
        self.serverName = serverString
        
    def getServerName(self):
        return self.serverName
        
    def getDn(self):
        return self.dn
        
    def setDn(self, dnString):
        self.dn = dnString
