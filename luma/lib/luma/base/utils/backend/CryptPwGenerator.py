###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from __future__ import generators
import random
import crypt
import string


class CryptPwGenerator(object):
    """A class for encrypting passwords to the crypt format.
    
    Two relevant functions are usable:
    
    get_random_password returns a random password in cleartext and crypt format.
    
    encrypt_password accepts a password string and returns the password in cleartext and 
    crypt format.
    """
    
###############################################################################

    def __init__(self):
        self.saltchars = string.uppercase + string.lowercase + string.digits + "./" 
        self.pwGen = self.password_generator()
        
###############################################################################

    def create_random_string(self, stringLength):
        """ Creates a random string of the length stringLength.
        """
        
        randChars = []
        for x in range(stringLength):
            randChars.append(random.choice(self.saltchars))
        return "".join(randChars)
        
###############################################################################

    def password_generator(self):
        """ This is the password generator. Do not call directly.
        """
        
        while 1:
            randPassword = self.create_random_string(8)
            salt = "$1$" + self.create_random_string(8)
            yield randPassword, crypt.crypt(randPassword, salt)
            
###############################################################################

    def get_random_password(self):
        """ Returns a random password in cleatext and in crypt format
        """
        
        return self.pwGen.next()
        
###############################################################################

    def encrypt_password(self, tmpString):
        """ Encrypts a given string to crypt format and returns the password in cleartext and in crypt.
        """
        
        salt = "$1$" + self.create_random_string(8)
        return tmpString, crypt.crypt(tmpString, salt)
        
        
        
        
