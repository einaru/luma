# -*- coding: utf-8 -*-
#
# plugins.search.__init__
#
# Copyright (c) 2011
#      Einar Uvsløkk, <einaru@stud.ntnu.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

import ldap

class SearchPlugin():
    """
    This class implements the search logic for the search plugin
    """
    def __ini__(self):
        pass
    
    def search(self, query, server, baseDN, scope=ldap.SCOPE_SUBTREE):
        pass

    def startSearch(self):
        """Starts the search for the given server and search filter.
        
        Emits the signal "ldap_result". Given arguments are the servername, the 
        search result and the criterias used for the filter.
        """
        
        # Returns was pressed but no server selected. So we don't want 
        # to search.
        if self.connection == None:
            return
        
        self.groupFrame.setEnabled(False)

        criteriaList = self.getSearchCriteria()
    
        bindSuccess, exceptionObject = self.connection.bind()
        
        if not bindSuccess:
                dialog = LumaErrorDialog()
                errorMsg = self.trUtf8("Could not bind to server.<br><br>Reason: ")
                errorMsg.append(str(exceptionObject))
                dialog.setErrorMessage(errorMsg)
                dialog.exec_loop()
                self.groupBox2.setEnabled(True)
                return
                
        self.currentServer.currentBase = unicode(self.baseBox.currentText())
        success, resultList, exceptionObject = self.connection.search(self.currentServer.currentBase, ldap.SCOPE_SUBTREE,
                unicode(self.searchEdit.currentText()).encode('utf-8'))
        self.connection.unbind()
        
        self.groupFrame.setEnabled(True)
        
        if success:
            self.emit(PYSIGNAL("ldap_result"), (self.currentServer, resultList, criteriaList, ))
        else:
            dialog = LumaErrorDialog()
            errorMsg = self.trUtf8("Error during search operation.<br><br>Reason: ")
            errorMsg.append(str(exceptionObject))
            dialog.setErrorMessage(errorMsg)
            dialog.exec_loop()
