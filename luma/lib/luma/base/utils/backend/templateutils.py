# -*- coding: utf-8 -*-

###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <widod@users.sourceforge.net>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import environment

import os.path

class LdapTemplate(object):
    """ A class for storing template information of ldap-objects.

    self.name is the name of the template.
    self.tData contains the template data.

    self.tdata has the following structure:
    [{'CLASSNAME': 'fooclassname', 'ATTRIBUTES': {'NAME': 'attributename', 
    {'MUST': int, 'SINGLE': int, 'SHOW': int}}}, 
    {...}, ...]

    This is really ugly. There must be something better.
    """

    def __init__(self, filename=None):
        # these attributes are the actual template data
        self.name = ""
        self.description = ""
        self.serverName = ""
        self.templateData = []

        # this is status data of the template
        self.edited = False

###############################################################################

    def get_objectclasses(self):
        """ Return a list of objectclasses.
        """
    
        tmpList = []
        for x in self.tData:
            tmpList.append(x["CLASSNAME"])
        return tmpList

###############################################################################

    def get_attributeinfos(self):
        """ Return a list of attributes together with their propperties.
        """
    
        tmpDict = {}
        for x in self.tData:
            for y in x["ATTRIBUTES"]:
                tmpDict[y["NAME"]] = {"MUST" : y["MUST"], "SINGLE" : y["SINGLE"] , "SHOW" : y["SHOW"] }
        return tmpDict

###############################################################################

    def set_attribute_show(self, attribute, value):
        """ Set the property 'SHOW' of attribute to value.
        """
    
        for x in self.tData:
            for y in x['ATTRIBUTES']:
                if y['NAME'] == attribute:
                    y['SHOW'] = value
                    
###############################################################################

    def getDataObject(self):
        """ Create a data structure which can be used by python-ldap and return it.
        """
    
        dataObject = {}
        
        for x in self.tData:
            objectClass = x["CLASSNAME"]
            if dataObject.has_key(objectClass):
                dataObject["objectClass"].append(objectClass)
            else:
                dataObject["objectClass"] = [objectClass]
                
            for y in x["ATTRIBUTES"]:
                if (y["SHOW"] == 1) or (y["MUST"] == 1):
                    dataObject[y["NAME"]] = [""]
        
        return dataObject

###############################################################################

    def __repr__(self):
        tmpList = []
        tmpList.append("Name: " + self.name.encode("utf-8") + "\n")
        for x in self.tData:
            tmpList.append("class ")
            tmpList.append(x["CLASSNAME"].encode("utf-8"))
            tmpList.append(" >> ")
            for y in x["ATTRIBUTES"]:
                tmpList.append(y["NAME"].encode("utf-8") + ",")
                if y["MUST"]:
                    tmpList.append("MUST,")
                else:
                    tmpList.append("NOMUST,")
                if y["SINGLE"]:
                    tmpList.append("SINGLE,")
                else:
                    tmpList.append("NOSINGLE,")
                if y["SHOW"]:
                    tmpList.append("SHOW")
                else:
                    tmpList.append("NOSHOW")
                tmpList.append(" || ")

            del tmpList[-1]
            tmpList.append("\n")
        tmpList.append("\n")
        return "".join(tmpList)

###############################################################################

class TemplateFile:
    """ A class for loading and saving template data to file.
    """

    def __init__(self):
        self.tplFile = os.path.join (environment.userHomeDir, ".luma", "templates")

        self.tplList = []

        try:
            self.read_list()
        except IOError, data:
            print "Template file could not be read. \nReason: " + str(data)

###############################################################################

    def read_list(self):
        """ Read template Info from file.
    
        Templates are stored in self.tplList
        """
    
        self.tplList = []
        content = open(self.tplFile, 'r').readlines()
        template = LdapTemplate()
        
        for x in content:
            #x = x.decode("utf-8")
            if x == "\n":
                self.tplList.append(template)
                template = LdapTemplate()
                template.name = []
                template.tData = []
                
            if x[:6] == "Name: ":
                template.name = x[6:-1].decode("utf-8")
                continue
                
            if x[:6] == "class ":
                tmpString = x[6:-1]
                tmpList = tmpString.split(" >> ")
                data = {}
                data['CLASSNAME'] = tmpList[0]
                tmpList = tmpList[1].split(" || ")
                attributeList = []
                
                for y in tmpList:
                    attrInfo = y.split(",")
                    tmpDict = {}
                    tmpDict["NAME"] = attrInfo[0]
                    
                    if attrInfo[1] == "MUST":
                        tmpDict["MUST"] = 1
                    else:
                        tmpDict["MUST"] = 0

                    if attrInfo[2] == "SINGLE":
                        tmpDict["SINGLE"] = 1
                    else:
                        tmpDict["SINGLE"] = 0

                    if attrInfo[3] == "SHOW":
                        tmpDict["SHOW"] = 1
                    else:
                        tmpDict["SHOW"] = 0
                        
                    attributeList.append(tmpDict)
                    
                data["ATTRIBUTES"] = attributeList
                template.tData.append(data)

###############################################################################

    def save_to_file(self):
        """ Save template list to file.
        """
        fileHandler = open(self.tplFile, "w")
        for x in self.tplList:
            fileHandler.write(str(x))
        fileHandler.close()

###############################################################################

    def add_template(self, name):
        pass

###############################################################################

    def delete_template(self, name):
        pass
        
###############################################################################

    def get_templateobject(self, templateName):
        """ Get a template given by templateName
        """
        
        for x in self.tplList:
            if x.name == templateName:
                return x
    
    

