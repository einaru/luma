'''
 Module written by Bjorn Ove Grotan <bgrotan@samfundet.no>

 For extra strength passwords, we wanted SSHA in our LDAP-environment
 as the standard python-module 'sha' does not support ssha, but this can 
 easily be implemented with a few extra functions. 

 SSHA can be described as:
     the SHA1-digest of a password with a sequence of "salt" bytes, where
     the bytes are randomly chosen - followed by the same salt bytes
 For LDAP-use, the SHA1 and SSHA-digest has to be base64-encoded. 

 SHA and SSHA are described at:
 http://developer.netscape.com/docs/technote/ldap/pass-sha.html
 This page have examples for Perl and Java if one would prefer that.

 Example-LDIF:
     {SSHA}oaEG3PJ10sHxGcSxsDRRooTifL55/2NOdN3nU1VEV+NFzc9Q

 Artistic Licence.
'''
import string,base64
import random,sys
import md5,sha,crypt

def getsalt(length=16):
    ''' Generate a random salt. Default length is 16 '''
    chars = string.letters + string.digits
    salt = ''
    for i in range(int(length)):
        salt += random.choice(chars)
    return salt


def mkpasswd(pwd,default='ssha'):
    ''' Make a given password cryptated, possibly with different 
        crypt-algorihtms. This module was written for use with 
	    LDAP - so default is seeded sha
    '''
    alg = {
        'ssha':'Seeded SHA',
	    'sha':'Secure Hash Algorithm',
	    'md5':'MD5',
	    'crypt':'standard unix crypt'
    }
    if default not in alg.keys():
        return 'algorithm <%s> not supported in this version.' % default
    else:
        salt = getsalt()
        if default == 'ssha':
            return "{SSHA}" + base64.encodestring(sha.new(str(pwd) + salt).digest() + salt)
        elif default =='sha':
            return "{SHA}" + base64.encodestring(sha.new(str(pwd)).digest())
        elif default =='md5':
            return "{MD5}" + base64.encodestring(md5.new(str(pwd)).digest())
        elif default =='crypt':
            return "{CRYPT}" + crypt.crypt(str(pwd),getsalt(2)) # crypt only uses a salt of length 2

