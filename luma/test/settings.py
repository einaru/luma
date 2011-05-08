from PyQt4.QtCore import QSettings

settings = QSettings('luma', 'luma')
settings = QSettings('luma', QSettings.IniFormat)
print settings.fileName()
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
