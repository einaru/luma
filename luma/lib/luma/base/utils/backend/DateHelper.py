###########################################################################
#    Copyright (C) 2003 by Wido Depping
#    <wido.depping@tu-clausthal.de>
#
# Copyright: See COPYING file that comes with this distribution
#
###########################################################################


from mx.DateTime import *

class DateHelper(object):
    """A class for doing some date calculations.
    """

###############################################################################

    def __init__(self):
        # setting the date for the birth of unix
        self.unixBirth = Date(1979, 1, 1)
        
###############################################################################

    def is_valid_date(self, year=1979, month=1, day=1):
        """Test  if a given date is valid. Default date is the birth of unix.
        
        If the date is valid 1 is returned, else 0.
        """
        
        try:
            dummyDate = Date(year, month, day)
            return 1
        except mx.DateTime.RangeError:
            return 0
            
###############################################################################

    def date_to_unix(self, year, month, day):
        """ Calculates the days since the birth of unix until the given date.
        
        The result is an integer. If the given date is not valid, return None.
        """
        
        if self.is_valid_date(year, month, day):
            tmpDate = Date(year, month, day)
            diff = tmpDate - self.unixBirth
            return int(diff.days)
            
        
###############################################################################

    def dateduration_to_unix(self, days):
        """Converts the current date plus 'days' into an integer which represents the days since 
        the birth of unix. 
        """
    
        curDate = now()
        tmpDays = curDate - self.unixBirth
        return int(tmpDays.days) + days
