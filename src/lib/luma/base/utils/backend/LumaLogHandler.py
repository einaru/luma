"""
@author: Christian Forfang
"""
import logging

class LumaLogHandler(logging.Handler):
        
    def __init__(self, logTo):
        logging.Handler.__init__(self)
        self.logTo = logTo
            
    def emit(self, record):
        m = (record.levelname,record.msg)
        self.logTo.log(m)
          