# -*- coding: <utf-8> -*-

###########################################################################
#    Copyright (C) 2004, 2005 by Wido Depping                                      
#    <widod@users.sourceforge.net>                                                             
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################

import ldap
import ldif,dsml
import copy
import base64
import StringIO
from sets import Set

from base.backend.ObjectClassAttributeInfo import ObjectClassAttributeInfo
from base.utils import stripSpecialChars
from base.utils import escapeSpecialChars
from base.utils import isBinaryAttribute
from base.utils import explodeDN

class SmartDataObject (object):

    passwordList = ["userpassword", "ntpassword", "lmpassword", "clearpassword",
                    "sambalmpassword", "sambantpassword", "goimappassword", 
                    "gokrbpassword", "gofaxpassword", "gologpassword", "gofonpassword",
                    "solarisbindpassword"]

    def __init__(self, data, serverMeta):
        self.doSchemaChecks = True
        self.isValid = False
        
        self.dn = data[0]
        self.data = data[1]
        
        # This is the string representing our key for the objectclasses.
        # Important for lower- and uppercase variants
        self.objectClassName = None
        for x in self.data.keys():
                if "objectclass" == x.lower():
                    self.objectClassName = x
                    break
        if self.objectClassName == None:
            self.objectClassName = "objectClass"
        
        # Set server meta information
        self.serverMeta = serverMeta
        
        # Set schema for current server
        self.serverSchema = ObjectClassAttributeInfo(self.serverMeta)
        
        #self.checkIntegrity()
        
###############################################################################

    def __cmp__(self, otherItem):
        """ Custom sort function for comparing SmartDataObjects. 
        
        Sorting is based on the distinguished name of the object. The higher 
        the object in the tree, the more it will be at the beginning of the 
        sorted list. Leaves should be at the end of the list.
        """
        
        
        if type(otherItem) == SmartDataObject:
            currentList = explodeDN(self.getDN())
            otherList = explodeDN(otherItem.getDN())
        
            curLength = len(currentList)
            otherLength = len(otherList)
            
            if curLength < otherLength:
                return -1
            elif curLength == otherLength:
                return 0
            elif curLength > otherLength:
                return 1
            else:
                return 0
            
        else:
            return 1
        
###############################################################################

    def getServerAlias(self):
        """ Returns a string representing the alias name of the server.
        """
        
        return copy.deepcopy(self.serverMeta.name)
        
###############################################################################

    def getServerMeta(self):
        """ Returns the meta information about the server.
        """
        
        return copy.deepcopy(self.serverMeta)
        
###############################################################################

    def getDN(self):
        """ Returns the DN of the current object as a string.
        """
        
        return self.dn

###############################################################################

    def getObjectClasses(self):
        """ Returns a list of the current objectClasses. Returns None if data 
        has no values for objectClass.
        """

        if None == self.objectClassName:
            #return None
            return []
        else:
            return self.data[self.objectClassName][:]
            
###############################################################################

    def getStructuralClasses(self):
        """ Returns a list of classes which are structural in this object.
        """
        
        structList = []
        
        for x in self.getObjectClasses():
            if self.isObjectclassStructural(x):
                structList.append(x)
                
        return structList
        
###############################################################################

    def hasStructuralClass(self):
        """ Returns boolean value if current object has a structural class.
        """
        
        for x in self.getObjectClasses():
            if self.isObjectclassStructural(x):
                return True
                
        return False
        
        
###############################################################################

    def getAttributeList(self):
        """ Returns a list of currently used attributes. 
        """
        
        tmpList = self.data.keys()
        
        # Remove attribute 'objectClass'. We don't want that.
        if not (None == self.objectClassName):
            tmpList.remove(self.objectClassName)
        
        return tmpList
        
###############################################################################

    def getAttributeValueList(self, attributeName=None):
        """Returns a list of values for the given attribute.
        """
        
        if None == attributeName:
            raise FunctionArgumentException("Function getAttributeValueList( attributeName ) called without a parameter.")
            
        if self.data.has_key(attributeName):
            # Binary values are returned normally.
            # String values have to be decoded from utf-8 to unicode.
            if self.isAttributeBinary(attributeName):
                return self.data[attributeName]
            else:
                tmpList = []
                for x in self.data[attributeName]:
                    if None == x:
                        tmpList.append(None)
                    else:
                        tmpList.append(x.decode('utf-8'))
                return tmpList
        else:
            return None
            
###############################################################################

    def getAttributeValue(self, attributeName=None, valueIndex=None):
        """Returns the values for the given attribute at index valueIndex.
        """
        
        if (None == attributeName) or (None == valueIndex):
            raise FunctionArgumentException("Function getAttributeValue( attributeName, valueIndex ) called without correct parameters.")
            
            
        if self.data.has_key(attributeName):
            # Is the data length of the attribute compatible with the given index?
            if valueIndex < len(self.data[attributeName]):
                
                # Binary values are returned normally.
                # String values have to be decoded from utf-8 to unicode.
                if self.isAttributeBinary(attributeName):
                    return self.data[attributeName][valueIndex]
                else:
                    tmpValue = self.data[attributeName][valueIndex]
                    
                    # Do we have an unset value?
                    if None == tmpValue:
                        return None
                    else:
                        return tmpValue.decode('utf-8')
                    
            # Index is out of range.
            else:
                errorList = []
                errorList.append("Can't get value for attribute. Index for attribute " + attributeName + " is out of range.")
                errorList.append(" DN: " + self.getPrettyDN() + ".")
                errorList.append(" Current data: " + repr(self.data))
                        
                raise LdapDataException("".join(errorList))
        else:
            return None
            
###############################################################################

    def getAttributeListForObjectClass(self, objectClass):
        return self.serverSchema.getAttributeListForObjectClass(objectClass)
    
###############################################################################

    def addAttributeValue(self, attributeName=None, valueList=None, replaceOldValues=False):
        """ Adds the values given by valueList to the attribute attributeName.
        """
        
        if None == attributeName:
            raise FunctionArgumentException("Function  addAttributeValue( attributeName, valueList) called without correct parameters.")
         
        # Do we work on an existing attribute?
        if self.data.has_key(attributeName):
            
            # Do we want values to a single valued attribute?
            if self.isAttributeSingle(attributeName):
                
                # Do we replace old values?
                if replaceOldValues:
                    if len(valueList) > 1:
                        errorList = []
                        errorList.append("Can't add value to attribute. Attribute " + attributeName + " is single valued and the valueList to add has more than one value.")
                        errorList.append(" DN: " + self.getPrettyDN() + ".")
                        if self.isAttributeBinary(attributeName):
                            errorList.append(" To add: Attribute= " + attributeName + "   Values= BINARY FORMAT" )
                        else:
                            errorList.append(" To add: Attribute= " + attributeName + "   Values=" + repr(valueList))
                            errorList.append(". Current data: " + repr(self.data))
                        
                        raise LdapDataException("".join(errorList))
                
                # We don't replace old values.
                else:
                    
                    # We want to add a value altough attribute is single valued and has a value.
                    if len(self.data[attributeName]) >= 1:
                        errorList = []
                        errorList.append("Can't add value to attribute. Attribute " + attributeName + " is single valued.")
                        errorList.append(" DN: " + self.getPrettyDN() + ".")
                        if self.isAttributeBinary(attributeName):
                            errorList.append(" To add: Attribute= " + attributeName + "   Values= BINARY FORMAT" )
                        else:
                            errorList.append(" To add: Attribute= " + attributeName + "   Values=" + repr(valueList))
                            errorList.append(". Current data: " + repr(self.data))
                        
                        raise LdapDataException("".join(errorList))
        
            # Attribute values are empty. This is important for other components.
            # An empty list indicates if the attribute is fresh and needs a value.
            if None == valueList:
                self.data[attributeName].append(None)
            else:
                # Binary values added normally.
                # String values have to be encoded in utf-8.
                if self.isAttributeBinary(attributeName):
                    if replaceOldValues:
                        self.data[attributeName] = valueList
                    else:
                        self.data[attributeName].extend(valueList)
                else:
                    if replaceOldValues:
                        self.data[attributeName] = map(lambda x: x.encode('utf-8'), valueList)
                    else:
                        self.data[attributeName].extend(map(lambda x: x.encode('utf-8'), valueList))
                        
        # We're adding a new attribute.
        else:
            # Is attribute allowed?
            if self.serverSchema.attributeAllowed(attributeName, self.getObjectClasses()):
                
                # Attribute values are empty. This is important for other components.
                # An empty list indicates if the attribute is fresh and needs a value.
                if None == valueList:
                    self.data[attributeName] = [None]
                else:
                
                    # Is attribute single?
                    if self.isAttributeSingle(attributeName):
                    
                        # Has valueList more than one value?
                        if len(valueList) > 1:
                            errorList = []
                            errorList.append("Can't add value to attribute. Attribute " + attributeName + " is single valued.")
                            errorList.append(" DN: " + self.getPrettyDN() + ".")
                            if self.isAttributeBinary(attributeName):
                                errorList.append(" To add: Attribute= " + attributeName + "   Values= BINARY FORMAT" )
                            else:
                                errorList.append(" To add: Attribute= " + attributeName + "   Values=" + repr(valueList))
                                errorList.append(". Current data: " + repr(self.data))
                            
                            raise LdapDataException("".join(errorList))
                        
                        # valueList has only one value
                        else:
                            if self.isAttributeBinary(attributeName):
                                self.data[attributeName] = valueList
                            else:
                                self.data[attributeName] = map(lambda x: x.encode('utf-8'), valueList)
                                
                    # The attribute is not single
                    else:
                    
                        # Since attribute is new to the object, we have no need to 
                        # join the values with the old list.
                        if self.isAttributeBinary(attributeName):
                            self.data[attributeName] = valueList
                        else:
                            self.data[attributeName] = map(lambda x: x.encode('utf-8'), valueList)
                            
            # Attribute is not allowed with the current list of objectclasses.
            else:
                errorList = []
                errorList.append("Can't add value to attribute. Attribute " + attributeName + " not allowed with current objectClasses.")
                errorList.append(" DN: " + self.getPrettyDN() + ".")
                if self.isAttributeBinary(attributeName):
                    errorList.append(" To add: Attribute= " + attributeName + "   Values= BINARY FORMAT" )
                else:
                    errorList.append(" To add: Attribute= " + attributeName + "   Values=" + repr(valueList))
                    errorList.append(". Current data: " + repr(self.data))
                    
                raise LdapDataException("".join(errorList))
            
                    
###############################################################################

    def setAttributeValue(self, attributeName=None, valueIndex=None, newValue=None):
        """Sets the value for the given attribute at index valueIndex.
        """
        
        if (None == attributeName) or (None == valueIndex) or (None == newValue):
            raise FunctionArgumentException("Function setAttributeValue( attributeName, valueIndex, newValue ) called without correct parameters.")
            
        if self.data.has_key(attributeName):
            # Is the data length of the attribute compatible with the given index?
            if valueIndex < len(self.data[attributeName]):
                
                # Binary values are returned normally.
                # String values have to be decoded from utf-8 to unicode.
                if self.isAttributeBinary(attributeName):
                    self.data[attributeName][valueIndex] = newValue
                else:
                    tmpValue = newValue.encode('utf-8')
                    self.data[attributeName][valueIndex] = tmpValue
                    
            # Index is out of range.
            else:
                errorList = []
                errorList.append("Can't get value for attribute. Index for attribute " + attributeName + " is out of range.")
                errorList.append(" DN: " + self.getPrettyDN() + ".")
                errorList.append(" Current data: " + repr(self.data))
                        
                raise LdapDataException("".join(errorList))
        elif "rdn" == attributeName.lower():
            self.setDN(newValue)
        else:
            errorList = []
            errorList.append("Can't set value for attribute. Object has no attribute " + attributeName + ".")
            errorList.append(" DN: " + self.getPrettyDN() + ".")
            errorList.append(" Current data: " + repr(self.data))
                        
            raise LdapDataException("".join(errorList))

###############################################################################

    def isAttributeAllowed(self, attributeName=None):
        """ Returns True if the attribute attributeName is allowed with the 
        current set of objectclasses.
        """
        
        if None == attributeName:
            raise FunctionArgumentException("Function isAttributeAllowed(attributeName) called without correct parameters.")
            
        mustSet, maySet = self.getPossibleAttributes()
        attributeList = mustSet.union(maySet)
        attributeName = attributeName.lower()
        
        for x in attributeList:
            if attributeName == x.lower():
                return True
                
        return False

###############################################################################

    def isAttributeMust(self, attributeName=None, classList=None):
        """ Returns a boolean if a given attribute is must for a list of objectClasses.
        
        classList can be None. Then the check is performed on the current classes of the object.
        Otherwise the check is done on the given list of classes.
        """
        
        if None == attributeName:
            raise FunctionArgumentException("Function isAttributeMust(attributeName, classList) called without correct parameters.")
            
        if None == classList:
            return self.serverSchema.isMust(attributeName, self.getObjectClasses())
        else:
            return self.serverSchema.isMust(attributeName, classList)
        
###############################################################################

    def isAttributeSingle(self, attributeName=None):
        """ Returns a boolean if a given attribute is single valued. 
        """
        
        if None == attributeName:
            raise FunctionArgumentException("Function isAttributeSingle(attributeName) called without correct parameters.")
            
        return self.serverSchema.isSingle(attributeName)
            
###############################################################################

    def isAttributeBinary(self, attributeName=None):
        """ Returns a boolean if a given attribute is of type binary. 
        """
        
        if None == attributeName:
            raise FunctionArgumentException("Function isAttributeBinary(attributeName) called without correct parameters.")
            
        return self.serverSchema.isBinary(attributeName)
        
###############################################################################

    def isAttributeImage(self, attributeName=None):
        """ Returns a boolean if a given attribute contains image data. 
        """
        
        if None == attributeName:
            raise FunctionArgumentException("Function isAttributeImage(attributeName) called without correct parameters.")
            
        if "jpegphoto" == attributeName.lower():
            return True
        else:
            return False
            
###############################################################################

    def isAttributePassword(self, attributeName=None):
        """ Returns a boolean if a given attribute contains password data. 
        """
        
        if None == attributeName:
            raise FunctionArgumentException("Function isAttributePassword(attributeName) called without correct parameters.")
          
        tmpName = attributeName.lower()
        if tmpName in self.passwordList:
            return True
        else:
            return False
            
###############################################################################

    def isAliasObject(self):
        """ Returns a boolean if the current object is an alias object.
        
        The object is from type alias if it has the alias objectClass.
        """
        
        for x in self.getObjectClasses():
            if "alias" == x.lower():
                return True
            
        return False

###############################################################################

    def isAttributeValueRDN(self, attributeName=None, attributeValue=None):
        """ Returns a boolean if the given attribute and it's value are the RDN of the object.
        
        The given parameters have to be in unicode format and special characters have
        to be decoded.
        """
        
        if None == attributeName:
            raise FunctionArgumentException("Function isAttributeValueRDN(attributeName, attributeValue) called without correct parameters.")
          
        # The attribute value is not yet initialized. We can safely ignore it.
        if None == attributeValue:
            return False
            
        # Is our attribute binary?
        if self.isAttributeBinary(attributeName):
            return False
            
        # No binary attribute
        else:
            tmpRDN = attributeName + "=" + attributeValue
        
            # Does the created RDN match the actual RDN?
            if tmpRDN == self.getPrettyRDN():
                return True
            else:
                return False
            
###############################################################################

    def getPrettyDN(self):
        """ Returns unicode string for the DN. All encoded special characters are 
        converted to their real repesentations.
        """
        
        tmpList = explodeDN(self.dn)
        newList = map(stripSpecialChars, tmpList)
        tmpString = ",".join(newList)
        
        return tmpString.decode('utf-8')
        
###############################################################################

    def setDN(self, tmpString):
        """ Set the dn of the current object.
        """
        
        tmpList = explodeDN(tmpString)
        newList = map(escapeSpecialChars, tmpList)
        tmpString = ",".join(newList)
        tmpString = unicode(tmpString)
        
        self.dn = tmpString.encode('utf-8')
        
        
###############################################################################

    def getPrettyRDN(self):
        """ Returns unicode string for the RDN. All encoded special characters are 
        converted to their real repesentations.
        """
        
        rdn = explodeDN(self.dn)[0]
        tmpString = stripSpecialChars(rdn)
        
        return tmpString.decode('utf-8')
        
###############################################################################
        
    def getPrettyParentDN(self):
        """ Returns a string with the parent of the current object. All encoded special 
        characters are converted to their real repesentations.
        """
        
        tmpList = explodeDN(self.dn)
        newList = map(stripSpecialChars, tmpList)
        tmpString = ",".join(newList[1:])
        
        return tmpString.decode('utf-8')

###############################################################################

    def checkIntegrity(self):
        pass
        
###############################################################################

    def deleteAttributeValue(self, attributeName, index):
        """ Delete value for attribute 'attributeName' at index 'index'.
        """
        
        # Is attribute present?
        if self.data.has_key(attributeName):
            valueLength = len(self.data[attributeName])
            
            # Is index lower or equal to the maximum length of the data?
            if index <= (valueLength - 1):
                
                # Is the value we want to delete the RDN of the object?
                if self.isAttributeValueRDN(attributeName, self.data[attributeName][index]):
                    errorList = []
                    errorList.append("Can't delete attribute. Attribute is RDN of this object.")
                    errorList.append(" DN: " + self.getPrettyDN() + ".")
                    errorList.append(" To delete: Attribute=" + attributeName + "   Index=" + str(index))
                    errorList.append(". Current data: " + repr(self.data))
                    raise LdapDataException("".join(errorList))
                    
                # Is the attribute must and only one value present?
                elif self.isAttributeMust(attributeName) and (valueLength == 1):
                    errorList = []
                    errorList.append("Can't delete attribute. Attribute is must and has no other value.")
                    errorList.append(" DN: " + self.getPrettyDN() + ".")
                    errorList.append(" To delete: Attribute=" + attributeName + "   Index=" + str(index))
                    errorList.append(". Current data: " + repr(self.data))
                    raise LdapDataException("".join(errorList))
                
                # Delete value.
                del(self.data[attributeName][index])
                
                # we have deleted the last entry. so this is a shortcut.
                # no more need to call len() angain.
                if 1 == valueLength:
                    del(self.data[attributeName])
                        
            # Index for deletion is higher than length of current data.
            else:
                errorList = []
                errorList.append("Can't delete attribute. Index for deletion is higher than actual data length.")
                errorList.append(" DN: " + self.getPrettyDN() + ".")
                errorList.append(" To delete: Attribute=" + attributeName + "   Index=" + str(index))
                errorList.append(". Current data: " + repr(self.data))
                raise LdapDataException("".join(errorList))
                    
        # We want to delete an attribute value for which no attribute entry exists.
        else:
            errorList = []
            errorList.append("Can't delete attribute. Attribute is not present in current object.")
            errorList.append(" DN: " + self.getPrettyDN() + ".")
            errorList.append(" To delete: Attribute=" + attributeName + "   Index=" + str(index))
            errorList.append(". Current data: " + repr(self.data))
            raise LdapDataException("".join(errorList))
        
###############################################################################

    def deleteAttribute(self, attributeName=None):
        """ Delete attribute 'attributeName' from current object.
        """
        
        # Has object the given attribute?
        if self.data.has_key(attributeName):
            
            # Is attribute must?
            if self.isAttributeMust(attributeName):
                errorList = []
                errorList.append("Can't delete attribute. Attribute must be present in object.")
                errorList.append(" DN: " + self.getPrettyDN() + ".")
                errorList.append(" To delete: Attribute=" + attributeName + "   Index=" + str(index))
                errorList.append(". Current data: " + repr(self.data))
                raise LdapDataException("".join(errorList))
                pass
                
            # Attribute is not must
            else:
                del self.data[attributeName]
        
###############################################################################

    def addObjectClass(self, className):
        """ Add an objectClass to the object.
        """
        
        className = className.lower()
        className = className.encode('utf-8')
        
        if self.hasObjectClass(className):
            return
            
        if self.isObjectclassStructural(className):
            structList = self.getStructuralClasses()
            for x in structList:
                if not self.serverSchema.sameObjectClassChain(className, x):
                    errorList = []
                    errorList.append("Can't add objectClass to object. ObjectClass " + className + " is structural and conflicts with other classes.")
                    errorList.append(" DN: " + self.getPrettyDN() + ".")
                    errorList.append(" Current objectClasses: " + repr(self.getObjectClasses()))
                        
                    raise LdapDataException("".join(errorList))
        
        self.data[self.objectClassName].append(className)
            
###############################################################################

    def hasObjectClass(self, className):
        """ Checks if the current object has the objectClass className.
        """
        
        className = className.lower()
        
        for x in self.getObjectClasses():
            if className == x.lower():
                return True
                
        return False
        
###############################################################################

    def hasAttribute(self, attributeName):
        """ Check if the current object has the attribute attributeName.
        """
        
        attributeName = attributeName.lower()
        
        for x in self.getAttributeList():
            if attributeName == x.lower():
                return True
                
        return False
        
###############################################################################

    def deleteObjectClass(self, className):
        className = className.lower()

        found = False
        for x in self.getObjectClasses():
            if className == x.lower():
                className = x
                found = True
                break
        if not found:
            return
            
        
        # We have to make sure that one structural class remains after deleting
        if self.isObjectclassStructural(className):
            classList = self.getObjectClasses()
            classList.remove(className)
            tmpList = self.getObjectClassChain(className, classList)
            if len(tmpList) == 0:
                errorList = []
                errorList.append("Can't delete objectClass to object. ObjectClass " + className + " is the last structural Class and can't be deleted.")
                errorList.append(" DN: " + self.getPrettyDN() + ".")
                errorList.append(" Current objectClasses: " + repr(self.getObjectClasses()))
                        
                raise LdapDataException("".join(errorList))

        self.data[self.objectClassName].remove(className)

        must, may = self.getPossibleAttributes()
        all = Set(self.getAttributeList())
        rest = all - must.union(may)

        for x in rest:
            self.deleteAttribute(x)
        
###############################################################################

    def getObsoleteAttributes(self, className):
        """ Returns list of attributes which will be removed when className 
            is removed from the list of objectClasses.
        """
        
        attributeList = self.serverSchema.getAttributeListForObjectClass(className)
        currentList = self.getAttributeList()
        
        tmpList = []
        for x in currentList:
            if x in attributeList:
                tmpList.append(x)
        
        return tmpList
        
###############################################################################

    def missingAttributes(self):
        pass
        
###############################################################################

    def checkSingleAttributes(self):
        pass
        
###############################################################################

    def checkMustAttributes(self):
        pass
        
###############################################################################

    def checkObjectClassCombination(self):
        pass
        
###############################################################################

    def convertToLdif(self):
        """ Return the current object into LDIF format.
        """
        
        tmpString = StringIO.StringIO()
        ldifWriter = ldif.LDIFWriter(tmpString)
        ldifWriter.unparse(self.dn, self.data)
        
        return tmpString.getvalue()
        
        
###############################################################################

    def importFromLdif(self):
        pass
        
###############################################################################

    def convertToDsml(self):
        """ Return the current object into DSML format.
        """

        tmpString = StringIO.StringIO()
        dsmlWriter = dsml.DSMLWriter(tmpString)
        dsmlWriter.writeRecord(self.dn, self.data)

        return tmpString.getvalue()

###############################################################################

    def importFromDsml(self):
        pass

###############################################################################

    def getCompatibleAttributes(self):
        """ Returns all attributes which are supported by the server and can be 
        added without violating the objectclass chain (keyword: structural).
        """
        pass
        
###############################################################################

    def getPossibleAttributes(self):
        """ Returns all attributes which are supported by the current objectclasses.
        
        The result is one set with must attributes and one set with may attributes.
        """
        
        return self.serverSchema.getAllAttributes(self.getObjectClasses())
        
###############################################################################

    def isObjectclassStructural(self, objclass):
        """ Returns True if the objectclass is structural"""
    
        return self.serverSchema.isStructural(objclass)

###############################################################################

    def getObjectClassChain(self, className, classList):
        """ Returns a list of objectClasses which belong to the same chain 
            as className, given by classList.
        """

        return self.serverSchema.getObjectClassChain(className, classList)
        
###############################################################################
###############################################################################
###############################################################################

class LdapDataException(Exception):
    """This exception class will be raised if invalid operations are done on 
    ldap data.
    """
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
        
###############################################################################
###############################################################################
###############################################################################

class FunctionArgumentException(Exception):
    """This exception class will be raised if a function is called with the wrong arguments.
    """
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
