#$Id: mkpasswd.py 711 2006-11-09 13:53:17Z bgrotan $
'''
 This module depends on python >= 2.3

 Module written by Bjorn Ove Grotan <bgrotan@grotan.com>

  mkpasswd is free software; you can redistribute it and/or modify it
  under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.
 
  mkpasswd is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with mkpasswd; if not, write to the Free Software Foundation,
  Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

 For extra strength passwords, we wanted SSHA in our LDAP-environment
 as the standard python-module 'sha' does not support ssha, but this can 
 easily be implemented with a few extra functions. 

 SSHA can be described as:
     the SHA1-digest of a password with a sequence of "salt" bytes, where
     the bytes are randomly chosen - followed by the same salt bytes
 For LDAP-use, the SHA1 and SSHA-digest has to be base64-encoded. 

 Example-LDIF:
     {SSHA}oaEG3PJ10sHxGcSxsDRRooTifL55/2NOdN3nU1VEV+NFzc9Q
 
 This package should now support passwords compatible with [1] Samba using the [2]
 smbpasswd module for [3] Python. The samba compability is added for use with Samba 
 as PDC with storing user and host-information in LDAP.

 [1] http://www.samba.org
 [2] http://barryp.org/software/py-smbpasswd/
 [3] http://www.python.org
'''
import string,base64
import random,sys
import exceptions
import hashlib
smb_module = 0 # Where 1 is true, and 0 is false
crypt_module = 0
debug = False

try:
    import crypt
    crypt_module = 1
except:
    crypt_module = 0
try:
    import smbpasswd
    smb_module = 1 
except:
    smb_module = 0
    if debug:
        print '''
        module <smbpasswd> not found or not installed. Windows-passwords are therefor
        not supported!
        '''

def getsalt(chars = string.letters + string.digits,length=16):
    ''' Generate a random salt. Default length is 16 '''
    salt = ''
    for i in range(int(length)):
        salt += random.choice(chars)
    return salt

def randpasswd(chars = string.digits + string.ascii_letters,length=8):
    ''' Returns a random password at a given length based on a character-set.'''
    result = ''
    for i in range(length):
        result = result + getsalt(chars,1)
    return result

def check_password(s):
    ''' Returns true or false if the argument is concidered a strong password.
        The password must meat certain rules.. like:
        both small and CAPITALIZED characters, numbers and special characters 
        such as .,/!"# etc
    '''
    return True

def mkpasswd(pwd,sambaver=3,default='ssha1'):
    ''' Make a given password cryptated, possibly with different 
        crypt-algorihtms. This module was written for use with 
	    LDAP - so default is seeded sha1
    '''
    alg = {
	    'sha1':'Secure Hash Algorithm',
            'ssha1':'Seeded SHA',
	    'md5':'MD5',
	    'smd5':'Seeded MD5',
    }
    if crypt_module:
        alg['crypt'] = 'standard unix crypt'
    if smb_module:
        alg['lmhash'] = 'lan man hash'
        alg['nthash'] = 'nt hash'
    if default not in alg.keys():
        return 'algorithm <%s> not supported in this version.' % default
    else:
        salt = getsalt()
        if default == 'ssha1':
            sha1 = hashlib.sha1()
            sha1.update(str(pwd) + salt)
            pwString = "{SSHA}" + base64.encodestring(sha1.digest() + salt)
            return pwString[:-1]
        elif default =='sha1':
            sha1 = hashlib.sha1()
            sha1.update(str(pwd))
            pwString = "{SHA}" + base64.encodestring(sha1.digest())
            return pwString[:-1]
        elif default =='md5':
            md5 = hashlib.md5()
            md5.update(str(pwd))
            pwString = "{MD5}" + base64.encodestring(md5.digest())
            return pwString[:-1]
        elif default =='smd5':
            salt = getsalt(length=4) # Newer versions of OpenLDAP should support the default length 16
            md5 = hashlib.md5()
            md5.update(str(pwd) + salt)
            pwString = "{SMD5}" + base64.encodestring(md5.digest() + salt)
            return pwString[:-1]
        elif default =='crypt':
            return "{CRYPT}" + crypt.crypt(str(pwd),getsalt(length=2)) # crypt only uses a salt of length 2
        elif default == 'lmhash':
            if sambaver==3:
                return "{sambaLMPassword}" + smbpasswd.lmhash(pwd)
            elif sambaver==2:
                return "{lmPassword}" + smbpasswd.lmhash(pwd)
        elif default == 'nthash':
            if sambaver==3:
                return "{sambaNTPassword}" + smbpasswd.lmhash(pwd)
            elif sambaver==2:
                return "{NTPassword}" + smbpasswd.lmhash(pwd)

def check_strength(passwordString=""):
    
    def check_length():
        return 13 * pLength
        
    def check_chars():
        upperBool = False
        lowerBool = False
        specialBool = False
        numberBool = False
        combination = 0
        
        valueDict = {0:50, 1:50, 2:20, 3:0, 4:0}
        
        for x in passwordString:
            if (not lowerBool) and (x in string.ascii_lowercase):
                lowerBool = True
                combination += 1
            if (not upperBool) and (x in string.ascii_uppercase):
                upperBool = True
                combination += 1
            if (not numberBool) and (x in string.digits):
                numberBool = True
                combination += 1
            if (not specialBool) and ((x in string.punctuation) \
                    and (not(x in string.ascii_uppercase)) \
                    and (not(x in string.ascii_lowercase)) \
                    and (not(x in string.digits))):
                specialBool = True
                combination += 1
            if upperBool and lowerBool and specialBool and numberBool:
                break
        
        return valueDict[combination]
        
        
    def check_distribution():
        tmpDict = {}
        for x in passwordString:
            if tmpDict.has_key(x):
                tmpDict[x] += 1
            else:
                tmpDict[x] = 0
                
        doubleCharSum = 0
        
        for x in tmpDict.keys():
            value = tmpDict[x]
            if value > 2:
                doubleCharSum += value
            
        
        #ratio = pLength / len(tmpDict.keys())
        #return 13 * (ratio-1)
        return 13 * doubleCharSum
        
    def check_special_characters():
        tmpVal = 0
        return tmpVal
    
    pLength = len(passwordString)
    
    if 0 == pLength:
        return 0
    
    value = check_length()
    value -= check_distribution()
    value -= check_chars()
    
    if value < 0:
        value = 0
    
    if value > 100:
        value = 100
        
    return value


def check_strength_function():

    pwList = ["a", "aA", "aaaaaaaaaaa", "abcdefgh", "aBcDeFgH", "abc123ef",
        "aBc123Ef", "      ", "abC12 \ *+"]
        
    for x in pwList:
        print x, check_strength(x)
        
    
def get_available_hash_methods():
    # basic algorithms which are supported by mkpasswd-module
    supportedAlgorithms = ['md5','smd5', 'sha1', 'ssha1', 'cleartext']
        
    # add lmhash and nthash algorithms if smbpasswd module is present
    try:
        import smbpasswd
        supportedAlgorithms.extend(['lmhash', 'nthash'])
    except ImportError, e:
        pass
    try:
        import crypt
        supportedAlgorithms.extend(['crypt'])
    except ImportError, e:
        pass
        
    supportedAlgorithms.sort()
    return supportedAlgorithms

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
