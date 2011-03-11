#!/usr/bin/env python

try:
    from luma import luma
    print 'installed'
except:
    from lumalib import luma

import sys
for i in sys.path:
    print i

luma.main()
    